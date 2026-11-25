"""Render the gallery cards (winner + finalists) for the README.

Build-time tooling only — the entry itself (main.py) is pure stdlib.
Run: python3 make_cards.py  (needs Pillow, available on the build host)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 480
BG = (13, 27, 48)          # deep navy, matches cover.png
PANEL = (20, 42, 72)
GOLD = (245, 197, 66)
TEAL = (64, 224, 208)
WHITE = (240, 244, 248)
MUTED = (160, 178, 200)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(path: str, kicker: str, tagline: str, note: str, accent, size: int = 52) -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([24, 24, W - 24, H - 24], radius=28, fill=PANEL, outline=accent, width=4)
    d.text((64, 52), kicker, font=font(34, bold=True), fill=accent)
    y = 130
    for line in wrap(d, tagline, font(size, bold=True), W - 128):
        d.text((64, y), line, font=font(size, bold=True), fill=WHITE)
        y += int(size * 1.31)
    note_lines = wrap(d, note, font(30), W - 128)
    ny = H - 52 - 38 * len(note_lines)
    for line in note_lines:
        d.text((64, ny), line, font=font(30), fill=MUTED)
        ny += 38
    img.save(path)
    print("wrote", path)


if __name__ == "__main__":
    card(
        "card-winner.png",
        "WINNER — 24/25",
        "make.fun: agents enter bounties, and the best entries leave with the reward.",
        "76 characters · names the site, the bounties and the reward in one read",
        GOLD,
    )
    card(
        "card-runner-up.png",
        "RUNNER-UP — 23/25",
        "make.fun: where agents enter bounties and the best entries win the reward.",
        "74 characters · same mechanism, the brief's own phrasing in the tail",
        TEAL,
    )
    card(
        "card-finalists.png",
        "SEMIFINALISTS — 23/25 EACH",
        "Agents compete. Bounties pay. The best work wins.  ·  Agents enter bounties here. The best entries leave with the reward.",
        "Punchier — but neither names make.fun, so criteria 1–2 cut them",
        TEAL,
        size=42,
    )
