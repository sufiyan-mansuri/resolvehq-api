# ResolveHQ

A multi-tenant Helpdesk SaaS API built with Django REST Framework — think a simplified backend for Zendesk or Freshdesk. Supports multiple organizations, role-based access control, ticket lifecycle management, internal/customer comments, and an in-app notification system.

🔗 **Live API:** [https://resolvehq.onrender.com/](https://resolvehq.onrender.com/)
📄 **Swagger Docs:** [https://resolvehq.onrender.com/](https://resolvehq.onrender.com/)

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Auth:** JWT (SimpleJWT)
- **API Docs:** drf-spectacular (Swagger / ReDoc)
- **Deployment:** Render

## Features

### Authentication
- JWT-based register, login, and token refresh
- Custom `User` model with email as the username field

### Multi-Tenancy
- Users create organizations and become the org admin automatically
- Admins invite existing users to join as agents
- Customers are automatically added as org members on their first ticket
- Role is scoped **per organization** via a dedicated `Membership` model (not a global field on `User`) — the same user can be an admin in one org and a customer in another

### Roles & Permissions
| Role | Capabilities |
|------|---------------|
| **Admin** | Full control of their organization — invite agents, assign/resolve/close tickets, delete tickets |
| **Agent** | View and comment on tickets assigned to them, resolve assigned tickets |
| **Customer** | Create tickets, view/comment on their own tickets only |

### Ticket Management
- Full CRUD with role-scoped querysets (customers only ever see their own tickets)
- Status lifecycle enforced through dedicated endpoints, not raw field updates:
  - `POST /tickets/{id}/assign/` — admin assigns an agent → status → `in_progress`
  - `POST /tickets/{id}/resolve/` — assigned agent resolves → status → `resolved`
  - `POST /tickets/{id}/close/` — admin closes a resolved ticket → status → `closed`
- Priority (`low` / `medium` / `high`) set at creation, editable via standard update
- Filtering by status, priority, and assignee

### Comments
- Customer replies and agent/admin internal notes on a shared model
- Internal notes (`is_internal=True`) are hidden from customers at the queryset level
- Comment access scoped to ticket ownership/assignment, not just org membership

### Notifications
- In-house DB-backed notification system — no email or Celery
- Django signals create a `Notification` record on ticket assignment, resolution, and closure
- `GET /notifications/` and `PATCH /notifications/{id}/read/` for retrieval and read-state

### API Documentation
- Interactive Swagger UI and ReDoc via drf-spectacular

## Architecture

```
apps/
├── users/
├── organizations/
├── tickets/
├── comments/
├── notifications/
└── common/
```

Each app is scoped to a single responsibility, with shared permission classes (`IsAdmin`, `IsAgentOrAdmin`) and helpers living in `common/`.

## Key Design Decisions

- **Membership over global roles** — a `Membership` model (user + org + role) replaces a role field on `User`, since the same person can hold different roles across different organizations.
- **State transitions as actions, not field updates** — `status` is excluded from the generic update serializer entirely. It can only change through `/assign/`, `/resolve/`, and `/close/`, each enforcing its own business rules (e.g. a ticket can't be closed before it's resolved).
- **Auto-provisioned customer membership** — customers don't go through an invite flow; submitting a first ticket to an org creates their membership behind the scenes.

## Setup

```bash
# Clone the repo
git clone https://github.com/sufiyan-mansuri/resolvehq-api.git
cd resolvehq-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (see below)
cp .env.example .env

# Run migrations
python manage.py migrate

# Create a superuser (assigned admin role)
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

## Environment Variables

```
SECRET_KEY=
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/resolvehq
ALLOWED_HOSTS=localhost,127.0.0.1
```

## API Documentation

**Live:** [https://resolvehq.onrender.com/](https://resolvehq.onrender.com/)

Or run locally and explore at:
- Swagger UI: `http://localhost:8000/`

## Roadmap / In Progress

- [ ] Automated test suite (pytest)
- [ ] Dockerize the project (Dockerfile + docker-compose for app + PostgreSQL)
- [ ] Deploy to Render
- [ ] Real-time notifications (Django Channels)
- [ ] Analytics endpoints (tickets created, resolution time, agent performance)
- [ ] Background email notifications (Celery + Redis)

## License

MIT
