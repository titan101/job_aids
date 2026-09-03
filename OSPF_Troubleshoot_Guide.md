# OSPF Troubleshooting Guide
# Visual conversion spec — paste Section 2 prompt into ChatGPT image gen

---

## SECTION 1 — FULL GUIDE CONTENT (the data)

### TITLE
OSPF Troubleshooting Guide
Subtitle: From Down to Full — and Why the Route Still Isn't There

---

### PLATFORM NOTE — COMMAND SYNTAX
Commands below use IOS / IOS-XE style (show ip ospf ...).
IOS-XR prefix: drop "ip" → show ospf neighbor, show ospf database
Juniper JunOS equivalent shown inline where it differs materially.

---

### PART A — THE OSPF NEIGHBOR STATE MACHINE (top of visual)

Eight states. Left to right. Arrows show the transition. Red annotations show what breaks each one.

DOWN ──► ATTEMPT ──► INIT ──► 2-WAY ──► EXSTART ──► EXCHANGE ──► LOADING ──► FULL
  ▲          │           │        │          │            │            │
  └──────────┴───────────┴────────┴──────────┴────────────┴────────────┘
        (dead-timer expiry or config error drops back to Down)

STATE DETAILS (each becomes a card in the visual):

┌─────────────────────────────────────────────────────────┐
│ 1. DOWN                              COLOR: RED          │
│ What it means: No Hello received from this neighbor yet   │
│ Why you're here:                                            │
│   • OSPF not enabled on the interface / area mismatch      │
│   • Interface down or missing IP                            │
│   • ACL blocking IP protocol 89 or multicast 224.0.0.5/6   │
│   • passive-interface configured where a peer is expected  │
│ Fix:                                                          │
│   show ip ospf interface brief                                │
│   show ip protocols                                           │
│   Verify network statement / area matches on both sides       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 2. ATTEMPT                           COLOR: ORANGE        │
│ What it means: NBMA only — neighbor manually configured,  │
│               no Hello received yet                          │
│ Why you're stuck here:                                        │
│   • Only valid on NBMA / point-to-multipoint networks         │
│   • "neighbor <IP>" statement missing or wrong                │
│   • Underlying Layer 2 mapping (Frame Relay / PVC) missing    │
│ Fix:                                                            │
│   show ip ospf neighbor                                        │
│   Verify "neighbor <IP>" statement under the OSPF process       │
│   Check Frame Relay map / underlying L2 circuit                 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 3. INIT                              COLOR: ORANGE        │
│ What it means: Hello received, but it doesn't list my      │
│               router ID yet — one-way communication          │
│ Why you're stuck here:                                        │
│   • Unidirectional path — check for a one-way ACL/firewall    │
│   • Hello/dead timer mismatch preventing recognition           │
│   • Neighbor hasn't processed my Hello yet (transient, brief) │
│ Fix:                                                            │
│   show ip ospf neighbor detail                                 │
│   Verify hello-interval and dead-interval match exactly         │
│   Check for asymmetric filtering in one direction                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 4. 2-WAY                             COLOR: YELLOW         │
│ What it means: Bidirectional Hello confirmed. DR/BDR        │
│               election happens at this state.                 │
│ Why it seems stuck (often isn't):                              │
│   • Normal end-state for DROTHER-to-DROTHER pairs on           │
│     broadcast/NBMA segments — not every neighbor goes Full     │
│   • If Full was expected: priority 0 on one/both sides, or     │
│     network-type mismatch (broadcast vs point-to-point)         │
│ Fix:                                                              │
│   show ip ospf neighbor                                          │
│   show ip ospf interface (check DR / BDR / network type)          │
│   Verify "ip ospf priority" if a specific DR was expected          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 5. EXSTART                           COLOR: YELLOW         │
│ What it means: Master/slave negotiation begins before DBD   │
│               exchange                                         │
│ Why you're stuck here (classic stuck-in-ExStart):              │
│   • MTU mismatch — the single most common cause                │
│   • Duplicate router-ID somewhere in the area                   │
│ Fix:                                                               │
│   show ip ospf interface (compare MTU both sides)                 │
│   show ip ospf neighbor detail                                    │
│   Check for duplicate router-id in "show ip ospf"                  │
│   "ip ospf mtu-ignore" is a workaround, not a fix — verify it's    │
│   actually safe before applying                                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 6. EXCHANGE                          COLOR: YELLOW          │
│ What it means: DBD packets being exchanged to build a        │
│               link-state summary of each other's LSDB          │
│ Why you're stuck here:                                          │
│   • DBD packet loss / corruption on an unstable link            │
│   • Retransmissions piling up on a lossy path                    │
│   • Very large LSDB timing out on a slow/congested link           │
│ Fix:                                                                │
│   show ip ospf neighbor detail (check retransmit counters)         │
│   debug ip ospf adj (careful — verbose)                             │
│   Check interface error/discard counters for packet loss             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 7. LOADING                           COLOR: YELLOW           │
│ What it means: LSRs sent for missing/outdated LSAs,           │
│               waiting on LSU responses                          │
│ Why you're stuck here:                                            │
│   • LSA request/response loss on the link                         │
│   • LSDB inconsistency between the two neighbors                   │
│   • A corrupted LSA triggering repeated re-requests                 │
│ Fix:                                                                  │
│   show ip ospf statistics                                            │
│   debug ip ospf packet (careful — verbose)                            │
│   Check "show ip ospf database" for corrupt/self-conflicting LSAs      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 8. FULL                              COLOR: GREEN            │
│ What it means: Adjacency complete — LSDBs fully synced         │
│ Still broken? Adjacency Full but routes missing:                │
│   • Stub / totally-stubby / NSSA area suppressing external      │
│     (type-5) or inter-area routes as designed                     │
│   • distribute-list or route-map filtering on the ABR              │
│   • Area 0 not contiguous — no path back to the backbone            │
│   • ABR not summarizing/advertising the range you expect             │
│ Fix:                                                                    │
│   show ip ospf database                                                │
│   show ip route ospf                                                   │
│   show ip ospf border-routers                                          │
│   Check "area <id>" stub / nssa configuration on all routers in it       │
└─────────────────────────────────────────────────────────┘

---

### PART B — OSPF-SPECIFIC FAILURE MATRIX (middle section of visual)

┌──────────────────────┬───────────────────────────────────────────────────────┐
│ SCENARIO             │ WHAT TO CHECK                                         │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Stuck in ExStart /    │ MTU mismatch is the #1 cause — compare "show ip ospf  │
│ 2-Way when Full is    │ interface" MTU on both sides first. Also check for    │
│ expected              │ duplicate router-ID and network-type mismatch.        │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ DR/BDR election wrong │ Priority values decide it, not uptime alone. Set      │
│ or flapping           │ "ip ospf priority 0" on routers that should never be  │
│                       │ DR/BDR. Election only re-runs if DR itself goes down. │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Area 0 connectivity   │ Every non-backbone area needs a direct or virtual-    │
│ broken / virtual-link │ link path to area 0. A partitioned backbone silently  │
│ needed                │ blackholes inter-area routes on one side.             │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Full adjacency but    │ Check area type first — stub/NSSA intentionally       │
│ expected routes are   │ suppress type-5 externals. Then check distribute-list │
│ missing               │ / route-map on the ABR before assuming a bug.         │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Adjacency flapping    │ Hello/dead timer mismatch, an unstable link, or MTU   │
│ repeatedly            │ intermittently black-holing large DBD packets are the │
│                       │ three most common causes, in that order.              │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ NBMA / point-to-      │ Network-type mismatch breaks DR election on broadcast │
│ multipoint neighbor   │ segments and blocks adjacency entirely on NBMA links. │
│ never forms           │ Confirm both sides agree on network type explicitly.  │
└──────────────────────┴───────────────────────────────────────────────────────┘

---

### PART C — QUICK COMMAND REFERENCE (sidebar or bottom panel)

VERIFICATION COMMANDS (run these in order when adjacency won't come up):

1.  show ip ospf neighbor
    → One-line view of every neighbor + state + DR/BDR role

2.  show ip ospf neighbor detail
    → Full detail: timers, retransmit counts, dead-timer countdown

3.  show ip ospf interface brief
    → Area, cost, MTU, network type, priority per interface

4.  show ip ospf database
    → The LSDB — confirms what each router actually knows

5.  show ip route ospf
    → OSPF routes actually installed in the RIB

6.  show ip protocols
    → Confirms network statements, passive-interfaces, area config

7.  show ip ospf border-routers
    → Path to ABRs/ASBRs — useful when inter-area routes are missing

8.  debug ip ospf adj
    → Watch adjacency formation live — use carefully in prod

9.  debug ip ospf hello
    → Confirms Hello packets are actually being sent/received

10. clear ip ospf process
    → Full reset — drops every adjacency, use only in a maintenance window

---

### PART D — GOLDEN RULES (footer strip)

• MTU mismatch is the #1 cause of stuck-in-ExStart — check both sides before anything else
• Hello and dead timers must match exactly between neighbors or the adjacency will never form
• Area 0 (backbone) must be contiguous — every other area needs a direct or virtual-link path to it
• 2-Way is the normal end-state for DROTHER-to-DROTHER pairs on broadcast segments — not a stuck state
• Stub/NSSA areas intentionally suppress external routes — check area type before assuming a bug
• Never "clear ip ospf process" in production without a maintenance window — it resets every adjacency
• passive-interface disables Hello entirely — verify it isn't set where a neighbor is expected
• Point-to-point vs broadcast network-type mismatch breaks DR election or blocks adjacency on NBMA links

---

## SECTION 2 — CHATGPT IMAGE GENERATION PROMPT

Paste the prompt below directly into ChatGPT (use the image generator / DALL-E):

---

Create a professional dark-themed technical reference poster titled "OSPF Troubleshooting Guide" on a dark navy (#0d1b2a) background. White body text, teal (#00bcd4) accent lines and headers. Landscape orientation, 1920x1080px.

LAYOUT — four zones from top to bottom:

ZONE 1 — TOP STRIP: OSPF neighbor state machine flow diagram
Eight boxes in a horizontal row connected by right-pointing arrows:
  DOWN (red border) → ATTEMPT (orange border) → INIT (orange border) → 2-WAY (yellow border) → EXSTART (yellow border) → EXCHANGE (yellow border) → LOADING (yellow border) → FULL (green border)
A curved arrow loops from FULL back to DOWN labeled "dead-timer expiry / config error"
Each box has: state name in bold white on top, one-line description below in small grey text.

ZONE 2 — MIDDLE: Eight state detail cards in two rows of four
Each card matches its state box color from Zone 1.
Card content:
  Card 1 DOWN: "Why: OSPF not enabled / interface down / ACL blocks proto 89" + "Fix: show ip ospf interface brief | show ip protocols"
  Card 2 ATTEMPT: "Why: NBMA only — neighbor statement missing/wrong" + "Fix: show ip ospf neighbor | verify neighbor <IP> statement"
  Card 3 INIT: "Why: unidirectional Hello / timer mismatch" + "Fix: show ip ospf neighbor detail | verify hello/dead intervals"
  Card 4 2-WAY: "Why: normal for DROTHER pairs; else priority/network-type" + "Fix: show ip ospf interface | verify ip ospf priority"
  Card 5 EXSTART: "Why: MTU mismatch (most common) / duplicate router-ID" + "Fix: compare MTU both sides | check duplicate router-id"
  Card 6 EXCHANGE: "Why: DBD packet loss on unstable link" + "Fix: check retransmit counters | debug ip ospf adj"
  Card 7 LOADING: "Why: LSR/LSU loss / corrupted LSA" + "Fix: show ip ospf statistics | check LSDB for corruption"
  Card 8 FULL: "Adjacency up but routes missing? Check: area type (stub/NSSA) | distribute-list | area 0 contiguity"
Cards have rounded corners, subtle glow matching their border color.

ZONE 3 — BOTTOM LEFT: Quick command reference panel (dark grey #1a2a3a background)
Title: "VERIFICATION COMMANDS — Run In This Order"
Numbered list 1-9, monospace font, teal numbers, white command text, grey description text:
  1. show ip ospf neighbor → all neighbors + state + DR/BDR role
  2. show ip ospf neighbor detail → timers, retransmit counts
  3. show ip ospf interface brief → area, cost, MTU, network type
  4. show ip ospf database → the LSDB
  5. show ip route ospf → routes actually installed
  6. show ip protocols → network statements, passive-interfaces
  7. show ip ospf border-routers → path to ABRs/ASBRs
  8. debug ip ospf adj → watch adjacency formation live
  9. clear ip ospf process → full reset, maintenance window only

ZONE 3 — BOTTOM RIGHT: Golden rules panel (dark grey #1a2a3a background)
Title: "GOLDEN RULES"
Eight short rules in white, each prefixed with a teal ✓ checkmark:
  ✓ MTU mismatch is the #1 cause of stuck-in-ExStart
  ✓ Hello and dead timers must match exactly or adjacency never forms
  ✓ Area 0 must be contiguous — every area needs a path to the backbone
  ✓ 2-Way is normal for DROTHER pairs on broadcast segments
  ✓ Stub/NSSA areas intentionally suppress external routes
  ✓ Never clear ip ospf process in production without a maintenance window
  ✓ passive-interface disables Hello — check it isn't set where a peer is expected
  ✓ Network-type mismatch breaks DR election or blocks NBMA adjacency

FOOTER: Two lines of small text centered at the very bottom:
  Line 1 — "OSPF Neighbor State Machine Reference · Single-Area & Multi-Area · Cisco / Juniper"
  Line 2 — "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019"
  Line 2 uses teal color (#00bcd4). Line 1 uses grey (#888888). Font size 9pt.

Style: flat design, no gradients, subtle grid lines in background, tech-professional. Font: monospace for commands, clean sans-serif for everything else.

---

## SECTION 3 — CHATGPT CODE INTERPRETER PROMPT (Python / matplotlib)

Use this in ChatGPT's Advanced Data Analysis mode for a pixel-perfect rendered version:

---

Write Python using matplotlib and matplotlib.patches to generate a dark-themed OSPF Troubleshooting Guide poster. Figure size 19.2 x 10.8 inches at 100 DPI (1920x1080 output). Dark navy background #0d1b2a throughout.

SECTION 1 — OSPF Neighbor State Machine (top 20% of figure):
Draw 8 rounded rectangle boxes in a horizontal row with right-pointing arrows between them.
Box colors (border + label): Down=#e74c3c, Attempt=#e67e22, Init=#e67e22, 2-Way=#f1c40f, ExStart=#f1c40f, Exchange=#f1c40f, Loading=#f1c40f, Full=#2ecc71.
Each box: state name in bold white 9pt, one-line description in grey 7pt below.
Draw a curved arrow from Full back to Down above the boxes, labeled "dead-timer expiry / config error" in red 7pt.

SECTION 2 — State Detail Cards (middle 45% of figure):
Two rows of 4 cards. Each card is a rounded rectangle matching its state color as the border.
Background of each card: #1a2a3a. White bold title. Grey body text 7.5pt.
Card content exactly as specified in the guide above (Why / Fix per state, Full card uses the "still broken?" checklist).

SECTION 3 — Bottom panels side by side (bottom 30%):
Left panel (#1a2a3a rounded rect): "VERIFICATION COMMANDS" header in teal. 9 numbered commands in monospace 8pt — teal numbers, white command, grey description.
Right panel (#1a2a3a rounded rect): "GOLDEN RULES" header in teal. 8 rules with teal checkmarks in 8pt white text.

Footer — two lines centered at bottom:
  ax.text(0.5, 0.01, "OSPF Neighbor State Machine Reference · Single-Area & Multi-Area · Cisco / Juniper", color="#888888", fontsize=7, ha="center", transform=fig.transFigure)
  ax.text(0.5, 0.005, "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019", color="#00bcd4", fontsize=7, ha="center", transform=fig.transFigure)

Save as ospf_troubleshoot_guide.png at 100 DPI.
