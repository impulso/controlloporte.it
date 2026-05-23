# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-05-23

Initial public release of `controlloporte.it`.

### Added

- Italian `Controllo Porte` branding.
- Italian localized homepage.
- SEO content pages about TCP ports, port forwarding, NAT, CGNAT, and closed ports.
- Privacy policy.
- GDPR-conscious frontend setup with local assets and no third-party tracking resources.
- Footer with links to Privacy Policy, AI, and Impulso.it.
- `controlloporte-logo` favicon and logo assets.
- Quick port presets and common port groups.
- Shareable result links.
- Frontend routes in the `/{host}/{ports}` format.
- `me` alias to check the visitor's public IP address.
- JSON endpoint `GET /api/check/{host}/{port}`.
- API responses with `latency_ms` for open ports.
- DNS resolution separated from TCP latency measurement.
- Public OpenAPI document at `/.well-known/openapi.json`.
- Updated API documentation.
- Sitemap and robots.txt.
- Locally served fonts and frontend dependencies.
- Caddy/Nginx production configuration.
- Nginx rules returning `404` for missing static assets.

### Changed

- User interface and user-facing messages translated to Italian.
- API validation and error messages adapted for Italian users.
- Frontend results displayed with separate columns for status, latency, and port.
- Project documentation and metadata updated for `controlloporte.it`.
- `/metrics` removed from the public API documentation and blocked from public access.

### Removed

- Public references and links unrelated to this derived project.
- `llms.txt` and `llms-full.txt` from the public repository.

### Origin

This release is derived from [dsgnr/portchecker.io](https://github.com/dsgnr/portchecker.io), with changes specific to `controlloporte.it`.
