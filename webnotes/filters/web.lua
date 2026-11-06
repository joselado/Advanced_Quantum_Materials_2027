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
--   a figure with src figures/web/... is a web schematic, "Schematic N.", numbered by build.py (labels.numbers),
--   a figure without an id is the display again of a PDF figure, with a link to the first display, and with
--   the attribute panel="a" it is one panel of it (build.py writes figures/panel/NAME_a.svg).
-- Every problem is written to stderr as one line, and build.py turns the line into an error with the page.

local labels, built, numbers, figsrc = {}, {}, {}, {}
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
  end
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

function Figure(f)
  local img = find_img(f)
  if not img then return nil end
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
    local n = numbers[id]
    if not n then
      io.stderr:write('the schematic ' .. src .. ' has no usable id\n')
      n = '?'
    end
    if not explicit then io.stderr:write('the schematic ' .. id .. ' has no alt text, add alt="..." to the image\n') end
    cap = strong_prefix(cap, { pandoc.Str('Schematic ' .. n .. '.') })
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
    cap = strong_prefix(cap, { pandoc.Str('Figure ' .. number .. '.') })
  end
  f.caption.long = { pandoc.Plain(cap) }
  img.src = '../' .. src
  img.caption = { pandoc.Str(alt) }
  img.attributes = pandoc.AttributeList({ { 'loading', 'lazy' } })
  f.content = { pandoc.Plain({ img }) }
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
    local fb = {}
    for k = 2, #item do fb[#fb + 1] = item[k] end
    if #fb > 0 then nfb = nfb + 1 end
    fbs[i] = fb
    opts[i] = { pandoc.Plain(first and first.content or {}) }
  end
  if not correct then io.stderr:write(where .. ' has no correct option, mark one with [x]\n'); return nil end
  local perOption = nfb > 0
  if perOption and nfb < #items then
    io.stderr:write(where .. ' has feedback on ' .. nfb .. ' of ' .. #items .. ' options, it needs all or none\n')
  end
  if not perOption and #after == 0 then io.stderr:write(where .. ' has no explanation after the options\n') end
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
    return pandoc.Div(out, pandoc.Attr('', { 'quiz' }, { { 'data-correct', letter }, { 'data-fb', '1' } }))
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

function Div(d)
  if d.classes:includes('widget') then return Widget(d) end
  if d.classes:includes('quiz') then return Quiz(d) end
  if d.classes:includes('tryit') then return TryIt(d) end
  return nil
end

return {
  { Meta = Meta },
  { Math = Math, Link = Link, Header = Header, Figure = Figure, Div = Div },
}
