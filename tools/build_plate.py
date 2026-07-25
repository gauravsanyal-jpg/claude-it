#!/usr/bin/env python3
"""Compose a plate image into the book's card format.

Deps: npm i @fontsource/playfair-display @fontsource/lora; pip install pillow
Render: chrome --headless --force-device-scale-factor=2 \\
         --window-size=1046,1760 --screenshot=out.png file://$PWD/card.html
then crop to 2092x3120.
"""
import base64, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "node_modules/@fontsource"

# --- palette, sampled from the artwork so card and art share one paper tone ---
CREAM = "#F9F7E9"
NAVY = "#1B2A47"
TERRA = "#BE5429"
RULE = "#CBBFA4"
INK = "#2F3A50"

# --- card geometry (logical px; rendered at 2x) ---
W, H = 1046, 1560
ART_TOP, ART_H, ART_W = 392, 990, 800

# crop the artwork's empty top (the card supplies its own headroom) and the
# lower edge that the fade will dissolve into the caption band
src = Image.open(HERE / "iqbal-art.png").convert("RGB")
crop_top = 250
crop_bot = crop_top + round(ART_H / (ART_W / src.width))
art = src.crop((0, crop_top, src.width, min(crop_bot, src.height)))
# upscale with Lanczos to 2x display size so the render stays crisp
art = art.resize((ART_W * 2, ART_H * 2), Image.LANCZOS)
art_path = HERE / "art_prepped.png"
art.save(art_path)


def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()


def face(family, file, weight, style):
    return f"""@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};
src:url(data:font/woff2;base64,{b64(file)}) format('woff2');}}"""


pf = FONTS / "playfair-display/files"
lo = FONTS / "lora/files"
faces = "\n".join([
    face("Playfair", pf / "playfair-display-latin-700-normal.woff2", 700, "normal"),
    face("Playfair", pf / "playfair-display-latin-400-normal.woff2", 400, "normal"),
    face("Lora", lo / "lora-latin-400-normal.woff2", 400, "normal"),
    face("Lora", lo / "lora-latin-400-italic.woff2", 400, "italic"),
    face("Lora", lo / "lora-latin-600-normal.woff2", 600, "normal"),
])

SPRIG = f"""<svg viewBox="0 0 120 34" width="120" height="34" fill="none"
 stroke="{RULE}" stroke-width="1.4" stroke-linecap="round">
<path d="M60 32V8"/>
<path d="M60 14c-7 0-11-3-12-8 5-1 10 2 12 8z"/><path d="M60 14c7 0 11-3 12-8-5-1-10 2-12 8z"/>
<path d="M60 23c-6 0-9-3-10-7 4-1 8 2 10 7z"/><path d="M60 23c6 0 9-3 10-7-4-1-8 2-10 7z"/>
<circle cx="60" cy="6" r="2.4" fill="{RULE}" stroke="none"/>
<path d="M6 30h34M80 30h34"/></svg>"""

LEAF = f"""<svg viewBox="0 0 160 14" width="160" height="14" fill="none"
 stroke="{RULE}" stroke-width="1.3" stroke-linecap="round">
<path d="M4 7h56M100 7h56"/>
<path d="M80 3c-5 0-8 1.7-9 4 4 1 7.5-.5 9-4z"/><path d="M80 3c5 0 8 1.7 9 4-4 1-7.5-.5-9-4z"/>
<path d="M80 3v8"/></svg>"""

html = f"""<meta charset="utf-8"><title>Iqbal Hameed — Scene Plate</title>
<style>
{faces}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;background:{CREAM};-webkit-font-smoothing:antialiased}}
.card{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{CREAM}}}
.frame{{position:absolute;z-index:3;inset:26px;border:1.5px solid {RULE};pointer-events:none}}
.label{{position:absolute;z-index:4;top:26px;left:50%;transform:translate(-50%,-50%);
  background:{CREAM};padding:0 26px;color:{TERRA};font:600 20px/1 Lora,serif;letter-spacing:.05em}}
.head{{position:absolute;z-index:2;top:74px;left:0;right:0;text-align:center}}
.name{{font:700 106px/1.05 Playfair,serif;color:{NAVY};letter-spacing:-.015em;margin-top:14px}}
.role{{font:400 31px/1.2 Lora,serif;color:{NAVY};margin-top:20px}}
.role .dot{{color:{TERRA};margin:0 12px}}
.tag{{font:italic 400 27px/1.3 Lora,serif;color:{INK};margin-top:22px}}
.divider{{margin-top:16px}}
.art{{position:absolute;z-index:1;top:{ART_TOP}px;left:50%;transform:translateX(-50%);
  width:{ART_W}px;height:{ART_H}px}}
.art img{{width:100%;height:100%;display:block}}
/* dissolve every edge of the plate into the paper */
.art::after{{content:"";position:absolute;inset:0;background:
  linear-gradient(to bottom,{CREAM} 0,rgba(249,247,233,0) 5%,rgba(249,247,233,0) 78%,{CREAM} 98%),
  linear-gradient(to right,{CREAM} 0,rgba(249,247,233,0) 7%,rgba(249,247,233,0) 93%,{CREAM} 100%)}}
.caption{{position:absolute;z-index:2;left:120px;right:120px;bottom:62px;text-align:center}}
.quote{{position:relative;font:italic 400 33px/1.35 Lora,serif;color:{NAVY}}}
.qm{{font:700 62px/0 Playfair,serif;color:{TERRA};vertical-align:-.28em}}
.qm.o{{margin-right:8px}} .qm.c{{margin-left:8px}}
.rule{{width:64px;height:1.5px;background:{TERRA};opacity:.55;margin:26px auto 0}}
.principle{{font:600 17px/1.5 Lora,serif;color:{TERRA};letter-spacing:.13em;
  text-transform:uppercase;margin-top:20px}}
</style>
<div class="card">
  <div class="frame"></div>
  <div class="label">Scene Plate</div>
  <div class="head">
    {SPRIG}
    <div class="name">Iqbal Hameed</div>
    <div class="role">The Tailor<span class="dot">&bull;</span>Hameed &amp; Sons</div>
    <div class="divider">{LEAF}</div>
    <div class="tag">The shop nobody thought to mention.</div>
  </div>
  <div class="art"><img src="data:image/png;base64,{b64(art_path)}"></div>
  <div class="caption">
    <div class="quote"><span class="qm o">&ldquo;</span>He just didn&rsquo;t
      think of me.<span class="qm c">&rdquo;</span></div>
    <div class="rule"></div>
    <div class="principle">Found but forgotten is the same as never found</div>
  </div>
</div>"""

out = HERE / "card.html"
out.write_text(html)
print("wrote", out, f"{len(html)/1e6:.1f}MB", "| art crop", crop_top, crop_bot)
