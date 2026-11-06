#!/usr/bin/env python3
"""List what changed in lecture_notes/src since the Markdown pages were last synced.

webnotes/SYNC holds one line per session, "sessionNN <commit>". For each session this
script compares sessions/sessionNN.tex and the figure files sNNf*.* between that commit and
HEAD, paragraph by paragraph, and prints the changed paragraphs and equations. For each one
it guesses the Markdown page that holds the matching text (the old text for a change, the
preceding paragraph for an addition), by searching distinctive pieces of it in the pages.

    python3 webnotes/texdiff.py                 all sessions with changes
    python3 webnotes/texdiff.py -s 3 -s 5       only these sessions
    python3 webnotes/texdiff.py --stat          one line per session
    python3 webnotes/texdiff.py --mark-synced -s 3    set the SYNC line of session 3 to HEAD
    python3 webnotes/texdiff.py --mark-synced --all   the same for every session
    python3 webnotes/texdiff.py --rev <rev>     compare with <rev> instead of HEAD

Nothing is changed except by --mark-synced, and that touches only webnotes/SYNC.
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
SRC = "lecture_notes/src"
SYNC = HERE / "SYNC"
PAGES = HERE / "pages"
MANIFEST = HERE / "manifest"
EQ = re.compile(r"\\begin\{(equation|align|eqnarray|gather|multline)\*?\}|\$\$|\\\[")


def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit("git %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def read_sync():
    out = {}
    if SYNC.exists():
        for line in SYNC.read_text().splitlines():
            p = line.split()
            if len(p) >= 2 and p[0].startswith("session"):
                out[int(p[0][7:])] = p[1]
    return out


def show(commit, path):
    r = subprocess.run(["git", "-C", str(ROOT), "show", "%s:%s" % (commit, path)],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def blocks(text):
    """Paragraphs separated by blank lines, as (first line number, text)."""
    out, cur, start = [], [], 1
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip() == "":
            if cur:
                out.append((start, "\n".join(cur)))
                cur = []
        else:
            if not cur:
                start = i
            cur.append(line)
    if cur:
        out.append((start, "\n".join(cur)))
    return out


def canon(b):
    """Comparison key: no comments, no whitespace differences."""
    b = re.sub(r"(?m)(?<!\\)%.*$", "", b)
    return re.sub(r"\s+", " ", b).strip()


def alnum(s):
    """Text reduced to lowercase letters and digits, without commands, refs and labels."""
    s = re.sub(r"(?m)(?<!\\)%.*$", "", s)
    s = re.sub(r"\\(label|ref|eqref|cite|input|includegraphics|vspace|hspace)\*?(\[[^\]]*\])?\{[^}]*\}", "", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", "", s)
    s = re.sub(r"\{\.[^}]*\}|\{#[^}]*\}|\{[a-z]+=[^}]*\}", "", s)   # pandoc attributes
    return re.sub(r"[^a-z0-9]", "", s.lower())


class Pages:
    def __init__(self, n):
        self.items = []  # (key, label, alnum text, session)
        for s in sorted(PAGES.glob("session*/")):
            m = MANIFEST / (s.name + ".json")
            num = {}
            if m.exists():
                for p in json.loads(m.read_text())["pages"]:
                    num[p["file"]] = p.get("number") or ""
            sn = int(s.name[7:])
            for f in sorted(s.glob("*.md")):
                label = "%s/%s" % (s.name, f.name)
                if num.get(f.name):
                    label += " (section %s)" % num[f.name]
                self.items.append((sn, label, alnum(f.read_text())))
        self.n = n

    def find(self, text, width=36, samples=6):
        a = alnum(text)
        if len(a) < width:
            return None
        step = max(1, (len(a) - width) // samples)
        wins = [a[i:i + width] for i in range(0, len(a) - width + 1, step)][:samples + 1]
        best = []
        for scope in (lambda sn: sn == self.n, lambda sn: True):
            best = sorted(((sum(w in t for w in wins), lab) for sn, lab, t in self.items if scope(sn)),
                          reverse=True)
            if best and best[0][0] > 0:
                return "%s  [%d of %d pieces found]" % (best[0][1], best[0][0], len(wins))
        return None


def kind(b):
    if re.match(r"\s*\\(sub)*section", b):
        return "heading"
    if EQ.search(b):
        return "equation"
    if re.search(r"\\begin\{(tikzpicture|figure|axis)", b):
        return "figure code"
    if b.lstrip().startswith("\\caption"):
        return "caption"
    return "paragraph"


def clip(b, n=7, w=110):
    ls = b.splitlines()
    out = [l[:w] + ("..." if len(l) > w else "") for l in ls[:n]]
    if len(ls) > n:
        out.append("... (%d more lines)" % (len(ls) - n))
    return out


def diff_file(path, old_c, new_c, pages, report):
    old = blocks(show(old_c, path))
    new = blocks(show(new_c, path))
    ok, nk = [canon(t) for _, t in old], [canon(t) for _, t in new]
    sm = difflib.SequenceMatcher(None, ok, nk, autojunk=False)
    count = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        count += 1
        # Search with the old text, because the pages still hold it; for a pure
        # addition, use the paragraph before it.
        if i2 > i1:
            probe = "\n".join(t for _, t in old[i1:i2])
        elif i1 > 0:
            probe = old[i1 - 1][1]
        else:
            probe = ""
        hint = pages.find(probe) if probe else None
        what = {"replace": "changed", "delete": "removed", "insert": "added"}[tag]
        kinds = sorted({kind(t) for _, t in (old[i1:i2] + new[j1:j2])})
        line = new[j1][0] if j2 > j1 else (old[i1][0] if i2 > i1 else 0)
        report.append("  %s, %s, tex line %d (old lines %s)" % (
            what, "/".join(kinds), line, old[i1][0] if i2 > i1 else "-"))
        report.append("    page: %s" % (hint or "not found (new text, or reworded on the web)"))
        ol = [l for _, t in old[i1:i2] for l in t.splitlines() + [""]]
        nl = [l for _, t in new[j1:j2] for l in t.splitlines() + [""]]
        if tag == "replace":
            # only the lines that differ, with one line of context
            d = [l for l in difflib.unified_diff(ol, nl, n=1, lineterm="")][2:]
            d = [l for l in d if l.strip() not in ("", "+", "-")]
            report += ["    " + (l[:130] + "..." if len(l) > 130 else l) for l in d[:24]]
            if len(d) > 24:
                report.append("    ... (%d more lines)" % (len(d) - 24))
        else:
            sign = "-" if tag == "delete" else "+"
            report += ["    %s %s" % (sign, l) for l in clip("\n".join(ol if tag == "delete" else nl).strip())]
        report.append("")
    return count


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-s", "--session", type=int, action="append", help="session number, repeatable")
    ap.add_argument("--all", action="store_true", help="all sessions (needed with --mark-synced)")
    ap.add_argument("--rev", default="HEAD", help="compare with this revision (default HEAD)")
    ap.add_argument("--stat", action="store_true", help="one line per session")
    ap.add_argument("--mark-synced", action="store_true",
                    help="set the SYNC line of the chosen sessions to --rev")
    a = ap.parse_args()

    sync = read_sync()
    if a.mark_synced:
        sel = sorted(sync) if a.all else (a.session or [])
        if not sel:
            sys.exit("--mark-synced needs -s N or --all")
        short = git("rev-parse", "--short", a.rev).strip()
        for n in sel:
            if n not in sync:
                sys.exit("session %d is not in SYNC" % n)
            sync[n] = short
        SYNC.write_text("".join("session%02d %s\n" % (n, sync[n]) for n in sorted(sync)))
        print("SYNC: sessions %s now at %s" % (", ".join(map(str, sel)), short))
        return

    sessions = a.session or sorted(sync)
    new_c = git("rev-parse", a.rev).strip()
    for n in sessions:
        if n not in sync:
            sys.exit("session %d is not in SYNC" % n)
        old_c = sync[n]
        tex = "%s/sessions/session%02d.tex" % (SRC, n)
        changed = git("diff", "--name-only", old_c, new_c, "--", SRC).split()
        figs = [f for f in changed if re.match(r"s%02df" % n, Path(f).name) and "/figures/" in f]
        pages = Pages(n)
        report, total = [], 0
        for f in [tex] + [f for f in figs if f.endswith(".tex")]:
            sub = []
            c = diff_file(f, old_c, new_c, pages, sub)
            if c:
                report.append(" %s: %d change%s" % (f.replace(SRC + "/", ""), c, "" if c == 1 else "s"))
                report += sub
                total += c
        other = [f for f in figs if not f.endswith(".tex")]
        if other:
            report.append(" figure files changed (rebuilt by the build from the PDF): " +
                          ", ".join(f.replace(SRC + "/", "") for f in other))
        if a.stat:
            print("session%02d  since %s  %d changed blocks, %d other figure files" % (n, old_c, total, len(other)))
            continue
        if not report:
            if a.session:
                print("session%02d since %s: nothing changed\n" % (n, old_c))
            continue
        print("=== session%02d since %s ===" % (n, old_c))
        print("\n".join(report))


if __name__ == "__main__":
    main()
