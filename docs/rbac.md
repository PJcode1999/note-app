## Role-Based Access Control (RBAC)

This document defines roles, permissions, and authorization rules for managing Venue, Services, and Resources, including module-specific admins and partner/customer capabilities.

### Roles
- **Admin**: Full CRUD across Venue, Service, Resource, plus approvals.
- **Co-Admin**: Read and Approve across all modules. No create/update/delete.
- **Customer**: Browse and book services/resources.
- **Admin (V/S/R)**: Module-specific admins with Add/Manage for their assigned module only.
  - Venue Admin
  - Services Admin
  - Resources Admin
- **Partner**: Showcase services/resources, create listings, and manage offers.

### Resources (Domains)
- Venue
- Service
- Resource
- Booking
- Offer

### Actions (Verbs)
- create, read, update, delete
- approve (where applicable)

### Permissions Namespace
Permissions are expressed as `resource:action` strings (e.g., `venue:create`, `service:read`).

### Role to Permission Matrix

| Role | Venue | Service | Resource | Booking | Offer | Approval |
|------|-------|---------|----------|---------|-------|----------|
| Admin | create, read, update, delete | create, read, update, delete | create, read, update, delete | create, read, update, delete | create, read, update, delete | approve:venue, approve:service, approve:resource |
| Co-Admin | read | read | read | read | read | approve:venue, approve:service, approve:resource |
| Customer | read | read | read | create (booking), read:own | - | - |
| Venue Admin | create, read, update, delete (Venue only) | - | - | - | - | approve:venue (optional) |
| Services Admin | - | create, read, update, delete (Service only) | - | - | - | approve:service (optional) |
| Resources Admin | - | - | create, read, update, delete (Resource only) | - | - | approve:resource (optional) |
| Partner | - | create, read, update, delete (own) | create, read, update, delete (own) | - | create, read, update, delete (own) | - |

Notes:
- "own" indicates ownership constraints enforced at the application layer (e.g., a partner can manage only their own listings/offers).
- Approvals may apply to publishing or status changes. If not needed, omit the `approve:*` permissions from role assignments.

### Suggested Permission Set

- venue:create, venue:read, venue:update, venue:delete, venue:approve
- service:create, service:read, service:update, service:delete, service:approve
- resource:create, resource:read, resource:update, resource:delete, resource:approve
- booking:create, booking:read, booking:update, booking:delete
- offer:create, offer:read, offer:update, offer:delete

### Role Definitions (Canonical)

- Admin
  - All permissions above

- Co-Admin
  - venue:read, service:read, resource:read, booking:read, offer:read
  - venue:approve, service:approve, resource:approve

- Customer
  - venue:read, service:read, resource:read
  - booking:create, booking:read (own)

- Venue Admin
  - venue:create, venue:read, venue:update, venue:delete
  - venue:approve (optional)

- Services Admin
  - service:create, service:read, service:update, service:delete
  - service:approve (optional)

- Resources Admin
  - resource:create, resource:read, resource:update, resource:delete
  - resource:approve (optional)

- Partner
  - service:create, service:read, service:update, service:delete (own)
  - resource:create, resource:read, resource:update, resource:delete (own)
  - offer:create, offer:read, offer:update, offer:delete (own)

### Authorization Policy Guidance

At request time, evaluate:
- The acted-on `resource` and desired `action`.
- The caller's `userId` and derived roles.
- If the permission implies ownership, verify `resource.ownerId == userId`.

Pseudocode:

```text
function isAllowed(userId, action, resource, resourceOwnerId?) {
  const permission = `${resource}:${action}`;
  const userPermissions = expandRolesToPermissions(getUserRoles(userId));
  if (!userPermissions.has(permission)) return false;
  if (permissionRequiresOwnership(permission)) {
    return resourceOwnerId && resourceOwnerId === userId;
  }
  return true;
}
```

