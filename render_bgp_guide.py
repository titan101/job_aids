from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

W, H = 1536, 1024
OUT = Path(__file__).with_name("BGP_ISP_Troubleshooting_Guide.png")

FONT_DIR = Path("C:/Windows/Fonts")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_TITLE = font("AGENCYB.TTF", 48)
F_SUB = font("consolab.ttf", 19)
F_STATE = font("consolab.ttf", 20)
F_STATE_SMALL = font("segoeui.ttf", 14)
F_CARD_HEAD = font("consolab.ttf", 22)
F_BODY = font("consola.ttf", 8)
F_BODY_BOLD = font("consolab.ttf", 10)
F_CODE = font("consola.ttf", 8)
F_PANEL = font("consolab.ttf", 24)
F_PANEL_SMALL = font("consola.ttf", 13)
F_FOOT = font("segoeui.ttf", 17)
F_SCRIPT = font("segoepr.ttf", 24)

BG = (2, 11, 22)
PANEL = (3, 18, 33)
PANEL_2 = (6, 28, 48)
WHITE = (245, 246, 248)
GRAY = (190, 198, 208)
DIM = (118, 138, 154)
RED = (255, 54, 48)
ORANGE = (255, 124, 8)
YELLOW = (255, 218, 0)
GREEN = (95, 220, 65)
TEAL = (0, 217, 238)
PURPLE = (178, 90, 245)
BLUE = (18, 105, 205)

DASH = "\u2014"
ARROW = "\u2192"
BULLET = "\u2022"
CHECK = "\u2713"
NE = "\u2260"
APPROX = "\u2248"


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_center(draw, x, y, text, fnt, fill):
    tw, _ = text_size(draw, text, fnt)
    draw.text((x - tw / 2, y), text, font=fnt, fill=fill)


def rounded(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_arrow(draw, x1, y1, x2, y2, color=WHITE, width=3):
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 12
    pts = [
        (x2, y2),
        (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45)),
        (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45)),
    ]
    draw.polygon(pts, fill=color)


def bezier(p0, p1, p2, p3, steps=160):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        pts.append((x, y))
    return pts


def dashed_curve(draw, pts, color, width=3, dash=14, gap=7):
    dist = 0
    on = True
    remain = dash
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        if seg == 0:
            continue
        start = 0
        while start < seg:
            take = min(remain, seg - start)
            t1 = start / seg
            t2 = (start + take) / seg
            p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            p2 = (a[0] + (b[0] - a[0]) * t2, a[1] + (b[1] - a[1]) * t2)
            if on:
                draw.line((p1, p2), fill=color, width=width)
            start += take
            remain -= take
            if remain <= 0:
                on = not on
                remain = dash if on else gap


def wrap_by_width(draw, text, fnt, width):
    words = text.split()
    if not words:
        return [""]
    lines = []
    cur = words[0]
    for word in words[1:]:
        test = cur + " " + word
        if text_size(draw, test, fnt)[0] <= width:
            cur = test
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, width, line_h, bullet=False):
    prefix = BULLET + " " if bullet else ""
    indent = 12 if bullet else 0
    lines = wrap_by_width(draw, text, fnt, width - indent - (10 if bullet else 0))
    for i, line in enumerate(lines):
        if bullet and i == 0:
            draw.text((x, y), BULLET, font=fnt, fill=fill)
        draw.text((x + (indent if bullet else 0), y), line, font=fnt, fill=fill)
        y += line_h
    return y


def draw_power(draw, cx, cy, color):
    draw.arc((cx - 18, cy - 12, cx + 18, cy + 24), 38, 322, fill=color, width=5)
    draw.line((cx, cy - 18, cx, cy + 4), fill=color, width=5)


def draw_chain(draw, cx, cy, color):
    draw.arc((cx - 27, cy - 10, cx + 5, cy + 22), 50, 310, fill=color, width=5)
    draw.arc((cx - 5, cy - 22, cx + 27, cy + 10), 230, 130, fill=color, width=5)
    draw.line((cx - 9, cy + 8, cx + 9, cy - 8), fill=color, width=4)


def draw_pulse(draw, cx, cy, color):
    pts = [(cx - 27, cy), (cx - 14, cy), (cx - 10, cy - 9), (cx - 2, cy + 14), (cx + 4, cy - 18), (cx + 13, cy + 9), (cx + 18, cy), (cx + 28, cy)]
    draw.line(pts, fill=color, width=4, joint="curve")


def draw_plane(draw, cx, cy, color):
    pts = [(cx - 24, cy - 8), (cx + 26, cy - 27), (cx + 6, cy + 25), (cx - 2, cy + 4)]
    draw.line(pts + [pts[0]], fill=color, width=4)
    draw.line((cx - 2, cy + 4, cx + 26, cy - 27), fill=color, width=3)


def draw_handshake(draw, cx, cy, color):
    draw.line((cx - 29, cy - 4, cx - 12, cy + 10, cx, cy), fill=color, width=4)
    draw.line((cx + 29, cy - 4, cx + 12, cy + 10, cx, cy), fill=color, width=4)
    for dx in [-5, 2, 9]:
        draw.line((cx + dx, cy + 2, cx + dx + 8, cy + 10), fill=color, width=3)
    draw.arc((cx - 24, cy - 23, cx - 2, cy - 1), 25, 230, fill=color, width=4)
    draw.arc((cx + 2, cy - 23, cx + 24, cy - 1), 310, 155, fill=color, width=4)


def draw_check(draw, cx, cy, color):
    draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), outline=color, width=4)
    draw.line((cx - 9, cy, cx - 2, cy + 8, cx + 12, cy - 10), fill=color, width=5)


def draw_star(draw, cx, cy, r, color):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    draw.polygon(pts, fill=color)


def code_box(draw, x, y, w, h):
    rounded(draw, (x, y, x + w, y + h), 4, (7, 31, 48), (42, 133, 160), 1)


def state_box(draw, idx, x, y, w, h, title, desc, color, icon):
    rounded(draw, (x, y, x + w, y + h), 8, PANEL, color, 2)
    draw.ellipse((x + 72, y + 8, x + 96, y + 32), fill=color)
    draw_center(draw, x + 84, y + 10, str(idx), font("consolab.ttf", 13), WHITE)
    title_font = F_STATE if len(title) <= 9 else font("consolab.ttf", 16)
    draw.text((x + 112, y + 12), title, font=title_font, fill=WHITE)
    icon(draw, x + 35, y + 55, color)
    lines = wrap_by_width(draw, desc, F_STATE_SMALL, w - 92)
    ty = y + 41
    for line in lines[:3]:
        draw.text((x + 74, ty), line, font=F_STATE_SMALL, fill=WHITE)
        ty += 18


def detail_card(draw, x, y, w, h, idx, title, color, why_lines, fix_lines, icon=None):
    rounded(draw, (x, y, x + w, y + h), 8, PANEL, color, 2)
    draw.ellipse((x + 24, y + 8, x + 47, y + 31), outline=color, width=2)
    draw_center(draw, x + 35.5, y + 10, str(idx), font("consolab.ttf", 13), WHITE)
    draw.text((x + 63, y + 9), title, font=F_CARD_HEAD, fill=WHITE)
    yy = y + 43
    draw.text((x + 13, yy), "WHY:", font=F_BODY_BOLD, fill=color)
    bx = x + 55
    by = yy + 3
    for line in why_lines:
        by = draw_wrapped(draw, bx, by, line, F_BODY, WHITE, w - 74, 12, bullet=True)
    sep_y = by + 4
    draw.line((x + 13, sep_y, x + w - 13, sep_y), fill=(95, 118, 130), width=1)
    fy = sep_y + 10
    draw.text((x + 13, fy), "FIX:", font=F_BODY_BOLD, fill=TEAL)
    box_h = max(57, y + h - fy - 12)
    code_box(draw, x + 52, fy - 1, w - 65, box_h)
    cy = fy + 8
    for line in fix_lines:
        draw.text((x + 61, cy), line, font=F_CODE, fill=WHITE)
        cy += 16


img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Background dot field.
for yy in range(14, H - 12, 14):
    for xx in range(18, W - 18, 14):
        if yy < 228 or yy > 742 or xx % 42 == 18:
            draw.point((xx, yy), fill=(72, 94, 111))

# Title.
title_parts = [("BGP ", WHITE), ("ISP ", TEAL), ("TROUBLESHOOTING ", WHITE), ("GUIDE", TEAL)]
total = sum(text_size(draw, t, F_TITLE)[0] for t, _ in title_parts)
tx = (W - total) / 2
for text, color in title_parts:
    draw.text((tx, 6), text, font=F_TITLE, fill=color, stroke_width=1, stroke_fill=(10, 10, 14))
    tx += text_size(draw, text, F_TITLE)[0]
draw_center(draw, W / 2, 58, f"From Idle to Established {DASH} and Everything That Breaks In Between", F_SUB, WHITE)

# Hold-down dashed arrow.
curve = bezier((112, 104), (232, 82), (1260, 82), (1370, 104))
dashed_curve(draw, curve, RED, 3)
draw.polygon([(108, 104), (125, 94), (119, 112)], fill=RED)
draw.polygon([(1374, 104), (1357, 94), (1363, 112)], fill=RED)
draw_center(draw, W / 2, 90, f"any error {ARROW} hold-down timer", F_STATE_SMALL, RED)

# State boxes.
states = [
    (1, "IDLE", f"Not attempting {DASH} check config & route to peer", RED, draw_power),
    (2, "CONNECT", f"TCP SYN sent {DASH} waiting for SYN-ACK", ORANGE, draw_chain),
    (3, "ACTIVE", f"TCP failing {DASH} BGP retrying aggressively", ORANGE, draw_pulse),
    (4, "OPENSENT", f"OPEN sent {DASH} waiting for remote OPEN", YELLOW, draw_plane),
    (5, "OPENCONFIRM", f"OPEN+KEEPALIVE sent {DASH} awaiting their KEEPALIVE", YELLOW, draw_handshake),
    (6, "ESTABLISHED", f"Session up {DASH} this is the only state that matters", GREEN, draw_check),
]
x0, y0, bw, bh, gap = 24, 116, 217, 98, 41
for i, (idx, name, desc, color, icon) in enumerate(states):
    x = x0 + i * (bw + gap)
    state_box(draw, idx, x, y0, bw, bh, name, desc, color, icon)
    if i < len(states) - 1:
        draw_arrow(draw, x + bw + 8, y0 + bh / 2, x + bw + gap - 8, y0 + bh / 2, WHITE, 3)

cards = {
    "IDLE": (
        RED,
        [
            "neighbor not configured or shutdown command active",
            "No route to peer IP in routing table (check IGP/static)",
            "BGP router process not running (missing router bgp <ASN>)",
            f"Hold-down timer from previous error {DASH} wait or clear",
            "Wrong VRF - neighbor defined in default, peering in VRF (or vice versa)",
            "Passive mode: neighbor <IP> passive - will not initiate TCP",
        ],
        [
            'show bgp neighbors <IP> | i "BGP state|shutdown"',
            "show route <peer-IP>  /  show ip route <peer-IP>",
            "clear bgp <neighbor>   [IOS: clear ip bgp <IP>]",
            'Juniper: show bgp neighbor <IP> | match "Type|State"',
        ],
        draw_power,
    ),
    "CONNECT": (
        ORANGE,
        [
            "Firewall or ACL blocking TCP port 179 inbound OR the TCP return path",
            "Source IP mismatch - router sending from physical IP, ISP expects loopback",
            f"Routing asymmetry {DASH} SYN leaves, TCP SYN-ACK dropped on return",
            "GTSM/TTL Security enabled on one side only (ttl-security hops mismatch)",
            "Both sides configured passive - neither initiates",
        ],
        [
            "telnet <peer-IP> 179 from the router CLI - proves port 179 is open",
            'show bgp neighbors <IP> | i "Local host|Foreign host"',
            "show tcp brief - confirm whether TCP session exists at all",
            "Verify ACL/firewall permits TCP 179 both directions",
            "Juniper: run telnet <IP> port 179",
        ],
        draw_chain,
    ),
    "ACTIVE": (
        ORANGE,
        [
            "update-source set to loopback but loopback not in IGP / not reachable",
            "eBGP multihop not configured - default TTL=1 drops packet at first hop",
            "Wrong neighbor IP configured (off-by-one in /30 - classic typo)",
            "ACL silently dropping TCP return traffic (not logging, no counter increment)",
            "GTSM mismatch - one side has ttl-security hops, other sends TTL=255",
            "MTU mismatch - TCP SYN gets through, large BGP OPEN fragment drops",
            "disable-connected-check missing for loopback peering on directly connected link",
        ],
        [
            "ping <peer-IP> source <loopback> - must succeed before BGP will work",
            'show bgp neighbors <IP> | i "BGP state|Local host|Remote"',
            "neighbor <IP> ebgp-multihop 2        (if peering via loopback)",
            "neighbor <IP> update-source Loopback0  (if peering via loopback)",
            "neighbor <IP> disable-connected-check   (loopback on directly connected link)",
            "Juniper: set protocols bgp group <name> multihop ttl <n>",
        ],
        draw_pulse,
    ),
    "OPENSENT": (
        YELLOW,
        [
            "Wrong remote AS configured - BGP rejects OPEN (NOTIFICATION code 2.2)",
            "2-byte AS configured locally, ISP using 4-byte AS (or vice versa)",
            "Router-ID collision - both peers using same BGP router-ID",
            "Address-family capability mismatch (e.g. IPv6 AF not accepted)",
            "Hold time < 3 seconds rejected per RFC 4271 - code 2.6",
            "Remote end receives OPEN, sends back NOTIFICATION, resets session",
        ],
        [
            "Confirm ASN with ISP - 2-byte (< 65536) or 4-byte (> 65535)",
            'show bgp neighbors <IP> | i "BGP version|remote AS|BGP Identifier"',
            "Check syslog/log buffer for NOTIFICATION messages with error codes",
            "debug bgp <neighbor> events   (IOS: debug ip bgp <IP> events)",
            "Packet capture port 179 - read the OPEN message fields directly",
            'Juniper: monitor traffic interface <int> matching "tcp port 179"',
        ],
        draw_plane,
    ),
    "OPENCONFIRM": (
        YELLOW,
        [
            "MD5 authentication password mismatch (one wrong character)",
            "Hold timer expired before KEEPALIVE received",
            "GTSM/TTL Security mismatch at this stage",
            "Excessive CPU load - router can't respond with KEEPALIVE in time",
            "TCP window size / buffer exhaustion under heavy load",
        ],
        [
            "Remove MD5 auth temporarily to test (NO AUTH = TEST ONLY)",
            "confirm password case-sensitive, no extra spaces",
            "show bgp neighbors <IP> | i authentication",
            "show bgp neighbors <IP> | i holdtime",
            "increase hold-time if needed (recommend 60-180 sec)",
            "Juniper: set protocols bgp group <name> hold-time <secs>",
        ],
        draw_handshake,
    ),
    "ESTABLISHED": (
        GREEN,
        [
            "Session up but no routes? Likely policy / reachability problem",
            "Route filtering - prefix-lists / route-maps / communities",
            "Next-hop not reachable - traffic blackholed even though routes received",
            "Network statement missing or incorrect on your side",
            "Max-prefix limit hit - routes received but not installed",
            "Outbound routes suppressed by policy",
        ],
        [
            "show bgp summary                  - check prefix counts (sent/received)",
            "show bgp neighbors <IP> advertised-routes",
            "show bgp neighbors <IP> received-routes",
            "show ip route <prefix>            - verify next-hop reachable?",
            "traceroute <prefix> source <loopback>",
            "Juniper: show route receive-protocol bgp <group>",
        ],
        draw_check,
    ),
}

cx0, cy1, cw, ch1, cg = 24, 230, 472, 268, 20
for col, name in enumerate(["IDLE", "CONNECT", "ACTIVE"]):
    color, why, fix, icon = cards[name]
    detail_card(draw, cx0 + col * (cw + cg), cy1, cw, ch1, col + 1, name, color, why, fix, icon)

cy2, ch2 = 502, 250
for col, name in enumerate(["OPENSENT", "OPENCONFIRM", "ESTABLISHED"]):
    color, why, fix, icon = cards[name]
    detail_card(draw, cx0 + col * (cw + cg), cy2, cw, ch2, col + 4, name, color, why, fix, icon)

# Bottom command panel.
py, ph = 762, 219
left_x, left_w = 24, 714
right_x, right_w = 756, 756
rounded(draw, (left_x, py, left_x + left_w, py + ph), 8, PANEL, (85, 176, 210), 1)
draw.rounded_rectangle((left_x + 14, py + 12, left_x + 48, py + 38), radius=3, fill=TEAL)
draw.text((left_x + 23, py + 12), ">", font=font("consolab.ttf", 20), fill=BG)
draw.text((left_x + 34, py + 12), "_", font=font("consolab.ttf", 20), fill=BG)
draw.text((left_x + 78, py + 11), f"VERIFICATION COMMANDS {DASH} Run In This Order", font=F_PANEL, fill=TEAL)
commands = [
    ("1.", "show bgp summary", f"{ARROW} all neighbors + state + prefix count"),
    ("2.", "show bgp neighbors <IP>", f"{ARROW} full state detail + error codes"),
    ("3.", "show bgp neighbors <IP> advertised-routes", f"{ARROW} what you're actually sending"),
    ("4.", "show bgp neighbors <IP> received-routes", f"{ARROW} what ISP is sending"),
    ("5.", "show ip route bgp", f"{ARROW} routes installed in RIB"),
    ("6.", "ping <peer> source <loopback>", f"{ARROW} verify Layer 3 reachability first"),
    ("7.", "telnet <peer> 179", f"{ARROW} test TCP port 179 directly"),
    ("8.", "clear ip bgp <IP> soft", f"{ARROW} refresh routes without dropping session"),
]
yy = py + 42
for num, cmd, desc in commands:
    draw.text((left_x + 30, yy), num, font=F_PANEL_SMALL, fill=TEAL)
    draw.text((left_x + 64, yy), cmd, font=F_PANEL_SMALL, fill=WHITE)
    draw.text((left_x + 388, yy), desc, font=F_PANEL_SMALL, fill=WHITE)
    yy += 19
draw.rounded_rectangle((left_x + 14, py + ph - 27, left_x + left_w - 14, py + ph - 10), radius=3, fill=(12, 77, 150))
draw.text((left_x + 30, py + ph - 28), "NOTE:", font=font("consolab.ttf", 12), fill=TEAL)
draw.text((left_x + 82, py + ph - 28), "Command syntax and output may vary between different vendors (Cisco, Juniper, Arista, etc.)", font=font("consola.ttf", 11), fill=WHITE)

# Golden rules.
rounded(draw, (right_x, py, right_x + right_w, py + ph), 8, PANEL, PURPLE, 1)
draw_star(draw, right_x + 200, py + 20, 15, PURPLE)
draw.text((right_x + 224, py + 10), "GOLDEN RULES", font=F_PANEL, fill=PURPLE)
draw.line((right_x + right_w / 2 + 60, py + 34, right_x + right_w / 2 + 60, py + ph - 32), fill=WHITE, width=1)
rules = [
    f"Test TCP 179 first {DASH} BGP won't come up if it's blocked",
    "ACTIVE state = Layer 3 or source IP problem, almost always",
    f"MD5 failures are silent {DASH} one wrong char =\nsame symptoms as firewall drop",
    f"Established {NE} traffic working {DASH}\nverify prefix counts and next-hop",
    "Never clear bgp * in production\nwithout a maintenance window",
    "Hold timer mismatch (Cisco 180s vs\nJuniper 90s) causes session flapping",
    f"Full BGP table {APPROX} 900K routes {DASH}\nverify RAM before accepting full table",
]
cols = [(right_x + 28, py + 48, 4), (right_x + right_w / 2 + 84, py + 48, 3)]
ri = 0
for x, y, count in cols:
    yy = y
    for _ in range(count):
        rule = rules[ri]
        draw.ellipse((x, yy + 2, x + 19, yy + 21), fill=PURPLE)
        draw.line((x + 5, yy + 12, x + 8, yy + 16, x + 15, yy + 7), fill=BG, width=3)
        for j, line in enumerate(rule.split("\n")):
            draw.text((x + 30, yy + j * 17), line, font=font("segoeui.ttf", 13), fill=WHITE)
        yy += 36 if "\n" in rule else 28
        ri += 1

# Footer.
fy = 992
draw.ellipse((44, fy + 5, 72, fy + 33), fill=WHITE)
draw.text((50, fy + 8), "GH", font=font("arialbd.ttf", 10), fill=BG)
draw.text((88, fy + 8), "github.com/titan101/job_aids/", font=F_FOOT, fill=WHITE)
draw.line((360, fy + 2, 360, fy + 36), fill=GRAY, width=1)
draw.rounded_rectangle((407, fy + 3, 433, fy + 29), radius=4, fill=(23, 130, 190))
draw.text((412, fy + 0), "in", font=font("arialbd.ttf", 20), fill=WHITE)
draw.text((446, fy + 8), "www.linkedin.com/in/varun-sinha-b778b019", font=F_FOOT, fill=WHITE)
draw.line((828, fy + 2, 828, fy + 36), fill=GRAY, width=1)
draw.text((882, fy + 3), "Created by Varun Sinha", font=F_SCRIPT, fill=TEAL)

img.save(OUT, "PNG", optimize=True)
print(OUT)
