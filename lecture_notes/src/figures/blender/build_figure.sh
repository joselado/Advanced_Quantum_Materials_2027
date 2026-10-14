#!/bin/sh
# Turn the final renders of a figure into the PDF that the notes include:
#   ./build_figure.sh <name>
# flattens out/<name>.png, or every out/<name>_<panel>.png of a multi-panel figure, onto white as
# .jpg, compiles ../overlays/<name>.tex (the TikZ overlay with the labels) and writes the
# compressed PDF to ../pdf/<name>.pdf.
set -e
cd "$(dirname "$0")"
python3 -c "
import glob, re
from PIL import Image
for f in glob.glob('out/$1.png') + glob.glob('out/$1_*.png'):
    if f.endswith('_still.png') or not re.fullmatch(r'out/$1(_[a-z0-9]+)?\.png', f):
        continue
    im = Image.open(f).convert('RGBA')
    a = im.getchannel('A').point(lambda v: max(0, v - 4) * 255 // 251)   # the catcher's faint haze
    im.putalpha(a); bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im); bg.convert('RGB').save(f[:-4] + '.jpg', quality=90)"
cd ../overlays
pdflatex -interaction=batchmode "$1.tex" > /dev/null || { tail -20 "$1.log"; exit 1; }
mkdir -p ../pdf
ps2pdf -dPDFSETTINGS=/printer "$1.pdf" "../pdf/$1.pdf"
rm -f "$1.aux" "$1.log" "$1.pdf"
ls -la "../pdf/$1.pdf"
