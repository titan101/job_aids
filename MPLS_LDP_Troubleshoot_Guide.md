# MPLS LDP Troubleshooting Guide
# Visual conversion spec — paste Section 2 prompt into ChatGPT image gen

---

## SECTION 1 — FULL GUIDE CONTENT (the data)

### TITLE
MPLS LDP Troubleshooting Guide
Subtitle: From Non-Existent to Operational — and Why the LSP Still Doesn't Forward

---

### PLATFORM NOTE — COMMAND SYNTAX
Commands below use IOS-XE / IOS-XR style (show mpls ldp ...).
Juniper JunOS equivalent shown inline where it differs materially.
Scope: LDP (RFC 5036) session establishment + label distribution. RSVP-TE noted separately where relevant.

---

### PART A — THE LDP SESSION STATE MACHINE (top of visual)

Five states. Left to right. Arrows show the transition. Red annotations show what breaks each one.

NON-EXISTENT ──► INITIALIZED ──► OPENSENT ──► OPENRECEIVED ──► OPERATIONAL
     ▲                │               │              │
     └────────────────┴───────────────┴──────────────┘
           (any error tears down session — Hello discovery restarts)

STATE DETAILS (each becomes a card in the visual):

┌─────────────────────────────────────────────────────────┐
│ 1. NON-EXISTENT                      COLOR: RED         │
│ What it means: No Hello adjacency, no LDP session        │
│ Why you're here:                                          │
│   • LDP not enabled on the interface (mpls ip missing)   │
│   • ACL blocking UDP 646 (Hello) or TCP 646 (session)    │
│   • No IGP reachability to peer's transport address      │
│ Fix:                                                       │
│   show mpls ldp discovery                                  │
│   show mpls ldp neighbor                                   │
│   Verify "mpls ip" is applied per-interface, not just     │
│   globally under "mpls ldp router-id"                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 2. INITIALIZED                       COLOR: ORANGE       │
│ What it means: TCP session up, Init message sent          │
│ Why you're stuck here:                                     │
│   • Firewall blocking TCP port 646                         │
│   • Wrong transport-address configured (interface vs      │
│     loopback mismatch)                                     │
│   • Asymmetric routing to the peer's transport address    │
│ Fix:                                                        │
│   show mpls ldp neighbor detail                            │
│   telnet <peer-transport-IP> 646                            │
│   Verify transport-address matches the loopback both       │
│   sides actually route through                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 3. OPENSENT                          COLOR: ORANGE       │
│ What it means: Init sent, waiting on peer's Init reply     │
│ Why you're stuck here:                                     │
│   • LDP parameter mismatch (label space, PVLim, KA hold)  │
│   • MD5 authentication mismatch — silent failure           │
│   • LDP protocol version mismatch (legacy gear)            │
│ Fix:                                                         │
│   debug mpls ldp session (targeted, brief)                  │
│   Verify MD5 password matches exactly on both peers         │
│   show mpls ldp neighbor — look for negotiation errors       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 4. OPENRECEIVED                      COLOR: YELLOW       │
│ What it means: Peer's Init received, KeepAlive sent,        │
│               waiting on peer's KeepAlive to complete        │
│ Why it drops back repeatedly:                                │
│   • KeepAlive filtered by a stateful firewall                │
│   • Hold-timer expired before KeepAlive arrived               │
│   • Unstable link flapping the TCP session mid-negotiation   │
│ Fix:                                                            │
│   show mpls ldp neighbor | include Up time                     │
│   Check hold-time configuration on both peers                  │
│   Check interface error counters for instability                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 5. OPERATIONAL                       COLOR: GREEN         │
│ What it means: Session up — labels are being exchanged     │
│ Still broken? Session up but LSP not forwarding:            │
│   • No label bound for the FEC (no IGP route to prefix)     │
│   • Label filtering — advertise-labels / neighbor filter    │
│   • PHP misconfigured — expecting explicit-null, got        │
│     implicit-null (or vice versa)                            │
│   • MTU too small — large labeled packets silently dropped  │
│ Fix:                                                            │
│   show mpls forwarding-table                                   │
│   show mpls ldp bindings <prefix>                               │
│   traceroute mpls ipv4 <prefix>/<mask>                          │
│   show route <prefix> detail (confirm IGP route exists first)  │
└─────────────────────────────────────────────────────────┘

---

### PART B — MPLS-SPECIFIC FAILURE MATRIX (middle section of visual)

┌──────────────────────┬───────────────────────────────────────────────────────┐
│ SCENARIO             │ WHAT TO CHECK                                         │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ LDP neighbor stuck at │ Confirm "mpls ip" on the interface, not just global.  │
│ Non-Existent / no     │ Check ACL for UDP 646. Verify IGP has a route to the  │
│ discovery             │ peer at all — LDP Hello needs basic reachability.     │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ LDP session up but    │ No IGP route to the FEC prefix — LDP only binds      │
│ traffic still         │ labels to prefixes already in the RIB. Check label    │
│ blackholes mid-LSP    │ filtering (advertise/accept lists) next.              │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Large packets dropped │ MPLS adds label overhead — check "mpls mtu" on every  │
│ only over MPLS core   │ transit hop. Ping with size set and DF-bit to find    │
│                       │ the exact hop that fragments/drops.                   │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ L3VPN PE-PE MPLS is   │ Core LSP working ≠ VPN working. Check route-target    │
│ fine but VRF traffic  │ import/export, VPN label (inner label) in the LFIB,   │
│ fails                 │ and BGP VPNv4/VPNv6 session state separately.         │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ RSVP-TE LSP won't     │ RSVP session state ≠ enough. Check CSPF found a valid │
│ come up               │ path, bandwidth is available end-to-end, and every    │
│                       │ explicit-path hop is actually reachable.              │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ traceroute mpls fails │ Confirms label switching stops mid-path. Check that   │
│ partway through       │ label imposition matches the current IGP best path —  │
│                       │ stale label after a reroute is a common cause.        │
└──────────────────────┴───────────────────────────────────────────────────────┘

---

### PART C — QUICK COMMAND REFERENCE (sidebar or bottom panel)

VERIFICATION COMMANDS (run these in order when an LSP won't forward):

1.  show mpls ldp neighbor
    → Session state per peer — is it even Operational?

2.  show mpls ldp discovery
    → Confirms Hello adjacency exists before session troubleshooting

3.  show mpls ldp bindings <prefix>
    → Local and remote labels bound to a specific FEC

4.  show mpls forwarding-table
    → LFIB — what label actions are actually programmed

5.  show mpls interfaces
    → Confirms MPLS is enabled per-interface, not just globally

6.  traceroute mpls ipv4 <prefix>/<mask>
    → Label-switched path validation, hop by hop

7.  ping mpls ipv4 <prefix>/<mask>
    → Fast LSP liveness check without full traceroute

8.  show ip cef <prefix> detail
    → Confirms label imposition matches the CEF entry

9.  show mpls ldp parameters
    → Router-ID, transport-address, session hold-time in effect

10. debug mpls ldp session state-machine
    → Watch session negotiation live — use carefully in prod

---

### PART D — GOLDEN RULES (footer strip)

• LDP needs basic IP reachability to the peer's transport address before Hello discovery works at all
• "mpls ip" (or "family mpls") must be enabled per-interface — global LDP config alone does nothing
• Session Operational ≠ every FEC has a label — check bindings per prefix, not just session state
• Penultimate-hop popping (implicit-null) is normal at the second-to-last hop — don't mistake it for a missing label
• MD5 auth failures on LDP are silent, exactly like BGP — one wrong character looks like a firewall drop
• RSVP-TE LSPs need a valid CSPF path AND available bandwidth — RSVP session up alone proves neither
• Check the IGP route to the FEC exists before troubleshooting label distribution — LDP won't bind what the RIB doesn't have

---

## SECTION 2 — CHATGPT IMAGE GENERATION PROMPT

Paste the prompt below directly into ChatGPT (use the image generator / DALL-E):

---

Create a professional dark-themed technical reference poster titled "MPLS LDP Troubleshooting Guide" on a dark navy (#0d1b2a) background. White body text, teal (#00bcd4) accent lines and headers. Landscape orientation, 1920x1080px.

LAYOUT — four zones from top to bottom:

ZONE 1 — TOP STRIP: LDP session state machine flow diagram
Five boxes in a horizontal row connected by right-pointing arrows:
  NON-EXISTENT (red border) → INITIALIZED (orange border) → OPENSENT (orange border) → OPENRECEIVED (yellow border) → OPERATIONAL (green border)
A curved arrow loops from OPERATIONAL back to NON-EXISTENT labeled "any error / Hello discovery restarts"
Each box has: state name in bold white on top, one-line description below in small grey text.

ZONE 2 — MIDDLE: Five state detail cards (2+3 grid or single row of 5)
Each card matches its state box color from Zone 1.
Card content:
  Card 1 NON-EXISTENT: "Why: mpls ip missing / ACL blocks UDP 646 / no IGP route to peer" + "Fix: show mpls ldp discovery | show mpls ldp neighbor"
  Card 2 INITIALIZED: "Why: TCP 646 blocked / wrong transport-address" + "Fix: telnet <transport-IP> 646 | verify transport-address"
  Card 3 OPENSENT: "Why: parameter mismatch / MD5 auth mismatch" + "Fix: debug mpls ldp session | verify MD5 password"
  Card 4 OPENRECEIVED: "Why: KeepAlive filtered / hold-timer expired" + "Fix: check hold-time config | check interface stability"
  Card 5 OPERATIONAL: "Session up but LSP not forwarding? Check: FEC has a label | label filtering | PHP config | MTU"
Cards have rounded corners, subtle glow matching their border color.

ZONE 3 — BOTTOM LEFT: Quick command reference panel (dark grey #1a2a3a background)
Title: "VERIFICATION COMMANDS — Run In This Order"
Numbered list 1-9, monospace font, teal numbers, white command text, grey description text:
  1. show mpls ldp neighbor → session state per peer
  2. show mpls ldp discovery → confirms Hello adjacency exists
  3. show mpls ldp bindings <prefix> → labels bound to a FEC
  4. show mpls forwarding-table → LFIB label actions
  5. show mpls interfaces → MPLS enabled per-interface
  6. traceroute mpls ipv4 <prefix>/<mask> → hop-by-hop LSP validation
  7. ping mpls ipv4 <prefix>/<mask> → fast LSP liveness check
  8. show ip cef <prefix> detail → label imposition matches CEF
  9. debug mpls ldp session state-machine → live negotiation (careful in prod)

ZONE 3 — BOTTOM RIGHT: Golden rules panel (dark grey #1a2a3a background)
Title: "GOLDEN RULES"
Seven short rules in white, each prefixed with a teal ✓ checkmark:
  ✓ LDP needs IP reachability to the peer's transport address before Hello even works
  ✓ mpls ip must be enabled per-interface — global config alone does nothing
  ✓ Session Operational ≠ every FEC has a label — check bindings per prefix
  ✓ Implicit-null (PHP) at the penultimate hop is normal, not a missing label
  ✓ MD5 auth failures are silent — one wrong character looks like a firewall drop
  ✓ RSVP-TE needs a valid CSPF path AND bandwidth — session state alone proves neither
  ✓ No IGP route to the FEC = no label bound — check the RIB before blaming LDP

FOOTER: Two lines of small text centered at the very bottom:
  Line 1 — "MPLS LDP Session Reference · Label Distribution & LSP Verification · IOS / IOS-XR / Juniper"
  Line 2 — "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019"
  Line 2 uses teal color (#00bcd4). Line 1 uses grey (#888888). Font size 9pt.

Style: flat design, no gradients, subtle grid lines in background, tech-professional. Font: monospace for commands, clean sans-serif for everything else.

---

## SECTION 3 — CHATGPT CODE INTERPRETER PROMPT (Python / matplotlib)

Use this in ChatGPT's Advanced Data Analysis mode for a pixel-perfect rendered version:

---

Write Python using matplotlib and matplotlib.patches to generate a dark-themed MPLS LDP Troubleshooting Guide poster. Figure size 19.2 x 10.8 inches at 100 DPI (1920x1080 output). Dark navy background #0d1b2a throughout.

SECTION 1 — LDP Session State Machine (top 20% of figure):
Draw 5 rounded rectangle boxes in a horizontal row with right-pointing arrows between them.
Box colors (border + label): Non-Existent=#e74c3c, Initialized=#e67e22, OpenSent=#e67e22, OpenReceived=#f1c40f, Operational=#2ecc71.
Each box: state name in bold white 10pt, one-line description in grey 8pt below.
Draw a curved arrow from Operational back to Non-Existent above the boxes, labeled "error → Hello discovery restarts" in red 8pt.

SECTION 2 — State Detail Cards (middle 45% of figure):
Five cards, either one row of 5 or 3+2 grid. Each card is a rounded rectangle matching its state color as the border.
Background of each card: #1a2a3a. White bold title. Grey body text 8pt.
Card content exactly as specified in the guide above (Why / Fix per state, Operational card uses the "still broken?" checklist).

SECTION 3 — Bottom panels side by side (bottom 30%):
Left panel (#1a2a3a rounded rect): "VERIFICATION COMMANDS" header in teal. 9 numbered commands in monospace 8pt — teal numbers, white command, grey description.
Right panel (#1a2a3a rounded rect): "GOLDEN RULES" header in teal. 7 rules with teal checkmarks in 8pt white text.

Footer — two lines centered at bottom:
  ax.text(0.5, 0.01, "MPLS LDP Session Reference · Label Distribution & LSP Verification · IOS / IOS-XR / Juniper", color="#888888", fontsize=7, ha="center", transform=fig.transFigure)
  ax.text(0.5, 0.005, "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019", color="#00bcd4", fontsize=7, ha="center", transform=fig.transFigure)

Save as mpls_ldp_troubleshoot_guide.png at 100 DPI.
