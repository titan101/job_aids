# BGP ISP Troubleshooting Guide
# Visual conversion spec — paste Section 2 prompt into ChatGPT image gen

---

## SECTION 1 — FULL GUIDE CONTENT (the data)

### TITLE
BGP ISP Troubleshooting Guide
Subtitle: From Idle to Established — and Everything That Breaks In Between

---

### PLATFORM NOTE — COMMAND SYNTAX
Commands below use IOS-XR / NX-OS style (show bgp ...).
Classic IOS prefix: add "ip" → show ip bgp summary, show ip bgp neighbors, show ip bgp regexp
Juniper JunOS equivalent shown inline where it differs materially.

---

### PART A — THE STATE MACHINE (top of visual)

Six states. Left to right. Arrows show the transition. Red annotations show what breaks each one.

IDLE ──► CONNECT ──► ACTIVE ──► OPENSENT ──► OPENCONFIRM ──► ESTABLISHED
  ▲          │           │            │               │
  └──────────┴───────────┴────────────┴───────────────┘
        (any error returns to IDLE — hold-down timer applies)

STATE DETAILS (each becomes a card in the visual):

┌─────────────────────────────────────────────────────────┐
│ 1. IDLE                              COLOR: RED         │
│ What it means: BGP not attempting connection            │
│ Why you're here:                                        │
│   • BGP process down / neighbor not configured          │
│   • Previous error triggered hold-down timer            │
│   • No route to neighbor IP in RIB                      │
│ Fix:                                                    │
│   show bgp neighbors <IP> | i "BGP state"               │
│   show route <neighbor-IP>  [IOS: show ip route <IP>]   │
│   clear bgp <neighbor>      [IOS: clear ip bgp <IP>]    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 2. CONNECT                           COLOR: ORANGE      │
│ What it means: TCP SYN sent, waiting for SYN-ACK        │
│ Why you're stuck here:                                  │
│   • Firewall blocking TCP port 179 (inbound OR return)  │
│   • Source IP mismatch (loopback vs physical)           │
│   • Routing asymmetry — SYN goes out, return dropped    │
│ Fix:                                                    │
│   telnet <neighbor-IP> 179 (from router itself)         │
│   show bgp neighbors <IP> | i "Local host"              │
│   Verify ACL allows TCP 179 both directions             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 3. ACTIVE                            COLOR: ORANGE      │
│ What it means: TCP failing, BGP retrying aggressively   │
│ Why you're here (most common stuck state):              │
│   • update-source set to loopback, not reachable        │
│   • eBGP multihop not set (TTL=1 by default)            │
│   • Wrong neighbor IP configured (typo in /30 subnet)   │
│   • ACL silently dropping return TCP traffic            │
│ Fix:                                                    │
│   show bgp neighbors <IP> | i "BGP state|Local|Remote"  │
│   ping <neighbor> source <correct-interface>            │
│   Add: neighbor <IP> ebgp-multihop 2 (if via loopback) │
│   Add: neighbor <IP> update-source <interface>          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 4. OPENSENT                          COLOR: YELLOW      │
│ What it means: TCP up, BGP OPEN sent, no reply          │
│ Why you're stuck here:                                  │
│   • Wrong remote AS configured (most common)            │
│   • BGP version mismatch (rare but happens on old gear) │
│   • Remote end receives OPEN but rejects it silently    │
│   • Hold time negotiation failure                       │
│ Fix:                                                    │
│   Verify AS number with ISP — confirm 2-byte vs 4-byte  │
│   debug ip bgp <neighbor> events (brief, targeted)      │
│   Packet capture on port 179 — look at OPEN message     │
│   show bgp neighbors <IP> | i "BGP version|remote AS"   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 5. OPENCONFIRM                       COLOR: YELLOW      │
│ What it means: OPEN + KEEPALIVE sent, waiting on remote │
│               KEEPALIVE to complete the handshake        │
│ Why it drops back repeatedly:                           │
│   • MD5 authentication mismatch (1 wrong character)     │
│   • Hold timer expired before KEEPALIVE received        │
│   • Notification sent by remote — check logs            │
│ Fix:                                                    │
│   Remove MD5 temporarily to isolate auth issue          │
│   show bgp neighbors <IP> | i "BGP state|MD5"           │
│   Check syslog for BGP NOTIFICATION messages            │
│   Confirm password string with ISP — case sensitive     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 6. ESTABLISHED                       COLOR: GREEN       │
│ What it means: Session up — this is the goal            │
│ Still broken? Session up but no routes:                 │
│   • No network statement / no redistribute configured   │
│   • Outbound route-map filtering everything             │
│   • ISP filtering your prefixes (prefix-list mismatch)  │
│   • Next-hop not reachable for received routes          │
│   • Missing next-hop-self on iBGP redistribution        │
│ Fix:                                                    │
│   show bgp summary (check Prefixes Received column)     │
│   show bgp neighbors <IP> advertised-routes             │
│   show bgp neighbors <IP> received-routes               │
│   show route-map (check what's filtering)               │
└─────────────────────────────────────────────────────────┘

---

### PART B — ISP-SPECIFIC FAILURE MATRIX (middle section of visual)

┌──────────────────────┬───────────────────────────────────────────────────────┐
│ SCENARIO             │ WHAT TO CHECK                                         │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Dual-ISP active/     │ Verify local-pref values. Check if both sessions are  │
│ standby not failing  │ Established. Confirm route-map sets local-pref        │
│ over correctly       │ correctly on each. Test by shutting primary.          │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Session flapping     │ Hold timer too low? Check keepalive interval.         │
│ every few minutes    │ CPU spike on router? SNMP or logging storm?           │
│                      │ ISP doing maintenance? Ask for BGP notification logs. │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Receiving full BGP   │ Memory? IPv4 table is ~960K+ routes (2025). Verify RAM│
│ table but router     │ Use soft-reconfiguration inbound to check without     │
│ acting strangely     │ resetting. Confirm default route handling.            │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ ISP says session is  │ Check if you're receiving their prefixes. Could be    │
│ up but traffic drops │ asymmetric routing. Traceroute from both ends.        │
│                      │ Verify next-hop reachability for received routes.     │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ Prefixes not         │ Confirm network statement matches exact prefix in RIB.│
│ advertising to ISP   │ Check outbound route-map / prefix-list. Verify        │
│                      │ aggregate-address if summarizing. No auto-summary.    │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ BGP communities      │ ISP uses communities to signal routes. Confirm you're │
│ not working          │ sending the right community value. Format: ASN:value. │
│                      │ Verify community is not stripped by outbound policy.  │
└──────────────────────┴───────────────────────────────────────────────────────┘

---

### PART C — QUICK COMMAND REFERENCE (sidebar or bottom panel)

VERIFICATION COMMANDS (run these in order when session won't come up):

1.  show bgp summary
    → One-line view of all neighbors + state + prefix count

2.  show bgp neighbors <IP>
    → Full detail: state, timers, error codes, capabilities

3.  show bgp neighbors <IP> advertised-routes
    → What you're actually sending (not what you think you're sending)

4.  show bgp neighbors <IP> received-routes
    → What the ISP is sending you
    → IOS PREREQ: neighbor <IP> soft-reconfiguration inbound must be set first
    → IOS-XR / Juniper: works without prereq (use show bgp neighbor <IP> routes)

5.  show ip route bgp
    → BGP routes installed in RIB — not all received routes make it here

6.  show bgp regexp _<ASN>_
    → Filter BGP table by AS path — useful for tracing route origin

7.  ping <neighbor-IP> source <interface>
    → Confirms reachability from the right interface before BGP tries

8.  telnet <neighbor-IP> 179
    → Directly tests TCP port 179 — fastest way to rule out firewall

9.  debug ip bgp <neighbor-IP> events
    → Watch BGP state changes in real time (use carefully in prod)

10. clear ip bgp <IP> soft
    → Soft reset — refreshes routes without dropping session

---

### PART D — GOLDEN RULES (footer strip)

• BGP won't come up if TCP 179 is blocked — test it first, always
• ACTIVE state almost always means a Layer 3 reachability or source IP problem
• MD5 failures are silent — one wrong character looks identical to a firewall drop
• Session Established ≠ traffic working — check prefix counts and next-hop reachability
• Never clear bgp * in production without a maintenance window
• Hold timer defaults: 180s (Cisco), 90s (Juniper) — mismatches cause flapping
• Full BGP table from ISP = ~960K+ IPv4 routes (2025) — verify your router has the RAM

---

## SECTION 2 — CHATGPT IMAGE GENERATION PROMPT

Paste the prompt below directly into ChatGPT (use the image generator / DALL-E):

---

Create a professional dark-themed technical reference poster titled "BGP ISP Troubleshooting Guide" on a dark navy (#0d1b2a) background. White body text, teal (#00bcd4) accent lines and headers. Landscape orientation, 1920x1080px.

LAYOUT — four zones from top to bottom:

ZONE 1 — TOP STRIP: State machine flow diagram
Six boxes in a horizontal row connected by right-pointing arrows:
  IDLE (red border) → CONNECT (orange border) → ACTIVE (orange border) → OPENSENT (yellow border) → OPENCONFIRM (yellow border) → ESTABLISHED (green border)
A curved arrow loops from ESTABLISHED back to IDLE labeled "any error / hold-down"
Each box has: state name in bold white on top, one-line description below in small grey text.

ZONE 2 — MIDDLE: Six state detail cards in two rows of three
Each card matches its state box color from Zone 1.
Card content:
  Card 1 IDLE: "Why: BGP down / no route to peer / hold timer" + "Fix: show ip route <peer> | clear ip bgp"
  Card 2 CONNECT: "Why: Port 179 blocked / source IP mismatch" + "Fix: telnet <peer> 179 from router"
  Card 3 ACTIVE: "Why: update-source wrong / multihop not set / ACL" + "Fix: ping source loopback | add ebgp-multihop"
  Card 4 OPENSENT: "Why: Wrong remote AS / BGP version mismatch" + "Fix: Verify ASN with ISP | packet capture port 179"
  Card 5 OPENCONFIRM: "Why: MD5 password mismatch / hold timer expired" + "Fix: Remove auth to test | confirm password case-sensitive"
  Card 6 ESTABLISHED: "Session up but no routes? Check: network statement | route-map filtering | next-hop reachable?"
Cards have rounded corners, subtle glow matching their border color.

ZONE 3 — BOTTOM LEFT: Quick command reference panel (dark grey #1a2a3a background)
Title: "VERIFICATION COMMANDS — Run In This Order"
Numbered list 1-8, monospace font, teal numbers, white command text, grey description text:
  1. show bgp summary → all neighbors + state + prefix count
  2. show bgp neighbors <IP> → full state detail + error codes
  3. show bgp neighbors <IP> advertised-routes → what you're actually sending
  4. show bgp neighbors <IP> received-routes → what ISP is sending
  5. show ip route bgp → routes installed in RIB
  6. ping <peer> source <loopback> → verify Layer 3 reachability first
  7. telnet <peer> 179 → test TCP port 179 directly
  8. clear ip bgp <IP> soft → refresh routes without dropping session

ZONE 3 — BOTTOM RIGHT: Golden rules panel (dark grey #1a2a3a background)
Title: "GOLDEN RULES"
Seven short rules in white, each prefixed with a teal ✓ checkmark:
  ✓ Test TCP 179 first — BGP won't come up if it's blocked
  ✓ ACTIVE state = Layer 3 or source IP problem, almost always
  ✓ MD5 failures are silent — one wrong char = same symptoms as firewall drop
  ✓ Established ≠ traffic working — verify prefix counts and next-hop
  ✓ Never clear bgp * in production without a maintenance window
  ✓ Hold timer mismatch (Cisco 180s vs Juniper 90s) causes session flapping
  ✓ Full BGP table ≈ 960K+ IPv4 routes (2025) — verify RAM before accepting

FOOTER: Two lines of small text centered at the very bottom:
  Line 1 — "BGP State Machine Reference · eBGP ISP Sessions · Cisco / Juniper / Arista"
  Line 2 — "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019"
  Line 2 uses teal color (#00bcd4). Line 1 uses grey (#888888). Font size 9pt.

Style: flat design, no gradients, subtle grid lines in background, tech-professional. Font: monospace for commands, clean sans-serif for everything else.

---

## SECTION 3 — CHATGPT CODE INTERPRETER PROMPT (Python / matplotlib)

Use this in ChatGPT's Advanced Data Analysis mode for a pixel-perfect rendered version:

---

Write Python using matplotlib and matplotlib.patches to generate a dark-themed BGP ISP Troubleshooting Guide poster. Figure size 19.2 x 10.8 inches at 100 DPI (1920x1080 output). Dark navy background #0d1b2a throughout.

SECTION 1 — BGP State Machine (top 20% of figure):
Draw 6 rounded rectangle boxes in a horizontal row with right-pointing arrows between them.
Box colors (border + label): Idle=#e74c3c, Connect=#e67e22, Active=#e67e22, OpenSent=#f1c40f, OpenConfirm=#f1c40f, Established=#2ecc71.
Each box: state name in bold white 11pt, one-line description in grey 8pt below.
Draw a curved arrow from Established back to Idle above the boxes, labeled "error → hold-down" in red 8pt.

SECTION 2 — State Detail Cards (middle 45% of figure):
Two rows of 3 cards. Each card is a rounded rectangle matching its state color as the border.
Background of each card: #1a2a3a. White bold title. Grey body text 8pt.
Card content exactly as specified in the guide above.

SECTION 3 — Bottom panels side by side (bottom 30%):
Left panel (#1a2a3a rounded rect): "VERIFICATION COMMANDS" header in teal. 8 numbered commands in monospace 8pt — teal numbers, white command, grey description.
Right panel (#1a2a3a rounded rect): "GOLDEN RULES" header in teal. 7 rules with teal checkmarks in 8pt white text.

Footer — two lines centered at bottom:
  ax.text(0.5, 0.01, "BGP State Machine Reference · eBGP ISP Sessions · Cisco / Juniper / Arista", color="#888888", fontsize=7, ha="center", transform=fig.transFigure)
  ax.text(0.5, 0.005, "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019", color="#00bcd4", fontsize=7, ha="center", transform=fig.transFigure)

Save as bgp_isp_troubleshoot_guide.png at 100 DPI.
