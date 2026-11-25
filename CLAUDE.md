# Herramienta DnD — Design & Roadmap

## Vision

Open-source, rules-agnostic D&D campaign management tool. Designed for DMs first. Campaigns are portable, self-contained SQLite files that work offline.

## Architecture (Closed)

### Backend Stack
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Validation:** Pydantic v2
- **Migrations:** Alembic
- **Package Manager:** uv
- **Linting:** ruff

**Three-layer architecture:**
- **Routers:** HTTP endpoints, request validation, response schemas
- **Services:** Business logic, campaign state management, rules engine
- **Repositories:** Data access, SQLAlchemy ORM interactions

### Frontend Stack
- **Framework:** React 18
- **Build:** Vite
- **Language:** TypeScript (types auto-generated from FastAPI OpenAPI spec)
- **UI Kit:** shadcn/ui + Tailwind CSS
- **Data Fetching:** React Query
- **Package Manager:** pnpm

### Database
- **Engine:** SQLite
- **Model:** One `.db` file per campaign (portable, shareable)
- **Seed Data:** Each new campaign saves a copy of the game `System` configuration at creation

### Core Concepts

**System:** Configurable rules engine (D&D 5e, Pathfinder, house rules, etc.). No hardcoded mechanics.

**Campaign:** Top-level container. One SQLite file per campaign. Contains:
- Metadata (name, DM, created date, last played)
- NPCs, locations, factions
- Sessions and session logs
- Encounter history
- Custom rules/System override

**Entity:** Base class for campaigns, NPCs, locations, factions. Supports custom fields.

## Implementation Phases

### Phase 1: Foundation (Backend + Core Data Models)
**Goal:** Working FastAPI backend with campaign/NPC/location models, SQLite persistence, basic CRUD endpoints.

Tasks:
- [ ] Set up FastAPI project structure
- [ ] Configure SQLAlchemy and Alembic
- [ ] Define Pydantic models for Campaign, NPC, Location, Faction, System
- [ ] Implement three-layer architecture (routers, services, repositories)
- [ ] CRUD endpoints for campaigns, NPCs, locations
- [ ] SQLite database initialization
- [ ] OpenAPI schema generation
- [ ] Basic error handling

### Phase 2: Frontend Scaffold + Campaign View
**Goal:** React frontend connected to backend. Campaign page, NPC/location listing.

Tasks:
- [ ] Set up Vite + React 18 + TypeScript project
- [ ] Generate TypeScript types from FastAPI OpenAPI spec
- [ ] React Query setup and hooks
- [ ] Campaign creation/selection UI
- [ ] Campaign view (dashboard with tabs for NPCs, locations, factions)
- [ ] NPC listing with add/edit/delete
- [ ] Location listing
- [ ] Tailwind + shadcn/ui component library integration

### Phase 3: Encounter Generator & Combat System
**Goal:** Procedural encounter generation, initiative tracking, combat log.

Tasks:
- [ ] Encounter generator service (backend)
- [ ] Encounter Generator UI
- [ ] Combat tracker UI with initiative
- [ ] Combat log / session notes
- [ ] Rules reference search (future: external data source)

### Phase 4: Lore & Worldbuilding Tools
**Goal:** Rich NPC/location/faction editing, timeline, worldbuilding aids.

Tasks:
- [ ] NPC editor with custom fields, relationships
- [ ] Location editor with maps/descriptions
- [ ] Faction tracker with relationships
- [ ] Timeline/session log
- [ ] Notes and linking (backlinks?)

### Phase 5: Polish & Distribution
**Goal:** Offline-first PWA, installer, public GitHub release.

Tasks:
- [ ] Service worker for offline support
- [ ] Export/import campaigns
- [ ] GitHub pages static hosting (optional)
- [ ] Electron/Tauri desktop app (future)
- [ ] Public release + marketing

## API Contract (Phase 1 MVP)

**Base:** `GET /api/campaigns` → list campaigns
**Create:** `POST /api/campaigns` → create campaign
**Read:** `GET /api/campaigns/{id}` → campaign detail
**Update:** `PATCH /api/campaigns/{id}` → update campaign
**Delete:** `DELETE /api/campaigns/{id}` → delete campaign

Similar for `/api/npcs`, `/api/locations`, `/api/factions`.

Responses: JSON, `{id, name, description, createdAt, updatedAt, ...}`

## Tools & Commands

```bash
# Backend
cd backend
uv sync              # Install dependencies
uv run uvicorn main:app --reload  # Run server
uv run pytest        # Run tests
uv run ruff check .  # Lint

# Frontend
cd frontend
pnpm install         # Install dependencies
pnpm dev             # Dev server
pnpm build           # Production build
pnpm lint            # Lint with ruff/eslint
```

## Git Workflow

1. Create feature branch: `git checkout -b feature/campaign-crud`
2. Implement in backend/frontend
3. Commit: `git commit -m "feat: add campaign CRUD endpoints"`
4. Push: `git push origin feature/campaign-crud`
5. (Open PR if team, merge to main)

## Success Criteria

**Phase 1:** Backend running locally, can create/read/update/delete campaigns and NPCs via HTTP API
**Phase 2:** Frontend runs, can view campaigns and NPCs in a web UI
**Phase 3:** Encounter generator works, combat tracker functional
**Phase 4:** Full NPC/location/faction management with linking
**Phase 5:** Offline-capable, shareable campaigns, public release

## Notes

- Rules-agnostic: No hardcoded D&D 5e mechanics in core code
- Portable: Campaigns are SQLite files, shareable like .txt or .pdf
- Open source: MIT license
- Future: Multiplayer via WebSockets, cloud sync (optional)
