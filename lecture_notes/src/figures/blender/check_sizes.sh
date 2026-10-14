#!/bin/sh
# Print the size on the page of every figure PDF and flag the ones above the size rule of the
# plan, an image higher than 7 cm or wider than the 15.6 cm text width (a label sticking out).
# The caption length is a rough count of printed lines of \small at the full text width.
cd "$(dirname "$0")/.."
for f in pdf/*.pdf; do
  n=$(basename "$f" .pdf)
  size=$(pdfinfo "$f" | awk '/Page size/ {printf "%.2f %.2f", $3/28.35, $5/28.35}')
  lines=$(python3 -c "
import re
s = open('$n.tex').read()
m = re.search(r'\\\\begin\{aqmfigure\}\{[^}]*\}\{(.*?)\}\s*\n\\\\includegraphics', s, re.S)
print(round(len(' '.join(m.group(1).split())) / 105 + 0.5) if m else '?')")
  echo "$n $size $lines" | awk '{flag = ($3 > 7.0 || $2 > 15.6) ? "  <-- too large" : "";
    printf "%-32s %5.2f x %5.2f cm   caption ~%s lines%s\n", $1, $2, $3, $4, flag}'
done
