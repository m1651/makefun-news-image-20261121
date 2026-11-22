"""Draw the 21 November 2026 world-news image.

A single 1024x1024 PNG: a dark teal banner with the date, then six
panels in two columns and three rows. Each panel has a small hand-drawn
pictogram on a coloured disc, a headline and two short factual lines.
Run:  python3 draw_entry.py   (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BANNER_H = 150
PANEL_W, PANEL_H = 492, 256
GAP = 12
MARGIN = 16

TEAL = (13, 71, 80)
TEAL_DARK = (8, 48, 55)
PAPER = (244, 241, 232)
INK = (24, 28, 32)
GREY = (84, 90, 96)
WHITE = (255, 255, 255)
ACCENTS = [(176, 58, 44), (30, 96, 145), (122, 62, 140),
           (196, 128, 20), (36, 122, 74), (16, 88, 110)]


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit `width` pixels."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_flame(d, cx, cy, r):
    d.polygon([(cx, cy - r), (cx + r * 0.75, cy + r * 0.4),
               (cx + r * 0.3, cy + r * 0.9), (cx - r * 0.3, cy + r * 0.9),
               (cx - r * 0.75, cy + r * 0.4)], fill=(255, 214, 90))
    d.ellipse([cx - r * 0.35, cy - r * 0.1, cx + r * 0.35, cy + r * 0.7],
              fill=(230, 90, 30))


def draw_ship(d, cx, cy, r):
    d.rectangle([cx - r, cy - r * 0.2, cx + r, cy + r * 0.25], fill=WHITE)
    d.polygon([(cx - r, cy + r * 0.25), (cx + r, cy + r * 0.25),
               (cx + r * 0.6, cy + r * 0.8), (cx - r * 0.6, cy + r * 0.8)],
              fill=(210, 210, 210))
    d.rectangle([cx - r * 0.1, cy - r, cx + r * 0.1, cy - r * 0.2], fill=WHITE)
    d.polygon([(cx + r * 0.1, cy - r), (cx + r * 0.7, cy - r * 0.4),
               (cx + r * 0.1, cy - r * 0.4)], fill=(255, 214, 90))


def draw_rocket(d, cx, cy, r):
    d.polygon([(cx, cy - r), (cx + r * 0.5, cy - r * 0.2),
               (cx + r * 0.35, cy + r * 0.7), (cx - r * 0.35, cy + r * 0.7),
               (cx - r * 0.5, cy - r * 0.2)], fill=WHITE)
    d.ellipse([cx - r * 0.22, cy - r * 0.75, cx + r * 0.22, cy - r * 0.3],
              fill=(255, 214, 90))
    d.polygon([(cx - r * 0.35, cy + r * 0.7), (cx, cy + r * 1.05),
               (cx + r * 0.35, cy + r * 0.7)], fill=(230, 90, 30))


def draw_coin(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 196, 60),
              outline=(150, 100, 0), width=3)
    d.text((cx, cy), "B", font=font(34), fill=(120, 70, 0), anchor="mm")


def draw_leaf(d, cx, cy, r):
    d.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], fill=(60, 160, 90))
    d.line([cx - r * 0.7, cy + r * 0.4, cx + r * 0.7, cy - r * 0.4],
           fill=(20, 90, 50), width=4)
    d.line([cx, cy, cx, cy + r * 0.9], fill=(110, 70, 20), width=4)


def draw_wave(d, cx, cy, r):
    for i, y in enumerate((cy - r * 0.4, cy + r * 0.1, cy + r * 0.6)):
        d.arc([cx - r, y - r * 0.35, cx + r, y + r * 0.35], 180, 360,
              fill=WHITE if i % 2 == 0 else (160, 210, 230), width=5)
    d.polygon([(cx - r * 0.5, cy - r), (cx + r * 0.5, cy - r),
               (cx, cy - r * 0.3)], fill=(255, 214, 90))


ICONS = [draw_flame, draw_ship, draw_rocket, draw_coin, draw_leaf, draw_wave]

STORIES = [
    ("BAHRAIN", "Iran strikes US bases in Bahrain",
     "Tehran says it hit two US positions; a civilian industrial site",
     "in Bahrain caught fire. No injuries; air defences intercepted more."),
    ("STRAIT OF HORMUZ", "Two tankers hit off Oman",
     "UK maritime agency: two tankers struck by projectiles near Khasab,",
     "an hour apart. No casualties reported on either vessel."),
    ("POLAND", "Russian missiles land in Poland",
     "Two missiles and a drone came down during NATO drills; Warsaw calls",
     "it a grave violation. A strike on Kryvyi Rih killed two people."),
    ("MARKETS", "Bitcoin crashes to $55k, then rebounds",
     "Bitcoin fell to $55,130, its lowest since September 2024, as $2.7bn",
     "of leveraged bets were wiped out, then climbed back toward $60,000."),
    ("CLIMATE", "COP31 talks spill into overtime",
     "The UN climate summit in Antalya ran past its deadline with no deal,",
     "deadlocked after a draft dropped all mention of fossil fuels."),
    ("NIGERIA", "Boat capsizes on way to a funeral",
     "At least 24 people died when a crowded boat sank in Bayelsa state;",
     "24 more were rescued and the search for others went on."),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Banner
    d.rectangle([0, 0, W, BANNER_H], fill=TEAL)
    d.rectangle([0, BANNER_H - 6, W, BANNER_H], fill=(255, 196, 60))
    d.text((MARGIN, 22), "Friday, 21 November 2026",
           font=font(44, True), fill=WHITE)
    d.text((MARGIN, 82), "Six stories that defined the day",
           font=font(28), fill=(200, 225, 225))
    d.text((W - MARGIN, 34), "WORLD NEWS", font=font(26, True),
           fill=(255, 196, 60), anchor="ra")
    d.text((W - MARGIN, 74), "One day, six stories", font=font(22),
           fill=(200, 225, 225), anchor="ra")

    for i, (tag, head, line1, line2) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = MARGIN + col * (PANEL_W + GAP)
        y = BANNER_H + GAP + row * (PANEL_H + GAP)
        accent = ACCENTS[i]
        d.rounded_rectangle([x, y, x + PANEL_W, y + PANEL_H], radius=14,
                            fill=WHITE, outline=accent, width=3)
        d.rectangle([x, y, x + PANEL_W, y + 8], fill=accent)
        # Pictogram disc
        cx, cy = x + 52, y + 78
        d.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], fill=accent)
        ICONS[i](d, cx, cy, 24)
        # Tag + headline
        tx = x + 104
        d.text((tx, y + 26), tag, font=font(19, True), fill=accent)
        for j, ln in enumerate(wrap(d, head, font(24, True), PANEL_W - 120)):
            d.text((tx, y + 54 + j * 30), ln, font=font(24, True), fill=INK)
        # Body lines
        body_y = y + 132
        for j, ln in enumerate(wrap(d, line1, font(19), PANEL_W - 32)):
            d.text((x + 16, body_y + j * 25), ln, font=font(19), fill=INK)
        body_y += len(wrap(d, line1, font(19), PANEL_W - 32)) * 25 + 2
        for j, ln in enumerate(wrap(d, line2, font(19), PANEL_W - 32)):
            d.text((x + 16, body_y + j * 25), ln, font=font(19), fill=GREY)

    # Footer, below the panels
    fy = H - 18
    d.text((W // 2, fy), "Events of 21 November 2026  •  Sources: Reuters, AP, AFP, UKMTO, NEMA",
           font=font(17), fill=GREY, anchor="mm")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
