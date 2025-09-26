-- RBAC schema (PostgreSQL)
-- Tables: users, roles, permissions, role_permissions, user_roles

BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT UNIQUE NOT NULL,
    display_name    TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS roles (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key         TEXT UNIQUE NOT NULL, -- e.g., admin, co_admin, customer, venue_admin, services_admin, resources_admin, partner
    label       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS permissions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource    TEXT NOT NULL, -- venue, service, resource, booking, offer
    action      TEXT NOT NULL, -- create, read, update, delete, approve
    key         TEXT GENERATED ALWAYS AS (lower(resource) || ':' || lower(action)) STORED,
    UNIQUE (resource, action),
    UNIQUE (key)
);

CREATE TABLE IF NOT EXISTS role_permissions (
    role_id         UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_id   UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS user_roles (
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id     UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- Seeds

-- Roles
INSERT INTO roles (key, label) VALUES
    ('admin', 'Admin'),
    ('co_admin', 'Co-Admin'),
    ('customer', 'Customer'),
    ('venue_admin', 'Venue Admin'),
    ('services_admin', 'Services Admin'),
    ('resources_admin', 'Resources Admin'),
    ('partner', 'Partner')
ON CONFLICT (key) DO NOTHING;

-- Permissions
-- Base resources/actions
WITH perms(resource, action) AS (
    VALUES
    ('venue','create'),('venue','read'),('venue','update'),('venue','delete'),('venue','approve'),
    ('service','create'),('service','read'),('service','update'),('service','delete'),('service','approve'),
    ('resource','create'),('resource','read'),('resource','update'),('resource','delete'),('resource','approve'),
    ('booking','create'),('booking','read'),('booking','update'),('booking','delete'),
    ('offer','create'),('offer','read'),('offer','update'),('offer','delete')
)
INSERT INTO permissions (resource, action)
SELECT resource, action FROM perms
ON CONFLICT (resource, action) DO NOTHING;

-- Helper: get ids by keys
WITH role_ids AS (
    SELECT key, id FROM roles
), perm_ids AS (
    SELECT key, id FROM permissions
)
-- Admin: all permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM role_ids r CROSS JOIN perm_ids p WHERE r.key = 'admin'
ON CONFLICT DO NOTHING;

-- Co-Admin: read on all + approve on venue/service/resource
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM role_ids r
JOIN perm_ids p ON (
    p.key IN (
        'venue:read','service:read','resource:read','booking:read','offer:read',
        'venue:approve','service:approve','resource:approve'
    )
)
WHERE r.key = 'co_admin'
ON CONFLICT DO NOTHING;

-- Customer: read venue/service/resource, booking create/read
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM role_ids r
JOIN perm_ids p ON p.key IN ('venue:read','service:read','resource:read','booking:create','booking:read')
WHERE r.key = 'customer'
ON CONFLICT DO NOTHING;

-- Venue Admin: venue CRUD (+ approve optional)
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM role_ids r
JOIN perm_ids p ON p.key IN ('venue:create','venue:read','venue:update','venue:delete','venue:approve')
WHERE r.key = 'venue_admin'
ON CONFLICT DO NOTHING;

-- Services Admin: service CRUD (+ approve optional)
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM role_ids r
JOIN perm_ids p ON p.key IN ('service:create','service:read','service:update','service:delete','service:approve')
WHERE r.key = 'services_admin'
ON CONFLICT DO NOTHING;

-- Resources Admin: resource CRUD (+ approve optional)
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM role_ids r
JOIN perm_ids p ON p.key IN ('resource:create','resource:read','resource:update','resource:delete','resource:approve')
WHERE r.key = 'resources_admin'
ON CONFLICT DO NOTHING;

-- Partner: service/resource/offer CRUD (ownership enforced in app layer)
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM role_ids r
JOIN perm_ids p ON p.key IN (
    'service:create','service:read','service:update','service:delete',
    'resource:create','resource:read','resource:update','resource:delete',
    'offer:create','offer:read','offer:update','offer:delete'
)
WHERE r.key = 'partner'
ON CONFLICT DO NOTHING;

COMMIT;

