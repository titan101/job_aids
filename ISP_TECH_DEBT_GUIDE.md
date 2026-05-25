# The Anatomy of Technical Debt in an ISP Environment — Reference Guide
# See ISP_TECH_DEBT_CHATGPT_PROMPTS.md for PNG poster + PDF carousel prompts.

---

## THE MENTAL MODEL

Technical debt in software = code shortcuts that slow future development.
Technical debt in an ISP = decisions that were "good enough then" but cost exponentially more the longer they stay.

The difference: software debt is invisible. ISP technical debt is physical, distributed across
thousands of devices, and when it fails — customers notice in seconds.

ISP technical debt is unique because:
  - It has a physical layer (EoL hardware you can't just "refactor")
  - It lives at internet scale — one config mistake = global reachability impact
  - It accumulates in silence — the network "works" until suddenly it doesn't
  - It concentrates in people, not just systems — tribal knowledge is the invisible debt

---

## THE 6 CATEGORIES OF ISP TECHNICAL DEBT

### 1. PROTOCOL DEBT
Definition: Legacy protocols still running alongside newer replacements, creating operational complexity with no business justification.

Examples:
  - LDP still running alongside SR-MPLS (deployed but not fully migrated)
  - RSVP-TE tunnels nobody knows the purpose of (1,200 tunnels, 400 active, 800 unknown)
  - OSPF running in the core when IS-IS was partially deployed then abandoned
  - IPv4-only network — IPv6 "planned for next year" for 8 years
  - Multiple IGP instances from acquisitions that were never consolidated
  - BGP communities defined 15 years ago with no documentation of meaning

Hidden cost: every engineer must understand ALL protocols, not just the intended ones.
MTTR impact: troubleshooting time multiplied by protocol count.

### 2. HARDWARE DEBT
Definition: Infrastructure running past end-of-life, end-of-support, or beyond its designed capacity.

Examples:
  - Core routers deployed in 2010, EoL declared 2018, still handling 400Gbps in 2025
  - No vendor security patches available (can't fix CVEs without replacement)
  - Spare parts sourced from grey market (unknown reliability)
  - Chassis running at 95% capacity with no upgrade path
  - 10G interfaces in a network that needs 100G
  - Linecard slots full — no expansion room without chassis replacement

Hidden cost: single hardware failure = no redundancy, no spare, emergency procurement.
Security impact: unpatched CVEs on internet-facing hardware = active attack surface.

### 3. CONFIGURATION DEBT
Definition: Absence of standards resulting in each device being a unique "snowflake" — configured differently by whoever touched it last.

Examples:
  - 500 routers, 500 unique BGP timer configurations
  - No naming convention — "CORE-RTR-01", "NYC_CORE_R1", "newyork-core1" all exist
  - Access-lists built over 12 years — nobody knows which entries are still needed
  - NTP servers: 6 different sources across the fleet
  - SNMP communities: 15 different strings, no audit since 2019
  - Loopback addressing: 3 different schemes from 3 different network architects

Hidden cost: every change requires reading the full config — no muscle memory, no templates.
Automation impact: you cannot automate what isn't standardized.

### 4. AUTOMATION DEBT
Definition: Manual processes doing work that should be handled by code, templates, or orchestration.

Examples:
  - Provisioning a new BGP peer: 4 hours, manual SSH, copy-paste from a Word doc
  - IP address management: a shared Excel spreadsheet
  - Change management: email thread with config attached
  - Capacity planning: quarterly report built manually from SNMP polls
  - Incident response: engineer SSHs to 40 devices to find the fault
  - No golden config templates — every provisioning starts from scratch

Measurable cost: provisioning time, MTTR, human error rate.
Scale impact: manual ops don't scale — as the network grows, you need more engineers,
not more automation. Headcount grows linearly with network size.

### 5. DOCUMENTATION DEBT
Definition: Operational knowledge that lives in people's heads instead of accessible systems.

Examples:
  - Network topology diagram last updated 2021 (two major expansions ago)
  - "Bob knows how the MPLS traffic engineering was set up" — Bob left in 2023
  - No runbooks for common failure scenarios
  - BGP policy rationale never written down — just "inherited from the previous team"
  - IPAM shows 60% of allocations as "unknown usage"
  - Maintenance windows rely on one engineer's personal knowledge of dependencies

Operational risk: every engineer departure takes undocumented knowledge with them.
Onboarding cost: new engineers take 6-12 months to become productive (vs 2-3 months with docs).

### 6. SECURITY DEBT
Definition: Security controls deferred, skipped, or never implemented — often invisible until exploited.

Examples:
  - No RPKI/ROV enforcement (route hijacking exposure — see: 2021 Vodafone Idea incident)
  - No BCP38 (ingress filtering) — network can be used as DDoS amplification source
  - BGP sessions with no MD5/TCP-AO authentication
  - Management plane accessible from internet (no OOB, no bastion)
  - No IRR registration for announced prefixes
  - Logging to syslog servers with no alerts, no retention policy
  - Default SNMP communities (public/private) still enabled on some devices

Business risk: a single BGP hijack of customer prefixes is a SLA breach and reputational event.
Compliance risk: MANRS, NIST, and customer contracts increasingly require routing security.

---

## HOW DEBT ACCUMULATES — THE LIFECYCLE

Stage 1 — THE QUICK FIX
"The network is down, customers are affected. Fix it now, document it later."
A workaround gets applied. The fix works. Documentation never happens.

Stage 2 — THE WORKAROUND LAYERS
The workaround becomes permanent. Future changes are built around it.
Engineers new to the team learn the workaround as "how it works."

Stage 3 — KNOWLEDGE SILOES
The original engineer who applied the fix becomes the single source of truth.
Nobody else fully understands the dependency chain.

Stage 4 — CHANGE FEAR
The phrase "don't touch it, it works" enters the team vocabulary.
Change windows shrink. Fewer changes attempted. Backlog grows.

Stage 5 — CRISIS POINT
Hardware failure. BGP incident. Security breach. Capacity exhaustion.
The debt becomes visible — usually to customers first.

Stage 6 — FORCED REMEDIATION
Emergency budget approved. External consultants engaged.
The fix costs 5–10× what proactive remediation would have cost.
Then: repeat from Stage 1 if root causes are not addressed.

---

## MEASURING YOUR DEBT

Protocol Debt Score:
  - Count unique routing protocols running in the network
  - Count orphaned tunnels/LSPs with unknown purpose
  - % of features deployed but not fully migrated to

Hardware Debt Score:
  - % of devices past EoL date
  - % of devices past EoS (End of Software Support)
  - # of devices with open unpatched CVEs (CVSS > 7.0)
  - # of chassis running > 80% capacity

Configuration Debt Score:
  - # of unique configuration patterns for the same function (NTP, logging, BGP timers)
  - % of devices provisioned from a standard template vs hand-crafted
  - Age of last access-list / prefix-list audit

Automation Debt Score:
  - Mean time to provision a new BGP peer (hours)
  - % of changes executed via automation vs manual CLI
  - MTTR for common failure types (benchmark against industry)

Documentation Debt Score:
  - Age of network topology diagrams
  - % of runbooks covering top 10 incident types
  - # of engineers who can operate the network independently

Security Debt Score:
  - % of originated prefixes covered by ROAs
  - % of BGP sessions with authentication
  - % of devices with management plane access restricted

---

## REMEDIATION PRIORITIZATION FRAMEWORK

Score each debt item on three axes (1–5):
  RISK:   What is the blast radius if this fails? (1=low, 5=customer-impacting outage)
  COST:   What is the total cost of remediation? (1=hours, 5=multi-quarter project)
  EFFORT: How much engineering capacity is required? (1=single change, 5=team effort)

Priority = RISK × (1 / COST) × (1 / EFFORT)
High risk + low cost + low effort = do it now.
High risk + high cost + high effort = plan it, fund it, commit to a timeline.
Low risk + any cost/effort = backlog, revisit quarterly.

The trap: most teams address low-risk/low-effort items and ignore high-risk/high-effort items.
The high-risk items are the ones that cause 3 AM calls.

---

## GOLDEN RULES

1.  Every workaround applied without a follow-up ticket is a future incident waiting to happen.
2.  "It works" is not a reason to keep something — understand WHY it works or it will break you.
3.  Automation cannot fix what isn't standardized — kill the snowflakes first.
4.  Hardware debt is the only category with a hard deadline — EoL is not negotiable.
5.  Documentation debt compounds fastest — every team change makes it worse, not better.
6.  Security debt has zero warning — it doesn't degrade gradually, it fails completely.
7.  You cannot manage what you cannot measure — define your debt metrics before remediation.
8.  Forced remediation costs 5–10× proactive remediation. Every time. Without exception.
9.  The most dangerous debt is the kind everyone knows about and nobody is responsible for.
10. Technical debt is a leadership problem first, an engineering problem second.
