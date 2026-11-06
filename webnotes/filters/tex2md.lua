-- One-time conversion filter: the LaTeX of one session of the lecture notes to the pandoc tree
-- that is written as the web Markdown master. Metadata read:
--   chapter  the session number
--   eqmax    comma list, the number of numbered equations of sessions 1, 2, ...
--   secmax   comma list, the number of sections of sessions 1, 2, ...
-- What it does, all on the tree, never on text:
--   numbers sections (C.K, C.K.J), numbered equations (C.n, as \tag) and figures (C.m),
--   links the plain references "(2.8)", "Section 2.11" and \ref{fig:...} to anchors,
--   turns the notebookbox into a div with a title paragraph that links the notebook,
--   turns the aqmfigure into one image with its caption, pointing to the SVG of the figure.

local chapter = 0
local sec, subsec, eq, fig = 0, 0, 0, 0
local figures = {}
local eqmax, secmax = {}, {}
local REPO = 'https://github.com/joselado/Advanced_Quantum_Materials_2027'
local stats = { eqrefs = 0, secrefs = 0, secwords = 0 }

local function numlist(s)
  local t = {}
  for v in tostring(s):gmatch('%d+') do t[#t + 1] = tonumber(v) end
  return t
end

function Meta(m)
  chapter = tonumber(pandoc.utils.stringify(m.chapter or '0'))
  eqmax = numlist(pandoc.utils.stringify(m.eqmax or ''))
  secmax = numlist(pandoc.utils.stringify(m.secmax or ''))
end

local function number_figures(doc)
  for _, b in ipairs(doc.blocks) do
    if b.t == 'Figure' then
      fig = fig + 1
      figures[b.identifier] = string.format('%d.%d', chapter, fig)
    end
  end
end

function Header(h)
  if h.level == 2 then
    sec = sec + 1; subsec = 0
    h.identifier = 'sec-' .. chapter .. '-' .. sec
    h.attributes = pandoc.AttributeList({ { 'number', string.format('%d.%d', chapter, sec) } })
  elseif h.level == 3 then
    subsec = subsec + 1
    h.identifier = 'sec-' .. chapter .. '-' .. sec .. '-' .. subsec
    h.attributes = pandoc.AttributeList({ { 'number', string.format('%d.%d.%d', chapter, sec, subsec) } })
  elseif h.level == 1 then
    h.identifier = 'session-' .. chapter
  end
  return h
end

function Math(m)
  if m.mathtype ~= 'DisplayMath' then return nil end
  local body = m.text
  local numbered = body:match('^%s*\\begin{equation}')
  body = body:gsub('^%s*\\begin{equation%*?}', ''):gsub('\\end{equation%*?}%s*$', '')
  body = body:gsub('^%s+', ''):gsub('%s+$', '')
  if numbered then
    eq = eq + 1
    body = body .. string.format(' \\tag{%d.%d}', chapter, eq)
  end
  m.text = '\n' .. body .. '\n'
  return m
end

local function ref_anchor(label)
  return '#' .. label
end

function Link(l)
  if l.attributes['reference-type'] == 'ref' then
    local label = l.attributes['reference']
    local n = figures[label]
    if not n then
      -- a figure of another session: the number is in the label, s06f03 is the third of session 6
      local s, f = label:match('^fig:s(%d+):')
      io.stderr:write('cross-session or unresolved reference ' .. label .. '\n')
      n = '??'
    end
    return pandoc.Link({ pandoc.Str(n) }, ref_anchor(label))
  end
  return l
end

function Figure(f)
  local img
  local function find(blocks)
    for _, b in ipairs(blocks) do
      if (b.t == 'Para' or b.t == 'Plain') then
        for _, i in ipairs(b.content) do if i.t == 'Image' and not img then img = i end end
      elseif b.t == 'Div' then find(b.content) end
    end
  end
  find(f.content)
  if not img then io.stderr:write('figure without image: ' .. f.identifier .. '\n'); return nil end
  local name = img.src:match('figures/pdf/(.*)%.pdf$')
  img.src = 'figures/' .. (name or img.src) .. (name and '.svg' or '')
  local cap = pandoc.utils.blocks_to_inlines(f.caption.long)
  img.caption = cap
  img.attributes = pandoc.AttributeList({ { 'number', figures[f.identifier] or '??' } })
  img.identifier = f.identifier
  return pandoc.Para({ img })
end

function Div(d)
  if d.classes[1] ~= 'notebookbox' then return nil end
  local first = d.content[1]
  if first and first.t == 'Para' and first.content[1] and first.content[1].t == 'Span' then
    local title = first.content[1].content
    table.remove(first.content, 1)
    while first.content[1] and (first.content[1].t == 'SoftBreak' or first.content[1].t == 'Space') do
      table.remove(first.content, 1)
    end
    local t = { pandoc.Strong({ pandoc.Str('Notebook check-in:') }), pandoc.Space() }
    for _, i in ipairs(title) do
      if i.t == 'Code' and i.text:match('^session%d+%.ipynb$') then
        i = pandoc.Link({ i }, REPO .. '/blob/main/jupyter-notebooks/' .. i.text)
      end
      table.insert(t, i)
    end
    table.insert(d.content, 1, pandoc.Para(t))
  end
  return d
end

-- plain-text references: "(2.8)" to the equation, "Section 2.11" to the section
local function link_eqrefs(str)
  local s = str.text
  local out, pos = {}, 1
  while true do
    local a, b, c, n = s:find('%((%d+)%.(%d+)%)', pos)
    if not a then break end
    c, n = tonumber(c), tonumber(n)
    if eqmax[c] and n >= 1 and n <= eqmax[c] then
      if a > pos then out[#out + 1] = pandoc.Str(s:sub(pos, a - 1)) end
      out[#out + 1] = pandoc.Link({ pandoc.Str(s:sub(a, b)) }, string.format('#eq-%d-%d', c, n))
      stats.eqrefs = stats.eqrefs + 1
    else
      if a > pos then out[#out + 1] = pandoc.Str(s:sub(pos, a - 1)) end
      out[#out + 1] = pandoc.Str(s:sub(a, b))
      io.stderr:write('number in parentheses left as text: ' .. s:sub(a, b) .. '\n')
    end
    pos = b + 1
  end
  if pos == 1 then return nil end
  if pos <= #s then out[#out + 1] = pandoc.Str(s:sub(pos)) end
  return out
end

function Inlines(inl)
  local out, i, changed = {}, 1, false
  while i <= #inl do
    local x = inl[i]
    if x.t == 'Str' then
      local w = x.text
      if w:match('[Ss]ections?$') then stats.secwords = stats.secwords + 1 end
      local r = link_eqrefs(x)
      if r then
        for _, y in ipairs(r) do out[#out + 1] = y end
        changed = true
      else
        if w:match('[Ss]ections?$') then
          -- "Section 2.5", "Sections 2.4 and 2.5": link every number of the chain
          local j, did = i + 1, false
          out[#out + 1] = x
          while true do
            local sp, num = inl[j], inl[j + 1]
            if not (sp and (sp.t == 'Space' or sp.t == 'SoftBreak') and num and num.t == 'Str') then break end
            local c, k, rest = num.text:match('^(%d+)%.(%d+)(.*)$')
            c, k = tonumber(c), tonumber(k)
            if not (c and secmax[c] and k >= 1 and k <= secmax[c] and (rest == '' or rest:match('^[%.,;:%)]+$'))) then break end
            out[#out + 1] = sp
            out[#out + 1] = pandoc.Link({ pandoc.Str(string.format('%d.%d', c, k)) }, string.format('#sec-%d-%d', c, k))
            if rest ~= '' then out[#out + 1] = pandoc.Str(rest) end
            stats.secrefs = stats.secrefs + 1
            did = true
            j = j + 2
            -- a chain continues after "and" or "to"
            local a, b = inl[j], inl[j + 1]
            if rest == '' and a and a.t == 'Space' and b and b.t == 'Str' and (b.text == 'and' or b.text == 'to') and inl[j + 2] and inl[j + 2].t == 'Space' then
              out[#out + 1] = a; out[#out + 1] = b
              j = j + 2
            else
              break
            end
          end
          i = j - 1; changed = changed or did
          goto continue
        end
        out[#out + 1] = x
      end
    else
      out[#out + 1] = x
    end
    ::continue::
    i = i + 1
  end
  if changed then return out end
  return nil
end

local function report(doc)
  io.stderr:write(string.format('sections %d, numbered equations %d, figures %d, equation links %d, section links %d, the word Section %d times\n',
    sec, eq, fig, stats.eqrefs, stats.secrefs, stats.secwords))
end

return {
  { Meta = Meta },
  { Pandoc = function(doc) number_figures(doc); return nil end },
  { Header = Header, Math = Math, Figure = Figure, Div = Div },
  { Link = Link },
  { Inlines = Inlines },
  { Pandoc = function(doc) report(doc); return nil end },
}
