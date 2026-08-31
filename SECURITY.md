# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

---

## Reporting a Vulnerability

The AI Code Intelligence Engine development team takes security and data privacy seriously.

If you discover a security vulnerability within this project (including input sanitization issues, remote code execution risks in repository cloning, path traversal, or dependency vulnerabilities), please report it responsibly:

1. **Do not open a public GitHub issue.**
2. Send an email with the subject line `[SECURITY VULNERABILITY] AI Code Intelligence Engine` to the repository maintainers or use GitHub's private vulnerability reporting feature on the repository.
3. Include detailed steps to reproduce the vulnerability, proof-of-concept payloads, and affected components.

### What to Expect:
- **Acknowledgement**: Within 48 hours of receipt.
- **Triage & Remediation**: We will investigate the root cause, determine impact, and prepare a fix in a private branch.
- **Disclosure**: A patched release and CVE advisory (if applicable) will be published alongside credit to the reporter.

---

## Best Practices for Local Deployment

- Do not expose the FastAPI backend or Streamlit frontend directly to the public internet without an authenticating reverse proxy (e.g., NGINX with TLS and basic/OAuth2 authentication).
- Ensure indexed repositories come from trusted internal or public sources.
- Avoid passing untrusted or sensitive environment variables into shared deployments.
