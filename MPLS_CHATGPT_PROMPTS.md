# MPLS LDP Troubleshooting Guide — ChatGPT Prompts
# ─────────────────────────────────────────────────────────────────────────────
# OPTION 1 → DALL-E image generator   (quick, good for sharing on LinkedIn)
# OPTION 2 → Code Interpreter          (precise, accurate, downloadable PNG)
#
# USE OPTION 2. DALL-E mangles monospace command text. Code Interpreter runs
# real Python, renders exact layout, gives you a download link.
# ─────────────────────────────────────────────────────────────────────────────

================================================================================
OPTION 1 — PASTE INTO CHATGPT IMAGE GENERATOR (DALL-E)
================================================================================

Create a professional dark-themed technical reference poster titled:
"MPLS LDP Troubleshooting Guide"
Subtitle: "From Non-Existent to Operational — and Why the LSP Still Doesn't Forward"

Canvas: dark navy #0d1b2a background, 1920x1080px landscape.
Style: flat design, no gradients, subtle dot-grid pattern in background.
Fonts: monospace (Courier/DejaVu Mono) for all CLI commands, clean sans-serif everywhere else.
Colors: white body text, teal #00bcd4 headers and accents, grey #888888 secondary text.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE 1 — TOP STRIP (12% height): LDP Session State Machine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Five rounded boxes in a horizontal row. White right-pointing arrows between them.
A red curved arrow arcs from OPERATIONAL back over the top to NON-EXISTENT, labeled "any error → Hello discovery restarts" in red italic above.

Box 1  NON-EXISTENT   red border     #e74c3c   subtext: "No Hello adjacency — check mpls ip & ACLs"
Box 2  INITIALIZED    orange border  #e67e22   subtext: "TCP up, Init sent — waiting on peer's Init"
Box 3  OPENSENT       orange border  #e67e22   subtext: "Init exchanged — waiting on parameter agreement"
Box 4  OPENRECEIVED   yellow border  #f1c40f   subtext: "KeepAlive sent — awaiting peer's KeepAlive"
Box 5  OPERATIONAL    green border   #2ecc71   subtext: "Session up — labels being exchanged"

Thin teal separator line below Zone 1.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE 2 — MIDDLE (44% height): Five State Detail Cards — 1 row of 5 (or 3+2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cards: dark #1a2a3a background, rounded corners, glowing border matching state color.
Each card has: bold white state name header / orange "WHY:" label + grey causes / teal "FIX:" label + white monospace commands.

CARD 1 — NON-EXISTENT (red border #e74c3c)
WHY:
  • LDP not enabled on the interface — "mpls ip" missing
  • ACL blocking UDP 646 (Hello) or TCP 646 (session)
  • No IGP reachability to the peer's transport address
FIX:
  show mpls ldp discovery
  show mpls ldp neighbor
  Verify "mpls ip" applied per-interface, not just under router-id

CARD 2 — INITIALIZED (orange border #e67e22)
WHY:
  • Firewall blocking TCP port 646
  • Wrong transport-address — interface IP vs loopback mismatch
  • Asymmetric routing to the peer's transport address
FIX:
  show mpls ldp neighbor detail
  telnet <peer-transport-IP> 646
  Verify transport-address matches the loopback both sides route through

CARD 3 — OPENSENT (orange border #e67e22)
WHY:
  • LDP parameter mismatch — label space, PVLim, KeepAlive hold
  • MD5 authentication mismatch — silent failure
  • LDP protocol version mismatch on legacy gear
FIX:
  debug mpls ldp session (targeted, brief)
  Verify MD5 password matches exactly on both peers
  show mpls ldp neighbor — check for negotiation errors

CARD 4 — OPENRECEIVED (yellow border #f1c40f)
WHY:
  • KeepAlive filtered by a stateful firewall
  • Hold-timer expired before KeepAlive arrived
  • Unstable link flapping TCP mid-negotiation
FIX:
  show mpls ldp neighbor | include Up time
  Check hold-time configuration on both peers
  Check interface error counters for instability

CARD 5 — OPERATIONAL (green border #2ecc71)
← Session up but LSP not forwarding? Work through this checklist:
  [ ] show mpls forwarding-table — is a label actually programmed?
  [ ] show mpls ldp bindings <prefix> — local/remote label for the FEC
  [ ] IGP route to the FEC prefix exists? (LDP won't bind what isn't in the RIB)
  [ ] Label filtering — advertise-labels / neighbor accept lists?
  [ ] PHP config — expecting explicit-null, got implicit-null (or vice versa)?
  [ ] MTU too small for labeled packets? (mpls mtu on every transit hop)
  traceroute mpls ipv4 <prefix>/<mask>
  ping mpls ipv4 <prefix>/<mask>

Thin teal separator line below Zone 2.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE 3 — BOTTOM (38% height): THREE panels side by side, equal width
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LEFT PANEL — dark grey #1a2a3a, teal border, teal header: "VERIFICATION COMMANDS — Run In This Order"

Monospace white commands, grey descriptions, teal numbers:

 1  show mpls ldp neighbor                          session state per peer — Operational yet?
 2  show mpls ldp discovery                         confirms Hello adjacency exists first
 3  show mpls ldp neighbor detail                   negotiation params, hold-time, up-time
 4  show mpls ldp bindings <prefix>                 local + remote labels bound to a FEC
 5  show mpls forwarding-table                       LFIB — what label actions are programmed
 6  show mpls interfaces                              MPLS enabled per-interface check
 7  show ip cef <prefix> detail                        confirms label imposition matches CEF
 8  traceroute mpls ipv4 <prefix>/<mask>               hop-by-hop LSP validation
 9  ping mpls ipv4 <prefix>/<mask>                      fast LSP liveness check
10  show mpls ldp parameters                            router-id, transport-address, hold-time
11  debug mpls ldp session state-machine                live negotiation — careful in prod

JUNIPER EQUIVALENTS (smaller grey text, single column):
  show ldp session  |  show ldp neighbor  |  show ldp database
  show route table mpls.0  |  show rsvp session  |  traceroute mpls ldp <prefix>

SMALL NOTE at bottom in #666666 6pt italic:
"* Penultimate-hop popping (implicit-null) is expected at the second-to-last hop — not a missing label"

MIDDLE PANEL — dark grey #1a2a3a, teal border, teal header: "MPLS LABEL OPERATIONS REFERENCE"
(What each label action means when you see it in the LFIB or a trace.)

PUSH — Label imposed on an unlabeled (or already-labeled) packet
  Happens at the ingress LER, or when a service label is added under a transport label

SWAP — Top label replaced with the next-hop's label for the same FEC
  Normal transit-hop behavior everywhere in the LSP core

POP — Top label removed
  Explicit-null: pop happens at egress, label 0/2 kept one hop for QoS/OAM visibility
  Implicit-null (PHP): penultimate hop pops the label before forwarding to egress — normal, saves the egress router a lookup

LABEL STACK
  Outer (transport) label — LDP/RSVP-TE, gets the packet across the core
  Inner (service) label — VPN/L2VPN label, identifies the VRF/circuit at egress
  TTL propagation: uniform mode copies IP TTL into label TTL (traceroute shows every hop);
  pipe mode hides the core (traceroute jumps straight to egress) — know which mode you're in
  before troubleshooting a traceroute that "skips" hops

SPECIAL LABELS
  0  — Explicit-null (IPv4)
  1  — Router-alert
  2  — Explicit-null (IPv6)
  3  — Implicit-null (PHP signal — never appears in an actual packet)

SMALL NOTE: "Command: show mpls forwarding-table detail  |  Juniper: show route table mpls.0 extensive"

RIGHT PANEL — dark grey #1a2a3a, teal border, teal header: "GOLDEN RULES + LDP TIMER REFERENCE"

GOLDEN RULES (teal ✓ prefix, white text):
✓  LDP needs IP reachability to the peer's transport address before Hello even works
✓  "mpls ip" must be enabled per-interface — global LDP config alone does nothing
✓  Session Operational ≠ every FEC has a label — check bindings per prefix
✓  Implicit-null (PHP) at the penultimate hop is normal, not a missing label
✓  MD5 auth failures on LDP are silent, exactly like BGP — verify the password character by character
✓  RSVP-TE needs a valid CSPF path AND available bandwidth — RSVP session state alone proves neither
✓  No IGP route to the FEC prefix = no label bound — check the RIB before blaming LDP
✓  A stale label after a reroute is a common cause of a traceroute that dies mid-path
✓  MTU issues in the core often only show up on large packets — test with size + DF-bit set

Grey divider line inside panel.

LDP TIMER REFERENCE header in #f39c12 7.5pt bold, then table in 6.8pt:

Parameter            Default        Config syntax
──────────────────────────────────────────────────────
Hello interval          5s          mpls ldp discovery hello interval 5
Hello hold-time         15s         mpls ldp discovery hello holdtime 15
KeepAlive interval      60s         mpls ldp session protection / hold config
KeepAlive hold-time     180s        mpls ldp holdtime 180
──────────────────────────────────────────────────────
Session protection:  keeps LDP bindings alive briefly across a link flap
                     without tearing down the whole session

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FOOTER — two lines centered at the very bottom:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Line 1  grey #888888   9pt:  "MPLS LDP Session Reference  ·  Label Distribution & LSP Verification  ·  IOS / IOS-XE / IOS-XR / Juniper JunOS"
Line 2  teal #00bcd4   9pt bold:  "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019"

================================================================================
END OPTION 1
================================================================================




================================================================================
OPTION 2 — PASTE INTO CHATGPT CODE INTERPRETER (Advanced Data Analysis)
Produces a real downloadable PNG. All text renders exactly as specified.
================================================================================

Write and execute Python code using matplotlib and matplotlib.patches to produce an MPLS LDP Troubleshooting Guide reference poster. Save as mpls_ldp_guide.png and provide a download link. Do not display the figure inline.

─────────────────────────────────────────────────────────────────────────────
CANVAS SETUP
─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(19.2, 10.8))
fig.patch.set_facecolor("#0d1b2a")
Use fig.add_axes([0, 0, 1, 1]) with no frame, no ticks, xlim=(0,1), ylim=(0,1).
All coordinates are in figure-fraction space (0.0 to 1.0).
Draw a subtle dot-grid: scatter small dots at 0.02 spacing across full canvas, color="#1a2a3a", alpha=0.5, s=0.5.

─────────────────────────────────────────────────────────────────────────────
SECTION A — LDP SESSION STATE MACHINE STRIP  (y: 0.88 to 0.99)
─────────────────────────────────────────────────────────────────────────────
Draw the title at x=0.5, y=0.975: "MPLS LDP TROUBLESHOOTING GUIDE" bold white 13pt centered.
Draw subtitle at x=0.5, y=0.963: "From Non-Existent to Operational — and Why the LSP Still Doesn't Forward" grey #888888 8pt centered italic.

Five FancyBboxPatch boxes ("round,pad=0.008") in a row at y_bottom=0.893, height=0.055, width=0.155.
X left-edge positions: NON-EXISTENT=0.030, INITIALIZED=0.205, OPENSENT=0.380, OPENRECEIVED=0.555, OPERATIONAL=0.730

All boxes: facecolor="#1a2a3a"

Box colors (edgecolor, linewidth=2.5):
  NON-EXISTENT:  #e74c3c
  INITIALIZED:   #e67e22
  OPENSENT:      #e67e22
  OPENRECEIVED:  #f1c40f
  OPERATIONAL:   #2ecc71

In each box, draw:
  - State name: bold white 9pt, centered horizontally, y at box_top - 0.015
  - Subtext (one line): #888888 6.5pt, centered, y at box_top - 0.030

Subtexts:
  NON-EXISTENT:  "No Hello adjacency — check mpls ip & ACLs"
  INITIALIZED:   "TCP up, Init sent — waiting on peer's Init"
  OPENSENT:      "Init exchanged — negotiating parameters"
  OPENRECEIVED:  "KeepAlive sent — awaiting peer's KeepAlive"
  OPERATIONAL:   "Session up — labels being exchanged"

Draw white right-pointing arrows (FancyArrowPatch, arrowstyle="->, head_width=0.008") between each consecutive box pair, centered vertically on the boxes.

Draw a red curved arc arrow from center-top of OPERATIONAL box to center-top of NON-EXISTENT box using ConnectionPatch with connectionstyle="arc3,rad=0.4", color="#e74c3c", linewidth=1.5, arrowstyle="->".
Place the arc label at x=0.5, y=0.958: "any error → Hello discovery restarts" color="#e74c3c" 6.5pt centered italic.

Draw a horizontal line at y=0.888 from x=0.01 to x=0.99, color="#00bcd4", linewidth=0.8, alpha=0.5.

─────────────────────────────────────────────────────────────────────────────
SECTION B — FIVE STATE DETAIL CARDS  (y: 0.435 to 0.882)
─────────────────────────────────────────────────────────────────────────────
One row of 5 cards (or 3+2 grid if text density requires it). Card size: width=0.185, height=0.44 for single row; adjust to 0.305 width x 0.215 height per card for a 3+2 grid matching row_bottom=0.660/0.437 with col x_left=[0.018,0.341,0.664].

All cards: FancyBboxPatch("round,pad=0.005"), facecolor="#1a2a3a", linewidth=2

CARD 1 — NON-EXISTENT  edgecolor=#e74c3c
Header "1. NON-EXISTENT" bold white 8.5pt at card_top - 0.012
"WHY:" in #e74c3c 7.5pt, then each cause in #aaaaaa 6.8pt (one per line, left-aligned, x=card_left+0.008):
  • mpls ip missing on the interface
  • ACL blocking UDP 646 (Hello) or TCP 646 (session)
  • No IGP reachability to peer's transport address
"FIX:" in #00bcd4 7.5pt, then commands in monospace white 6.5pt:
  show mpls ldp discovery
  show mpls ldp neighbor
  Verify mpls ip is per-interface, not just global

CARD 2 — INITIALIZED  edgecolor=#e67e22
Header "2. INITIALIZED"
WHY causes:
  • Firewall blocking TCP port 646
  • Wrong transport-address — interface vs loopback mismatch
  • Asymmetric routing to peer's transport address
FIX commands:
  show mpls ldp neighbor detail
  telnet <peer-transport-IP> 646
  Verify transport-address matches routed loopback

CARD 3 — OPENSENT  edgecolor=#e67e22
Header "3. OPENSENT"
WHY causes:
  • LDP parameter mismatch — label space, PVLim, hold time
  • MD5 authentication mismatch — silent failure
  • LDP version mismatch on legacy gear
FIX commands:
  debug mpls ldp session   (targeted, brief)
  Verify MD5 password matches exactly
  show mpls ldp neighbor — check negotiation errors

CARD 4 — OPENRECEIVED  edgecolor=#f1c40f
Header "4. OPENRECEIVED"
WHY causes:
  • KeepAlive filtered by stateful firewall
  • Hold-timer expired before KeepAlive arrived
  • Unstable link flapping TCP mid-negotiation
FIX commands:
  show mpls ldp neighbor | include Up time
  Check hold-time config on both peers
  Check interface error counters

CARD 5 — OPERATIONAL  edgecolor=#2ecc71
Header "5. OPERATIONAL — Session up. LSP not forwarding? Checklist:"
Content as a checklist in #cccccc 6.8pt (use □ prefix for each item):
  □ show mpls forwarding-table — is a label programmed?
  □ show mpls ldp bindings <prefix> — labels for this FEC?
  □ IGP route to the FEC prefix exists? (required for LDP to bind)
  □ Label filtering — advertise-labels / accept lists?
  □ PHP config — explicit-null vs implicit-null expectation?
  □ MTU sufficient for labeled packets on every transit hop?
  traceroute mpls ipv4 <prefix>/<mask>
  ping mpls ipv4 <prefix>/<mask>

Draw a horizontal teal separator at y=0.432 from x=0.01 to x=0.99, color="#00bcd4", linewidth=0.8, alpha=0.5.

─────────────────────────────────────────────────────────────────────────────
SECTION C — THREE BOTTOM PANELS SIDE BY SIDE  (y: 0.065 to 0.428)
─────────────────────────────────────────────────────────────────────────────
Three equal-width panels. Each: FancyBboxPatch facecolor=#131f2e edgecolor=#00bcd4 linewidth=1 alpha=0.9
Panel widths: x_left=[0.010, 0.345, 0.678], each width=0.322, y_bottom=0.068, height=0.358

PANEL 1 — LEFT: "VERIFICATION COMMANDS — Run In This Order"
Header in #00bcd4 bold 8.5pt.
Commands in monospace 7pt — teal number, white command text, grey #888888 description after tab:

 1  show mpls ldp neighbor                           session state per peer — Operational yet?
 2  show mpls ldp discovery                          confirms Hello adjacency exists first
 3  show mpls ldp neighbor detail                    negotiation params, hold-time, up-time
 4  show mpls ldp bindings <prefix>                  local + remote labels bound to a FEC
 5  show mpls forwarding-table                       LFIB — what label actions are programmed
 6  show mpls interfaces                              MPLS enabled per-interface check
 7  show ip cef <prefix> detail                        label imposition matches CEF entry
 8  traceroute mpls ipv4 <prefix>/<mask>                hop-by-hop LSP validation
 9  ping mpls ipv4 <prefix>/<mask>                      fast LSP liveness check
10  debug mpls ldp session state-machine                live negotiation — careful in prod

Grey separator line inside panel.
JUNIPER EQUIVALENTS header in #f39c12 7pt bold, then in monospace grey 6.5pt:
  show ldp session  ·  show ldp neighbor  ·  show ldp database
  show route table mpls.0  ·  traceroute mpls ldp <prefix>

Small italic note at very bottom in #666666 6pt:
"* Implicit-null (PHP) at the penultimate hop is expected — not a missing label"

PANEL 2 — MIDDLE: "MPLS LABEL OPERATIONS REFERENCE"
Header in #00bcd4 bold 8.5pt.
Intro line in grey 7pt: "What each label action means when you see it in the LFIB or a trace."

PUSH  (header in #f39c12 7.5pt bold)
  Label imposed on a packet — ingress LER, or service label added under transport label

SWAP  (header in #f39c12)
  Top label replaced with next-hop's label for the same FEC — normal transit behavior

POP  (header in #f39c12)
  Explicit-null: label kept one hop past egress for QoS/OAM visibility
  Implicit-null (PHP): penultimate hop pops before forwarding — saves egress a lookup

LABEL STACK  (header in #f39c12)
  Outer (transport) label — LDP/RSVP-TE, moves packet across the core
  Inner (service) label — VPN/L2VPN, identifies VRF/circuit at egress
  TTL propagation: uniform mode shows every hop in traceroute; pipe mode hides the core

SPECIAL LABELS  (header in #f39c12)
  0 = Explicit-null (IPv4)   1 = Router-alert
  2 = Explicit-null (IPv6)   3 = Implicit-null (never in an actual packet)

Small note at bottom in #666666 6.5pt italic:
"Command: show mpls forwarding-table detail  |  Juniper: show route table mpls.0 extensive"

PANEL 3 — RIGHT: "GOLDEN RULES  +  LDP TIMER REFERENCE"
Header in #00bcd4 bold 8.5pt.

GOLDEN RULES section — each rule: teal ✓ in 8pt, white text 7pt:
✓  LDP needs IP reachability to the peer's transport address before Hello even works
✓  mpls ip must be enabled per-interface — global LDP config alone does nothing
✓  Session Operational ≠ every FEC has a label — check bindings per prefix
✓  Implicit-null (PHP) at the penultimate hop is normal, not a missing label
✓  MD5 auth failures are silent, exactly like BGP — verify password char by char
✓  RSVP-TE needs a valid CSPF path AND bandwidth — session state alone proves neither
✓  No IGP route to the FEC = no label bound — check the RIB before blaming LDP
✓  A stale label after a reroute is a common cause of a mid-path traceroute failure
✓  Core MTU issues often only show up on large packets — test with size + DF-bit

Grey divider line inside panel.

LDP TIMER REFERENCE header in #f39c12 7.5pt bold, then table in 6.8pt:

Parameter            Default    Config syntax
──────────────────────────────────────────────────────
Hello interval          5s      mpls ldp discovery hello interval 5
Hello hold-time         15s     mpls ldp discovery hello holdtime 15
KeepAlive interval      60s     session protection / hold config
KeepAlive hold-time    180s     mpls ldp holdtime 180
──────────────────────────────────────────────────────
Session protection: keeps LDP bindings alive briefly across a link
flap without tearing down the whole session

─────────────────────────────────────────────────────────────────────────────
FOOTER  (y: 0.008 to 0.062)
─────────────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.038, "MPLS LDP Session Reference  ·  Label Distribution & LSP Verification  ·  IOS / IOS-XE / IOS-XR  ·  Juniper JunOS",
         color="#888888", fontsize=7, ha="center")
fig.text(0.5, 0.018, "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019",
         color="#00bcd4", fontsize=8, ha="center", fontweight="bold")

─────────────────────────────────────────────────────────────────────────────
SAVE
─────────────────────────────────────────────────────────────────────────────
plt.savefig("mpls_ldp_guide.png", dpi=100, bbox_inches="tight",
            facecolor="#0d1b2a", edgecolor="none")
print("Saved. Provide download link.")

================================================================================
END OPTION 2
================================================================================
