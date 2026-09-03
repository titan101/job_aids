# OSPF Troubleshooting Guide — ChatGPT Prompts
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
"OSPF Troubleshooting Guide"
Subtitle: "From Down to Full — and Why the Route Still Isn't There"

Canvas: dark navy #0d1b2a background, 1920x1080px landscape.
Style: flat design, no gradients, subtle dot-grid pattern in background.
Fonts: monospace (Courier/DejaVu Mono) for all CLI commands, clean sans-serif everywhere else.
Colors: white body text, teal #00bcd4 headers and accents, grey #888888 secondary text.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE 1 — TOP STRIP (12% height): OSPF Neighbor State Machine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Eight rounded boxes in a horizontal row. White right-pointing arrows between them.
A red curved arrow arcs from FULL back over the top to DOWN, labeled "dead-timer expiry / config error" in red italic above.

Box 1  DOWN         red border     #e74c3c   subtext: "No Hello received — check config & ACLs"
Box 2  ATTEMPT      orange border  #e67e22   subtext: "NBMA only — manual neighbor, no Hello yet"
Box 3  INIT         orange border  #e67e22   subtext: "Hello received — one-way so far"
Box 4  2-WAY        yellow border  #f1c40f   subtext: "Bidirectional — DR/BDR election happens here"
Box 5  EXSTART      yellow border  #f1c40f   subtext: "Master/slave negotiation begins"
Box 6  EXCHANGE     yellow border  #f1c40f   subtext: "DBD packets exchanged"
Box 7  LOADING      yellow border  #f1c40f   subtext: "LSRs sent for missing LSAs"
Box 8  FULL         green border   #2ecc71   subtext: "Adjacency complete — LSDBs synced"

Thin teal separator line below Zone 1.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE 2 — MIDDLE (44% height): Eight State Detail Cards — 2 rows × 4 columns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cards: dark #1a2a3a background, rounded corners, glowing border matching state color.
Each card has: bold white state name header / orange "WHY:" label + grey causes / teal "FIX:" label + white monospace commands.

CARD 1 — DOWN (red border #e74c3c)
WHY:
  • OSPF not enabled on the interface / area mismatch
  • Interface down or missing IP
  • ACL blocking IP protocol 89 or multicast 224.0.0.5/6
  • passive-interface configured where a peer is expected
FIX:
  show ip ospf interface brief
  show ip protocols
  Verify network statement / area matches both sides

CARD 2 — ATTEMPT (orange border #e67e22)
WHY:
  • NBMA/point-to-multipoint only — manual neighbor config
  • "neighbor <IP>" statement missing or wrong
  • Underlying L2 mapping (Frame Relay/PVC) missing
FIX:
  show ip ospf neighbor
  Verify "neighbor <IP>" statement
  Check Frame Relay map / underlying L2 circuit

CARD 3 — INIT (orange border #e67e22)
WHY:
  • Unidirectional path — one-way ACL/firewall
  • Hello/dead timer mismatch preventing recognition
  • Transient — neighbor hasn't processed my Hello yet
FIX:
  show ip ospf neighbor detail
  Verify hello-interval / dead-interval match exactly
  Check for asymmetric filtering in one direction

CARD 4 — 2-WAY (yellow border #f1c40f)
WHY:
  • Normal for DROTHER-to-DROTHER pairs on broadcast/NBMA
  • If Full expected: priority 0, or network-type mismatch
FIX:
  show ip ospf neighbor
  show ip ospf interface (check DR/BDR/network type)
  Verify ip ospf priority if a specific DR was expected

CARD 5 — EXSTART (yellow border #f1c40f)  ← classic stuck state
WHY:
  • MTU mismatch — the single most common cause
  • Duplicate router-ID somewhere in the area
FIX:
  Compare MTU on show ip ospf interface, both sides
  show ip ospf neighbor detail
  Check for duplicate router-id in show ip ospf

CARD 6 — EXCHANGE (yellow border #f1c40f)
WHY:
  • DBD packet loss/corruption on an unstable link
  • Retransmissions piling up on a lossy path
  • Large LSDB timing out on a slow/congested link
FIX:
  show ip ospf neighbor detail (retransmit counters)
  debug ip ospf adj (careful — verbose)
  Check interface error/discard counters

CARD 7 — LOADING (yellow border #f1c40f)
WHY:
  • LSA request/response loss on the link
  • LSDB inconsistency between neighbors
  • Corrupted LSA triggering repeated re-requests
FIX:
  show ip ospf statistics
  debug ip ospf packet (careful — verbose)
  Check show ip ospf database for corrupt LSAs

CARD 8 — FULL (green border #2ecc71)
← Adjacency up but routes missing? Work through this checklist:
  [ ] Area type — stub/totally-stubby/NSSA suppresses external routes
  [ ] distribute-list / route-map filtering on the ABR
  [ ] Area 0 contiguous — path to the backbone exists
  [ ] ABR summarizing/advertising the range you expect
  show ip ospf database
  show ip route ospf
  show ip ospf border-routers

Thin teal separator line below Zone 2.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE 3 — BOTTOM (38% height): THREE panels side by side, equal width
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LEFT PANEL — dark grey #1a2a3a, teal border, teal header: "VERIFICATION COMMANDS — Run In This Order"

Monospace white commands, grey descriptions, teal numbers:

 1  show ip ospf neighbor                            all neighbors + state + DR/BDR role
 2  show ip ospf neighbor detail                      timers, retransmit counts, dead countdown
 3  show ip ospf interface brief                       area, cost, MTU, network type, priority
 4  show ip ospf database                               the LSDB — what each router knows
 5  show ip route ospf                                   routes actually installed in the RIB
 6  show ip protocols                                     network statements, passive-interfaces
 7  show ip ospf border-routers                            path to ABRs/ASBRs
 8  debug ip ospf adj                                       watch adjacency form live
 9  debug ip ospf hello                                      confirm Hellos sent/received
10  clear ip ospf process                                     full reset — maintenance window only

JUNIPER EQUIVALENTS (smaller grey text, single column):
  show ospf neighbor  |  show ospf interface  |  show ospf database
  show route protocol ospf  |  show ospf overview  |  clear ospf neighbor

SMALL NOTE at bottom in #666666 6pt italic:
"* IOS-XR: drop the 'ip' prefix — show ospf neighbor, show ospf database"

MIDDLE PANEL — dark grey #1a2a3a, teal border, teal header: "LSA TYPES REFERENCE"
(When you see an LSA type in the database, this is exactly what it means.)

Type 1 — Router LSA
  Every router originates one per area. Lists its links and costs.

Type 2 — Network LSA
  Originated by the DR on broadcast/NBMA segments. Lists attached routers.

Type 3 — Summary LSA (Inter-Area)
  Originated by an ABR. Advertises a route from one area into another.

Type 4 — ASBR Summary LSA
  Originated by an ABR. Advertises the route TO an ASBR, not a prefix.

Type 5 — AS External LSA
  Originated by an ASBR. Redistributed external routes — flooded everywhere
  except stub areas.

Type 7 — NSSA External LSA
  Used inside an NSSA instead of Type 5. Translated to Type 5 by the ABR
  when it leaves the NSSA.

SMALL NOTE: "Stub area = no Type 5.  Totally stubby = no Type 3, 4, or 5.  NSSA = Type 7 instead of 5."

RIGHT PANEL — dark grey #1a2a3a, teal border, teal header: "GOLDEN RULES + AREA TYPE REFERENCE"

GOLDEN RULES (teal ✓ prefix, white text):
✓  MTU mismatch is the #1 cause of stuck-in-ExStart — check both sides first
✓  Hello and dead timers must match exactly or the adjacency never forms
✓  Area 0 must be contiguous — every area needs a path to the backbone
✓  2-Way is normal for DROTHER pairs on broadcast segments, not a stuck state
✓  Stub/NSSA areas intentionally suppress external routes — check area type first
✓  Never clear ip ospf process in production without a maintenance window
✓  passive-interface disables Hello — check it isn't set where a peer is expected
✓  Network-type mismatch breaks DR election or blocks NBMA adjacency entirely
✓  Duplicate router-ID silently breaks adjacencies across the whole area

Grey divider line inside panel.

AREA TYPE REFERENCE header in #f39c12 7.5pt bold, then table in 6.8pt:

Area type          Type 3/4    Type 5    Type 7    Notes
──────────────────────────────────────────────────────────
Standard              Yes         Yes       No      Full visibility
Stub                   Yes         No        No      No externals; default route injected
Totally Stubby         No          No        No      Only a default route from the ABR
NSSA                  Yes          No        Yes     Local externals allowed, translated at ABR
──────────────────────────────────────────────────────────
Backbone (Area 0):  every other area needs a direct or virtual-link path to it

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FOOTER — two lines centered at the very bottom:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Line 1  grey #888888   9pt:  "OSPF Neighbor State Machine Reference  ·  Single-Area & Multi-Area  ·  Cisco IOS / IOS-XE / IOS-XR / Juniper JunOS"
Line 2  teal #00bcd4   9pt bold:  "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019"

================================================================================
END OPTION 1
================================================================================




================================================================================
OPTION 2 — PASTE INTO CHATGPT CODE INTERPRETER (Advanced Data Analysis)
Produces a real downloadable PNG. All text renders exactly as specified.
================================================================================

Write and execute Python code using matplotlib and matplotlib.patches to produce an OSPF Troubleshooting Guide reference poster. Save as ospf_guide.png and provide a download link. Do not display the figure inline.

─────────────────────────────────────────────────────────────────────────────
CANVAS SETUP
─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(19.2, 10.8))
fig.patch.set_facecolor("#0d1b2a")
Use fig.add_axes([0, 0, 1, 1]) with no frame, no ticks, xlim=(0,1), ylim=(0,1).
All coordinates are in figure-fraction space (0.0 to 1.0).
Draw a subtle dot-grid: scatter small dots at 0.02 spacing across full canvas, color="#1a2a3a", alpha=0.5, s=0.5.

─────────────────────────────────────────────────────────────────────────────
SECTION A — OSPF NEIGHBOR STATE MACHINE STRIP  (y: 0.88 to 0.99)
─────────────────────────────────────────────────────────────────────────────
Draw the title at x=0.5, y=0.975: "OSPF TROUBLESHOOTING GUIDE" bold white 13pt centered.
Draw subtitle at x=0.5, y=0.963: "From Down to Full — and Why the Route Still Isn't There" grey #888888 8pt centered italic.

Eight FancyBboxPatch boxes ("round,pad=0.006") in a row at y_bottom=0.893, height=0.055, width=0.108.
X left-edge positions (0.012 gap): DOWN=0.020, ATTEMPT=0.140, INIT=0.260, 2-WAY=0.380, EXSTART=0.500, EXCHANGE=0.620, LOADING=0.740, FULL=0.860

All boxes: facecolor="#1a2a3a"

Box colors (edgecolor, linewidth=2.5):
  DOWN:      #e74c3c
  ATTEMPT:   #e67e22
  INIT:      #e67e22
  2-WAY:     #f1c40f
  EXSTART:   #f1c40f
  EXCHANGE:  #f1c40f
  LOADING:   #f1c40f
  FULL:      #2ecc71

In each box, draw:
  - State name: bold white 8pt, centered horizontally, y at box_top - 0.015
  - Subtext (one line): #888888 6pt, centered, y at box_top - 0.030

Subtexts:
  DOWN:      "No Hello — check config/ACLs"
  ATTEMPT:   "NBMA only — no Hello yet"
  INIT:      "Hello received — one-way"
  2-WAY:     "Bidirectional — DR/BDR election"
  EXSTART:   "Master/slave negotiation"
  EXCHANGE:  "DBD packets exchanged"
  LOADING:   "LSRs sent for missing LSAs"
  FULL:      "Adjacency complete"

Draw white right-pointing arrows (FancyArrowPatch, arrowstyle="->, head_width=0.007") between each consecutive box pair, centered vertically on the boxes.

Draw a red curved arc arrow from center-top of FULL box to center-top of DOWN box using ConnectionPatch with connectionstyle="arc3,rad=0.4", color="#e74c3c", linewidth=1.5, arrowstyle="->".
Place the arc label at x=0.5, y=0.958: "dead-timer expiry / config error" color="#e74c3c" 6.5pt centered italic.

Draw a horizontal line at y=0.888 from x=0.01 to x=0.99, color="#00bcd4", linewidth=0.8, alpha=0.5.

─────────────────────────────────────────────────────────────────────────────
SECTION B — EIGHT STATE DETAIL CARDS  (y: 0.435 to 0.882)
─────────────────────────────────────────────────────────────────────────────
Two rows of 4 cards. Card size: width=0.232, height=0.215. Padding between cards=0.012. Left margin=0.014.

Row 1 (y_bottom=0.660): col x_left values = [0.014, 0.258, 0.502, 0.746]
Row 2 (y_bottom=0.437): col x_left values = [0.014, 0.258, 0.502, 0.746]

All cards: FancyBboxPatch("round,pad=0.005"), facecolor="#1a2a3a", linewidth=2

ROW 1, CARD 1 — DOWN  edgecolor=#e74c3c
Header "1. DOWN" bold white 8pt at card_top - 0.012
"WHY:" in #e74c3c 7pt, then each cause in #aaaaaa 6.3pt (one per line, left-aligned, x=card_left+0.007):
  • OSPF not enabled / area mismatch
  • Interface down or missing IP
  • ACL blocking IP protocol 89 or multicast
  • passive-interface where a peer is expected
"FIX:" in #00bcd4 7pt, then commands in monospace white 6pt:
  show ip ospf interface brief
  show ip protocols
  Verify network statement / area matches

ROW 1, CARD 2 — ATTEMPT  edgecolor=#e67e22
Header "2. ATTEMPT"
WHY causes:
  • NBMA only — manual neighbor config
  • neighbor <IP> statement missing/wrong
  • L2 mapping (Frame Relay/PVC) missing
FIX commands:
  show ip ospf neighbor
  Verify neighbor <IP> statement
  Check Frame Relay map / L2 circuit

ROW 1, CARD 3 — INIT  edgecolor=#e67e22
Header "3. INIT"
WHY causes:
  • Unidirectional — one-way ACL/firewall
  • Hello/dead timer mismatch
  • Transient — Hello not yet processed
FIX commands:
  show ip ospf neighbor detail
  Verify hello/dead intervals match
  Check asymmetric filtering

ROW 1, CARD 4 — 2-WAY  edgecolor=#f1c40f
Header "4. 2-WAY"
WHY causes:
  • Normal for DROTHER pairs on broadcast/NBMA
  • If Full expected: priority 0 / network-type mismatch
FIX commands:
  show ip ospf neighbor
  show ip ospf interface (DR/BDR/network type)
  Verify ip ospf priority

ROW 2, CARD 5 — EXSTART  edgecolor=#f1c40f
Header "5. EXSTART  ← classic stuck state"  (make "classic stuck state" smaller orange text)
WHY causes:
  • MTU mismatch — most common cause
  • Duplicate router-ID in the area
FIX commands:
  Compare MTU both sides (show ip ospf interface)
  show ip ospf neighbor detail
  Check for duplicate router-id

ROW 2, CARD 6 — EXCHANGE  edgecolor=#f1c40f
Header "6. EXCHANGE"
WHY causes:
  • DBD packet loss on unstable link
  • Retransmissions on a lossy path
  • Large LSDB timing out on slow link
FIX commands:
  show ip ospf neighbor detail (retransmit)
  debug ip ospf adj (careful — verbose)
  Check interface error/discard counters

ROW 2, CARD 7 — LOADING  edgecolor=#f1c40f
Header "7. LOADING"
WHY causes:
  • LSA request/response loss
  • LSDB inconsistency between neighbors
  • Corrupted LSA triggering re-requests
FIX commands:
  show ip ospf statistics
  debug ip ospf packet (careful — verbose)
  Check show ip ospf database for corruption

ROW 2, CARD 8 — FULL  edgecolor=#2ecc71
Header "8. FULL — Adjacency up. Routes missing? Checklist:"
Content as a checklist in #cccccc 6.3pt (use □ prefix for each item):
  □ Area type — stub/totally-stubby/NSSA suppresses externals
  □ distribute-list / route-map filtering on the ABR
  □ Area 0 contiguous — path to backbone exists
  □ ABR summarizing/advertising the expected range
  show ip ospf database
  show ip route ospf
  show ip ospf border-routers

Draw a horizontal teal separator at y=0.432 from x=0.01 to x=0.99, color="#00bcd4", linewidth=0.8, alpha=0.5.

─────────────────────────────────────────────────────────────────────────────
SECTION C — THREE BOTTOM PANELS SIDE BY SIDE  (y: 0.065 to 0.428)
─────────────────────────────────────────────────────────────────────────────
Three equal-width panels. Each: FancyBboxPatch facecolor=#131f2e edgecolor=#00bcd4 linewidth=1 alpha=0.9
Panel widths: x_left=[0.010, 0.345, 0.678], each width=0.322, y_bottom=0.068, height=0.358

PANEL 1 — LEFT: "VERIFICATION COMMANDS — Run In This Order"
Header in #00bcd4 bold 8.5pt.
Commands in monospace 7pt — teal number, white command text, grey #888888 description after tab:

 1  show ip ospf neighbor                             all neighbors + state + DR/BDR role
 2  show ip ospf neighbor detail                       timers, retransmit counts, dead countdown
 3  show ip ospf interface brief                        area, cost, MTU, network type, priority
 4  show ip ospf database                                the LSDB — what each router knows
 5  show ip route ospf                                    routes actually installed in the RIB
 6  show ip protocols                                      network statements, passive-interfaces
 7  show ip ospf border-routers                             path to ABRs/ASBRs
 8  debug ip ospf adj                                        watch adjacency form live
 9  debug ip ospf hello                                       confirm Hellos sent/received
10  clear ip ospf process                                      full reset — maintenance window only

Grey separator line inside panel.
JUNIPER EQUIVALENTS header in #f39c12 7pt bold, then in monospace grey 6.5pt:
  show ospf neighbor  ·  show ospf interface  ·  show ospf database
  show route protocol ospf  ·  show ospf overview  ·  clear ospf neighbor

Small italic note at very bottom in #666666 6pt:
"* IOS-XR: drop the 'ip' prefix — show ospf neighbor, show ospf database"

PANEL 2 — MIDDLE: "LSA TYPES REFERENCE"
Header in #00bcd4 bold 8.5pt.
Intro line in grey 7pt: "When you see an LSA type in the database, this is exactly what it means."

Type 1 — Router LSA  (header in #f39c12 7.5pt bold)
  Every router originates one per area — lists its links and costs

Type 2 — Network LSA  (header in #f39c12)
  Originated by the DR on broadcast/NBMA — lists attached routers

Type 3 — Summary LSA  (header in #f39c12)
  Originated by an ABR — advertises a route from one area into another

Type 4 — ASBR Summary LSA  (header in #f39c12)
  Originated by an ABR — advertises the route TO an ASBR, not a prefix

Type 5 — AS External LSA  (header in #f39c12)
  Originated by an ASBR — redistributed routes, flooded except in stub areas

Type 7 — NSSA External LSA  (header in #f39c12)
  Used inside an NSSA instead of Type 5 — translated to Type 5 at the ABR

Small note at bottom in #666666 6.5pt italic:
"Stub = no Type 5.  Totally stubby = no Type 3/4/5.  NSSA = Type 7 instead of 5."

PANEL 3 — RIGHT: "GOLDEN RULES  +  AREA TYPE REFERENCE"
Header in #00bcd4 bold 8.5pt.

GOLDEN RULES section — each rule: teal ✓ in 8pt, white text 7pt:
✓  MTU mismatch is the #1 cause of stuck-in-ExStart — check both sides first
✓  Hello and dead timers must match exactly or the adjacency never forms
✓  Area 0 must be contiguous — every area needs a path to the backbone
✓  2-Way is normal for DROTHER pairs on broadcast segments
✓  Stub/NSSA areas intentionally suppress external routes
✓  Never clear ip ospf process in production without a maintenance window
✓  passive-interface disables Hello — check it isn't set where a peer is expected
✓  Network-type mismatch breaks DR election or blocks NBMA adjacency
✓  Duplicate router-ID silently breaks adjacencies across the whole area

Grey divider line inside panel.

AREA TYPE REFERENCE header in #f39c12 7.5pt bold, then table in 6.8pt:

Area type          Type 3/4   Type 5   Type 7   Notes
──────────────────────────────────────────────────────
Standard              Yes        Yes      No     Full visibility
Stub                   Yes        No       No     No externals; default injected
Totally Stubby          No         No       No     Only a default route from ABR
NSSA                   Yes         No      Yes    Local externals, translated at ABR
──────────────────────────────────────────────────────
Area 0 (backbone): every other area needs a direct or virtual-link path to it

─────────────────────────────────────────────────────────────────────────────
FOOTER  (y: 0.008 to 0.062)
─────────────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.038, "OSPF Neighbor State Machine Reference  ·  Single-Area & Multi-Area  ·  Cisco IOS / IOS-XE / IOS-XR  ·  Juniper JunOS",
         color="#888888", fontsize=7, ha="center")
fig.text(0.5, 0.018, "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019",
         color="#00bcd4", fontsize=8, ha="center", fontweight="bold")

─────────────────────────────────────────────────────────────────────────────
SAVE
─────────────────────────────────────────────────────────────────────────────
plt.savefig("ospf_guide.png", dpi=100, bbox_inches="tight",
            facecolor="#0d1b2a", edgecolor="none")
print("Saved. Provide download link.")

================================================================================
END OPTION 2
================================================================================
