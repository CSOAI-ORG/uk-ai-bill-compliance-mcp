# UK AI Regulation Compliance MCP

**UK AI Regulation White Paper + upcoming AI (Regulation) Bill + sector-regulator crosswalk**, automated for AI agents.

By [MEOK AI Labs](https://meok.ai).

## What it does

- Audits against the **five UK AI principles**: safety, transparency, fairness, accountability, contestability
- Maps AI systems to the **primary sector regulator** (ICO, FCA, MHRA, CMA, Ofcom, HSE, CDDO, etc.)
- Scores readiness for the anticipated **AI (Regulation) Bill** frontier-model obligations
- Flags **Algorithmic Transparency Recording Standard (ATRS)** requirement for public-sector systems
- Issues **HMAC-signed UK AI readiness attestations** (Pro tier — procurement-ready)

## Why this MCP

The UK approach is *context-specific + pro-innovation*. There is no EU-AI-Act-style horizontal statute (yet) — sector regulators apply the five principles under their existing powers.

The AI (Regulation) Bill was signalled in the King's Speech 2024 and narrowed to frontier foundation models. Binding obligations expected 2026-2027+.

Most UK organisations have to comply with the **five principles + existing sectoral law + ATRS + AISI voluntary commitments** — and they need evidence artefacts their board, auditor, or commissioning authority will accept.

This MCP generates those artefacts + a signed readiness cert.

## Tools

- `classify_system` — which regulator + scope applies to your system
- `audit_principle` — check current controls against one of the 5 principles
- `audit_sector_regulator` — surface primary regulator + key guidance
- `ai_bill_readiness` — score frontier-model readiness against anticipated Bill obligations
- `sign_uk_ai_readiness_attestation` — Pro/Enterprise: cryptographically signed readiness cert
- `enforcement_status` — current framework + upcoming Bill timeline

## Install

```bash
pip install uk-ai-bill-compliance-mcp
```

## Claude Desktop

```json
{
  "mcpServers": {
    "uk-ai": { "command": "uk-ai-bill-compliance-mcp" }
  }
}
```

## Tiers

- **Free** — 10 queries/day, classification + principle audits
- **Pro £199/mo** — unlimited + signed attestations + AI Bill readiness re-scoring + ATRS-ready outputs
- **Enterprise £1,499/mo** — multi-system dashboards, cross-MCP framework crosswalk, co-branded PDFs
- **£5,000 one-time assessment** — bespoke 48h review of your UK AI compliance posture

## Full Compliance Platform

Need UK + EU coverage in one platform? **[councilof.ai](https://councilof.ai)** — UK AI Bill, EU AI Act, DORA, NIS2, CRA, CSRD compliance from £29/mo.

→ **[Get started at councilof.ai](https://councilof.ai)**

## Related MEOK MCPs (ecosystem)

- [`eu-ai-act-compliance-mcp`](https://pypi.org/project/eu-ai-act-compliance-mcp/) — EU AI Act
- [`dora-compliance-mcp`](https://pypi.org/project/dora-compliance-mcp/) — EU DORA
- [`nis2-compliance-mcp`](https://pypi.org/project/nis2-compliance-mcp/) — EU NIS2
- [`cra-compliance-mcp`](https://pypi.org/project/cra-compliance-mcp/) — EU CRA
- [`ai-bom-mcp`](https://pypi.org/project/ai-bom-mcp/) — AI Bill of Materials (CycloneDX ML-BOM + SPDX 3.0 + EU AI Act Annex IV)
- [`csrd-compliance-mcp`](https://pypi.org/project/csrd-compliance-mcp/) — EU CSRD
- [`meok-attestation-verify`](https://pypi.org/project/meok-attestation-verify/) — zero-dep verifier

> **If this tool helps your compliance workflow, please [star this repo](https://github.com/CSOAI-ORG/uk-ai-bill-compliance-mcp/stargazers)** — it helps other teams find it.

## License

MIT — [MEOK AI Labs](https://meok.ai), 2026.

<!-- mcp-name: io.github.CSOAI-ORG/uk-ai-bill-compliance-mcp -->
