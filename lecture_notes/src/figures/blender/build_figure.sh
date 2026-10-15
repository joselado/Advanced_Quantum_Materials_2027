#!/bin/sh
# Turn the final renders of a figure into the PDF that the notes include:
#   ./build_figure.sh <name>          from the final renders
#   ./build_figure.sh <name> still    a preview from the stills, to check the labels
# flattens out/<name>.png, or every out/<name>_<panel>.png of a multi-panel figure, onto white as
# .jpg, compiles ../overlays/<name>.tex (the TikZ overlay with the labels) and writes the
# compressed PDF to ../pdf/<name>.pdf. It also writes out/<name>_bbox.tex, the painted part of each image,
# which the overlay uses as its bounding box so that the empty margins of the render are cropped.
set -e
cd "$(dirname "$0")"
python3 -c "
import glob, re
from PIL import Image
still = '$2' == 'still'
for f in glob.glob('out/$1.png') + glob.glob('out/$1_*.png'):
    if still != f.endswith('_still.png') or not re.fullmatch(r'out/$1(_[a-z0-9]+)?(_still)?\.png', f):
        continue
    im = Image.open(f).convert('RGBA')
    f = f.replace('_still', '')
    a = im.getchannel('A').point(lambda v: max(0, v - 4) * 255 // 251)   # the catcher's faint haze
    im.putalpha(a); bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im); bg = bg.convert('RGB'); bg.save(f[:-4] + '.jpg', quality=90)
    # the painted part of the image, so that the overlay crops the empty margins of the render
    m = bg.point(lambda v: 255 if v < 247 else 0).convert('L').point(lambda v: 255 if v else 0)
    w, h = bg.size
    x0, y0, x1, y1 = m.crop((3, 3, w - 3, h - 3)).getbbox() or (0, 0, w - 6, h - 6)   # not the edge pixels
    x0, y0, x1, y1 = x0 + 3, y0 + 3, x1 + 3, y1 + 3
    open(f[:-4] + '_bbox.tex', 'w').write('%% written by build_figure.sh; the painted part of the image\\n'
        '\\\\path (%.4f\\\\figw,%.4f\\\\figw) rectangle (%.4f\\\\figw,%.4f\\\\figw);\\n'
        % (x0 / w, (h - y1) / w, x1 / w, (h - y0) / w))"
cd ../overlays
pdflatex -interaction=batchmode "$1.tex" > /dev/null || { tail -20 "$1.log"; exit 1; }
mkdir -p ../pdf
ps2pdf -dPDFSETTINGS=/printer "$1.pdf" "../pdf/$1.pdf"
rm -f "$1.aux" "$1.log" "$1.pdf"
ls -la "../pdf/$1.pdf"
