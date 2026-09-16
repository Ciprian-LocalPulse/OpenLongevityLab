# Threat model

Threats include malicious scientific payloads, prompt injection inside abstracts or PDFs, API enumeration and denial of service, dependency compromise, path traversal in dataset importers, and accidental disclosure through logs. Mitigations include strict schemas and size limits, treating documents as untrusted data, allow-listed filesystem roots, rate limiting at the edge, pinned dependencies, secret scanning, least-privilege CI permissions, and provenance checks before publication.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
