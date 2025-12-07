# Production Readiness TODO

- [ ] Implement chat API endpoint `/api/v1/chat/generate` and wire `src/utils/responseGenerator.js` to it
- [ ] Add HTTP client layer with auth header + 401 interceptor to auto-refresh token (using refresh token) and retry
- [ ] Harden auth storage: prefer HttpOnly cookies (or keep localStorage with secure/HTTPS + CORS tightened)
- [ ] Implement forgot-password flow on backend: `/api/v1/auth/forgot-password` (send email) and `/api/v1/auth/reset-password` (apply token+new password)
- [ ] Surface API errors in UI for chat send, PDF upload, regenerate, and downloads (user-facing toasts/messages)
- [ ] Connect PDF upload UI to backend `/api/v1/documents/upload` and fetch extracted text/metadata for context
- [ ] Implement message history endpoints to persist/reload chat sessions; hook ChatBox to load history per session
- [ ] Implement regenerate endpoint wiring for “Regenerate response” action
- [ ] Implement report generation/download endpoints and wire the download button in Message to real API
- [ ] Optimize bundles: code-split heavy routes/components/assets; lazy-load charts/pdf libs
- [ ] Add e2e smoke tests: login, chat send, PDF upload, regenerate, report download; add API contract tests
- [ ] Confirm agent endpoints strategy (session_id requirement vs removal) or align UI to execute agents
- [ ] Production ops: enable HTTPS, set CORS allowlist, add rate limiting on chat endpoints, logging/monitoring
- [ ] Database migrations for sessions/messages/documents/reports tables (see BACKEND_INTEGRATION_GUIDE.md)
