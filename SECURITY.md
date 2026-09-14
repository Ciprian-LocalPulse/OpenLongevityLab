# Security

Report vulnerabilities privately to the maintainers rather than in a public issue. Include a minimal reproduction, affected version, and suggested contact channel. Do not include credentials or personal data in reports.

The threat model covers API abuse, malicious datasets, dependency and action compromise, prompt injection in scientific content, path traversal, and leakage of secrets. Inputs are validated by typed models; source content is treated as data, never as trusted instructions. Deployments should use environment variables, least-privilege credentials, TLS, dependency review, and immutable audit logs.

Supported versions: the latest `0.1.x` release receives fixes while the project is pre-1.0. See `docs/security/THREAT_MODEL.md` for details.
