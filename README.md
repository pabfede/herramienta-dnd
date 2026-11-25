# Herramienta DnD

Open-source D&D campaign management tool. Designed first for DMs (campaigns, NPCs, lore, combat, encounter generation, rules reference). Later: players and full table support.

## Features (Planned)

- **Campaign Management** — Create, manage, and organize campaigns
- **NPC & Lore Management** — Track NPCs, factions, locations, worldbuilding
- **Combat System** — Initiative tracking, turn management, combat grid (future)
- **Encounter Generator** — Procedural encounter creation
- **Rules Reference** — Searchable rules, spells, monsters
- **Portability** — Campaigns as self-contained SQLite files

## Tech Stack

**Backend:** FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic, uv
**Frontend:** React 18, Vite, TypeScript, Tailwind, shadcn/ui, React Query, pnpm
**Database:** SQLite (one .db per campaign)
**Tools:** ruff (linting), pytest (testing)

## Project Structure

```
herramienta-dnd/
├── backend/          # FastAPI application
├── frontend/         # React application
├── docs/            # Documentation
├── CLAUDE.md        # Design spec & roadmap
└── README.md
```

## Getting Started

(Coming soon)

## Contributing

Open source. All contributions welcome.
