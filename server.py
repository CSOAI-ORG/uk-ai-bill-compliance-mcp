#!/usr/bin/env python3
"""
UK AI Regulation Compliance MCP Server
=======================================
By MEOK AI Labs | https://meok.ai

Automates UK AI regulation compliance under the **context-specific, pro-innovation**
UK approach set out by DSIT. Covers:

  - UK AI Regulation White Paper (March 2023 + February 2024 government response)
  - The five UK AI principles: Safety, Transparency, Fairness, Accountability, Contestability
  - Regulator-level implementation from the Digital Regulation Cooperation Forum (DRCF):
      ICO (Information Commissioner's Office) — data + AI governance
      FCA (Financial Conduct Authority) — algorithmic decision-making in finance
      MHRA (Medicines and Healthcare products Regulatory Agency) — SaMD / AIaMD
      CMA (Competition and Markets Authority) — AI competition + foundation models
      Ofcom — AI + online safety
      HSE (Health and Safety Executive) — AI in workplace
  - AI Safety Institute (AISI) — frontier model evaluations + commitments
  - Public-sector AI: Algorithmic Transparency Recording Standard (ATRS)
  - UK AI Opportunities Action Plan (January 2025)
  - Upcoming AI (Regulation) Bill — scope, timeline, anticipated binding obligations

POSITIONING: UK does NOT have an EU-AI-Act-style horizontal statute (yet). UK
regulators operate under *existing* legal frameworks applying the five principles.
This MCP maps where your AI system sits against each principle + regulator AND
gives you a running readiness score for the AI Bill that government has confirmed
is in scope for this Parliament.

Install: pip install uk-ai-bill-compliance-mcp
Run:     python server.py
"""

import json
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

import os as _os
import sys
import os

_MEOK_API_KEY = _os.environ.get("MEOK_API_KEY", "")

try:
    from auth_middleware import check_access as _shared_check_access
except ImportError:
    def _shared_check_access(api_key: str = ""):
        if _MEOK_API_KEY and api_key and api_key == _MEOK_API_KEY:
            return True, "OK", "pro"
        if _MEOK_API_KEY and api_key and api_key != _MEOK_API_KEY:
            return False, "Invalid API key. Get one at https://meok.ai/api-keys", "free"
        return True, "OK, Pro at https://www.csoai.org/checkout", "free"


try:
    from attestation import get_attestation_tool_response
    _ATTESTATION_LOCAL = True
except ImportError:
    _ATTESTATION_LOCAL = False

_ATTESTATION_API = _os.environ.get(
    "MEOK_ATTESTATION_API", "https://meok-attestation-api.vercel.app"
)


def _sign_via_api(api_key: str, regulation: str, entity: str, score: float,
                  findings: list, articles_audited: list, tier: str = "pro",
                  include_pdf_base64: bool = False) -> dict:
    """Fallback: hit the remote MEOK signing API when the local module isn't present."""
    import urllib.request as _url, urllib.error as _urlerr
    payload = {
        "api_key": api_key, "regulation": regulation, "entity": entity,
        "score": score, "findings": findings or [],
        "articles_audited": articles_audited or [], "tier": tier,
    }
    try:
        req = _url.Request(
            f"{_ATTESTATION_API}/sign",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with _url.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except _urlerr.HTTPError as e:
        try:
            return json.loads(e.read())
        except Exception:
            return {"error": f"Attestation API HTTP {e.code}. Contact hello@meok.ai."}
    except Exception as e:
        return {"error": f"Could not reach MEOK attestation API: {e}. Contact hello@meok.ai."}


def _attestation(regulation, entity, score, findings, articles_audited, tier,
                 include_pdf_base64, api_key):
    if _ATTESTATION_LOCAL:
        return get_attestation_tool_response(
            regulation=regulation, entity=entity, score=score, findings=findings,
            articles_audited=articles_audited, tier=tier,
            include_pdf_base64=include_pdf_base64,
        )
    return _sign_via_api(
        api_key=api_key, regulation=regulation, entity=entity, score=score,
        findings=findings, articles_audited=articles_audited or [], tier=tier,
        include_pdf_base64=include_pdf_base64,
    )


def check_access(api_key: str = ""):
    return _shared_check_access(api_key)


FREE_DAILY_LIMIT = 50
_usage: dict[str, list[datetime]] = defaultdict(list)
STRIPE_199 = "https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t"
STRIPE_1499 = "https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t"
STRIPE_5K = "https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t"


def _rl(tier: str = "free") -> Optional[str]:
    if tier in ("pro", "professional", "enterprise"):
        return None
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=1)
    _usage["anonymous"] = [t for t in _usage["anonymous"] if t > cutoff]
    if len(_usage["anonymous"]) >= FREE_DAILY_LIMIT:
        return f"Free tier limit ({FREE_DAILY_LIMIT}/day). Pro £199/mo: {STRIPE_199}"
    _usage["anonymous"].append(now)
    return None


# ── UK AI Regulation Knowledge Base ─────────────────────────────
FIVE_PRINCIPLES = {
    "safety": {
        "name": "Safety, Security & Robustness",
        "summary": "AI systems must function robustly, securely, and safely throughout their lifecycle, with risks continuously identified, assessed, and managed.",
        "evidence_expected": [
            "Risk register covering safety-critical behaviours",
            "Adversarial robustness testing results",
            "Incident-response plan for AI failures",
            "Model monitoring + drift detection",
        ],
        "primary_regulators": ["HSE", "MHRA", "DSIT", "AISI"],
    },
    "transparency": {
        "name": "Appropriate Transparency & Explainability",
        "summary": "Where appropriate given context, AI systems must be able to provide users and regulators with sufficient information about how decisions are reached.",
        "evidence_expected": [
            "Model documentation (model card / system card)",
            "Decision-logging capability",
            "User-facing explanation mechanisms",
            "Public listing on Algorithmic Transparency Recording Standard (if public-sector)",
        ],
        "primary_regulators": ["ICO", "CDEI", "DSIT"],
    },
    "fairness": {
        "name": "Fairness",
        "summary": "AI systems must not discriminate against individuals or groups; outcomes must be justifiable under Equality Act 2010 and sector-specific anti-discrimination law.",
        "evidence_expected": [
            "Equality impact assessment (EqIA)",
            "Bias testing across protected characteristics (Equality Act 2010 s.4)",
            "Disparate-impact analysis",
            "Mitigation plan for identified disparities",
        ],
        "primary_regulators": ["ICO", "EHRC", "FCA"],
    },
    "accountability": {
        "name": "Accountability & Governance",
        "summary": "Clear governance with identifiable accountable persons throughout the AI lifecycle.",
        "evidence_expected": [
            "Board / senior-accountable-person assignment",
            "AI governance framework document",
            "Training log for decision-makers",
            "Third-party risk-management for AI vendors",
        ],
        "primary_regulators": ["FCA", "PRA", "ICO"],
    },
    "contestability": {
        "name": "Contestability & Redress",
        "summary": "Affected parties must be able to challenge AI decisions and obtain redress where appropriate.",
        "evidence_expected": [
            "Published route to contest automated decisions",
            "Human-in-the-loop for material decisions",
            "Documented appeal / complaint handling SLA",
            "Regulator-complaint signposting",
        ],
        "primary_regulators": ["ICO", "FOS", "Ofcom"],
    },
}

SECTOR_REGULATORS = {
    "finance": {"name": "FCA / PRA / Bank of England", "key_guidance": [
        "FCA Discussion Paper DP5/22 on AI + Machine Learning",
        "PRA/FCA SS1/23 Model Risk Management",
        "Bank of England AI Public-Private Forum output",
    ]},
    "healthcare": {"name": "MHRA + NHSE", "key_guidance": [
        "MHRA Software and AI as a Medical Device roadmap",
        "NHS AI Lab Buyer's Guide",
        "Digital Technology Assessment Criteria (DTAC)",
    ]},
    "employment": {"name": "ICO + EHRC + DWP", "key_guidance": [
        "ICO Guidance on AI and data protection",
        "EHRC guidance on AI in recruitment",
        "TUC Manifesto on AI at Work",
    ]},
    "public_sector": {"name": "CDDO + CDEI + DSIT", "key_guidance": [
        "Algorithmic Transparency Recording Standard (mandatory for central gov)",
        "CDEI AI Assurance Roadmap",
        "Generative AI Framework for HMG",
    ]},
    "consumer_online": {"name": "Ofcom + CMA + ICO", "key_guidance": [
        "Online Safety Act 2023 — AI + harmful content",
        "CMA AI Foundation Models initial report + update",
        "ICO 'Consultation on Generative AI and data protection'",
    ]},
    "education": {"name": "DfE + Ofsted + ICO", "key_guidance": [
        "DfE policy paper on generative AI in education (2023, 2024)",
        "Ofsted approach to AI in schools",
    ]},
    "transport": {"name": "DfT + ORR + CAA", "key_guidance": [
        "Automated Vehicles Act 2024",
        "CAA AI/ML safety guidance for aviation",
    ]},
    "defence_security": {"name": "MoD + NCSC", "key_guidance": [
        "Ambitious, Safe, Responsible — MoD AI Strategy",
        "NCSC Guidelines for Secure AI System Development (joint with CISA + allies)",
    ]},
}

# AI (Regulation) Bill — anticipated scope (government consultation response + open letters)
AI_BILL_ANTICIPATED_SCOPE = {
    "in_scope_models": "Currently signalled: 'most powerful' frontier foundation models only (developer-level obligations)",
    "anticipated_obligations": [
        "Pre-deployment safety testing against capability thresholds",
        "Information sharing with AI Safety Institute (AISI)",
        "Serious incident reporting",
        "Misuse-mitigation plan prior to deployment",
        "Model-evaluation transparency",
        "Accountability designation for the developer's most senior responsible person",
    ],
    "likely_timeline": {
        "consultation_close_target": "2025 (DSIT consultation window)",
        "bill_introduction_target": "This Parliament (signalled by King's Speech 2024 and subsequent ministerial statements)",
        "commencement_target": "Phased — initial provisions 2026, full enforcement 2027+",
    },
    "government_position": (
        "UK approach remains context-specific and sector-based for the vast majority of AI "
        "systems. Binding legislation is targeted at the frontier tier. Sectoral regulators "
        "retain primary enforcement authority under existing law (Equality Act 2010, GDPR/UK "
        "Data Protection Act, consumer protection, product safety, financial services law, etc.)"
    ),
}


mcp = FastMCP(
    "uk-ai-bill-compliance",
    instructions=(
        "MEOK AI Labs UK AI Regulation MCP. Automates audits against the UK AI Regulation "
        "White Paper five principles (safety, transparency, fairness, accountability, "
        "contestability) + upcoming AI (Regulation) Bill frontier-model obligations + "
        "sector-specific regulator guidance (ICO, FCA, MHRA, CMA, Ofcom, HSE). Ask me to "
        "classify your system, audit against each principle, map to the sector regulator, "
        "or issue a signed readiness attestation."
    ),
)

def _server_meter_check(api_key: str = "") -> dict:
    """Calls the live /verify endpoint for server-side metering. Returns the JSON dict.
    Fail-open: if /verify is unreachable or KV isn't configured, returns allowed=True
    (so the local rate-limit in _check_rate_limit remains the safety net)."""
    try:
        data = json.dumps({"api_key": api_key, "tool": ""}).encode()
        req = _meter_urlreq.Request(_METER_URL, data=data,
            headers={"Content-Type": "application/json"}, method="POST")
        with _meter_urlreq.urlopen(req, timeout=2.5) as r:
            d = json.loads(r.read())
            if isinstance(d, dict) and "allowed" in d:
                return d
    except Exception:
        pass
    return {"allowed": True, "tier": "anonymous", "remaining": 200, "upgrade_url": "https://meok.ai/pricing"}


_METER_URL = "https://proofof.ai/verify"


@mcp.tool()
def classify_system(
    sector: str,
    system_type: str,
    public_sector: bool = False,
    is_frontier_model: bool = False,
    api_key: str = "",
) -> str:
    """Classify a UK AI system against sector regulator + signalled AI Bill scope.

    - sector: finance | healthcare | employment | public_sector | consumer_online | education | transport | defence_security
    - system_type: plain description (e.g. 'credit scoring', 'clinical triage')
    - is_frontier_model: True for the most capable general-purpose foundation models
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_199})

    sector_info = SECTOR_REGULATORS.get(sector.lower(), {
        "name": "No named sector regulator — defaults to ICO + relevant general-purpose regulators",
        "key_guidance": ["ICO Guidance on AI and data protection", "DSIT context-specific principles"],
    })
    ai_bill_scope = "IN_SCOPE (frontier-model obligations expected)" if is_frontier_model else "LIKELY_OUT_OF_SCOPE of binding Bill; still regulated via sectoral law + five principles"

    atrs_required = public_sector
    return json.dumps({
        "sector": sector,
        "system_type": system_type,
        "is_public_sector": public_sector,
        "is_frontier_model": is_frontier_model,
        "regulator_primary": sector_info["name"],
        "regulator_key_guidance": sector_info["key_guidance"],
        "ai_bill_scope": ai_bill_scope,
        "algorithmic_transparency_recording_standard_required": atrs_required,
        "five_principles_required": True,
        "applicable_statutes": [
            "UK GDPR + Data Protection Act 2018",
            "Equality Act 2010",
            "Consumer Rights Act 2015",
            "Product Safety and Metrology etc. (Amendment) Regulations 2024 (for safety-critical)",
        ],
        "next_actions": [
            "Run audit_principle() for each of the 5 principles",
            "Run audit_sector_regulator() for the primary regulator above",
            "If public-sector: open an ATRS record",
            "If frontier-model: engage AISI + prepare for Bill obligations",
        ],
        "upsell_pro": f"Unlimited classification + signed UK AI readiness attestation: Pro £199/mo at {STRIPE_199}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def audit_principle(principle: str, current_controls_csv: str = "", api_key: str = "") -> str:
    """Audit the entity's current controls against one of the 5 UK AI principles.

    - principle: safety | transparency | fairness | accountability | contestability
    - current_controls_csv: comma-separated keywords describing what you have in place
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_199})

    p = FIVE_PRINCIPLES.get(principle.lower())
    if not p:
        return json.dumps({"error": f"Unknown principle '{principle}'. Use: {list(FIVE_PRINCIPLES.keys())}"})

    controls = [c.strip().lower() for c in current_controls_csv.split(",") if c.strip()]
    hits = []
    gaps = []
    for evidence in p["evidence_expected"]:
        ev_lower = evidence.lower()
        matched = any(
            any(word in ev_lower for word in ctrl.split())
            for ctrl in controls
        )
        (hits if matched else gaps).append(evidence)
    score = round(100 * len(hits) / max(1, len(p["evidence_expected"])), 1)

    return json.dumps({
        "principle": principle,
        "principle_name": p["name"],
        "score_percent": score,
        "evidence_present": hits,
        "evidence_gaps": gaps,
        "primary_regulators": p["primary_regulators"],
        "recommendation": (
            "Strong coverage. Proceed with signed attestation + ATRS entry where applicable."
            if score >= 80 else
            "Partial coverage. Close gaps before pre-deployment."
            if score >= 50 else
            "Material gaps. Assign senior-accountable-person and build evidence plan before proceeding."
        ),
    }, indent=2)


@mcp.tool()
def audit_sector_regulator(sector: str, api_key: str = "") -> str:
    """Surface the primary sector regulator + key guidance for an AI system in that sector."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_199})
    info = SECTOR_REGULATORS.get(sector.lower())
    if not info:
        return json.dumps({"error": f"Unknown sector '{sector}'. Use: {list(SECTOR_REGULATORS.keys())}"})
    return json.dumps({
        "sector": sector,
        **info,
        "note": "Under the UK context-specific approach, this regulator enforces existing sectoral law + applies the five AI principles.",
    }, indent=2)


@mcp.tool()
def ai_bill_readiness(
    entity_name: str,
    is_frontier_model: bool,
    has_pre_deployment_eval: bool = False,
    has_aisi_engagement: bool = False,
    has_incident_reporting: bool = False,
    has_misuse_mitigation_plan: bool = False,
    has_senior_accountable_person: bool = False,
    api_key: str = "",
) -> str:
    """Score readiness against anticipated AI (Regulation) Bill obligations."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_199})

    if not is_frontier_model:
        return json.dumps({
            "entity_name": entity_name,
            "scope_assessment": "OUT_OF_BILL_SCOPE",
            "note": "Current signalled Bill scope is frontier foundation models only. Continue to apply the five principles + sectoral law.",
            "ai_bill_scope_details": AI_BILL_ANTICIPATED_SCOPE,
        }, indent=2)

    items = [
        ("pre_deployment_evaluation", has_pre_deployment_eval),
        ("aisi_engagement", has_aisi_engagement),
        ("serious_incident_reporting", has_incident_reporting),
        ("misuse_mitigation_plan", has_misuse_mitigation_plan),
        ("senior_accountable_person", has_senior_accountable_person),
    ]
    score = round(100 * sum(1 for _, v in items if v) / len(items), 1)
    gaps = [k for k, v in items if not v]

    return json.dumps({
        "entity_name": entity_name,
        "scope_assessment": "IN_BILL_SCOPE — frontier model",
        "readiness_score_percent": score,
        "gaps": gaps,
        "anticipated_obligations": AI_BILL_ANTICIPATED_SCOPE["anticipated_obligations"],
        "anticipated_timeline": AI_BILL_ANTICIPATED_SCOPE["likely_timeline"],
        "upsell_pro": f"Generate a signed UK AI Bill readiness attestation and quarterly re-score: Pro £199/mo at {STRIPE_199}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def sign_uk_ai_readiness_attestation(
    entity_name: str,
    overall_score: float,
    principles_audited_csv: str = "safety,transparency,fairness,accountability,contestability",
    findings_csv: str = "",
    include_pdf_base64: bool = False,
    api_key: str = "",
) -> str:
    """Generate a cryptographically signed UK AI readiness attestation (Pro/Enterprise).

    HMAC-SHA256 signed JSON + public verify URL + optional PDF. Auditors / boards
    / procurement validate via verify_url without MEOK backend access. Expires 365d.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if tier == "free":
        return json.dumps({
            "error": "Signed attestations require Pro (£199/mo) or Enterprise tier.",
            "upgrade_url": STRIPE_199,
            "why_pro": "HMAC-signed attestation with public verify URL. UK procurement-ready (Digital Marketplace, CCS frameworks, public-sector ATRS).",
        })

    findings = [f.strip() for f in findings_csv.split(",") if f.strip()]
    principles = [p.strip() for p in principles_audited_csv.split(",") if p.strip()]
    cert = _attestation(
        regulation="UK AI Regulation (White Paper five principles + AI Bill readiness)",
        entity=entity_name,
        score=overall_score,
        findings=findings or [f"Overall UK AI readiness score: {overall_score}"],
        articles_audited=principles or None,
        tier=tier,
        include_pdf_base64=include_pdf_base64,
        api_key=api_key,
    )
    return json.dumps(cert, indent=2)


@mcp.tool()
def enforcement_status(api_key: str = "") -> str:
    """Current UK AI regulation status + upcoming AI (Regulation) Bill timeline."""
    now = datetime.now(timezone.utc)
    return json.dumps({
        "framework": "UK AI Regulation White Paper (March 2023) + government response (Feb 2024) + AI Opportunities Action Plan (Jan 2025)",
        "approach": "Context-specific, pro-innovation. No horizontal statute yet. Sectoral regulators enforce existing law + the five principles.",
        "ai_bill": AI_BILL_ANTICIPATED_SCOPE,
        "current_public_sector_obligations": [
            "Algorithmic Transparency Recording Standard — central government departments + ALBs (mandatory since January 2024)",
            "Data Protection Impact Assessments (DPIAs) — UK GDPR Article 35",
            "Equality Impact Assessments — PSED under Equality Act 2010 s.149",
        ],
        "key_voluntary_commitments": [
            "AI Safety Institute frontier model evaluation MoU (signatories include Anthropic, Google DeepMind, Microsoft, OpenAI, Meta, Amazon)",
            "Bletchley Declaration (November 2023) + Seoul Declaration (May 2024)",
        ],
        "pro_upsell": f"Unlimited audits + signed UK AI readiness attestations at £199/mo: {STRIPE_199}",
    }, indent=2)


def main():
    """Entry point for the UK AI Regulation MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
