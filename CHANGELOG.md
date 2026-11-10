# changelog

## v1.13.0

- ui: refresh Material 3 styling (spacing, elevation, focus rings, dark mode,
  responsive layout) and tighten accessibility across all pages.
- ux: make the dashboard single-purpose — weight entry first, with a large
  save action, collapsed timestamp, last-entry context, and a save
  confirmation showing the change since the previous reading.
- ux: move settings and logout into an account menu; show chart range,
  history and full entries as secondary actions.
- a11y: remove nested interactive elements, add live regions, proper labels,
  table captions, keyboard navigation, and reduced-motion support.

## v1.12.0

- security: `DEBUG` now defaults to `false`; production settings (secure
  cookies, HSTS, security headers, CSP) are enabled automatically.
- security: `SECRET_KEY` is read from the environment instead of being
  hard-coded; the Docker entrypoint generates an ephemeral key when missing.
- security: entry deletion is POST-only and protected by CSRF.
- security: OpenAPI schema and documentation endpoints require login.
- security: add input validation for non-positive weights and future
  timestamps, plus a database index for per-user history queries.
- auth: consolidate login/signup on django-allauth and remove the duplicate
  Django auth views.
- api: list endpoints are paginated and rate limited; schema generation is
  clean and uses enum overrides.
- pwa: serve the service worker from `/sw.js` with root scope and stop caching
  authenticated pages.
- ui: pin Chart.js with subresource integrity, add a running-average trendline,
  improve accessible chart controls, and handle pagination edge cases.
- docker: run as a non-root user, add a healthcheck, and make gunicorn workers,
  timeout, and migrations configurable.
- deps: remove unused crispy forms, update Django, requests, and lockfile;
  add ruff to the development workflow.

## v1.11.0

- add unit in WeightEntry model.
- add per-user target weights and preferred display unit.
- bug fix: add migration to delete duplicate social apps.

## v1.10.0

- change graph to default to 7d and persist filters after refresh.
- add avg trendline in graph.

## v1.9.0

- add django rest framework and swagger ui for apis.

## v1.8.0

- update graph to show different durations on homepage.

## v1.7.0

- bug fix in dockerfile.
- remove bootstrap and use material 3 web components.

## v1.6.0 (unstable)

- add oauth config to **env**.
- bug fix in dockerfile.
- add documentation on how to start the project.

## v1.5.0 (unstable)

- improve accessibility.
- move to uv.

## v1.4.0

- tweaks to pwa support.
- add backend type hints and security decorators.
- integrate pytest for automated testing.
- add whitenoise for static file serving.
- update dockerfile for production with gunicorn and auto migrations.

## v1.3.0

- add export csv option.

## v1.2.0

- update ui.
- add login with social account.

## v1.1.0

- make pwa compatible.
- subdomain change to wait.domain.com.

## v1.0.0

- initial commit.
