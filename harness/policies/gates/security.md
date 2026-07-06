# Security Gate Checklist

Required for: user input, PII, secrets, auth/authz, data export/import, admin
operations, third-party integrations, file handling, webhooks. Verify each
item against the artifact:

- [ ] Authentication: identity is established where required
- [ ] Authorization: least privilege; permission checks at every boundary
- [ ] Input validation at trust boundaries
- [ ] Output encoding where content crosses contexts
- [ ] Secret handling: no secrets in code, config, or artifacts
- [ ] Logging: no secrets, PII, tokens, credentials, or sensitive payloads logged
- [ ] Abuse cases considered (hostile input, resource exhaustion, injection)
- [ ] Dependency risk: new dependencies justified and reputable
- [ ] Negative tests exist for unauthorized and invalid cases
