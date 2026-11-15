#!/usr/bin/env python3
"""Builds Inside the Machine (PDF).

Pipeline: assemble HTML -> render (pass 1, with invisible page markers) -> read which page each
marker landed on -> fill in contents page numbers and the index -> render again -> stamp running
footers and page numbers, add bookmarks and metadata.
Run: python3 build.py   (needs node + playwright, pypdf, reportlab, pdftotext)
"""
import glob, html, io, json, os, re, subprocess, sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs
from glossary import GLOSSARY

TITLE = "Inside the Machine"
SUBTITLE = "A plain-English guide to how AI works, from a single neuron to today's language models"
OUT = os.path.join(HERE, "Inside-the-Machine.pdf")
BUILD = os.path.join(HERE, "build")
os.makedirs(BUILD, exist_ok=True)

PARTS = {
    1: ("Foundations", "What AI is, what a neuron is, and how a pile of numbers can learn from its mistakes."),
    2: ("Kinds of networks", "The main families of neural networks, what each is good at, and the different ways they can be taught."),
    3: ("Language models", "How a machine turns text into numbers, pays attention, learns to write, and splits its brain into experts."),
    4: ("The machinery", "The chips, memory, number formats and software that all of this actually runs on."),
    5: ("Living with AI", "How AI is measured, where it goes wrong, and a map from here to building your own."),
}

# ---------------------------------------------------------------- chapters
def load_chapters():
    chs = []
    for f in sorted(glob.glob(os.path.join(HERE, "chapters", "*.html"))):
        src = open(f, encoding="utf8").read()
        m = re.match(r"\s*<!--(.*?)-->", src, re.S)
        meta = dict(kv.split(":", 1) for kv in [x.strip() for x in m.group(1).split("|")] if kv)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        chs.append({"part": int(meta["part"]), "num": int(meta["num"]), "title": meta["title"],
                    "lede": meta.get("lede", ""), "body": src[m.end():]})
    return chs

MK = 0
markers = {}   # marker id -> kind info
def marker(kind, **info):
    global MK
    MK += 1
    mid = f"{kind}{MK}"
    markers[mid] = info | {"kind": kind}
    return mid, f'<span class="mk">ZQ{mid}QZ</span>'

index_terms = []  # (term, anchor id, marker id)

def process_body(ch):
    body = ch["body"]
    n = ch["num"]
    fig_no = [0]
    def fig_sub(m):
        name, cap = m.group(1).strip(), m.group(2).strip()
        fig_no[0] += 1
        if not hasattr(figs, name):
            raise SystemExit(f"missing figure {name}")
        svg = getattr(figs, name)()
        return f'<figure>{svg}<figcaption><b>Figure {n}.{fig_no[0]}.</b> {cap}</figcaption></figure>'
    body = re.sub(r"\{\{fig:([^|}]+)\|(.*?)\}\}", fig_sub, body, flags=re.S)

    secs = []
    def h2_sub(m):
        title = m.group(1)
        mid, mk = marker("h", chapter=n, title=re.sub("<.*?>", "", title))
        secs.append(mid)
        return f'<h2 id="{mid}">{mk}{title}</h2>'
    body = re.sub(r"<h2>(.*?)</h2>", h2_sub, body, flags=re.S)

    def dfn_sub(m):
        attr, text = m.group(1) or "", m.group(2)
        term = re.search(r'data-idx="([^"]+)"', attr)
        term = term.group(1) if term else re.sub("<.*?>", "", text)
        mid, mk = marker("d", term=term)
        index_terms.append((term, mid))
        return f'<dfn id="{mid}">{mk}{text}</dfn>'
    body = re.sub(r"<dfn([^>]*)>(.*?)</dfn>", dfn_sub, body, flags=re.S)

    def ix_sub(m):
        term = m.group(1)
        mid, mk = marker("d", term=term)
        index_terms.append((term, mid))
        return f'<span id="{mid}">{mk}</span>'
    body = re.sub(r"<ix>(.*?)</ix>", ix_sub, body)
    return body, secs

def build_html(chs, pages=None):
    """pages: marker id -> display page number (None on the first pass)."""
    global MK, markers, index_terms
    MK, markers, index_terms = 0, {}, []
    pg = (lambda mid: str(pages.get(mid, "")) if pages else "00")

    parts_html, toc = [], []
    for p, (ptitle, pblurb) in PARTS.items():
        pmid, pmk = marker("p", part=p, title=ptitle)
        items = [c for c in chs if c["part"] == p]
        parts_html.append(f'''<section class="part-opener" id="{pmid}">{pmk}<div class="bar"></div>
          <div class="num">Part {["I","II","III","IV","V"][p-1]}</div><h1>{ptitle}</h1><p>{pblurb}</p></section>''')
        toc.append(f'<div class="part">Part {["I","II","III","IV","V"][p-1]} · {ptitle}</div>')
        for c in items:
            body, secs = process_body(c)
            cmid, cmk = marker("c", chapter=c["num"], title=c["title"])
            parts_html.append(f'''<section class="chapter" id="{cmid}">
              <div class="chapter-head">{cmk}<div class="num">{c["num"]:02d}</div><h1>{c["title"]}</h1>
              <p class="lede">{c["lede"]}</p><div class="rule"></div></div>{body}</section>''')
            toc.append(f'<a class="row ch" href="#{cmid}"><span class="t"><span class="n">{c["num"]}</span>{c["title"]}</span><span class="dots"></span><span class="p">{pg(cmid)}</span></a>')
            for s in secs:
                toc.append(f'<a class="row sec" href="#{s}"><span class="t">{markers[s]["title"]}</span><span class="dots"></span><span class="p">{pg(s)}</span></a>')

    # glossary
    gmid, gmk = marker("b", title="Glossary")
    gl, letter = [], None
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower().lstrip(".")):
        L = term.lstrip(".")[0].upper()
        L = "#" if not L.isalpha() else L
        if L != letter:
            gl.append(f'<div class="letter">{L}</div>'); letter = L
        gl.append(f"<dt>{term}</dt><dd>{d}</dd>")
    glossary = f'''<section class="backmatter glossary" id="{gmid}">{gmk}<h1>Glossary</h1>
      <p class="lede">Short definitions of every term in this book, in alphabetical order. The index that follows shows where each one is explained in full.</p>
      <dl>{"".join(gl)}</dl></section>'''

    # index (filled on second pass)
    imid, imk = marker("b", title="Index")
    entries = {}
    for term, mid in index_terms:
        entries.setdefault(term, []).append(mid)
    ix, letter = [], None
    for term in sorted(entries, key=lambda t: t.lower().lstrip(".")):
        L = term.lstrip(".")[0].upper()
        L = "#" if not L.isalpha() else L
        if L != letter:
            ix.append(f'<div class="letter">{L}</div>'); letter = L
        seen, links = set(), []
        for mid in entries[term]:
            p_ = pg(mid)
            if p_ in seen: continue
            seen.add(p_); links.append(f'<a class="pg" href="#{mid}">{p_}</a>')
        if pages:
            links.sort(key=lambda a: int(re.search(r">(\d+)<", a).group(1)))
        ix.append(f'<div class="entry">{term}, {", ".join(links)}</div>')
    index = f'''<section class="backmatter index" id="{imid}">{imk}<h1>Index</h1>
      <p class="lede">Page numbers point to where a term is explained. They are clickable in the PDF.</p>
      <div class="cols">{"".join(ix)}</div></section>'''
    toc.append(f'<div class="part">Reference</div>')
    toc.append(f'<a class="row back" href="#{gmid}"><span class="t">Glossary</span><span class="dots"></span><span class="p">{pg(gmid)}</span></a>')
    toc.append(f'<a class="row back" href="#{imid}"><span class="t">Index</span><span class="dots"></span><span class="p">{pg(imid)}</span></a>')

    front = open(os.path.join(HERE, "front.html"), encoding="utf8").read()
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{TITLE}</title>
<link rel="stylesheet" href="../style.css"></head><body>
<section class="cover">{figs.cover_art()}<div class="words"><div class="kicker">A plain-English field guide</div>
<h1>Inside the<br>Machine</h1><p class="subtitle">How AI works, from a single neuron to today's language models: the ideas, the words, and the hardware.</p>
<div class="byline">Written with Claude · 2026</div></div></section>
<section class="titlepage"><h1>{TITLE}</h1><p class="subtitle">{SUBTITLE}</p>
<p class="small">Written with Claude, November 2026.<br>Illustrations drawn for this book.<br>Moby-Dick quotations are from the public-domain text (1851).</p></section>
<section class="toc"><h1>Contents</h1>{"".join(toc)}</section>
{front}
{"".join(parts_html)}
{glossary}
{index}
</body></html>'''
    return doc

# ---------------------------------------------------------------- render + page lookup
def render(html_text, name):
    hp = os.path.join(BUILD, name + ".html")
    pp = os.path.join(BUILD, name + ".pdf")
    open(hp, "w", encoding="utf8").write(html_text)
    subprocess.run(["node", os.path.join(HERE, "render.js"), hp, pp], check=True)
    return pp

def find_markers(pdf):
    n = len(PdfReader(pdf).pages)
    found = {}
    for i in range(n):
        t = subprocess.run(["pdftotext", "-f", str(i+1), "-l", str(i+1), pdf, "-"], capture_output=True, text=True).stdout
        t = re.sub(r"\s+", "", t)
        for mid in re.findall(r"ZQ([a-z]\d+)QZ", t):
            found.setdefault(mid, i)
    return found, n

# ---------------------------------------------------------------- footers, outline
def find_font():
    # A built-in PDF font: nothing is embedded, so stamping 150 footers adds almost no size.
    return "Helvetica"

def stamp(pdf_in, found, body_start, chapter_pages, no_footer, chapter_open, out):
    font = find_font()
    r = PdfReader(pdf_in)
    w = PdfWriter()
    W, H = 6 * 72, 9 * 72
    for i, page in enumerate(r.pages):
        if i >= body_start and i not in no_footer:
            num = i - body_start + 1
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=(W, H))
            c.setFillColorRGB(0.36, 0.42, 0.47)
            y = 0.42 * 72
            if i in chapter_open:
                c.setFont(font, 8); c.drawCentredString(W/2, y, str(num))
            else:
                running = chapter_pages.get(i, TITLE)
                c.setFont(font, 8)
                if num % 2:   # right-hand page
                    c.drawRightString(W - 0.68*72, y, str(num))
                    c.setFont(font, 7); c.drawRightString(W - 0.68*72 - 22, y, running.upper())
                else:
                    c.drawString(0.68*72, y, str(num))
                    c.setFont(font, 7); c.drawString(0.68*72 + 22, y, TITLE.upper())
                c.setStrokeColorRGB(0.81, 0.85, 0.87); c.setLineWidth(0.5)
                c.line(0.68*72, y + 12, W - 0.68*72, y + 12)
            c.save(); buf.seek(0)
            page.merge_page(PdfReader(buf).pages[0])
        w.add_page(page)
        w.pages[-1].compress_content_streams()  # merging leaves content uncompressed
    # bookmarks
    w.add_outline_item("Cover", 0)
    w.add_outline_item("Contents", found_first(found, "toc", 2))
    for mid, info in sorted(markers.items(), key=lambda kv: found.get(kv[0], 0)):
        if mid not in found: continue
        if info["kind"] == "p":
            parent = w.add_outline_item(f'Part {["I","II","III","IV","V"][info["part"]-1]} · {info["title"]}', found[mid])
            stamp.parent = parent
        elif info["kind"] == "c":
            w.add_outline_item(f'{info["chapter"]}. {info["title"]}', found[mid], parent=getattr(stamp, "parent", None))
        elif info["kind"] == "b":
            w.add_outline_item(info["title"], found[mid])
    w.add_metadata({"/Title": TITLE, "/Subject": SUBTITLE, "/Author": "Written with Claude", "/Keywords": "AI, neural networks, language models, transformers, mixture of experts, GPU"})
    w.page_mode = "/UseOutlines"
    w.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    with open(out, "wb") as f:
        w.write(f)

def found_first(found, _k, default):
    return default

def main():
    chs = load_chapters()
    print(f"{len(chs)} chapters")
    p1 = render(build_html(chs), "pass1")
    found, n = find_markers(p1)
    missing = [m for m in markers if m not in found]
    if missing: print("warning: markers not found:", missing[:10], len(missing))
    first_part = min(found[m] for m, i in markers.items() if i["kind"] == "p" and m in found)
    pages = {m: found[m] - first_part + 1 for m in found}
    html2 = build_html(chs, pages)
    html2 = re.sub(r'<span class="mk">ZQ[a-z]\d+QZ</span>', "", html2)
    p2 = render(html2, "pass2")
    # the second pass re-reads markers from pass 1 positions; verify page count is unchanged before the index
    n2 = len(PdfReader(p2).pages)
    # running heads: which chapter each page belongs to
    starts = sorted((found[m], i) for m, i in markers.items() if m in found and i["kind"] in "pcb")
    chapter_pages, no_footer, chapter_open = {}, set(), set()
    for k, (pg0, info) in enumerate(starts):
        end = starts[k+1][0] if k + 1 < len(starts) else n2
        for q in range(pg0, end):
            chapter_pages[q] = info["title"]
        if info["kind"] == "p": no_footer.add(pg0)
        else: chapter_open.add(pg0)
    stamp(p2, found, first_part, chapter_pages, no_footer, chapter_open, OUT)
    print(f"pages: {n2}  ->  {OUT}")

if __name__ == "__main__":
    main()
