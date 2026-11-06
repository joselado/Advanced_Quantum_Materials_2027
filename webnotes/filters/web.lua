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
-- The blocks "quiz", "tryit" and "widget" are fenced divs that pass through as <div class="...">,
-- and notes.js is the place that turns them into the interactive blocks of the later phases.

local labels, built = {}, {}
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
  end
end

local function session_of(id)
  local c = id:match('^eq%-(%d+)%-') or id:match('^sec%-(%d+)%-') or id:match('^session%-(%d+)$')
  if c then return tonumber(c) end
  local s = id:match('^fig:s(%d+):')
  if s then return tonumber(s) end
  return nil
end

local function dirname(p) return p:match('^(.*)/') or '' end

local function relative(from, to)
  if from == to then return '' end
  if dirname(from) == dirname(to) then return to:match('[^/]+$') end
  return '../' .. to
end

function Link(l)
  local id = l.target:match('^#(.+)$')
  if not id then return nil end
  local target = labels[id]
  if target then
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
  if kind == 'section' then h.level = h.level - 1 end
  return h
end

local function first_sentence(inlines)
  local s = pandoc.utils.stringify(pandoc.Inlines(inlines))
  local cut = s:find('%.%s') or s:find('%.$')
  return cut and s:sub(1, cut) or s
end

function Figure(f)
  local img
  for _, b in ipairs(f.content) do
    if b.t == 'Plain' or b.t == 'Para' then
      for _, i in ipairs(b.content) do if i.t == 'Image' and not img then img = i end end
    end
  end
  if not img then return nil end
  local number = img.attributes['number'] or f.attributes['number'] or ''
  local cap = pandoc.utils.blocks_to_inlines(f.caption.long)
  local alt = first_sentence(cap)
  table.insert(cap, 1, pandoc.Space())
  table.insert(cap, 1, pandoc.Strong({ pandoc.Str('Figure ' .. number .. '.') }))
  f.caption.long = { pandoc.Plain(cap) }
  img.src = '../' .. img.src
  img.caption = { pandoc.Str(alt) }
  img.attributes = pandoc.AttributeList({ { 'loading', 'lazy' } })
  f.content = { pandoc.Plain({ img }) }
  return f
end

return {
  { Meta = Meta },
  { Math = Math, Link = Link, Header = Header, Figure = Figure },
}
