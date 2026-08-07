#!/usr/bin/env python3
"""Ensambla el rediseño Maggiore del hub de Combe:
mock renderizado + fuentes reales + datos reales + explorador IEP V2 dark."""
import re, os, shutil, json

import os as _os
# Rutas relativas al repo: este archivo vive en tools/redesign/
RD = _os.path.dirname(_os.path.abspath(__file__))
REPO = _os.path.dirname(_os.path.dirname(RD))
HANDOFF = RD + "/design_handoff_combe_hub"  # opcional (no versionado)

body = open(RD + "/mock-body.html", encoding="utf-8").read()
css = open(RD + "/mock-styles.css", encoding="utf-8").read()
realdata = open(RD + "/real-data.js", encoding="utf-8").read()
_sl = REPO + "/tools/sl-data/studies.json"
if os.path.exists(_sl):
    _studies = [st for st in json.load(open(_sl, encoding="utf-8")) if st.get("show", True)]
    _projects_js = "const projects = " + json.dumps([
        {"year": st["year"], "month": st.get("month",""), "category": st.get("category",""),
         "brand": st["brand"], "theme": st["theme"], "tools": st.get("tools",""),
         "summary": st.get("summary",""), "link": st.get("link",""), "file": st.get("file","")} for st in _studies
    ], ensure_ascii=False) + ";"
    _i = realdata.index("const projects")
    _j = realdata.index("[", _i)
    _d = 0
    for _k in range(_j, len(realdata)):
        if realdata[_k] == "[": _d += 1
        elif realdata[_k] == "]":
            _d -= 1
            if _d == 0: break
    realdata = realdata[:_i] + _projects_js + realdata[_k+1:].lstrip(";")
auditport = open(RD + "/audit-port.js", encoding="utf-8").read()
cur = open(REPO + "/combe/index.html", encoding="utf-8").read()

# ---------- 1. fuentes ----------
os.makedirs(REPO + "/combe/fonts", exist_ok=True)
os.makedirs(REPO + "/combe/assets", exist_ok=True)
picks = ["NeueHaasGroteskDisplay-350.ttf", "NeueHaasGroteskDisplay-400.ttf",
         "NeueHaasGroteskDisplay-500.ttf", "NeueHaasGroteskDisplay-700.ttf",
         "Switzer-100.ttf", "Switzer-100-italic.ttf"]
if os.path.isdir(HANDOFF + "/extracted-fonts"):
    for p in picks:
        shutil.copy(HANDOFF + "/extracted-fonts/" + p, REPO + "/combe/fonts/" + p)
    shutil.copy(HANDOFF + "/source/assets/logo-blanco.svg", REPO + "/combe/assets/logo-blanco.svg")

fonts_css = """
@font-face{font-family:"Neue Haas Grotesk Display";font-weight:350;font-style:normal;font-display:swap;src:url("/combe/fonts/NeueHaasGroteskDisplay-350.ttf") format("truetype")}
@font-face{font-family:"Neue Haas Grotesk Display";font-weight:400;font-style:normal;font-display:swap;src:url("/combe/fonts/NeueHaasGroteskDisplay-400.ttf") format("truetype")}
@font-face{font-family:"Neue Haas Grotesk Display";font-weight:500;font-style:normal;font-display:swap;src:url("/combe/fonts/NeueHaasGroteskDisplay-500.ttf") format("truetype")}
@font-face{font-family:"Neue Haas Grotesk Display";font-weight:700;font-style:normal;font-display:swap;src:url("/combe/fonts/NeueHaasGroteskDisplay-700.ttf") format("truetype")}
@font-face{font-family:"Switzer";font-weight:100 900;font-style:normal;font-display:swap;src:url("/combe/fonts/Switzer-100.ttf") format("truetype")}
@font-face{font-family:"Switzer";font-weight:100 900;font-style:italic;font-display:swap;src:url("/combe/fonts/Switzer-100-italic.ttf") format("truetype")}
@import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap");
"""

# ---------- 2. body: logo real ----------
body = re.sub(r'src="blob:[^"]+"', 'src="/combe/assets/logo-blanco.svg"', body)

# ---------- 3. explorador IEP V2 dark ----------
block = open(REPO + "/tools/iepv2-block2.html", encoding="utf-8").read()
m = re.search(r'var IEPV2_DATA = (\[.*?\]);\n', cur, re.S)
payload = m.group(1)
assert block.count("/*__IEPV2_DATA__*/[]") == 1
block = block.replace("/*__IEPV2_DATA__*/[]", payload)

dark_swaps = [
    ("#2C8C89", "#2cced6"), ("#1F7A77", "#00aab0"),
    ("rgba(66,184,180", "rgba(44,206,214"),
    ("#6B8AF2", "#a399ff"), ("#4a68c4", "#a399ff"),
    ("rgba(107,138,242", "rgba(163,153,255"),
    ("#4a5568", "#c9c9d0"), ("#1a2332", "#fcfcfc"), ("#e2e8f0", "#3a3a42"),
    ("rgba(232,115,74,0.12)", "rgba(237,198,36,0.14)"), ("#B85042", "#edc624"),
    ("rgba(13,26,43,0.72)", "rgba(0,0,0,0.72)"),
]
for a, b in dark_swaps:
    block = block.replace(a, b)

scope_vars = ("#iepv2x,.v2-modal,.v2-tip{--bg-card:var(--ink-base);--bg-main:#15151b;"
              "--bg-card-hover:var(--ink-raised);--bg-header:var(--ink-deep);--border:var(--ink-line);"
              "--text-primary:var(--fg);--text-secondary:var(--fg-2);--text-muted:var(--fg-3);"
              "--accent:var(--primary);--radius:6px;--shadow:none}\n"
              "#iepv2x .v2-headline,#iepv2x .v2-round-head h4,#iepv2x .v2-card h4,#iepv2x .v2-dhead{font-family:var(--font-display)}\n")
block = block.replace("<style>", "<style>\n" + scope_vars, 1)
# navegación: al abrir/cerrar ficha, quedarse en el explorador (no saltar al hero)
block = block.replace(
    'window.scrollTo({top:0,behavior:"smooth"});',
    'window.scrollTo(0, Math.min(window.scrollY, (document.getElementById("iep-v2-explorer")||{getBoundingClientRect:function(){return {top:0}}}).getBoundingClientRect().top + window.scrollY - 80));')
old_close = 'function v2Close(){\n  document.getElementById("iepV2Detail").classList.remove("open");\n  document.getElementById("iepV2Home").style.display="block";\n}'
if old_close in block:
    block = block.replace(old_close, old_close[:-1] + '  var _ex=document.getElementById("iep-v2-explorer"); if(_ex){window.scrollTo({top:_ex.getBoundingClientRect().top+window.scrollY-80,behavior:"smooth"});}\n}')

explorer = ('\n<section id="iep-v2-explorer" style="padding:0 80px 96px;">'
            '<div id="iepv2x" style="max-width:1280px;margin:0 auto;">'
            '<div id="iepV2Home"><div class="v2-stats" id="v2Stats"></div>'
            '<div class="v2-grid" id="iepV2Grid"></div></div>'
            '<div id="iepV2Detail" class="v2-detail"></div>'
            '</div></section>\n' + block + '\n')

# renombrar visible "IEP V2" -> "IEP" (los ids no cambian)
body = body.replace(">IEP V2<", ">IEP<")
body = body.replace(">IEP V2 <", ">IEP <")

# insertar después del </section> de la sección iep-v2 del mock
i = body.find('id="iep-v2"')
j = body.find("</section>", i) + len("</section>")
body = body[:j] + explorer + body[j:]

# ---------- 4. wiring runtime con datos reales ----------
wiring = """
<script>
""" + realdata + "\n" + auditport + """

function slBrand(p){return p.brand;}
document.addEventListener('DOMContentLoaded', function(){
  try{ wireSL(); }catch(e){ console.warn('wireSL', e); }
  try{ wireIEP(); }catch(e){ console.warn('wireIEP', e); }
  try{ wirePortfolio(); }catch(e){ console.warn('wirePortfolio', e); }
  try{ wireHero(); }catch(e){ console.warn('wireHero', e); }
  try{ wireAsk(); }catch(e){ console.warn('wireAsk', e); }
  try{ wireAudit(); }catch(e){ console.warn('wireAudit', e); }
  try{ wireJTBD(); }catch(e){ console.warn('wireJTBD', e); }
  try{ navActive(); }catch(e){ console.warn('navActive', e); }
});

function findCardGrid(section){
  var girds = Array.prototype.slice.call(section.querySelectorAll('div'));
  for (var k=0;k<girds.length;k++){
    var d = girds[k];
    if (d.querySelector(':scope > .scp2')) return d;
  }
  return null;
}

var _slState = {brand:null, year:null};
function wireSL(){
  var sec = document.getElementById('social-listening');
  var grid = findCardGrid(sec);
  var tpl = grid.querySelector('.scp2').cloneNode(true);
  // pills
  var pillGroups = [];
  Array.prototype.forEach.call(sec.querySelectorAll('span'), function(sp){
    if ((sp.getAttribute('style')||'').indexOf('cursor: pointer') >= 0) pillGroups.push(sp);
  });
  var brandPills = pillGroups.filter(function(p){ return ['All Brands','Astroglide','Just For Men','Vagisil'].indexOf(p.textContent.trim())>=0; });
  var yearPills = pillGroups.filter(function(p){ return /^(All Years|20\\d\\d)$/.test(p.textContent.trim()); });
  var ACTIVE = 'padding: 6px 14px; border-radius: 999px; font-size: 12px; font-weight: 600; background: var(--primary); color: var(--ink-deep); cursor: pointer;';
  var IDLE = 'padding: 6px 14px; border-radius: 999px; font-size: 12px; border: 1px solid var(--ink-line); color: var(--fg-2); cursor: pointer;';
  function setPills(group, val, prefix){
    group.forEach(function(p){
      var on = (val===null && p.textContent.indexOf('All')===0) || p.textContent.trim()===String(val);
      p.setAttribute('style', on ? ACTIVE : IDLE);
    });
  }
  function attach(group, key){
    group.forEach(function(p){
      p.addEventListener('click', function(){
        var t = p.textContent.trim();
        _slState[key] = (t.indexOf('All')===0) ? null : (key==='year'? parseInt(t,10): t);
        setPills(brandPills, _slState.brand); setPills(yearPills, _slState.year);
        render();
      });
    });
  }
  function render(){
    grid.innerHTML = '';
    projects.filter(function(p){
      return (_slState.brand===null || p.brand===_slState.brand) &&
             (_slState.year===null || p.year===_slState.year);
    }).forEach(function(p){
      var c = tpl.cloneNode(true);
      var head = c.children[0];
      head.children[0].textContent = p.brand;
      head.children[1].textContent = p.year + ' · ' + (p.month||'');
      c.children[1].textContent = p.theme;
      if (p.summary){
        var sm = document.createElement('div');
        sm.style.cssText = 'font-size:12.5px;color:var(--fg-3);line-height:1.55;font-weight:350;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;';
        sm.textContent = p.summary;
        c.insertBefore(sm, c.children[2]);
      }
      if (p.link){
        c.addEventListener('click', function(){ window.open(p.link, '_blank'); });
      } else {
        c.style.cursor = 'default';
        c.title = 'Deck disponible en la Clients Folder: ' + (p.file || '');
      }
      grid.appendChild(c);
    });
  }
  attach(brandPills, 'brand'); attach(yearPills, 'year');
  setPills(brandPills, null); setPills(yearPills, null);
  render();
}

function wireIEP(){
  var sec = document.getElementById('iep');
  var grid = findCardGrid(sec);
  if (!grid) return;
  var tpl = grid.querySelector('.scp2').cloneNode(true);
  grid.innerHTML = '';
  IEPV2_DATA.forEach(function(e, idx){
    var c = tpl.cloneNode(true);
    var mono = c.querySelector('.mono') || c.children[0];
    if (mono) mono.textContent = e.brand === 'Vagisil' ? 'VG-' + e.experiment_id : 'JFM-' + e.experiment_id;
    var titleEl = null;
    Array.prototype.forEach.call(c.querySelectorAll('span,div'), function(el){
      var st = el.getAttribute('style')||'';
      if (!titleEl && st.indexOf('font-family: var(--font-display)')>=0 && st.indexOf('font-size: 1')>=0) titleEl = el;
    });
    if (titleEl) titleEl.textContent = e.name;
    var pill = null, meta = null;
    Array.prototype.forEach.call(c.querySelectorAll('span'), function(el){
      var st = el.getAttribute('style')||'';
      if (!pill && st.indexOf('border-radius: 999px')>=0) pill = el;
    });
    if (pill) pill.textContent = e.brand;
    var small = Array.prototype.filter.call(c.querySelectorAll('span'), function(el){
      return (el.getAttribute('style')||'').indexOf('font-size: 12px')>=0;
    });
    if (small.length) small[small.length-1].textContent = e.rounds.length + ' round' + (e.rounds.length>1?'s':'') + (e.status==='in_progress' ? ' · LIVE' : '');
    c.addEventListener('click', function(){
      showTab('iep-v2');
      v2Open(idx);
    });
    grid.appendChild(c);
  });
}

function wirePortfolio(){
  var counts = {};
  projects.forEach(function(p){ counts[p.brand] = counts[p.brand]||{sl:0,iep:0}; counts[p.brand].sl++; });
  IEPV2_DATA.forEach(function(e){
    var b = e.brand==='Just For Men' ? 'Just For Men' : e.brand;
    counts[b] = counts[b]||{sl:0,iep:0}; counts[b].iep++;
  });
  var nums = document.querySelectorAll('span,div');
  Array.prototype.forEach.call(nums, function(el){
    var st = el.getAttribute('style')||'';
    if (st.indexOf('font-size: 36px')<0) return;
    var cell = el.closest('div');
    for (var up=0; up<4 && cell; up++){
      var txt = cell.textContent;
      var hit = Object.keys(counts).find(function(b){ return txt.indexOf(b)>=0; });
      if (hit){
        var label = (el.parentElement.textContent||'').toLowerCase();
        if (label.indexOf('iep')>=0) el.childNodes[0] && (el.childNodes[0].textContent = counts[hit].iep);
        else if (label.indexOf('listening')>=0 || label.indexOf('sl')>=0) el.childNodes[0] && (el.childNodes[0].textContent = counts[hit].sl);
        break;
      }
      cell = cell.parentElement;
    }
  });
}

function wireHero(){
  var kpis = document.querySelectorAll('#hub .kpi');
  if (kpis.length>=2){ kpis[0].textContent = projects.length; kpis[1].textContent = IEPV2_DATA.length; }
  Array.prototype.forEach.call(document.querySelectorAll('span,div'), function(el){
    if (el.children.length===0 && /Last updated/i.test(el.textContent)) el.textContent = 'Last updated: August 2026 · IEP live via Meta API';
  });
}

function wireAsk(){
  var sec = document.getElementById('ask');
  if (!sec) return;
  // el mock trae un span de placeholder: convertirlo en input real
  var ph = Array.prototype.find.call(sec.querySelectorAll('span'), function(el){
    var st = el.getAttribute('style')||'';
    return st.indexOf('flex: 1')>=0 && /\?$/.test(el.textContent.trim());
  });
  var input = sec.querySelector('input');
  if (!input && ph){
    input = document.createElement('input');
    input.type = 'text';
    input.placeholder = ph.textContent.trim();
    input.style.cssText = 'flex:1 1 0%;background:transparent;border:0;outline:none;font:400 15px var(--font-text);color:var(--fg);';
    ph.replaceWith(input);
  }
  var btn = Array.prototype.find.call(sec.querySelectorAll('button,span,div'), function(el){ return el.textContent.trim()==='ASK'; });
  if (!input) return;
  var out = document.createElement('div');
  out.style.cssText = 'max-width:760px;margin:28px auto 0;display:grid;gap:10px;text-align:left;';
  input.closest('div').parentElement.appendChild(out);
  function go(){
    var q = (input.value||'').toLowerCase().trim();
    out.innerHTML = '';
    if (q.length<2) return;
    var hits = [];
    projects.forEach(function(p){
      var hay = (p.theme+' '+(p.summary||'')+' '+p.brand).toLowerCase();
      if (hay.indexOf(q)>=0) hits.push({t:p.theme, s:'Social Listening · '+p.brand+' · '+p.year, fn:function(){window.open(p.link,'_blank');}});
    });
    IEPV2_DATA.forEach(function(e, idx){
      var hay = (e.name+' '+(e.headline||'')+' '+(e.objective||'')+' '+e.brand).toLowerCase();
      if (hay.indexOf(q)>=0) hits.push({t:e.headline||e.name, s:'IEP · '+e.brand+' · '+e.experiment_id, fn:function(){ showTab('iep-v2'); v2Open(idx); }});
    });
    hits.slice(0,6).forEach(function(h){
      var d = document.createElement('div');
      d.style.cssText = 'background:var(--ink-base);border:1px solid var(--ink-line);border-radius:6px;padding:14px 18px;cursor:pointer;';
      d.innerHTML = '<div style="font-size:15px;color:var(--fg);">'+h.t+'</div><div style="font-size:11px;color:var(--fg-3);font-family:var(--font-mono);margin-top:4px;">'+h.s+'</div>';
      d.addEventListener('click', h.fn);
      out.appendChild(d);
    });
    if (!hits.length){
      var d = document.createElement('div');
      d.style.cssText = 'color:var(--fg-3);font-size:13px;text-align:center;';
      d.textContent = 'No matches across reports and experiments.';
      out.appendChild(d);
    }
  }
  if (btn) btn.addEventListener('click', go);
  input.addEventListener('keydown', function(ev){ if (ev.key==='Enter') go(); });
}

function wireAudit(){
  var sec = document.getElementById('ai-audit');
  if (!sec || typeof aidSummaries === 'undefined') return;
  var order = ['Astroglide', 'Just For Men', 'Vagisil'];
  // score cards: los 3 con % grande
  var cards = Array.prototype.filter.call(sec.querySelectorAll('div'), function(d){
    return /%/.test(d.textContent) && d.querySelectorAll('*').length < 20 && (d.getAttribute('style')||'').indexOf('ink-base') >= 0;
  }).slice(0, 3);
  cards.forEach(function(card, i){
    var b = order[i]; var sm = aidSummaries[b]; if (!sm) return;
    var pct = sm.avg_visibility;
    var color = pct >= 60 ? '#00d97f' : (pct >= 40 ? '#edc624' : '#ef446f');
    Array.prototype.forEach.call(card.querySelectorAll('span,div'), function(el){
      var t = el.textContent.trim();
      if (el.children.length === 0){
        if (/^\d+%$/.test(t)){ el.textContent = pct + '%'; el.style.color = color; }
        else if (/prompts/i.test(t)){ el.textContent = sm.total_prompts + ' prompts'; }
        else if (order.indexOf(t) >= 0){ el.textContent = b; }
      }
      var st = el.getAttribute('style')||'';
      if (st.indexOf('height: 4px') >= 0 && el.children.length === 1){
        el.children[0].style.width = pct + '%';
        el.children[0].style.background = color;
      }
    });
  });
  // tabla: filas = prompts
  var grids = Array.prototype.filter.call(sec.querySelectorAll('div'), function(d){
    return ((d.getAttribute('style')||'').indexOf('2.4fr') >= 0);
  });
  if (grids.length > 1){
    var header = grids[0];
    var tplRow = grids[1];
    var parent = tplRow.parentElement;
    grids.slice(1).forEach(function(r){ r.remove(); });
    var plats = ['ChatGPT', 'Perplexity', 'Gemini', 'Google AI Overview', 'Claude'];
    aidAudits.forEach(function(a){
      var row = tplRow.cloneNode(true);
      var cells = row.children;
      if (cells[0]) cells[0].textContent = a.prompt.length > 68 ? a.prompt.slice(0, 66) + '…' : a.prompt;
      plats.forEach(function(pl, k){
        var cell = cells[k + 1]; if (!cell) return;
        var sq = cell.querySelector('span,div') || cell;
        var res = a.results[pl] || {};
        sq.style.background = res.mentioned ? '#00d97f' : '#535353';
      });
      var scoreCell = cells[cells.length - 1];
      if (scoreCell) scoreCell.textContent = a.visibility_score + '%';
      parent.appendChild(row);
    });
  }
}

function wireJTBD(){
  var sec = document.getElementById('jtbd');
  if (!sec || typeof jtbdData === 'undefined') return;
  var brands = Object.keys(jtbdData.brands);
  // filas por marca: contenedores que incluyen el nombre y pills
  brands.forEach(function(b){
    var nameEl = Array.prototype.find.call(sec.querySelectorAll('span,div,h3,h4'), function(el){
      return el.children.length === 0 && el.textContent.trim() === b;
    });
    if (!nameEl) return;
    var row = nameEl.parentElement;
    for (var up = 0; up < 3 && row && !row.querySelector('[style*="999px"]'); up++) row = row.parentElement;
    if (!row) return;
    var pills = Array.prototype.filter.call(row.querySelectorAll('span,div'), function(el){
      return (el.getAttribute('style')||'').indexOf('999px') >= 0 && el.textContent.trim().length > 2;
    });
    var cur = jtbdData.brands[b].phase;
    jtbdData.phases.forEach(function(ph, i){
      var pill = pills[i]; if (!pill) return;
      pill.innerHTML = '<span style=\"font-family:var(--font-mono);color:' + (ph.num <= cur ? 'var(--primary)' : 'var(--fg-3)') + ';font-size:11px;margin-right:8px;\">0' + ph.num + '</span>' + ph.label;
      pill.style.opacity = ph.num <= cur ? '1' : '0.45';
      if (ph.num === cur) pill.style.borderColor = 'var(--primary)';
    });
    for (var k = jtbdData.phases.length; k < pills.length; k++) pills[k].style.display = 'none';
  });
}

var TABS = {
  'hub': ['Hero', 'Brand Portfolio'],
  'social-listening': ['Social Listening'],
  'iep-v2': ['IEP V2'],
  'insights': ['Key Insights'],
  'ask': ['Ask the Hub'],
  'ai-audit': ['AI Audit'],
  'jtbd': ['JTBD']
};
function allTabSections(){
  var els = Array.prototype.slice.call(document.querySelectorAll('[data-screen-label]'));
  els = els.filter(function(e){ var l=e.getAttribute('data-screen-label'); return l!=='Nav' && l!=='Footer'; });
  var ex = document.getElementById('iep-v2-explorer');
  if (ex) els.push(ex);
  return els;
}
function sectionsFor(tab){
  var els = [];
  (TABS[tab]||[]).forEach(function(lbl){
    Array.prototype.forEach.call(document.querySelectorAll('[data-screen-label="'+lbl+'"]'), function(e){ els.push(e); });
  });
  if (tab === 'iep-v2'){ var ex = document.getElementById('iep-v2-explorer'); if (ex) els.push(ex); }
  return els;
}
function showTab(tab){
  if (!TABS[tab]) tab = 'hub';
  allTabSections().forEach(function(sn){ sn.style.display = 'none'; });
  sectionsFor(tab).forEach(function(sn){ sn.style.display = ''; });
  Array.prototype.forEach.call(document.querySelectorAll('[data-screen-label="Nav"] a[href^="#"]'), function(a){
    var on = a.getAttribute('href') === '#' + tab;
    a.style.color = on ? 'var(--fg)' : 'var(--fg-2)';
    a.style.borderBottom = on ? '1px solid var(--primary)' : '0';
  });
  window.scrollTo(0, 0);
  try{ history.replaceState(null, '', '#' + tab); }catch(e){}
}
function navActive(){
  Array.prototype.forEach.call(document.querySelectorAll('[data-screen-label="Nav"] a[href^="#"]'), function(a){
    if (a.getAttribute('href') === '#iep' && a.textContent.trim() === 'IEP'){ a.style.display = 'none'; return; }
    a.addEventListener('click', function(ev){ ev.preventDefault(); var t = a.getAttribute('href').slice(1); showTab(t === 'iep' ? 'iep-v2' : t); });
  });
  var initial = (location.hash || '#hub').slice(1);
  showTab(initial);
}
</script>
"""

# ---------- 5. página final ----------
nav_fixes = """
/* --- fixes de navegación --- */
section[id], div[id="iep-v2-explorer"] { scroll-margin-top: 84px; }
[data-screen-label="Nav"] { flex-wrap: nowrap; }
[data-screen-label="Nav"] > div { flex-wrap: nowrap; white-space: nowrap; overflow-x: auto; scrollbar-width: none; }
[data-screen-label="Nav"] > div::-webkit-scrollbar { display: none; }
@media (max-width: 1180px){ [data-screen-label="Nav"] a { font-size: 12px !important; } }
"""
css = css + nav_fixes

page = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "<title>Combe Consumer Insights Hub</title>\n"
        "<style>\n" + fonts_css + "\n" + css + "\n</style>\n</head>\n<body>\n"
        + body + "\n" + wiring + "\n</body>\n</html>\n")

open(REPO + "/combe/index.html", "w", encoding="utf-8").write(page)
print(f"página: {len(page):,} chars · fuentes: {len(picks)} · payload IEPV2: {len(payload):,}")
