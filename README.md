# UK AI Regulation Compliance MCP


> ## Buy Starter — £29/mo
> **Signed attestations + unlimited audits + email support.**
> 👉 **[Subscribe at meok.ai](https://buy.stripe.com/cNi4gB80kdQS9wpdCU8k83X)** — instant HMAC signing key + Stripe-managed billing.
>
> Free tier remains MIT-licensed and zero-config. Upgrade only when you need signed compliance artefacts for audit.

[![PyPI](https://img.shields.io/pypi/v/uk-ai-bill-compliance-mcp)](https://pypi.org/project/uk-ai-bill-compliance-mcp/) [![Python](https://img.shields.io/pypi/pyversions/uk-ai-bill-compliance-mcp)](https://pypi.org/project/uk-ai-bill-compliance-mcp/)


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

> **If this tool helps your compliance workflow, please [star this repo](https://github.com/meok-ai-labs/uk-ai-bill-compliance-mcp/stargazers)** — it helps other teams find it.

## Wire it up — full stack

Pair this with the MEOK chain that turns one agent action into ONE signed compliance event:

1. **bft-progress-council-mcp** — anti-loop guardrail
2. **agent-token-budget-mcp** — hard spend cap
3. **agent-prompt-injection-firewall-mcp** — OWASP LLM01 scan
4. **agent-audit-logger-mcp** — hash-chained evidence
5. **a2a-governance-bridge-mcp** — fold N attestations → 1 signed event
6. **agent-incident-relay-mcp** — broadcast incidents to 5 regimes simultaneously

See [meok.ai/mcp-stack](https://meok.ai/mcp-stack) for the full architecture and [meok.ai/mcp-stack/demo](https://meok.ai/mcp-stack/demo) for the live in-browser demo.

## License

MIT — [MEOK AI Labs](https://meok.ai), 2026.


## Sister MCPs

Part of the MEOK **Governance** pack — designed to work together as a fleet. Install the whole pack with `npx meok-setup --pack governance`, or pick the ones you need:

- **EU AI Act** → `uvx eu-ai-act-compliance-mcp` · [PyPI](https://pypi.org/project/eu-ai-act-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/eu-ai-act-compliance-mcp)
- **DORA** → `uvx dora-compliance-mcp` · [PyPI](https://pypi.org/project/dora-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/dora-compliance-mcp)
- **NIS2** → `uvx nis2-compliance-mcp` · [PyPI](https://pypi.org/project/nis2-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/nis2-compliance-mcp)
- **Cyber Resilience Act** → `uvx cra-compliance-mcp` · [PyPI](https://pypi.org/project/cra-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/cra-compliance-mcp)
- **AI Bill of Materials** → `uvx ai-bom-mcp` · [PyPI](https://pypi.org/project/ai-bom-mcp/) · [GitHub](https://github.com/CSOAI-ORG/ai-bom-mcp)
- **AI Incident Reporting** → `uvx ai-incident-reporting-mcp` · [PyPI](https://pypi.org/project/ai-incident-reporting-mcp/) · [GitHub](https://github.com/CSOAI-ORG/ai-incident-reporting-mcp)

Full catalogue + Anthropic Registry verify links: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)


## Protocol coverage + Universal PAYG

This MCP is part of MEOK's 47-MCP fleet that bridges every active agent-interop protocol
and 30+ regulatory frameworks. See the full coverage matrix at [meok.ai/protocols](https://meok.ai/protocols).

**Agent interop protocols supported (8 live):**

- ✅ **MCP** (Anthropic) — native
- ✅ **A2A** (Google + Linux Foundation, absorbed IBM ACP Sept 2025)
- ✅ **IBM ACP** — covered via A2A merge
- ◐ **Stripe ACP** (Agentic Commerce Protocol) — Q3 bridge via [agent-commerce-protocol-mcp](https://github.com/CSOAI-ORG/agent-commerce-protocol-mcp)
- ◐ **AP2** (Google Agent Payments) — partial via [agent-commerce-payments-mcp](https://github.com/CSOAI-ORG/agent-commerce-payments-mcp)
- ◐ **x402** (Coinbase HTTP 402) — partial via api.meok.ai gateway
- → **OASF / AGNTCY** (Cisco Outshift + Linux Foundation) — Q3 bridge
- 👁 **ANP** (Cisco Agent Network) — watch-list

**Pricing options:**

| Option | Price | Best for |
|---|---|---|
| Self-host (this MCP) | £0 — MIT | Devs |
| This MCP Starter | £29/mo | One-MCP teams |
| This MCP Pro | £79/mo | Production + 24h SLA |
| [Universal PAYG](https://buy.stripe.com/00w3cxcgAaEGcIBcyQ8k90s) | £29/mo + £0.0002/call | Spiky usage across many MCPs |
| Substrate bundle (this category) | £99-£499/mo | A whole pack |
| [MEOK Universe](https://buy.stripe.com/cNi9AV0xS8wy5g9aqI8k90u) | £1,499/mo | All 47 MCPs, 500K calls |

Each tier above the free self-host adds HMAC-signed attestations verifiable at
`verify.meok.ai`. Linux Foundation governance on the A2A spine means EU regulated
buyers can deploy without vendor-lock-in objections.

<!-- mcp-name: io.github.CSOAI-ORG/uk-ai-bill-compliance-mcp -->
