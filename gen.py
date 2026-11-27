"""Render entry.png for news-image-20261126, variant b68, layout V66.

Layout V66: masthead -> DATE CHECK (2 lines) -> LEFT 42%: tall map +
PIN INDEX + ALSO in 2 columns; RIGHT 58%: 3 hero bands stacked, then
2x5 cards -> timeline strip -> footer with tag legend.
All facts from KANON-20261126.md (26 Nov 2026 = Thursday).
"""
import math
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 30)
F_DATE = font("DejaVuSans-Bold.ttf", 13)
F_SEC = font("DejaVuSans-Bold.ttf", 12)
F_HERO_T = font("DejaVuSans-Bold.ttf", 15)
F_HERO_D = font("DejaVuSans.ttf", 11)
F_WHY_L = font("DejaVuSans-Bold.ttf", 9)
F_WHY = font("DejaVuSans.ttf", 10)
F_STAT = font("DejaVuSans-Bold.ttf", 10)
F_CARD_T = font("DejaVuSans-Bold.ttf", 11)
F_CARD_D = font("DejaVuSans.ttf", 10)
F_CARD_S = font("DejaVuSans-Bold.ttf", 9)
F_ALSO = font("DejaVuSans.ttf", 9)
F_PIN = font("DejaVuSans-Bold.ttf", 9)
F_PINI = font("DejaVuSans.ttf", 9)
F_DC = font("DejaVuSans.ttf", 10)
F_DC_L = font("DejaVuSans-Bold.ttf", 10)
F_TL = font("DejaVuSans.ttf", 10)
F_FOOT = font("DejaVuSans.ttf", 10)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 10)
F_TAG = font("DejaVuSans-Bold.ttf", 9)

PAPER = (247, 243, 232)
INK = (20, 20, 20)
MUTED = (90, 90, 90)
RED = (179, 38, 30)
BLUE = (29, 78, 137)
GREEN = (30, 122, 52)
CARD_BG = (255, 253, 245)
HERO_BG = (255, 255, 255)
OCEAN = (220, 233, 242)
LAND_C = (201, 214, 168)
LAND2_C = (185, 200, 150)
GOLD = (176, 141, 26)

STOP = set("""a an the and or of to in on for with by at from as is are was were be been
it its this that these those not no do does did will would can could should
have has had he she they we you i his her their our your my me him us them
over under after before between into through during about against among
within without upon per via etc""".split())


def tokens(text):
    words = re.findall(r"[a-z0-9]+(?:[.'\-][a-z0-9]+)?", text.lower())
    return {w for w in words if w not in STOP and len(w) > 1}


def wrap(text, fnt, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(drw, lines, x, y, fnt, fill, leading):
    for line in lines:
        drw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def measure_ok(text, fnt, maxw):
    return fnt.getlength(text) <= maxw


# ---------------------------------------------------------------- content
HEROES = [
    {
        "tag": "[C]", "label": "100TH",
        "title": "MACY'S 100TH PARADE DELAYED BY STORM",
        "deck": "First weather postponement ever; gusts to 60 mph. "
                "Rescheduled Sat 28 Nov, 08:30 ET.",
        "why": "America's biggest Thanksgiving parade moves for the first "
               "time over weather, as a major East Coast storm hits the "
               "holiday itself.",
        "stat": "100TH  \u00b7  60 MPH GUSTS",
    },
    {
        "tag": "[CL]", "label": "2M",
        "title": "IRGC CLAIMS 2 TANKERS HIT BY MINES",
        "deck": "Supertanker carrying over 2M barrels said ablaze off "
                "Khasab; claim unverified.",
        "why": "The claim widens the Iran war to the world's busiest oil "
               "chokepoint, and Brent crude climbed again.",
        "stat": "2M BARRELS  \u00b7  KHASAB",
    },
    {
        "tag": "[C]", "label": "+1.6%",
        "title": "TRUMP TARIFFS: MARKETS REBOUND",
        "deck": "Stocks rally as new levies seen milder than feared; "
                "STOXX +1.6%, MSCI +0.4%.",
        "why": "Investors judged the 14-partner salvo softer than feared, "
               "with no stacking on July tariffs.",
        "stat": "+1.6% STOXX  \u00b7  14 PARTNERS",
    },
]

CARDS = [
    ("[C]", "GAZA: ISRAEL KILLS HAMAS EDUCATION OFFICIAL",
     "Khaled Abu Nada and his wife killed in Deir al-Balah strike; "
     "9 dead overnight.", "9 KILLED OVERNIGHT"),
    ("[C]", "KYIV: MISSILES HIT MALL, 7 HURT",
     "Desnianskyi mall struck amid 113 drones; 7 hurt.",
     "7 HURT \u00b7 113 DRONES"),
    ("[C]", "BOGOR: FLOODED GOLD MINE KILLS 13",
     "Illegal mine floods 100 m underground; 13 dead, 13 missing "
     "after heavy rain.", "13 DEAD \u00b7 13 MISSING"),
    ("[C]", "NETANYAHU: JUDGE URGES BRIBERY CHARGE DROPPED",
     "Judge recommends prosecutors drop Case 4000, the sole bribery "
     "count.", "CASE 4000"),
    ("[C]", "NORTH KOREA: KIM TOURS NUCLEAR PLANT",
     "Kim Jong Un urges wider use of tactical nuclear weapons, state "
     "media says.", "TACTICAL ARMS PUSH"),
    ("[CL]", "SPACEX 'STARMIND': 1M SATELLITES OK'D NOV 25",
     "FCC approves up to 1M orbital data centres, a first for space "
     "computing.", "1M MODULES \u00b7 25 Nov"),
    ("[C]", "UK NET MIGRATION FALLS TO 77,000",
     "Lowest since 1997 outside the pandemic, ONS figures show.",
     "77,000 \u00b7 LOWEST SINCE 1997"),
    ("[C]", "RUSSIA APPROVES RECORD MILITARY BUDGET",
     "Post-Soviet record defence spending signed off in Moscow.",
     "RECORD POST-SOVIET"),
    ("[C]", "BANGKOK OIL DEPOT BLAST HURTS 7",
     "Explosion at Bangkok oil depot injures 7; fire out in about "
     "30 minutes.", "7 HURT \u00b7 FIRE OUT IN 30 MIN"),
    ("[C]", "GERMANY: 2 HELD OVER SYNAGOGUE PLOT",
     "Two Iraqi suspects arrested in Cologne and Heidelberg over "
     "March plot.", "2 ARRESTED \u00b7 COLOGNE"),
]

ALSO = [
    ("[C]", "Eisenkot seals first Israel coalition deal."),
    ("[C]", "Merz warns Russia's ambitions go beyond Ukraine."),
    ("[R]", "UK on alert over drone threat to air bases."),
    ("[C]", "Norse Atlantic suspends all flights, warns of bankruptcy."),
    ("[C]", "Poundland enters administration; 11,000 jobs at risk."),
    ("[C]", "Malaysia sues Google for $146M over harmful content."),
    ("[C]", "Kenya court halts US-backed Ebola facility."),
    ("[C]", "Belarus offers to fly Zelensky to Moscow for peace talks; "
            "he refuses."),
    ("[C]", 'Kushner calls Putin a "historic figure" and "grandmaster".'),
    ("[C]", "Estonia decides to close its border."),
    ("[C]", "Copernicus confirms longest stretch above 2\u00b0C warming."),
    ("[R]", "Nvidia halts AI server shipments to 4 countries."),
    ("[C]", "US Bitcoin funds hit record $4.94B."),
    ("[C]", "Savasleyka: Ukraine drones damage 5 jets \u2014 3 MiG-31 "
            "and 2 Su-34."),
    ("[C]", "UKMTO: blast near tanker 50 nautical miles west of Dubai; "
            "crew safe."),
    ("[CL]", "Saudi defences down 2 ballistic missiles bound for "
             "Riyadh. Nov 25"),
    ("[CL]", "Houthis claim strike on Ras Tanura refinery. 25 Nov"),
    ("[CL]", "Minor damage at Jazan port after drone attack. Nov 25"),
    ("[C]", "Philadelphia's oldest Thanksgiving march called off in bad "
            "weather."),
    ("[C]", "NYC Mayor Mamdani to miss rescheduled parade for foot "
            "surgery."),
    ("[C]", "NBC airs last year's march on Thursday; live march airs "
            "Saturday."),
    ("[C]", "Volker Turk warns of risk of atrocity crimes against "
            "Palestinians."),
    ("[C]", "Kharkiv: couple aged 37 and 38 killed in flat strike."),
    ("[C]", "Kryvyi Rih: 18 hurt in Russian strikes."),
    ("[C]", "Subkhankulovo pump station in Bashkortostan burns after "
            "drone hit."),
    ("[C]", "Gold $3,572 an ounce, down 0.2%."),
    ("[C]", "Dollar flat at 103.71."),
    ("[C]", "Nvidia closes down 3.91% at $149.30."),
    ("[C]", "S&P 500 futures up 0.5% as Wall Street shuts for "
            "Thanksgiving."),
    ("[C]", "OPEC+ meets 29 Nov on 2027 output."),
    ("[CL]", "Warning 223: unknown projectile 18 nautical miles east "
             "of Khasab. 25 Nov"),
    ("[C]", "Macy's balloons inflated Wednesday, then deflated again "
            "that night."),
    ("[C]", "High wind warning in force for New York City from 10:00 "
            "Thursday."),
    ("[C]", "Balloons grounded if sustained winds top 23 mph."),
    ("[C]", "Ceasefire a year old as overnight raids hit a third night."),
    ("[C]", "WTI crude $83.32, up 0.2%."),
    ("[C]", "Brent crude $93.8, up 0.9% on Thursday."),
]

DATE_CHECK = [
    "COP31 no-deal (22 Nov) \u00b7 Shenzhou-24 "
    "launch (25 Nov) \u00b7 Cairo ship blast, 31 dead (25 Nov)",
    "Cartagena hostages freed (25 Nov) \u00b7 "
    "Huawei guilty verdict (24 Nov) \u00b7 Australia\u2013Solomon pact "
    "(25 Nov)",
]

# name, lon, lat, index tag
PINS = [
    ("NEW YORK", -74.0, 40.7, "PARADE"),
    ("KHASAB", 56.2, 26.2, "TANKERS"),
    ("LONDON", -0.1, 51.5, "MIGRATION"),
    ("KYIV", 30.5, 50.45, "MISSILES"),
    ("BOGOR", 106.8, -6.6, "MINE FLOOD"),
    ("DEIR AL-BALAH", 34.45, 31.4, "AIRSTRIKE"),
    ("BANGKOK", 100.5, 13.75, "EXPLOSION"),
    ("KUALA LUMPUR", 101.7, 3.1, "LAWSUIT"),
    ("NAIROBI", 36.8, -1.3, "COURT"),
    ("PYONGYANG", 125.75, 39.03, "NUCLEAR"),
    ("JAZAN", 42.5, 16.9, "PORT"),
    ("OSLO", 10.75, 59.9, "AIRLINE"),
]

TIMELINE = [
    "10:00 \u2014 NYC wind warning in force",
    "08:30 ET Sat 28 Nov \u2014 Macy's parade restaged",
    "29 Nov \u2014 OPEC+ decides 2027 output",
    "FCC Starmind nod came 25 Nov",
]

LAND = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 55), (-55, 47), (-70, 42), (-75, 35), (-80, 26),
     (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -10), (-35, -20),
     (-45, -30), (-55, -35), (-65, -40), (-70, -50), (-73, -40),
     (-75, -30), (-80, -20), (-80, -10)],
    [(-18, 35), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
     (30, -30), (20, -35), (15, -30), (12, -18), (9, 0), (0, 5),
     (-10, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (45, 65),
     (40, 55), (35, 50), (30, 46), (28, 44), (23, 40), (20, 38),
     (15, 38), (10, 37), (5, 38), (0, 36)],
    [(40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
     (160, 70), (178, 66), (170, 60), (160, 55), (150, 45), (142, 40),
     (135, 35), (127, 33), (122, 30), (120, 25), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 8), (75, 8),
     (70, 20), (65, 25), (60, 25), (55, 26), (50, 29), (48, 30),
     (43, 35), (40, 40), (40, 50)],
    [(114, -22), (122, -14), (132, -12), (142, -11), (150, -22),
     (153, -27), (150, -37), (140, -38), (130, -32), (122, -34),
     (115, -33), (113, -26)],
]


# ---------------------------------------------------------------- drawing
def tag_color(tag):
    if tag == "[C]":
        return (30, 122, 52)
    if tag == "[R]":
        return (176, 141, 26)
    return RED


def draw_tag(drw, tag, x, y):
    w = int(F_TAG.getlength(tag)) + 8
    h = 14
    drw.rounded_rectangle([x, y, x + w, y + h], radius=3,
                          fill=tag_color(tag))
    drw.text((x + 4, y + 2), tag, font=F_TAG, fill=(255, 255, 255))
    return w


def art_balloon(drw, x0, y0, x1, y1):
    drw.rectangle([x0, y0, x1, y1], fill=(183, 211, 235))
    for i, bx in enumerate(range(x0, x1, 26)):
        drw.rectangle([bx, y1 - 34, bx + 20, y1], fill=(120, 120, 120)
                      if i % 2 else (90, 90, 90))
    drw.rectangle([x0, y1 - 34, x1, y1 - 30], fill=(60, 60, 60))
    cx, cy = (x0 + x1) // 2, y0 + 52
    drw.ellipse([cx - 52, cy - 38, cx + 52, cy + 38], fill=RED)
    drw.ellipse([cx - 52, cy - 38, cx + 52, cy + 38], outline=(120, 20, 16))
    drw.ellipse([cx - 18, cy - 38, cx + 18, cy + 38], fill=(255, 255, 255))
    drw.line([cx - 40, cy + 36, cx - 26, y1 - 34], fill=(60, 60, 60))
    drw.line([cx + 40, cy + 36, cx + 26, y1 - 34], fill=(60, 60, 60))
    drw.rectangle([cx - 16, y1 - 46, cx + 16, y1 - 34], fill=(120, 90, 40))


def art_tanker(drw, x0, y0, x1, y1):
    drw.rectangle([x0, y0, x1, y1], fill=(196, 222, 235))
    drw.rectangle([x0, y0 + 78, x1, y1], fill=(43, 108, 150))
    drw.polygon([(x0 + 12, y0 + 92), (x1 - 12, y0 + 92), (x1 - 34, y0 + 122),
                 (x0 + 34, y0 + 122)], fill=(40, 40, 40))
    drw.rectangle([x0 + 96, y0 + 58, x0 + 128, y0 + 92], fill=(230, 230, 230))
    drw.rectangle([x0 + 100, y0 + 46, x0 + 112, y0 + 58], fill=(200, 60, 40))
    for sx in (x0 + 34, x0 + 58, x1 - 62, x1 - 38):
        drw.ellipse([sx, y0 + 96, sx + 16, y0 + 112], fill=(255, 170, 40))
    for i in range(3):
        drw.ellipse([x0 + 108 + i * 8, y0 + 18 + i * 6,
                     x0 + 128 + i * 8, y0 + 36 + i * 6], fill=(120, 120, 120))
    drw.ellipse([x1 - 30, y0 + 14, x1 - 14, y0 + 30], fill=(20, 20, 20))
    for dx, dy in ((-6, 0), (6, 0), (0, -6), (0, 6)):
        drw.line([x1 - 22 + dx, y0 + 22 + dy, x1 - 22 - dx * 2,
                  y0 + 22 - dy * 2], fill=(20, 20, 20))


def art_chart(drw, x0, y0, x1, y1):
    drw.rectangle([x0, y0, x1, y1], fill=(238, 244, 238))
    for i, bh in enumerate((34, 22, 48, 30, 58, 44, 72)):
        bx = x0 + 14 + i * 20
        drw.rectangle([bx, y1 - 22 - bh, bx + 13, y1 - 22],
                      fill=(120, 160, 200) if i % 2 else (29, 78, 137))
    pts = [(x0 + 12, y1 - 60), (x0 + 44, y1 - 84), (x0 + 76, y1 - 70),
           (x0 + 108, y1 - 96), (x0 + 140, y1 - 108)]
    drw.line(pts, fill=GREEN, width=4)
    for px, py in pts:
        drw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GREEN)
    drw.line([x0 + 8, y1 - 18, x1 - 8, y1 - 18], fill=(60, 60, 60))
    drw.line([x0 + 8, y0 + 10, x0 + 8, y1 - 18], fill=(60, 60, 60))


ARTS = [art_balloon, art_tanker, art_chart]
ART_LINE_COLORS = [(120, 20, 16), (30, 122, 52),
                   (29, 78, 137), (200, 60, 40)]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 58], fill=(20, 20, 20))
    d.text((14, 12), "THE WORLD IN ONE PAGE", font=F_TITLE, fill=(255, 255, 255))
    date_txt = "Thursday, 26 November 2026"
    dw = F_DATE.getlength(date_txt)
    d.text((W - 14 - dw, 14), date_txt, font=F_DATE, fill=(255, 255, 255))
    badge = "50 STORIES"
    bw = F_DATE.getlength(badge) + 16
    d.rounded_rectangle([W - 14 - bw, 34, W - 14, 52], radius=4, fill=RED)
    d.text((W - 14 - bw + 8, 37), badge, font=F_DATE, fill=(255, 255, 255))
    d.text((14, 44), "ONE DAY \u00b7 ONE PAGE \u00b7 EVERY STORY THAT MATTERED",
           font=F_DC, fill=(200, 200, 200))
    # DATE CHECK
    d.rectangle([12, 64, W - 12, 106], fill=(255, 248, 220),
                outline=(176, 141, 26))
    d.text((20, 67), "DATE CHECK", font=F_DC_L, fill=RED)
    d.text((20, 82), "LEFT OUT:", font=F_DC_L, fill=RED)
    y = 67
    for line in DATE_CHECK:
        assert measure_ok(line, F_DC, 1000 - 130), "DATE CHECK too wide"
        d.text((118, y), line, font=F_DC, fill=INK)
        y += 15
    # geometry
    LX0, LX1 = 12, 432
    RX0, RX1 = 440, 1012
    MAIN_Y = 112
    # ---- left: map
    map_box = (LX0, MAIN_Y, LX1, 350)
    d.rectangle(map_box, fill=OCEAN, outline=INK)
    mx0, my0, mx1, my1 = LX0 + 4, 134, LX1 - 4, 346
    lon0, lon1, lat0, lat1 = -125.0, 140.0, 72.0, -50.0

    def proj(lon, lat):
        x = mx0 + (lon - lon0) / (lon1 - lon0) * (mx1 - mx0)
        yy = my0 + (lat0 - lat) / (lat0 - lat1) * (my1 - my0)
        return x, yy

    for poly in LAND:
        d.polygon([proj(lo, la) for lo, la in poly], fill=LAND_C)
    d.polygon([proj(lo, la) for lo, la in LAND[3]], fill=LAND2_C)
    d.polygon([proj(lo, la) for lo, la in LAND[4]], fill=LAND2_C)
    # header band AFTER land polygons
    d.rectangle([LX0, MAIN_Y, LX1, 132], fill=(20, 20, 20))
    d.text((LX0 + 8, MAIN_Y + 4), "WORLD MAP \u2014 12 STORIES PINNED",
           font=F_SEC, fill=(255, 255, 255))
    # pins
    dots = []
    for name, lon, lat, _tag in PINS:
        px, py = proj(lon, lat)
        dots.append((px, py))
    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            dist = math.hypot(dots[i][0] - dots[j][0], dots[i][1] - dots[j][1])
            assert dist >= 18, f"pins {i},{j} too close: {dist:.1f}"
    for px, py in dots:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255))
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    # pin labels: auto-place, never touching a dot
    label_boxes = []
    cands = [(12, -26), (12, 12), (-12, -26), (-12, 12), (12, -40),
             (-12, -40), (12, 26), (-12, 26), (30, -26), (-30, -26),
             (-48, -26), (-48, 12), (-30, -40), (12, -54), (-12, -54),
             (-48, -40), (-66, -26), (-66, 12), (30, 12), (-30, 26)]
    for (name, lon, lat, _tag), (px, py) in zip(PINS, dots):
        tw = int(F_PIN.getlength(name))
        placed = None
        for dx, dy in cands:
            if dx >= 0:
                bx0 = px + dx
            else:
                bx0 = px + dx - tw
            by0 = py + dy
            box = (bx0 - 3, by0 - 2, bx0 + tw + 3, by0 + 12)
            if box[0] < mx0 or box[2] > mx1 or box[1] < my0 or box[3] > my1:
                continue
            ok = True
            for qx, qy in dots:
                # distance from dot circle (r=8) to label box >= 9
                cx = min(max(qx, box[0]), box[2])
                cy = min(max(qy, box[1]), box[3])
                if math.hypot(qx - cx, qy - cy) < 8 + 9:
                    ok = False
                    break
                if box[0] <= qx <= box[2] and box[1] <= qy <= box[3]:
                    ok = False
                    break
            if not ok:
                continue
            for ob in label_boxes:
                if not (box[2] < ob[0] or box[0] > ob[2] or
                        box[3] < ob[1] or box[1] > ob[3]):
                    ok = False
                    break
            if ok:
                placed = box
                break
        assert placed is not None, f"no label spot for {name}"
        label_boxes.append(placed)
        d.rectangle(placed, fill=(255, 255, 255), outline=(20, 20, 20))
        d.text((placed[0] + 3, placed[1] + 2), name, font=F_PIN, fill=INK)
    # pin index
    py = 358
    d.text((LX0, py), "PIN INDEX", font=F_SEC, fill=INK)
    d.line([LX0, py + 16, LX1, py + 16], fill=INK, width=1)
    py += 22
    for i, (name, _lo, _la, tag) in enumerate(PINS):
        col = i % 2
        row = i // 2
        x = LX0 + col * 212
        yy = py + row * 15
        txt = f"{i + 1:>2}  {name} \u00b7 {tag}"
        assert measure_ok(txt, F_PINI, 206), f"pin index too wide: {txt}"
        d.text((x, yy), txt, font=F_PINI, fill=INK)
    # ---- left: ALSO, 2 columns
    ay = 464
    d.text((LX0, ay), "ALSO ON 26 NOV", font=F_SEC, fill=INK)
    d.line([LX0, ay + 16, LX1, ay + 16], fill=INK, width=1)
    ay += 22
    col_w = 204
    rows = (len(ALSO) + 1) // 2
    row_h = 21
    for idx, (tag, txt) in enumerate(ALSO):
        col = idx // rows
        row = idx % rows
        x = LX0 + col * 212
        yy = ay + row * row_h
        lines = wrap(txt, F_ALSO, col_w - 34)
        assert len(lines) <= 2, f"ALSO too long: {txt}"
        d.text((x, yy), tag, font=F_TAG, fill=tag_color(tag))
        draw_wrapped(d, lines, x + 34, yy, F_ALSO, INK, 10)
    # ---- right: heroes
    hy = MAIN_Y
    hero_label_boxes = []
    for hero, art in zip(HEROES, ARTS):
        d.rectangle([RX0, hy, RX1, hy + 148], fill=HERO_BG, outline=INK)
        ax0, ay0, ax1, ay1 = RX0 + 1, hy + 1, RX0 + 172, hy + 147
        art(d, ax0, ay0, ax1, ay1)
        # art label chip on top, fully inside art box
        lab = hero["label"]
        lw = int(F_STAT.getlength(lab)) + 12
        lh = 20
        lx, ly = ax0 + 6, ay0 + 6
        assert lx + lw <= ax1 - 2 and ly + lh <= ay1 - 2
        d.rectangle([lx, ly, lx + lw, ly + lh], fill=(20, 20, 20))
        d.text((lx + 6, ly + 3), lab, font=F_STAT, fill=(255, 255, 255))
        hero_label_boxes.append((lx, ly, lx + lw, ly + lh))
        tx = RX0 + 182
        tw = RX1 - tx - 8
        ty = hy + 6
        tw_tag = draw_tag(d, hero["tag"], tx, ty)
        title_lines = wrap(hero["title"], F_HERO_T, tw - tw_tag - 8)
        assert len(title_lines) <= 2, "hero title too long"
        draw_wrapped(d, title_lines, tx + tw_tag + 8, ty, F_HERO_T, INK, 17)
        ty += len(title_lines) * 17 + 3
        deck_lines = wrap(hero["deck"], F_HERO_D, tw)
        assert len(deck_lines) <= 2, "hero deck too long"
        ty = draw_wrapped(d, deck_lines, tx, ty, F_HERO_D, INK, 13)
        ty += 3
        d.text((tx, ty), "WHY IT MATTERS:", font=F_WHY_L, fill=RED)
        ty += 12
        why_lines = wrap(hero["why"], F_WHY, tw)
        assert len(why_lines) <= 2, "hero why too long"
        ty = draw_wrapped(d, why_lines, tx, ty, F_WHY, INK, 12)
        assert hy + 148 - (ty + 6) >= 18, "hero stat gap missing"
        sy = hy + 148 - 18
        assert sy - ty >= 6, "WHY-to-stat gap < 6px"
        d.line([tx, sy - 4, RX1 - 8, sy - 4], fill=(180, 180, 180))
        d.text((tx, sy), hero["stat"], font=F_STAT, fill=RED)
        hy += 151
    # ---- right: cards 2x5
    cy0 = 566
    cw = (RX1 - RX0 - 8) // 2
    ch = 64
    for i, (tag, title, deck, stat) in enumerate(CARDS):
        col = i % 2
        row = i // 2
        x0 = RX0 + col * (cw + 8)
        y0 = cy0 + row * (ch + 3)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD_BG, outline=(120, 120, 120))
        tx = x0 + 6
        tw = cw - 12
        ty = y0 + 4
        tw_tag = draw_tag(d, tag, tx, ty)
        t_lines = wrap(title, F_CARD_T, tw - tw_tag - 6)
        assert len(t_lines) <= 2, f"card title too long: {title}"
        draw_wrapped(d, t_lines, tx + tw_tag + 6, ty, F_CARD_T, INK, 12)
        ty += len(t_lines) * 12 + 2
        d_lines = wrap(deck, F_CARD_D, tw)
        assert len(d_lines) <= 2, f"card deck too long: {deck}"
        ty = draw_wrapped(d, d_lines, tx, ty, F_CARD_D, MUTED, 11)
        assert y0 + ch - (ty + 1) >= 11, "card stat overflow"
        d.text((tx, y0 + ch - 12), stat, font=F_CARD_S, fill=RED)
    # ---- timeline strip
    ty = 902
    d.rectangle([12, ty, W - 12, ty + 34], fill=(20, 20, 20))
    d.text((20, ty + 9), "TIMELINE", font=F_DC_L, fill=(255, 200, 60))
    tx = 20 + int(F_DC_L.getlength("TIMELINE")) + 16
    parts = "   \u00b7   ".join(TIMELINE)
    assert measure_ok(parts, F_TL, W - 12 - tx - 8), "timeline too wide"
    d.text((tx, ty + 9), parts, font=F_TL, fill=(255, 255, 255))
    # ---- footer
    fy = 944
    legend = ("[C] CONFIRMED  \u00b7  [R] REPORTED  \u00b7  [CL] CLAIM / "
              "25 NOV EVENT")
    assert measure_ok(legend, F_FOOT_B, 1000)
    d.text((12, fy), legend, font=F_FOOT_B, fill=INK)
    src = "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 CNN \u00b7 UKMTO \u00b7 ONS"
    d.text((12, fy + 18), src, font=F_FOOT, fill=MUTED)
    d.text((12, fy + 36),
           "THE WORLD IN ONE PAGE \u00b7 50 STORIES \u00b7 THURSDAY, "
           "26 NOVEMBER 2026", font=F_FOOT, fill=MUTED)
    return img, label_boxes, hero_label_boxes


# ---------------------------------------------------------------- checks
def check_content():
    assert len(HEROES) == 3 and len(CARDS) == 10 and len(ALSO) == 37
    total = len(HEROES) + len(CARDS) + len(ALSO)
    assert total == 50, f"story count {total} != 50"
    full = []
    for h in HEROES:
        for k in ("title", "deck", "why", "stat"):
            assert "third senior" not in h[k].lower()
            assert "3rd senior" not in h[k].lower()
        assert h["why"].endswith(".")
        assert "WHY IT MATTERS" not in h["why"]
        full.append(("hero", h["title"] + " " + h["deck"] + " " + h["why"]))
    for tag, title, deck, stat in CARDS:
        assert tag in ("[C]", "[R]", "[CL]")
        assert "bangchak" not in (title + deck).lower()
        assert "third senior" not in (title + deck).lower()
        assert "3rd senior" not in (title + deck).lower()
        full.append(("card", title + " " + deck + " " + stat))
    for tag, txt in ALSO:
        assert tag in ("[C]", "[R]", "[CL]"), txt
        if "25 Nov" in txt or "Nov 25" in txt:
            assert tag == "[CL]", f"25 Nov item not [CL]: {txt}"
        full.append(("also", txt))
    # Kyiv card pure Kyiv; Savasleyka only as ALSO
    kyiv = [c for c in CARDS if c[1].startswith("KYIV")][0]
    assert "Savasleyka" not in kyiv[1] + kyiv[2]
    assert "Desnianskyi" in kyiv[2] and "113" in kyiv[2]
    assert sum("Savasleyka" in t for _t, t in ALSO) == 1
    # Ras Tanura / Riyadh exactly once across all rendered story text
    blob = " ".join(t for _k, t in full)
    assert blob.count("Ras Tanura") == 1, blob.count("Ras Tanura")
    assert blob.count("Riyadh") == 1, blob.count("Riyadh")
    assert blob.count("Bangchak") == 0
    assert "significant figure" not in blob
    assert '"historic figure"' in blob and '"grandmaster"' in blob
    assert "13 dead" in blob and "13 missing" in blob
    # dup scan: >=3 shared distinctive words between any two items
    items = [(k, t) for k, t in full]
    for line in DATE_CHECK:
        items.append(("datecheck", line))
    for name, _lo, _la, tag in PINS:
        items.append(("pin", f"{name} {tag}"))
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            shared = tokens(items[i][1]) & tokens(items[j][1])
            assert len(shared) < 3, (
                f"dup {items[i][0]} vs {items[j][0]}: {sorted(shared)} :: "
                f"{items[i][1][:60]} || {items[j][1][:60]}")
    # hero stat numbers must not repeat in ALSO
    for h in HEROES:
        for num in re.findall(r"100TH|60 MPH|2M|\+1\.6%|14 PARTNERS",
                              h["stat"]):
            for _t, t in ALSO:
                assert num not in t, f"hero stat {num} repeated in ALSO"
    # 25 Nov events tagged [CL]
    for tag, txt in ALSO:
        if any(s in txt for s in ("Starmind", "Khasab", "Riyadh",
                                  "Ras Tanura", "Jazan")):
            assert tag == "[CL]", f"25 Nov event not [CL]: {txt}"
    return True


def check_pixels(img, label_boxes, hero_label_boxes):
    px = img.load()
    # 0 red pixels inside pin label boxes
    for box in label_boxes:
        for x in range(int(box[0]), int(box[2]) + 1):
            for y in range(int(box[1]), int(box[3]) + 1):
                r, g, b = px[x, y]
                assert not (r > 180 and g < 90 and b < 90), \
                    f"red pixel inside pin label {box} at {(x, y)}"
    # 0 art-line pixels inside hero label textboxes
    for box in hero_label_boxes:
        for x in range(int(box[0]), int(box[2]) + 1):
            for y in range(int(box[1]), int(box[3]) + 1):
                p = px[x, y]
                for lc in ART_LINE_COLORS:
                    if all(abs(a - b) <= 2 for a, b in zip(p, lc)):
                        raise AssertionError(
                            f"art line pixel inside hero label {box}")
    # map header band is solid dark (drawn after land)
    for x in range(20, 420, 40):
        assert px[x, 118] == (20, 20, 20), f"map header not solid at {x}"
    return True


def main():
    check_content()
    img, label_boxes, hero_label_boxes = render()
    check_pixels(img, label_boxes, hero_label_boxes)
    assert img.size == (1024, 1024)
    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    assert size <= 1048576, f"entry.png {size} > 1 MiB"
    print(f"OK entry.png {img.size[0]}x{img.size[1]} {size} bytes")
    print("stories: 3 heroes + 10 cards + 37 ALSO = 50")


if __name__ == "__main__":
    main()
