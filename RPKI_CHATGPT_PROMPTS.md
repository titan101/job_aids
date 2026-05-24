# RPKI — ChatGPT Visual Prompts
# Option 2A: PNG poster (1920×1080). Option 2B: PDF carousel (7 pages, LinkedIn-optimized).
# Paste each into ChatGPT Advanced Data Analysis separately.

---

## OPTION 1 — DALL-E (quick, less accurate)

Create a dark-themed technical reference poster titled "RPKI — Securing BGP" on dark navy (#0d1b2a). Landscape 1920×1080. Teal accents, white text, orange warnings. Top strip: 6-step RPKI deployment lifecycle with colored boxes and arrows. Middle: 6 visual diagram cards showing ROA certificate, 5 RIR globe map, validator-to-router RTR flow, three RPKI states (VALID/INVALID/NOT FOUND) as colored traffic lights, hijack prevention before/after, and deployment checklist. Bottom: three panels with generic commands, RPKI vs IRR comparison table, and golden rules. Footer: github.com/titan101 · linkedin.com/in/varun-sinha-b778b019

---

## OPTION 2A — PNG POSTER — CODE INTERPRETER (RECOMMENDED)

Paste into ChatGPT Advanced Data Analysis:

---

Write Python using matplotlib and matplotlib.patches to generate a dark-themed RPKI reference poster. Figure size 19.2 x 10.8 inches at 100 DPI (1920x1080). Save as RPKI_guide.png at 100 DPI.

GLOBAL STYLE:
- Background everywhere: #0d1b2a
- ax.axis('off') on all axes
- Dot grid: tiny dots (#1e3a5f, size=0.8, alpha=0.35) in a 70×40 grid across full figure
- DejaVu Sans Mono for all CLI-style text, DejaVu Sans for labels

COLOR PALETTE:
  BG=#0d1b2a  CARD=#1a2a3a  PANEL=#131f2e
  TEAL=#00bcd4  ORANGE=#e67e22  WHITE=#ffffff  GREY=#888888
  RED=#e74c3c  YELLOW=#f1c40f  GREEN=#2ecc71  BLUE=#3498db  PURPLE=#9b59b6

════════════════════════════════════════════════════════════
SECTION 1 — RPKI Deployment Lifecycle (top 12%, y=0.876–0.995)
════════════════════════════════════════════════════════════

Draw 6 FancyBboxPatch rounded boxes (boxstyle="round,pad=0.015") in a horizontal row.
Each box: ~0.130 wide × 0.088 tall. x-centers: 0.083, 0.240, 0.397, 0.554, 0.711, 0.868
y-center: 0.935. facecolor = color at 25% alpha, edgecolor = color, linewidth=2.

Box definitions (label \n subtext, color):
  Box 1: "1. CREATE ROA"       / "Prefix+AS+maxlen at RIR"    color=RED
  Box 2: "2. RIR SIGNS"        / "Cryptographic certificate"  color=ORANGE
  Box 3: "3. VALIDATOR FETCHES"/ "rsync/RRDP from 5 RIRs"    color=YELLOW
  Box 4: "4. RTR SYNC"         / "VRPs pushed to routers"     color=YELLOW
  Box 5: "5. ROV APPLIED"      / "VALID / INVALID / NOT FOUND" color=GREEN
  Box 6: "6. ENFORCED"         / "INVALID routes dropped"     color=GREEN

Each box: bold white 8.5pt label, grey 6.5pt subtext.
Draw a large lock icon (Unicode 🔒 or draw a small padlock shape) inside box 1 at top-left, 10pt teal.
Draw teal arrows (linewidth=1.5, arrowstyle='->') between consecutive boxes.
Draw curved red arc (connectionstyle='arc3,rad=-0.45', arrowstyle='<-') from Box 1 top to Box 6 top.
Label the arc: "Misconfigured ROA → own prefix INVALID → traffic blackhole" in red 6.5pt.
Draw thin teal line at y=0.876 across full width.

════════════════════════════════════════════════════════════
SECTION 2 — Visual Diagram Cards (middle 44%, y=0.442–0.872)
════════════════════════════════════════════════════════════

2 rows × 3 columns. Card w=0.315 h=0.207. Col x-starts: 0.010, 0.341, 0.672. Row y-starts: 0.657, 0.445.
Each card: FancyBboxPatch facecolor=CARD, edgecolor=matching Zone 1 color, linewidth=2.
Glow: slightly larger same-color box behind at alpha=0.14.
Bold white header 8.5pt top-left. Diagram fills ~65% of card. FIX/NOTE section below.

─────────────────────────────────────────────────────────
CARD 1 — "ROA — ROUTE ORIGIN AUTHORIZATION" (RED border)
─────────────────────────────────────────────────────────
DIAGRAM: Draw a certificate visual — a large rounded rectangle (#1e3a5f fill, teal border, linewidth=2) centered in the card's diagram area. Inside the certificate:
  Top: draw a small ribbon/seal icon (a circle with a star ★ in teal, 14pt) centered
  Three rows of fields, each: orange label + white monospace value:
    PREFIX:      192.0.2.0/24
    MAX-LENGTH:  /24
    ORIGIN AS:   AS65001
  Bottom of certificate: small teal text "RIR-SIGNED ✓"
Outside the certificate, bottom-right: small orange warning box with text "⚠ max-length too short = own routes INVALID"

─────────────────────────────────────────────────────────
CARD 2 — "THE 5 TRUST ANCHORS — GLOBAL RIR COVERAGE" (ORANGE border)
─────────────────────────────────────────────────────────
DIAGRAM: Draw 5 colored rounded boxes arranged in a cross/plus pattern inside the card:
  Center-top:    RIPE NCC  — blue box  — "Europe / W.Asia / Russia"
  Left:          ARIN      — teal box  — "North America"
  Right:         APNIC     — purple box — "Asia-Pacific"
  Bottom-left:   LACNIC    — green box — "Latin America"
  Bottom-right:  AFRINIC   — orange box — "Africa"
Each box: ~0.07 wide, bold white name 7pt, grey 6pt region text below.
Draw thin lines from each box to a central point (a small teal circle labeled "IANA\nRoot" 6.5pt).
This creates a hub-and-spoke trust hierarchy visual.
Below the diagram: grey italic 6.5pt "All 5 RIRs = 5 Trust Anchors. Validator fetches from all."

─────────────────────────────────────────────────────────
CARD 3 — "VALIDATOR → RTR → ROUTER FLOW" (YELLOW border)
─────────────────────────────────────────────────────────
DIAGRAM: Draw a horizontal flow with three main components:
  Left box: "RPKI\nVALIDATOR" (yellow border, #1a2a3a fill, white 7pt bold)
    Inside: small text stack in grey 6pt: "Routinator" / "OctoRPKI" / "FORT" / "rpki-client"
  Middle annotation between validator and router:
    Draw a double-headed arrow (teal, linewidth=2) connecting the two boxes
    Above the arrow: "RTR PROTOCOL" in teal 7pt bold
    Below the arrow: "RFC 8210 · TCP 323" in grey 6pt
    A small cylinder shape between them labeled "VRP TABLE" in yellow 6.5pt
  Right box: "BGP\nROUTER" (teal border, #1a2a3a fill, white 7pt bold)
    Inside: small text in grey 6pt: "ROV enabled"
  Above the whole flow: grey 6pt "Validator fetches from 5 RIRs via rsync/RRDP, builds VRP table, pushes to routers"

─────────────────────────────────────────────────────────
CARD 4 — "RPKI VALIDATION STATES" (YELLOW border)
─────────────────────────────────────────────────────────
DIAGRAM: Draw three large side-by-side state boxes filling most of the card's diagram area.
Each state box: rounded rectangle, bold colored header, white body text 6.5pt.

  Box A — VALID (green, facecolor green at 20% alpha, edgecolor GREEN):
    Header: "✓  VALID"  (bold green 10pt, large checkmark)
    Body: "AS + prefix match ROA\nLength ≤ max-length\n→ ACCEPT & PREFER"

  Box B — INVALID (red, facecolor red at 20% alpha, edgecolor RED):
    Header: "✗  INVALID"  (bold red 10pt, large X)
    Body: "Wrong origin AS\nOR prefix too specific\n→ DROP"

  Box C — NOT FOUND (grey, facecolor grey at 20% alpha, edgecolor GREY):
    Header: "?  NOT FOUND"  (bold grey 10pt, question mark)
    Body: "No ROA exists\nfor this prefix\n→ ACCEPT + MONITOR"

Below the three boxes: small orange text 6pt "57% of IPv4 prefixes have ROAs (2025). NOT FOUND ≠ malicious."

─────────────────────────────────────────────────────────
CARD 5 — "HIJACK PREVENTION — BEFORE vs AFTER RPKI" (GREEN border)
─────────────────────────────────────────────────────────
DIAGRAM: Two-row comparison layout with a grey dashed divider between rows.

TOP ROW — WITHOUT RPKI (label: red "WITHOUT RPKI" at left):
  Three boxes in a row:
    "ATTACKER\nAS666" (red border) → arrow → "ANNOUNCES\n1.2.3.0/24" (red border) → arrow → "ROUTER\nACCEPTS ✗" (red border)
  Below the last arrow: red text 6pt "Traffic hijacked — no verification"

BOTTOM ROW — WITH RPKI (label: green "WITH RPKI" at left):
  Three boxes in a row:
    "ATTACKER\nAS666" (red border) → arrow → "ANNOUNCES\n1.2.3.0/24" (orange border) → arrow labeled "ROA CHECK" → "INVALID\nDROPPED ✓" (green border)
  Below: green text 6pt "ROA says AS12345 owns 1.2.3.0/24 — AS666 = INVALID → dropped"

─────────────────────────────────────────────────────────
CARD 6 — "DEPLOYMENT CHECKLIST" (GREEN border)
─────────────────────────────────────────────────────────
DIAGRAM: Vertical numbered step list rendered as visual progress steps. Each step is a row with:
  - A circle on the left (teal fill for completed concept, #1a2a3a for action steps) with step number in white bold 7pt
  - Step text in white 7pt to the right
  - Thin vertical teal line connecting circles (like a timeline)

Steps:
  1  Audit all prefixes you currently announce
  2  Log in to your RIR portal — enable Hosted RPKI
  3  Create ROAs — set max-length = your actual announced length
  4  Deploy validator (Routinator recommended)
  5  Connect routers via RTR (TCP 323 or 3323)
  6  Enable ROV in MONITOR-ONLY mode — fix own INVALIDs first
  7  Phase to enforcement — DROP INVALID routes
  8  Require customers to register ROAs

Draw thin teal separator at y=0.442.

════════════════════════════════════════════════════════════
SECTION 3 — Bottom Three Panels (bottom 37%, y=0.040–0.436)
════════════════════════════════════════════════════════════

Three FancyBboxPatch panels (facecolor=PANEL, edgecolor=TEAL, linewidth=1.5, rounded).
x-starts: 0.008, 0.341, 0.674 — each width=0.316, height=0.388, y=0.042

────────────────────────────────
PANEL 1 (LEFT) — GENERIC COMMANDS
────────────────────────────────
Header: "VERIFICATION COMMANDS" teal bold 9pt centered.
Subheader: small italic grey 7pt centered: "Syntax varies by platform — verify against your vendor documentation"

Draw a light orange rounded box around the subheader text to make it stand out.

Then numbered list, monospace 6.5pt, teal numbers + white operation + grey description:

  1.  Show RPKI/RTR session status        → Confirm validator connection is up
  2.  Show validated ROA cache            → List all VRPs currently held by router
  3.  Show BGP route RPKI state           → See VALID/INVALID/NOT FOUND per prefix
  4.  Show BGP neighbor RPKI stats        → Counts of each state from a peer
  5.  Show route with RPKI tag detail     → Full validation detail for a prefix
  6.  Debug RPKI validation events        → Real-time validation decisions (use carefully)
  7.  Clear / refresh RTR cache           → Force re-sync from validator
  8.  Show RTR connection status          → Validator IP, session state, last update time
  9.  Verify specific prefix RPKI state   → Check a single prefix VALID/INVALID/NOT FOUND
  10. Show RPKI origin validation table   → Full local VRP database

────────────────────────────────
PANEL 2 (MIDDLE) — RPKI vs IRR + KEY STATS
────────────────────────────────
Header: "RPKI vs IRR — WHY THE UPGRADE?" teal bold 9pt centered.

Draw a 3-column comparison table with alternating row shading (#1a2a3a / #131f2e):
Col headers (bold, 7pt): Feature | IRR | RPKI
Col header colors: white | orange | green

Row data (feature in white 6.5pt, IRR in orange, RPKI in green):
  Verification      | Manual / trust-based      | Cryptographic (RIR-signed)
  Data accuracy     | Stale, inconsistent        | Authoritative, RIR-maintained
  Update speed      | Manual, days               | Automatic, ~15 min (RRDP)
  Enforcement       | Neighbor cooperation       | DROP on INVALID (ROV)
  Coverage          | High but unverified        | 57% IPv4, growing
  Hijack protection | Partial (filter lists)     | Yes (cryptographic proof)

Thin grey divider.
Header: "2025 COVERAGE STATS" teal bold 8pt.

Draw 3 large stat boxes side by side:
  Box 1: large "57%" in teal 18pt bold + grey 7pt "IPv4 prefixes\nhave ROAs"
  Box 2: large "70%" in green 18pt bold + grey 7pt "of internet traffic\nevaluated VALID"
  Box 3: large "5" in ORANGE 18pt bold + grey 7pt "RIRs providing\nHosted RPKI"

Each stat box: rounded, #1a2a3a fill, teal border.

────────────────────────────────
PANEL 3 (RIGHT) — GOLDEN RULES + BLACKHOLE WARNING
────────────────────────────────
Header: "GOLDEN RULES" teal bold 9pt centered.

8 rules, teal ✓ prefix, white text 7pt, tight spacing:
  ✓ RPKI validates ORIGIN only — not the full AS path (that's BGPsec, not deployed)
  ✓ Create the ROA BEFORE announcing the route — not after
  ✓ max-length = your most specific announced prefix, not shorter
  ✓ Run 2+ validators — RTR session loss should never be a single point of failure
  ✓ Monitor-only mode first — fix your own INVALIDs before enforcing on peers
  ✓ NOT FOUND ≠ malicious — means no ROA exists, not that the route is hijacked
  ✓ INVALID = drop with confidence — a ROA exists and this announcement violates it
  ✓ Update ROAs before announcing new subnets — propagation takes ~15 minutes

Grey divider line.
Header: "⚠  BLACKHOLE RISK" in orange bold 8pt.

Draw an orange-bordered warning box (#1a2a3a fill, orange edgecolor, linewidth=2):
  Title in orange 7pt bold: "MAX-LENGTH MISCONFIGURATION"
  Body in white 6.5pt:
    "You announce 10.0.0.0/22"
    "ROA max-length set to /22"
    "You start announcing 10.0.0.0/24"
    "→ That /24 is now INVALID"
    "→ Peers enforcing RPKI DROP it"
    "→ Your traffic disappears silently"
  Bottom: green 6.5pt "Fix: set max-length to most specific prefix you'll ever announce"

════════════════════════════════════════════════════════════
FOOTER
════════════════════════════════════════════════════════════

ax.text(0.5, 0.013, "RPKI Reference  ·  BGP Route Origin Validation  ·  Platform-Agnostic", color="#888888", fontsize=7, ha="center", transform=fig.transFigure)
ax.text(0.5, 0.005, "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019", color="#00bcd4", fontsize=7, ha="center", transform=fig.transFigure)
ax.text(0.98, 0.005, "Created by Varun Sinha", color="#00bcd4", fontsize=7, ha="right", fontstyle="italic", transform=fig.transFigure)

Save as RPKI_guide.png at 100 DPI.

---

## OPTION 2B — PDF CAROUSEL (LinkedIn document — 7 pages) — CODE INTERPRETER

Paste into ChatGPT Advanced Data Analysis separately from Option 2A:

---

Write Python using matplotlib to generate a 7-page PDF carousel optimized for LinkedIn document posts. Each page: 10.8 x 13.5 inches at 100 DPI (1080x1350px portrait). Save as RPKI_carousel.pdf using matplotlib's PdfPages.

Global style: background #0d1b2a everywhere. White text. Teal (#00bcd4) accents. No dot grid on PDF pages (keep clean for readability).

Use matplotlib.backends.backend_pdf.PdfPages to write all 7 pages into one PDF file.

─────────────────────────────────────────────────────────
PAGE 1 — COVER
─────────────────────────────────────────────────────────
Full dark navy page. Centered content:
  Large teal lock icon: draw a padlock shape using matplotlib patches — a rectangle body with a semicircle arc on top (like a shackle), teal fill, centered in upper-third of page.
  Title: "RPKI" in bold white 52pt, centered below lock
  Subtitle: "Securing BGP Route Announcements" in teal 20pt, centered
  Divider: thin teal horizontal line (width = 60% of page)
  Body line: "Cryptographic proof that an AS is authorized to announce a prefix." white 14pt centered
  Bottom section (y ≈ 0.15):
    "github.com/titan101" in teal 11pt
    "linkedin.com/in/varun-sinha-b778b019" in teal 11pt
    "Created by Varun Sinha" in grey italic 10pt

─────────────────────────────────────────────────────────
PAGE 2 — THE PROBLEM: BGP HAS NO SECURITY
─────────────────────────────────────────────────────────
Header: "THE PROBLEM" in red bold 28pt, top-left with a red left border bar.
Subheader: "BGP was designed in 1989 on trust. Any AS can announce any prefix." white 14pt.

Draw a visual attack scenario (center of page):
  Row 1 (legitimate): 
    Green box "OWNER\nAS12345" → solid green arrow → green box "1.2.3.0/24\nlegitimate" → green arrow → "INTERNET ✓"
  Spacer
  Row 2 (attacker, draw below):
    Red box "ATTACKER\nAS666" → dashed red arrow → red box "1.2.3.0/24\nHIJACKED" → red arrow → "INTERNET ✗"
    Red text below: "Without RPKI — both get accepted. Traffic can go anywhere."

Below the diagram, draw 3 incident boxes side by side (dark fill, orange border):
  Box 1: "2020\nRostelecom\nAWS · Cloudflare\nhijacked ~1hr"
  Box 2: "2020\nTelstra\n500 prefixes\n50 countries"
  Box 3: "2021\nVodafone Idea\n30,000+ prefixes\n13× traffic spike"
Each box: orange border, white text 9pt, #1a2a3a fill.

Footer bar: thin teal line + small grey text "RPKI Reference · Created by Varun Sinha · github.com/titan101"

─────────────────────────────────────────────────────────
PAGE 3 — HOW RPKI WORKS
─────────────────────────────────────────────────────────
Header: "HOW RPKI WORKS" in teal bold 28pt.
Subheader: "From ROA creation to route validation — 4 steps" white 14pt.

Draw a vertical flow diagram (top to bottom, centered):

Step 1 box (orange border): 
  Left: large circle with "1" in orange bold 16pt
  Right: Title "CREATE ROA" orange bold 14pt
         Body: "At your RIR portal: define Prefix + Origin AS + Max-Length" white 11pt
         Mini certificate visual: small rectangle showing PREFIX / AS / MAX-LEN fields

Arrow down.

Step 2 box (yellow border):
  "2" circle (yellow) | "VALIDATOR FETCHES" yellow bold 14pt
  "Routinator / OctoRPKI / FORT fetch ROAs from all 5 RIRs via rsync or RRDP" white 11pt
  Draw 5 small colored circles labeled ARIN · RIPE · APNIC · LACNIC · AFRINIC with arrows pointing to validator box

Arrow down.

Step 3 box (yellow border):
  "3" circle (yellow) | "RTR PROTOCOL SYNCS" yellow bold 14pt
  "Validator pushes Validated Route Prefixes (VRPs) to routers via TCP" white 11pt
  "RFC 8210 · Port 323 (or 3323)" grey 10pt

Arrow down.

Step 4 box (green border):
  "4" circle (green) | "ROUTE ORIGIN VALIDATION" green bold 14pt
  "Router checks every BGP announcement against VRP table" white 11pt
  Three mini colored badges inline: [VALID ✓] green [INVALID ✗] red [NOT FOUND ?] grey

Footer bar: teal line + grey attribution text.

─────────────────────────────────────────────────────────
PAGE 4 — THE THREE RPKI STATES
─────────────────────────────────────────────────────────
Header: "THE 3 RPKI STATES" in teal bold 28pt.

Draw three large portrait-oriented state cards stacked vertically (each ~⅓ page height):

Card 1 — VALID (green):
  Left strip: solid green rectangle (full height of card, ~5% width)
  Header: large "✓  VALID" in green bold 22pt
  Condition: "Origin AS matches ROA AND prefix length ≤ max-length" white 12pt
  Action: "→ ACCEPT and PREFER in route selection" green 12pt bold
  Visual: small green shield icon (draw a pentagon shape with ✓ inside)

Card 2 — INVALID (red):
  Left strip: solid red rectangle
  Header: large "✗  INVALID" in red bold 22pt
  Condition: "Wrong origin AS  OR  prefix more specific than max-length" white 12pt
  Action: "→ DROP  (cryptographically proven wrong)" red 12pt bold
  Visual: small red X in a circle

Card 3 — NOT FOUND (grey):
  Left strip: solid grey rectangle
  Header: large "?  NOT FOUND" in grey bold 22pt
  Condition: "No ROA exists for this prefix — no assertion either way" white 12pt
  Action: "→ ACCEPT (tag for monitoring)   43% of IPv4 still here (2025)" grey 12pt
  Visual: small grey question mark in a circle

Footer bar.

─────────────────────────────────────────────────────────
PAGE 5 — DEPLOYMENT STEPS
─────────────────────────────────────────────────────────
Header: "DEPLOYING RPKI" in teal bold 28pt.
Subheader: "8 steps from zero to enforcing" white 13pt.

Draw 8 steps as a vertical timeline (circle + line + content):
Each step: left-side teal circle (numbered 1-8, white bold 12pt inside) + teal vertical connector line + right-side content box.

  1  Audit all prefixes you currently announce to BGP
  2  Log in to your RIR portal — enable Hosted RPKI (free)
  3  Create ROAs — set max-length = your actual announced prefix length
  4  Deploy RPKI validator on your infrastructure
  5  Connect routers to validator via RTR protocol
  6  Enable ROV in MONITOR-ONLY mode — log but do not drop
  7  Fix any of your own prefixes showing INVALID before enforcing
  8  Switch to enforcement — DROP INVALID routes

Each step: circle in teal, connector line in teal (dashed for steps 6-8 = "phased rollout"),
step text in white 11pt, small grey italic note below each step (3-5 words of context).

Add a small orange box at the bottom:
"⚠  Always test ROA changes in monitor mode before enforcement — misconfigured ROAs can black-hole your own traffic"
Orange border, #1a2a3a fill, orange text 10pt.

Footer bar.

─────────────────────────────────────────────────────────
PAGE 6 — WHAT RPKI DOESN'T COVER + COMMANDS
─────────────────────────────────────────────────────────
Header: "KNOW THE LIMITS" in orange bold 28pt.

Left half of page — draw 4 "Not covered" boxes in a 2×2 grid:
  Box 1 (grey border): "AS_PATH attacks\n→ That's BGPsec\n(not deployed in 2025)"
  Box 2 (grey border): "Route leaks\n→ Legitimate AS,\nwrong upstream"
  Box 3 (grey border): "Path plausibility\n→ ASPA objects\n(still RFC draft)"
  Box 4 (grey border): "Full path signing\n→ BGPsec RFC 8205\n0 prod deployments"
Each box: grey border, #1a2a3a fill, white text 9pt, "✗" in red 12pt top-right.

Right half — "VERIFICATION COMMANDS" panel:
  Teal header 13pt bold.
  Orange italic subtext: "Syntax varies by platform"
  Numbered list white 9pt monospace:
    1. Show RTR/RPKI session status
    2. Show validated ROA cache (VRP table)
    3. Show BGP route RPKI state
    4. Debug validation events
    5. Clear/refresh RTR cache
    6. Verify specific prefix state
    7. Show RPKI origin validation table

Footer bar.

─────────────────────────────────────────────────────────
PAGE 7 — SAVE THIS + FOOTER
─────────────────────────────────────────────────────────
Full dark navy page, centered content.

Top third:
  Teal shield icon (draw pentagon shape, teal fill, white "✓" inside, large ~80pt equivalent)

Middle:
  "Save this." in white bold 36pt centered
  Thin teal divider line
  "RPKI protects BGP from origin hijacking." white 16pt centered
  "57% of IPv4 prefixes have ROAs. 70% of traffic validated." grey 13pt centered
  "" (spacer)
  "Still no RPKI? You're trusting every peer on the internet." orange italic 13pt centered

Bottom third:
  Three stat boxes side by side (same as PNG poster stats):
    "57%"  teal 28pt bold / "IPv4 prefixes\nwith ROAs" grey 10pt
    "70%"  green 28pt bold / "traffic\nVALID (2025)" grey 10pt
    "FREE" orange 28pt bold / "Hosted RPKI\nat every RIR" grey 10pt

Footer:
  "github.com/titan101  ·  linkedin.com/in/varun-sinha-b778b019" teal 11pt centered
  "Created by Varun Sinha" grey italic 10pt centered
  "RPKI Reference  ·  BGP Route Origin Validation  ·  Platform-Agnostic" grey 9pt centered

Save as RPKI_carousel.pdf using matplotlib.backends.backend_pdf.PdfPages.
