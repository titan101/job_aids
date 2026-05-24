# RPKI (Resource Public Key Infrastructure) — Reference Guide
# Visual-first. See RPKI_CHATGPT_PROMPTS.md for PNG poster + PDF carousel prompts.

---

## BUSINESS CASE — WHY RPKI EXISTS

THE PROBLEM WITH BGP:
  BGP was designed in 1989 on a foundation of trust between peers.
  Any AS can announce any prefix. There is no cryptographic proof of ownership.
  A misconfigured or malicious router can claim your IP space — and the internet will believe it.

WHAT THIS LOOKS LIKE IN PRACTICE:
  "Route hijacking" — an unauthorized AS announces your prefix.
  Traffic destined for you is diverted to the attacker's network.
  The legitimate owner goes dark. Users see timeouts. No error. No warning.

REAL INCIDENTS (all happened without RPKI enforcement):
  1997  AS7007 bug — route leak caused internet-wide disruption (first major incident)
  2017  80 prefixes hijacked — Google, Apple, Facebook, Microsoft traffic intercepted
  2020  Rostelecom (Russia) — announced Akamai, AWS, Cloudflare, Digital Ocean (~1 hour)
  2020  Telstra (AS1221) — 500 prefixes, 266 ASNs, 50 countries affected, 3 hours
  2021  Vodafone Idea (AS55410) — 30,000+ prefixes, 13× inbound traffic spike
  2025  North Korea — faulty ROA max-length caused their own prefixes to go INVALID

WHAT WAS THERE BEFORE RPKI:
  IRR (Internet Routing Registry) — manually maintained databases of prefix ownership
  Prefix-lists — routers filter based on manually written lists
  Problems with both:
    - No cryptographic verification — anyone can register anything in IRR
    - Manual maintenance — stale data, inconsistent across databases
    - No enforcement mechanism — depends entirely on neighbor cooperation
    - Slow to update — changes take hours or days to propagate

WHAT RPKI PROVIDES:
  Cryptographic proof that a specific AS is authorized to announce a specific prefix.
  Machine-readable, automatically distributed, RIR-signed.
  Routers can validate every BGP announcement against a verified, trusted database.

---

## HOW RPKI WORKS — END TO END

STEP 1 — CREATE ROA (Route Origin Authorization)
  At your RIR's web portal, you create a ROA for each prefix you announce.
  A ROA is a signed certificate containing three fields:
    PREFIX:      The IP prefix (e.g., 192.0.2.0/24)
    MAX-LENGTH:  The most specific prefix allowed (e.g., /24 means no /25s or longer)
    ORIGIN AS:   The AS number authorized to announce this prefix (e.g., AS65001)
  The RIR signs the ROA with their certificate (the Trust Anchor for that region).
  HOSTED vs DELEGATED:
    Hosted RPKI   — RIR manages your CA and signing (recommended for 98% of organizations)
    Delegated RPKI — You run your own CA and publication server (for large operators only, complex)

STEP 2 — RIR PUBLISHES TO RPKI REPOSITORY
  The signed ROA is published to the RIR's RPKI repository.
  Access methods: rsync (RFC 5781) or RRDP (RFC 8182 — preferred, HTTP-based)
  The 5 Trust Anchors (one per RIR):
    AFRINIC  — Africa
    APNIC    — Asia-Pacific, Oceania
    ARIN     — North America, Caribbean
    LACNIC   — Latin America, Caribbean
    RIPE NCC — Europe, Central/West Asia, Russia, Middle East

STEP 3 — VALIDATOR FETCHES AND VERIFIES
  An RPKI validator daemon fetches ROAs from all 5 RIRs.
  It verifies the cryptographic chain from each Trust Anchor.
  Output: VRP table (Validated Route Prefixes) — a trusted list of {AS, prefix, max-length} tuples.
  Common validators:
    Routinator   — NLnet Labs; production-grade; built-in RTR server; most widely deployed
    OctoRPKI     — Cloudflare; cloud-native; used internally by Cloudflare
    FORT         — Lightweight; RFC 6810/8210 compliant; good for constrained environments
    rpki-client  — OpenBSD; minimal; UNIX-style design; used by many ISPs

STEP 4 — RTR PROTOCOL PUSHES VRPs TO ROUTERS
  RTR (RPKI-to-Router) protocol defined in RFC 8210 (v1), RFC 6810 (v0).
  Default port: 323/TCP (root-privileged); many deployments use 3323 or 8282 instead.
  The validator acts as an RTR server. Routers connect as RTR clients.
  Protocol sends: initial full cache, then incremental updates as ROAs change.
  Multiple routers can connect to the same validator.
  Recommendation: run 2+ validators for redundancy. No single point of failure.

STEP 5 — ROUTE ORIGIN VALIDATION (ROV)
  For each BGP announcement received, the router checks the VRP table.
  Result is one of three states:

  VALID       The prefix+AS combination matches a ROA, and length ≤ max-length
              Action: ACCEPT and PREFER in route selection

  INVALID     The AS is not authorized for this prefix, OR the prefix is more specific
              than max-length allows (e.g., /25 announced but ROA only covers /24)
              Action: DROP (best practice) — something is provably wrong

  NOT FOUND   No ROA exists for this prefix — no cryptographic assertion either way
              Action: ACCEPT (most of the internet still lacks ROAs)
              Tagging NOT FOUND for monitoring is recommended during rollout

STEP 6 — POLICY AND ENFORCEMENT
  Recommended policy approach (phased rollout):
    Phase 1: Monitor-only — tag all three states, log INVALID routes, fix your own
    Phase 2: Soft enforcement — deprioritize INVALID, prefer VALID
    Phase 3: Full enforcement — DROP INVALID routes
    Phase 4: Customer requirements — require customers to register ROAs

---

## RPKI STATES — DECISION MATRIX

  State       BGP Route Condition                     Recommended Action
  ─────────────────────────────────────────────────────────────────────────
  VALID       AS + prefix match ROA, length OK        Accept; prefer over NOT FOUND
  INVALID     Wrong AS OR prefix too specific         Drop (cryptographically proven wrong)
  NOT FOUND   No ROA exists for this prefix           Accept; tag for monitoring

IMPORTANT: ~43% of IPv4 prefixes have NO ROA (NOT FOUND) as of 2025.
Dropping NOT FOUND would black-hole a significant portion of the internet.
Enforcement strategy must account for current global RPKI coverage.

---

## CURRENT STATISTICS (2025)

  IPv4 prefixes with ROAs:          57.1%
  IPv6 prefixes with ROAs:          52%
  Global internet traffic VALID:    70.3%
  Major networks fully signed:      AWS, Google, Microsoft, Cloudflare, Meta
  MANRS participants enforcing ROV: Growing — MANRS compliance requires ROV

---

## WHAT RPKI DOES NOT PROTECT AGAINST

  Route leaks       Legitimate AS announces routes via wrong upstream (e.g., AS_PATH valid but topology wrong)
  AS_PATH attacks   Attacker inserts/removes ASNs in the path — RPKI only validates the ORIGIN AS
  BGPsec            Cryptographic signing of the full AS_PATH — RFC 8205; zero production deployment in 2025
  ASPA              AS Provider Authorization — validates path plausibility; RFC draft status as of 2025

RPKI validates only: "Is this AS authorized to originate this prefix?"
It does NOT validate: "Did the route take a plausible path to get here?"

---

## IMPLEMENTATION CHECKLIST (ISP/OPERATOR)

  □ 1. Audit all prefixes you currently announce to BGP
  □ 2. Log into your RIR portal (ARIN / RIPE / APNIC / LACNIC / AFRINIC)
  □ 3. Enable Hosted RPKI on your account
  □ 4. Create a ROA for every prefix — set max-length = your actual announced length
  □ 5. Deploy an RPKI validator (Routinator recommended for most operators)
  □ 6. Connect routers to validator via RTR protocol
  □ 7. Enable ROV in monitor-only mode — log INVALID routes for 2–4 weeks
  □ 8. Fix any of your own prefixes showing INVALID before enforcing
  □ 9. Enable INVALID route dropping (enforcement phase)
  □ 10. Consider requiring downstream customers to create ROAs

---

## COMMON MISTAKES AND BLACKHOLE RISK

MAX-LENGTH TOO RESTRICTIVE (most common mistake):
  You announce 192.0.2.0/22 and create a ROA with max-length /22.
  Later you start announcing 192.0.2.0/24 (a more specific) for traffic engineering.
  That /24 is now INVALID — other networks enforcing RPKI will DROP it.
  Your traffic goes dark. No error. Just timeouts.
  Fix: Set max-length to the most specific prefix you will EVER announce from that block.
  Caution: Setting max-length too permissive (e.g., /32) enables hijacking of sub-prefixes.

WRONG AS IN ROA:
  If your ROA says AS65001 but you announce from AS65002 (e.g., after merger/renumbering),
  every router enforcing RPKI will drop your routes. Full traffic blackhole.

NOT UPDATING ROAS AFTER IP CHANGES:
  Acquired a new block? Announced it before creating the ROA? INVALID immediately.
  Best practice: create the ROA first, wait for propagation (~15 min), then announce the route.

ROA FOR DELEGATED SPACE WITH WRONG PARENT:
  If your upstream delegated a block to you but the ROA chain is broken, routes = INVALID.

---

## GOLDEN RULES

1.  RPKI only validates route ORIGIN — it does NOT validate the full AS path (that's BGPsec).
2.  Create the ROA BEFORE announcing the route — not after.
3.  Set max-length carefully — too short = your own /24s go INVALID.
4.  Run 2+ validators — no single point of failure for your routing security.
5.  Use monitor-only mode first — fix your own INVALID routes before enforcing on others.
6.  NOT FOUND ≠ malicious — it means no ROA exists, not that the route is hijacked.
7.  INVALID = drop with confidence — it means a ROA exists and this announcement violates it.
8.  Update ROAs before announcing new subnets — propagation takes ~15 minutes.
9.  RTR session loss ≠ route loss — routers cache VRPs; graceful degradation is built in.
10. RPKI alone is not complete routing security — combine with IRR, MANRS, BGP communities filtering.
