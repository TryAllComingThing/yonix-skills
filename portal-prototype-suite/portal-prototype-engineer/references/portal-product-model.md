# Portal product expert — decision framework
## Classify before layout
Service/catalog Portal: discover → compare → detail → access → manage usage. Developer Portal: docs → credentials → examples → test → troubleshooting. Knowledge Portal: discover → search → read → save/share. Self-service Portal: task → form → review → feedback → status. Hybrid: define a primary journey and explicit secondary journeys; avoid copying admin IA.
## Required modeling artifacts
1. Personas, access assumptions, goals, first-visit vs returning-user behavior.
2. Top three user journeys with entry, decision, success, failure and recovery.
3. Sitemap with page IDs, primary/secondary nav, deep links and back behavior.
4. Per-page contract: purpose, sections, data source, states, actions, validation and navigation.
5. Content hierarchy: primary CTA, discovery/filter/search, supporting details, help.
6. Portal/back-office boundary and non-goals.
## Anti-patterns
- Generating isolated beautiful pages without navigable journeys.
- Treating every portal as an admin console with dense sidebar and tables.
- Creating a service request flow when user needs immediate API access.
- Treating permissions or quotas shown by mock data as real entitlements.
## Gate
No code until at least one complete journey maps to concrete pages, state changes and acceptance assertions. For small screenshot-only revisions, use a scoped delta contract instead.
