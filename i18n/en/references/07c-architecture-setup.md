# Development Handoff — ARCHITECTURE.md + setup.sh

## 📄 ARCHITECTURE.md Template

```markdown
# [Product Name] — Technical Architecture

## Directory Structure

[Generate the corresponding directory structure based on the tech stack]

## Database Design

[Consolidate from the PRD's DB Schema — convert to CREATE TABLE SQL or ORM model definitions]

### ER Diagram

[Mermaid erDiagram]

### Key Table Descriptions

| Table | Description | Key Fields | Index Recommendations |
|-------|------------|------------|----------------------|
| | | | |

## API Design

[Define RESTful API endpoints or GraphQL schema based on User Stories and feature specs]

### Endpoints List

| Method | Path | Description | Corresponding Task |
|--------|------|------------|-------------------|
| GET | /api/v1/[resource] | [Description] | T1.1 |
| POST | /api/v1/[resource] | [Description] | T1.2 |

### Authentication

[JWT / Session / OAuth, etc.]

## Third-Party Services

| Service | Purpose | Corresponding Feature |
|---------|---------|----------------------|
| | | |

## Security Architecture

### CORS Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Allowed Origins | [Production domain, localhost:port] | Do not use wildcard * |
| Allowed Methods | GET, POST, PUT, DELETE | Based on actual API needs |
| Allowed Headers | Content-Type, Authorization | |
| Credentials | true/false | Depends on authentication method |

### Security Headers

[Select applicable headers from references/08-security-checklist.md §5 based on product requirements]

### Rate Limiting Strategy

| Endpoint Type | Limit | Identification Method |
|--------------|-------|----------------------|
| General API | [X] req/min | IP + User ID |
| Login/Register | [X] req/min | IP |
| File Upload | [X] req/min | User ID |

### Sensitive Data Handling

- Secret management: [.env + platform env vars / Secrets Manager]
- Logging rules: Never log passwords, tokens, or personal data
- Data encryption: [TLS in transit / encryption at rest requirements]

> Full security checklist at `references/08-security-checklist.md`
```

---

## 📄 .gitignore Template

```gitignore
# Environment variables and secrets
.env
.env.local
.env.*.local
*.pem
*.key

# Product planning progress (may contain sensitive business information)
.product-playbook-progress.md
# Product-playbook dev-handoff marker (session-local; do not commit)
.product-dev-active

# IDE and OS
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# Dependencies
node_modules/
__pycache__/
*.pyc
venv/

# Build output
dist/
build/
.next/
```

---

## 📄 setup.sh Template

```bash
#!/bin/bash
# [Product Name] — Project Initialization Script
# Usage: chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🚀 Initializing [Product Name]..."

# ===== Check prerequisites =====
command -v [node/python/etc] >/dev/null 2>&1 || { echo "❌ [runtime] is required"; exit 1; }

# ===== Install dependencies =====
echo "📦 Installing dependencies..."
[npm install / pip install -r requirements.txt / etc]

# ===== Environment setup =====
if [ ! -f .env ]; then
  echo "📝 Creating .env file..."
  cp .env.example .env
  echo "⚠️  Please edit .env and fill in the required environment variables"
fi

# ===== Database initialization =====
echo "🗄️  Initializing database..."
[migration commands]

echo ""
echo "✅ Initialization complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env to fill in environment variables"
echo "  2. Start the dev server: [start command]"
echo "  3. Start developing: claude \"Read CLAUDE.md and TASKS.md, then start executing Phase 1\""
```

---

## User Guidance Text

### In Claude Chat / Cowork

After producing the handoff package, display the following guidance:

```
📦 Development handoff package is ready! It includes the following files:

  CLAUDE.md        → Claude Code's project memory (product context + tech specs)
  TASKS.md         → Development task list (4 Phases, [N] Tasks total)
  TICKETS.md       → Ticket list ([N] tickets, ready to create in Jira/Asana/Linear)
  docs/PRD.md      → Full PRD
  docs/ARCHITECTURE.md → Technical architecture (DB schema + API + directory structure)
  docs/PRODUCT-SPEC.md → Product Spec Summary
  scripts/setup.sh → One-click initialization script

🔗 How to start developing:

  1. Download and extract to your project folder
  2. Open a terminal and navigate to the project folder
  3. Launch Claude Code:
     $ claude
  4. Tell Claude Code to begin:
     > Read CLAUDE.md and TASKS.md, then start executing Phase 0

💡 Tips:
  - Claude Code automatically reads CLAUDE.md, so it already knows the full product context
  - After each Phase is complete, it will ask whether to proceed to the next Phase
  - To adjust feature scope, just edit TASKS.md directly
  - The "Explicitly Not Doing" list in CLAUDE.md prevents Claude Code from building out of scope
```

### Pre-Output Final Confirmation

```
Before producing the development handoff package, I need to confirm a few things:

1. Tech stack: [Confirmed / Needs confirmation]
2. Product name (for the project folder name): [Confirmed / Needs confirmation]
3. Any other technical constraints or preferences?
   - e.g., Must use a specific ORM, need to support specific browsers, existing CI/CD, etc.
```
