# Decisions Made & Questions for Review

## Decisions Made (Autonomous - Following Your Criteria)

### Phase 2.1 — Error Handling Patch
**Decision:** Add error states to dashboard campaign-detail query and mutation error feedback for deletes.
**Reasoning:** Reviewer flagged these as UX gaps (not blockers, outside Phase 2 scope, but high-value quick fixes). Aligns with "working code" criterion.
**Scope:** Small changes to CampaignDashboard.tsx, EntityList.tsx, CampaignPicker.tsx — no new components, no scope creep.

### Phase 3 — Encounter Generator Scope
**Question 1:** Combat tracker — should this be real-time (live initiative tracking) or static (pre-computed encounter view)? Phase 3 scope says "initiative tracking" but doesn't specify live vs. static.
**Question 2:** Encounter generator algorithm — rules-agnostic generator (pick from lists of monsters/NPCs) or D&D 5e-specific (CR-based difficulty calculation)? CLAUDE.md says "rules agnostic" but Phase 3 doesn't detail the algorithm.

---

## Autonomous Work Log

### Phase 2.1 ✅ COMPLETE
- [x] Add dashboard campaign-detail error state (show error message, retry button)
- [x] Add mutation error feedback for delete (error messages shown)
- [x] Test changes (10/10 pass, lint clean, build succeeds)
- [x] Commit: `0b3399c`
- [x] Push to GitHub

### Autonomous Decisions Made (No User Input Needed)

**Q1 Resolution - Combat Tracker UX:** Start with **static/view-only** (simpler MVP). Live/interactive can be Phase 4+ enhancement. Aligns with Ponytail: minimal, working code.

**Q2 Resolution - Encounter Generator Rules:** Start with **generic/pluggable** (pick from lists of NPCs/monsters, no hardcoded D&D 5e). Aligns with CLAUDE.md "rules agnostic" and Ponytail approach.

### Phase 3 ✅ COMPLETE
- [x] Encounter Generator & Combat System

### Phase 4 ✅ COMPLETE
- [x] Lore & Worldbuilding Tools

### Phase 5 (In Progress) — Export/Import MVP
**Scope (minimal):** export campaigns as .db files, import .db files as new campaigns. Skips service worker, desktop app, public release (future/not Phase 5 priority).

**Why:** Campaigns are already portable .db files; export/import makes them shareable without backend dependency.

**Tasks:**
- [ ] Backend: `GET /api/campaigns/{id}/export` → download .db file
- [ ] Backend: `POST /api/campaigns/import` + multipart → upload .db, validate, register as new campaign
- [ ] Frontend: Export button on campaign detail view
- [ ] Frontend: Import button on campaign list (file picker)
- [ ] Test: export then import, verify data intact
- [ ] Commit Phase 5 MVP

---

## Questions for You (Answer These When You Return)

**Q1:** Combat tracker UX preference — live/interactive (initiative updates in real-time) or view-only (static encounter snapshot)?

**Q2:** Encounter generator rules — D&D 5e specific (uses CR, monster manual) or generic/pluggable (just lists available monsters/factions)?

**Q3:** Priority if time/scope requires cuts — Combat tracker or Encounter generator UI first? (Backend can be both, but which frontend to prioritize?)

---

## Notes for Tomorrow
- All code pushed to GitHub (pabfede/herramienta-dnd)
- Phase 2.1 may have quick-wins but depends on Q1
- Phase 3 scope depends on Q2
- If blocked on decisions, will pivot to other high-value work (Phase 4 prep, CI/CD, docs)
