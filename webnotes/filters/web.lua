-- Build filter: one page of the web Markdown master to HTML. Metadata read:
--   labels  path of labels.json, written by the first pass of build.py:
--           {"built": [2], "anchors": {"eq-2-8": "session2/05-blochs-theorem.html", ...}}
--   page    the notes-relative path of the page that is built, "session2/05-blochs-theorem.html"
--   kind    "section" or "index"
-- What it does, all on the tree:
--   resolves every link "#anchor" to the page that holds the anchor, also in another session,
--   gives each numbered display equation (the \tag{C.n} written by the conversion) its anchor,
--   writes the number of sections and of figures from the attribute "number",
--   moves the headings one level up on a section page, and drops the chapter title on an index page.
-- The blocks added for the web, all described in webnotes/README.md:
--   "quiz"    a fenced div with a question, a list of options marked [x] or [ ], and an explanation. It becomes
--             a div with the options and a <details> with the answer, and notes.js makes the options buttons.
--   "tryit"   a fenced div with notebook="..." and optionally cell="...", with the links to GitHub, Colab, Binder.
--   "widget"  a fenced div with name="NAME" and the introduction of the widget. It becomes <div class="widget"
--             data-widget="NAME">, and notes.js adds the sliders and the plots from widgets/NAME.json.
--   "comesback" a fenced div with the pages and sessions where the concepts of the page return. It becomes a
--             box titled "Where this comes back", and it must hold at least one link.
--   "steps"   a fenced div with title="...", the steps of a derivation that the text tells in words. It becomes a
--             closed <details> with the summary "The steps" and the title.
--   "problem" a fenced div with a pen-and-paper problem. It holds exactly one nested div "solution", which becomes
--             a closed <details> with the summary "Solution".
--   "lab"     a fenced div with one material, one number with its unit and the probe. It becomes a box titled
--             "In the lab", and it must hold a link to the measurement.
--   "key"     a fenced div with the main result of the page. It becomes a box titled "To remember".
--   "recall"  a fenced div with eq="3.2", the equations of other pages that this page starts from. It becomes a
--             box titled "From before" that shows them again with their numbers.
-- A figure with script="NAME.py" gets a button that downloads webnotes/scripts/sessionNN/NAME.py, the pyqula
-- script that it is drawn from.
-- A quiz shows every numbered equation that it refers to, under the question or in the feedback that uses it,
-- and an option of a quiz can be one picture, a web schematic written as ![alt](figures/web/...svg).
-- Plain text "Session N" (N from 1 to 10, a built session) becomes a link to the index page of that session,
-- except inside a heading, a link, math or code, and on the index page of that session itself.
--   a figure with src figures/web/... is a web schematic, "Schematic N.", numbered by build.py (labels.numbers),
--   a figure without an id is the display again of a PDF figure, with a link to the first display, and with
--   the attribute panel="a" it is one panel of it (build.py writes figures/panel/NAME_a.svg).
-- Every problem is written to stderr as one line, and build.py turns the line into an error with the page.

local labels, built, numbers, figsrc = {}, {}, {}, {}
local equations = {}
local nsections = 0
local page, kind = '', 'section'

function Meta(m)
  page = pandoc.utils.stringify(m.page or '')
  kind = pandoc.utils.stringify(m.kind or 'section')
  local path = pandoc.utils.stringify(m.labels or '')
  local f = io.open(path, 'r')
  if f then
    local d = pandoc.json.decode(f:read('a'), false)
    f:close()
    for _, s in ipairs(d.built) do built[s] = true end
    labels = d.anchors
    numbers = d.numbers or {}
    figsrc = d.figsrc or {}
    equations = d.equations or {}
  end
end

-- A numbered equation shown again, in a quiz or in a recall box. It keeps its number, since the \tag stays in the
-- TeX, and it has no anchor, since the anchor belongs to the first display. The Math elements made here are not
-- visited by the handler Math, which has already run on the block that holds them.
local function eq_again(id)
  local tex = equations[id]
  if not tex then return nil end
  return pandoc.Div({ pandoc.Para({ pandoc.Math('DisplayMath', tex) }) }, pandoc.Attr('', { 'eq-again' }))
end

-- The anchors of the equations that some blocks refer to, in the order of the text, each one once. The handler
-- Link has already written the targets as "page.html#eq-3-4" or "#eq-3-4".
local function eq_refs(blocks, seen)
  local ids = {}
  pandoc.Blocks(blocks):walk({ Link = function(l)
    local id = l.target:match('#(eq%-[%w%-]+)$')
    if id and not seen[id] then seen[id] = true; ids[#ids + 1] = id end
  end })
  return ids
end

-- The equations that some blocks already display, by their \tag, so that they are not shown twice.
local function eq_shown(blocks, seen)
  pandoc.Blocks(blocks):walk({ Math = function(m)
    local tag = m.mathtype == 'DisplayMath' and m.text:match('\\tag{([^}]*)}')
    if tag then seen['eq-' .. tag:gsub('%.', '-')] = true end
  end })
end

local function session_of(id)
  local c = id:match('^eq%-(%d+)%-') or id:match('^sec%-(%d+)%-') or id:match('^session%-(%d+)$')
  if c then return tonumber(c) end
  local s = id:match('^fig:s(%d+):') or id:match('^sch:s(%d+):')
  if s then return tonumber(s) end
  return nil
end

local function dirname(p) return p:match('^(.*)/') or '' end

local function relative(from, to)
  if from == to then return '' end
  if dirname(from) == dirname(to) then return to:match('[^/]+$') end
  return '../' .. to
end

local function href_to(id)
  local target = labels[id]
  if not target then return nil end
  if target == page then return '#' .. id end
  return relative(page, target) .. '#' .. id
end

function Link(l)
  local id = l.target:match('^#(.+)$')
  if not id then return nil end
  local target = labels[id]
  if target then
    if #l.content == 0 and id:match('^sch:') and numbers[id] then
      l.content = { pandoc.Str('Schematic ' .. numbers[id]) }
    end
    l.target = relative(page, target) .. '#' .. id
    if target == page then l.target = '#' .. id end
    return l
  end
  local s = session_of(id)
  if s and not built[s] then
    -- the session is not converted yet, so the text stays and the link waits for it
    io.stderr:write('PENDING ' .. id .. '\n')
    return l.content
  end
  io.stderr:write('DANGLING ' .. id .. '\n')
  return nil
end

function Math(m)
  if m.mathtype ~= 'DisplayMath' then return nil end
  local tag = m.text:match('\\tag{([^}]*)}')
  if not tag then return nil end
  local id = 'eq-' .. tag:gsub('%.', '-')
  return pandoc.Span({ m }, pandoc.Attr(id, { 'eq' }))
end

function Header(h)
  if kind == 'index' and h.level == 1 then return {} end
  local number = h.attributes['number']
  h.attributes = pandoc.AttributeList({})
  if number and number ~= '' then
    table.insert(h.content, 1, pandoc.Space())
    table.insert(h.content, 1, pandoc.Span({ pandoc.Str(number) }, pandoc.Attr('', { 'num' })))
  end
  if kind == 'section' then
    if h.level == 2 and number and number ~= '' then
      nsections = nsections + 1
      -- a merged page: the sections after the first start with a rule
      if nsections > 1 then h.classes:insert('sec-next') end
    end
    h.level = h.level - 1
  end
  return h
end

local function first_sentence(inlines)
  local s = pandoc.utils.stringify(pandoc.Inlines(inlines))
  local cut = s:find('%.%s') or s:find('%.$')
  return cut and s:sub(1, cut) or s
end

local function find_img(f)
  for _, b in ipairs(f.content) do
    if b.t == 'Plain' or b.t == 'Para' then
      for _, i in ipairs(b.content) do if i.t == 'Image' then return i end end
    end
  end
end

local function strong_prefix(cap, inlines)
  table.insert(cap, 1, pandoc.Space())
  table.insert(cap, 1, pandoc.Strong(inlines))
  return cap
end

-- A figure inside a quiz, in the question or in the feedback of an option, is small, centred and has no number
-- of its own (class quiz-fig). The first stage of the filter marks them, since a Figure is visited before the
-- quiz Div that holds it.
function MarkQuizFigures(d)
  if not d.classes:includes('quiz') then return nil end
  return d:walk({ Figure = function(f) f.classes:insert('quiz-fig'); return f end })
end

-- A solution belongs to a problem. The first stage marks the solutions of a problem and writes their number on
-- it, since the solution Div is visited before the problem Div that holds it.
function MarkSolutions(d)
  if not d.classes:includes('problem') then return nil end
  local n = 0
  local out = d:walk({ Div = function(x)
    if x.classes:includes('solution') then n = n + 1; x.classes:insert('in-problem'); return x end
  end })
  out.attributes['nsol'] = tostring(n)
  return out
end

function MarkBlocks(d)
  return MarkQuizFigures(d) or MarkSolutions(d)
end

function Figure(f)
  local img = find_img(f)
  if not img then return nil end
  local inquiz = f.classes:includes('quiz-fig')
  local number = img.attributes['number'] or f.attributes['number'] or ''
  local cap = pandoc.utils.blocks_to_inlines(f.caption.long)
  local capstr = pandoc.utils.stringify(cap)
  local altstr = pandoc.utils.stringify(img.caption)
  local explicit = altstr ~= '' and altstr ~= capstr
  local alt = explicit and altstr or first_sentence(cap)
  local src = img.src
  local id = f.identifier
  local where = id ~= '' and id or src
  if src:match('^figures/web/') then
    -- a web schematic, with its own counter
    if not explicit then io.stderr:write('the schematic ' .. (inquiz and src or id) .. ' has no alt text, add alt="..." to the image\n') end
    if inquiz then
      -- in a quiz: no number, no id, the caption as written
      f.identifier = ''
    else
      local n = numbers[id]
      if not n then
        io.stderr:write('the schematic ' .. src .. ' has no usable id\n')
        n = '?'
      end
      cap = strong_prefix(cap, { pandoc.Str('Schematic ' .. n .. '.') })
    end
    f.classes:insert('schematic')
  elseif id == '' then
    -- a PDF figure shown again, here or in another session
    local name = src:match('^figures/([%w_]+)%.svg$')
    local orig = name and figsrc[name]
    if not orig then
      io.stderr:write('the figure ' .. src .. ' is shown again, but its first display is not known\n')
      return nil
    end
    local panel = img.attributes['panel']
    local href = href_to(orig) or ('#' .. orig)
    local what = panel and ', one panel shown again.' or ', shown again.'
    local label = pandoc.Link({ pandoc.Str('Figure ' .. (numbers[orig] or '?')) }, href)
    if #cap > 0 then
      cap = strong_prefix(cap, { label, pandoc.Str(what) })
    else
      cap = { pandoc.Strong({ label, pandoc.Str(what) }) }
    end
    if not explicit and capstr == '' then
      io.stderr:write('the figure ' .. src .. ' shown again has no alt text, add alt="..." to the image\n')
    end
    f.classes:insert('again')
    if panel then
      f.classes:insert('panel')
      src = 'figures/panel/' .. name .. '_' .. panel .. '.svg'
    end
  else
    if inquiz then io.stderr:write('the figure ' .. src .. ' is inside a quiz and has an id, a quiz can only show a figure again or a schematic without id\n') end
    cap = strong_prefix(cap, { pandoc.Str('Figure ' .. number .. '.') })
  end
  if #cap > 0 then f.caption.long = { pandoc.Plain(cap) } else f.caption.long = {} end
  -- script="NAME.py" names the pyqula script that the figure is drawn from, webnotes/scripts/sessionNN/NAME.py.
  -- build.py checks and copies it, and here the figure gets a button to download it, right under the plot.
  local script = img.attributes['script'] or f.attributes['script']
  f.attributes['script'] = nil
  img.src = '../' .. src
  img.caption = { pandoc.Str(alt) }
  img.attributes = pandoc.AttributeList({ { 'loading', 'lazy' } })
  f.content = { pandoc.Plain({ img }) }
  if script and script ~= '' then
    local sess = tonumber(page:match('^session(%d+)/') or '')
    if not sess then
      io.stderr:write('the figure ' .. where .. ' has a script, but the page is not a page of a session\n')
    else
      local href = string.format('../scripts/session%02d/%s', sess, script)
      local link = pandoc.Link({ pandoc.Str('Download the pyqula script') }, href, '',
                               pandoc.Attr('', { 'script-dl' }, { { 'download', script } }))
      f.content[#f.content + 1] = pandoc.Div({ pandoc.Plain({ link, pandoc.Space(),
        pandoc.Span({ pandoc.Code(script) }, pandoc.Attr('', { 'script-name' })) }) }, pandoc.Attr('', { 'script-row' }))
      f.classes:insert('has-script')
    end
  end
  return f
end

local LETTERS = 'ABCDEFGH'

function Quiz(d)
  local question, items, after = {}, nil, {}
  for _, b in ipairs(d.content) do
    if not items and b.t == 'BulletList' then items = b.content
    elseif not items then question[#question + 1] = b
    else after[#after + 1] = b end
  end
  local where = 'quiz "' .. pandoc.utils.stringify(question[1] or ''):sub(1, 40) .. '"'
  if not items then io.stderr:write(where .. ' has no list of options\n'); return nil end
  if #items < 3 or #items > 4 then io.stderr:write(where .. ' has ' .. #items .. ' options, it needs 3 (4 only in an old quiz)\n') end
  if #question == 0 then io.stderr:write(where .. ' has no question\n') end
  -- An option is its first block, with the mark [x] or [ ]. The blocks that follow, indented under it, are the
  -- feedback of that option: why it is correct, or a counterexample that shows why it is false.
  local correct, opts, fbs, nfb = nil, {}, {}, 0
  local npics = 0
  for i, item in ipairs(items) do
    local first = item[1]
    local mark = first and first.content and first.content[1]
    local m = mark and mark.t == 'Str' and mark.text
    if m ~= '\u{2612}' and m ~= '\u{2610}' then
      io.stderr:write(where .. ', option ' .. i .. ' is not marked with [x] or [ ]\n')
    else
      if m == '\u{2612}' then
        if correct then io.stderr:write(where .. ' has more than one correct option\n') end
        correct = i
      end
      table.remove(first.content, 1)
      if first.content[1] and first.content[1].t == 'Space' then table.remove(first.content, 1) end
    end
    -- An option that is one image and nothing else is a picture option. The image is a web schematic, it needs an
    -- alt text, and it gets the path of the page, as the handler Figure does for a figure.
    local only = first and first.content and #first.content == 1 and first.content[1]
    if only and only.t == 'Image' then
      npics = npics + 1
      if not only.src:match('^figures/web/') then
        io.stderr:write(where .. ', option ' .. i .. ' is a picture that is not a web schematic (figures/web/...)\n')
      end
      if pandoc.utils.stringify(only.caption) == '' then
        io.stderr:write(where .. ', option ' .. i .. ' is a picture with no alt text, write it as ![alt text](file)\n')
      end
      only.src = '../' .. only.src
      only.attributes = pandoc.AttributeList({ { 'loading', 'lazy' } })
    end
    local fb = {}
    for k = 2, #item do fb[#fb + 1] = item[k] end
    if #fb > 0 then nfb = nfb + 1 end
    fbs[i] = fb
    -- an option becomes a button in notes.js, so a "Session N" that the build linked stays plain text there
    local optinl = pandoc.Inlines(first and first.content or {}):walk({ Link = function(l)
      if l.target:match('^[%./]*session%d+/index%.html$') or l.target == 'index.html' then return l.content end
    end })
    opts[i] = { pandoc.Plain(optinl) }
  end
  if not correct then io.stderr:write(where .. ' has no correct option, mark one with [x]\n'); return nil end
  local perOption = nfb > 0
  if perOption and nfb < #items then
    io.stderr:write(where .. ' has feedback on ' .. nfb .. ' of ' .. #items .. ' options, it needs all or none\n')
  end
  if not perOption and #after == 0 then io.stderr:write(where .. ' has no explanation after the options\n') end
  if npics > 0 and npics < #items then
    io.stderr:write(where .. ' has ' .. npics .. ' picture options of ' .. #items .. ', it needs all or none\n')
  end
  -- A quiz is read alone, so an equation that it refers to by its number is shown inside it. The equations of the
  -- question and of the options go under the question. An equation that only the feedback of one option uses
  -- goes at the end of that feedback.
  local seen = {}
  eq_shown(question, seen)
  local qrefs = eq_refs(question, seen)
  for _, o in ipairs(opts) do
    for _, id in ipairs(eq_refs(o, seen)) do qrefs[#qrefs + 1] = id end
  end
  for _, id in ipairs(qrefs) do
    local e = eq_again(id)
    if e then question[#question + 1] = e end
  end
  for _, fb in ipairs(fbs) do
    local mine = {}
    for k, v in pairs(seen) do mine[k] = v end
    eq_shown(fb, mine)
    for _, id in ipairs(eq_refs(fb, mine)) do
      local e = eq_again(id)
      if e then fb[#fb + 1] = e end
    end
  end
  local qclasses = { 'quiz' }
  if npics > 0 then qclasses[#qclasses + 1] = 'quiz-pics' end
  local letter = LETTERS:sub(correct, correct)
  local out = {
    pandoc.Div({ pandoc.Plain({ pandoc.Str(perOption and 'Question' or 'Quick check') }) },
               pandoc.Attr('', { 'quiz-label' })),
    pandoc.Div(question, pandoc.Attr('', { 'quiz-q' })),
    pandoc.Div({ pandoc.OrderedList(opts, pandoc.ListAttributes(1, 'UpperAlpha', 'Period')) },
               pandoc.Attr('', { 'quiz-options' })),
  }
  if perOption then
    -- With no script this details lists every option with its verdict and its feedback. notes.js takes the
    -- feedback from here, puts it under its option, and keeps the details only for the general explanation.
    local rows = {}
    for i, fb in ipairs(fbs) do
      local ok = (i == correct)
      local row = { pandoc.Plain({ pandoc.Span({ pandoc.Str(LETTERS:sub(i, i) .. '. ' .. (ok and '\u{2713} True' or '\u{2717} False')) },
                                  pandoc.Attr('', { 'quiz-verdict' }, { { 'data-verdict', ok and 'true' or 'false' } })) }) }
      for _, b in ipairs(fb) do row[#row + 1] = b end
      rows[#rows + 1] = row
    end
    out[#out + 1] = pandoc.RawBlock('html', '<details class="quiz-answer"><summary>Show the answers</summary>')
    out[#out + 1] = pandoc.Div({ pandoc.BulletList(rows) }, pandoc.Attr('', { 'quiz-fbs' }))
    if #after > 0 then out[#out + 1] = pandoc.Div(after, pandoc.Attr('', { 'quiz-expl' })) end
    out[#out + 1] = pandoc.RawBlock('html', '</details>')
    return pandoc.Div(out, pandoc.Attr('', qclasses, { { 'data-correct', letter }, { 'data-fb', '1' } }))
  end
  out[#out + 1] = pandoc.RawBlock('html', '<details class="quiz-answer"><summary>Show the answer</summary>')
  out[#out + 1] = pandoc.Para({ pandoc.Str('The correct option is '), pandoc.Strong({ pandoc.Str(letter) }), pandoc.Str('.') })
  for _, b in ipairs(after) do out[#out + 1] = b end
  out[#out + 1] = pandoc.RawBlock('html', '</details>')
  return pandoc.Div(out, pandoc.Attr('', { 'quiz' }, { { 'data-correct', letter } }))
end

local GH = 'https://github.com/joselado/Advanced_Quantum_Materials_2027'

function TryIt(d)
  local nb = d.attributes['notebook']
  if not nb or nb == '' then io.stderr:write('a try-it box has no notebook="..."\n'); return nil end
  local cell = d.attributes['cell']
  local blocks = {}
  for i, b in ipairs(d.content) do blocks[i] = b end
  local lead = pandoc.Strong({ pandoc.Str('Try it.') })
  if blocks[1] and (blocks[1].t == 'Para' or blocks[1].t == 'Plain') then
    table.insert(blocks[1].content, 1, pandoc.Space())
    table.insert(blocks[1].content, 1, lead)
  else
    table.insert(blocks, 1, pandoc.Para({ lead }))
  end
  local enc = nb:gsub('[^%w%-_%.]', function(c) return string.format('%%%02X', c:byte()) end)
  local links = { pandoc.Str('Notebook '), pandoc.Code(nb) }
  if cell and cell ~= '' then
    links[#links + 1] = pandoc.Str(', cell ')
    links[#links + 1] = pandoc.Quoted('DoubleQuote', { pandoc.Str(cell) })
  end
  links[#links + 1] = pandoc.Str('. Open it in ')
  links[#links + 1] = pandoc.Link({ pandoc.Str('GitHub') }, GH .. '/blob/main/jupyter-notebooks/' .. enc)
  links[#links + 1] = pandoc.Str(', ')
  links[#links + 1] = pandoc.Link({ pandoc.Str('Colab') },
    'https://colab.research.google.com/github/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/' .. enc)
  links[#links + 1] = pandoc.Str(' or ')
  links[#links + 1] = pandoc.Link({ pandoc.Str('Binder') },
    'https://mybinder.org/v2/gh/joselado/Advanced_Quantum_Materials_2027/main?labpath=jupyter-notebooks%2F' .. enc)
  links[#links + 1] = pandoc.Str('.')
  blocks[#blocks + 1] = pandoc.Div({ pandoc.Plain(links) }, pandoc.Attr('', { 'tryit-links' }))
  return pandoc.Div(blocks, pandoc.Attr('', { 'tryit' }))
end

function Widget(d)
  local id = d.attributes['name'] or d.attributes['id'] or d.identifier
  if not id or id == '' then io.stderr:write('a widget block has no name="..."\n'); return nil end
  local out = {
    pandoc.Div({ pandoc.Plain({ pandoc.Str('Interactive') }) }, pandoc.Attr('', { 'widget-label' })),
  }
  for _, b in ipairs(d.content) do out[#out + 1] = b end
  out[#out + 1] = pandoc.RawBlock('html', '<noscript><p class="widget-nojs">This widget needs JavaScript.</p></noscript>')
  return pandoc.Div(out, pandoc.Attr('', { 'widget' }, { { 'data-widget', id } }))
end

function ComesBack(d)
  local nlinks = 0
  d:walk({ Link = function(l) nlinks = nlinks + 1 end })
  if nlinks == 0 then
    io.stderr:write('a comesback box has no link, it needs at least one link to a later page or session\n')
  end
  local out = {
    pandoc.Div({ pandoc.Plain({ pandoc.Str('Where this comes back') }) }, pandoc.Attr('', { 'comesback-label' })),
  }
  for _, b in ipairs(d.content) do out[#out + 1] = b end
  return pandoc.Div(out, pandoc.Attr('', { 'comesback' }))
end

-- A closed <details>, for the steps of a derivation and for the solution of a problem. It needs no script.
local function escape(t)
  return (t:gsub('&', '&amp;'):gsub('<', '&lt;'):gsub('>', '&gt;'))
end

local function fold(kind, label, title, content)
  local summary = '<summary><span class="fold-label">' .. label .. '</span>'
  if title and title ~= '' then summary = summary .. ' <span class="fold-title">' .. escape(title) .. '</span>' end
  return pandoc.Div({
    pandoc.RawBlock('html', '<details class="fold-details">' .. summary .. '</summary>'),
    pandoc.Div(content, pandoc.Attr('', { 'fold-body' })),
    pandoc.RawBlock('html', '</details>'),
  }, pandoc.Attr('', { 'fold', kind }))
end

function Steps(d)
  local title = d.attributes['title']
  if not title or title == '' then io.stderr:write('a steps box has no title="...", it says which equations it joins\n') end
  return fold('steps', 'The steps', title, d.content)
end

function Solution(d)
  if not d.classes:includes('in-problem') then
    io.stderr:write('a solution box is outside a problem box, it goes inside ::: problem\n')
  end
  return fold('solution', 'Solution', '', d.content)
end

function Problem(d)
  if d.attributes['nsol'] ~= '1' then
    io.stderr:write('a problem box has ' .. (d.attributes['nsol'] or '0') .. ' solution boxes, it needs exactly one\n')
  end
  local out = {
    pandoc.Div({ pandoc.Plain({ pandoc.Str('Problem') }) }, pandoc.Attr('', { 'problem-label' })),
  }
  for _, b in ipairs(d.content) do out[#out + 1] = b end
  return pandoc.Div(out, pandoc.Attr('', { 'problem' }))
end

-- The main result of a page, in a box that a reader who skims the page sees first.
function Key(d)
  local out = {
    pandoc.Div({ pandoc.Plain({ pandoc.Str('To remember') }) }, pandoc.Attr('', { 'keybox-label' })),
  }
  for _, b in ipairs(d.content) do out[#out + 1] = b end
  return pandoc.Div(out, pandoc.Attr('', { 'keybox' }))
end

-- Equations of another page that this page starts from, shown again with their numbers, so that the page can be
-- read without the pages before it. eq="3.2" or eq="3.2 3.3", and the text says in words what they are.
function Recall(d)
  local out = {
    pandoc.Div({ pandoc.Plain({ pandoc.Str('From before') }) }, pandoc.Attr('', { 'recall-label' })),
  }
  local n = 0
  for num in (d.attributes['eq'] or ''):gmatch('%S+') do
    local id = 'eq-' .. num:gsub('%.', '-')
    local e = eq_again(id)
    if not e then
      io.stderr:write('a recall box asks for the equation ' .. num .. ', which no page holds with a \\tag\n')
    else
      if labels[id] == page then
        io.stderr:write('a recall box shows the equation ' .. num .. ' of its own page, link it in the text instead\n')
      end
      out[#out + 1] = e
      n = n + 1
    end
  end
  if n == 0 then io.stderr:write('a recall box has no eq="...", it names the equations that it shows again\n') end
  if #d.content == 0 then io.stderr:write('a recall box has no text, it says in words what the equations are\n') end
  for _, b in ipairs(d.content) do out[#out + 1] = b end
  return pandoc.Div(out, pandoc.Attr('', { 'recall' }))
end

function Lab(d)
  local next = 0
  d:walk({ Link = function(l) if l.target:match('^https?:') then next = next + 1 end end })
  if next == 0 then
    io.stderr:write('a lab box has no link to the measurement, a number of a real material needs its source\n')
  end
  local out = {
    pandoc.Div({ pandoc.Plain({ pandoc.Str('In the lab') }) }, pandoc.Attr('', { 'lab-label' })),
  }
  for _, b in ipairs(d.content) do out[#out + 1] = b end
  return pandoc.Div(out, pandoc.Attr('', { 'lab' }))
end

-- "Session N" in plain text, as Str "Session", a Space or SoftBreak, and Str "N" with punctuation after it.
-- The pass is top-down, and a Header or a Link stops the descent, so their text is never linked. Math and Code
-- hold no Str, so they are never touched.
local function session_link(n, punct, prefix)
  if not n or n < 1 or n > 10 or not built[n] then return nil end
  local target = 'session' .. n .. '/index.html'
  if target == page then return nil end
  local out = {}
  if prefix ~= '' then out[#out + 1] = pandoc.Str(prefix) end
  out[#out + 1] = pandoc.Link({ pandoc.Str('Session ' .. n) }, relative(page, target))
  if punct ~= '' then out[#out + 1] = pandoc.Str(punct) end
  return out
end

local function autolink(inlines)
  local out, i, changed = {}, 1, false
  while i <= #inlines do
    local a, b, c = inlines[i], inlines[i + 1], inlines[i + 2]
    local repl = nil
    if a.t == 'Str' and b and (b.t == 'Space' or b.t == 'SoftBreak') and c and c.t == 'Str' then
      local prefix = a.text:match('^(%p*)Session$')
      local num, punct = c.text:match('^(%d%d?)(%p*)$')
      -- "Session 4.2" or "Session 4-5" is not a session reference
      if prefix and num and not punct:match('^[%.%-]%d') then
        repl = session_link(tonumber(num), punct, prefix)
      end
    end
    if repl then
      for _, x in ipairs(repl) do out[#out + 1] = x end
      i = i + 3
      changed = true
    else
      out[#out + 1] = a
      i = i + 1
    end
  end
  if changed then return pandoc.Inlines(out) end
  return nil
end

local SessionLinks = {
  traverse = 'topdown',
  Header = function(h) return h, false end,
  Link = function(l) return l, false end,
  Inlines = autolink,
}

function Div(d)
  if d.classes:includes('comesback') then return ComesBack(d) end
  if d.classes:includes('widget') then return Widget(d) end
  if d.classes:includes('quiz') then return Quiz(d) end
  if d.classes:includes('tryit') then return TryIt(d) end
  if d.classes:includes('steps') then return Steps(d) end
  if d.classes:includes('solution') then return Solution(d) end
  if d.classes:includes('problem') then return Problem(d) end
  if d.classes:includes('lab') then return Lab(d) end
  if d.classes:includes('key') then return Key(d) end
  if d.classes:includes('recall') then return Recall(d) end
  return nil
end

return {
  { Meta = Meta },
  { Div = MarkBlocks },
  SessionLinks,
  { Math = Math, Link = Link, Header = Header, Figure = Figure, Div = Div },
}
