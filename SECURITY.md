# Security

Report vulnerabilities privately to the maintainers rather than in a public issue. Include a minimal reproduction and affected version without credentials or personal data.

The threat model covers API abuse, malicious datasets, dependency and action compromise, prompt injection in scientific content, path traversal, and leakage of secrets. Inputs use typed validation; source content is data, never trusted instructions. Deployments should use environment variables, least-privilege credentials, TLS, dependency review, and immutable audit logs.

Supported versions: the latest `0.1.x` release receives fixes while the project is pre-1.0. See `docs/security/THREAT_MODEL.md`.
