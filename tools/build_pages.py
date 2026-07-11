#!/usr/bin/env python3
"""Генератор страниц услуг skill-dev.ai из content/*.md на дизайн-системе сайта.

Использование:
  python3 tools/build_pages.py                # тестовая сборка (BASE=/site, noindex)
  BASE="" NOINDEX=0 python3 tools/build_pages.py   # боевая сборка при запуске на домене

Читает content/{slug}.md (черновики v2), пишет {url}/index.html + sitemap.xml.
"""
import os, re, sys, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("BASE", "/site")           # префикс GitHub Pages project-site
SITE = os.environ.get("SITE", "https://geeedy.github.io/site")  # для canonical/sitemap
NOINDEX = os.environ.get("NOINDEX", "1") == "1"  # тестовый домен не индексируем

# ---------- реестр страниц (URL, названия, silo) ----------
PAGES = {
 "vnedrenie-ii":        ("/uslugi/vnedrenie-ii/", "Внедрение ИИ", None),
 "ii-agenty":           ("/uslugi/ii-agenty/", "ИИ-агенты", None),
 "chat-boty":           ("/uslugi/chat-boty/", "Чат-боты с ИИ", None),
 "razrabotka-saitov":   ("/uslugi/razrabotka-saitov/", "Разработка сайтов", None),
 "vnedrenie-crm":       ("/uslugi/vnedrenie-crm/", "Внедрение CRM", None),
 "seo-prodvizhenie":    ("/uslugi/seo-prodvizhenie/", "SEO-продвижение", None),
 "golosovye-boty":      ("/uslugi/golosovye-boty/", "Голосовые боты", "chat-boty"),
 "agenty-dlya-prodazh": ("/uslugi/ii-agenty/dlya-prodazh/", "ИИ-агент для продаж", "ii-agenty"),
 "agenty-dlya-yuristov":("/uslugi/ii-agenty/dlya-yuristov/", "ИИ для юристов", "ii-agenty"),
 "ii-analitika":        ("/uslugi/ii-agenty/ii-analitika/", "ИИ-аналитика", "ii-agenty"),
 "korporativnyi-sait":  ("/uslugi/razrabotka-saitov/korporativnyi-sait/", "Корпоративный сайт", "razrabotka-saitov"),
 "internet-magazin":    ("/uslugi/razrabotka-saitov/internet-magazin/", "Интернет-магазин", "razrabotka-saitov"),
 "lending":             ("/uslugi/razrabotka-saitov/lending/", "Лендинг", "razrabotka-saitov"),
 "sait-s-ii":           ("/uslugi/razrabotka-saitov/sait-s-ii/", "Сайт с ИИ", "razrabotka-saitov"),
 "sait-na-tilde":       ("/uslugi/razrabotka-saitov/sait-na-tilde/", "Сайт на Тильде", "razrabotka-saitov"),
 "veb-prilozheniya":    ("/uslugi/razrabotka-saitov/veb-prilozheniya/", "Веб-приложения", "razrabotka-saitov"),
 "bitrix24":            ("/uslugi/vnedrenie-crm/bitrix24/", "Битрикс24", "vnedrenie-crm"),
 "amocrm":              ("/uslugi/vnedrenie-crm/amocrm/", "amoCRM", "vnedrenie-crm"),
 "seo-audit":           ("/uslugi/seo-prodvizhenie/seo-audit/", "SEO-аудит", "seo-prodvizhenie"),
 "geo-aeo":             ("/uslugi/seo-prodvizhenie/geo-aeo/", "GEO/AEO-продвижение", "seo-prodvizhenie"),
 "o-kompanii":          ("/o-kompanii/", "О компании", None),
 "audit-ii-strategiya":  ("/uslugi/vnedrenie-ii/audit-ii-strategiya/", "Аудит и ИИ-стратегия", "vnedrenie-ii"),
 "avtomatizatsiya-dokumentooborota": ("/uslugi/vnedrenie-ii/avtomatizatsiya-dokumentooborota/", "Автоматизация документооборота", "vnedrenie-ii"),
 "ii-v-1c":              ("/uslugi/vnedrenie-ii/ii-v-1c/", "ИИ в 1С", "vnedrenie-ii"),
 "obuchenie-ii":         ("/uslugi/vnedrenie-ii/obuchenie-ii/", "Обучение команды ИИ", "vnedrenie-ii"),
 "dlya-hr":              ("/uslugi/ii-agenty/dlya-hr/", "ИИ в HR", "ii-agenty"),
 "bot-na-sait":          ("/uslugi/chat-boty/bot-na-sait/", "Чат-бот на сайт", "chat-boty"),
 "telegram-bot":         ("/uslugi/chat-boty/telegram-bot/", "Телеграм-бот", "chat-boty"),
 "skvoznaya-analitika":  ("/uslugi/vnedrenie-crm/skvoznaya-analitika/", "Сквозная аналитика", "vnedrenie-crm"),
}
HUBS = ["vnedrenie-ii","ii-agenty","chat-boty","razrabotka-saitov","vnedrenie-crm","seo-prodvizhenie"]
KIDS = {h: [s for s,(u,t,p) in PAGES.items() if p==h] for h in HUBS}

def u(path): return BASE + path  # внутренняя ссылка с префиксом

def esc(s): return html.escape(s, quote=True)

# ---------- markdown-конвертер (наш диалект) ----------
def inline(md):
    md = esc(md)
    md = re.sub(r'\[\[TBD[^\]]*\]\]', '<mark class="tbd">уточняется</mark>', md)
    def link(m):
        text, url = m.group(1), m.group(2)
        if url.startswith('/'):
            return f'<a href="{u(url)}">{text}</a>'
        return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'
    md = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, md)
    md = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', md)
    return md

def parse(md_text):
    """Возвращает meta(dict) и список блоков после '---'."""
    meta = {}
    for k, key in (("Title","title"),("Meta description","description"),
                   ("OG title","og_title"),("OG description","og_desc")):
        m = re.search(rf'\*\*{k}:\*\*\s*(.+)', md_text)
        if m: meta[key] = m.group(1).strip()
    body = md_text.split('\n---\n', 1)[1]
    body = re.sub(r'\n---\n\*Word count.*$', '', body, flags=re.S)
    lines = body.strip().split('\n')
    blocks, buf = [], []
    def flush():
        nonlocal buf
        if buf:
            blocks.append(('p', ' '.join(buf).strip())); buf = []
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln: flush(); i += 1; continue
        if ln.startswith('### '): flush(); blocks.append(('h3', ln[4:])); i += 1; continue
        if ln.startswith('## '):  flush(); blocks.append(('h2', ln[3:])); i += 1; continue
        if ln.startswith('# '):   flush(); blocks.append(('h1', ln[2:])); i += 1; continue
        m = re.match(r'\[IMG:\s*([^|\]]+)\|\s*([^\]]+)\]', ln)
        if m: flush(); blocks.append(('img', (m.group(1).strip(), m.group(2).strip()))); i += 1; continue
        m = re.match(r'\[INFOGRAPHIC:\s*([^|\]]+)\|\s*([^\]]+)\]', ln)
        if m: flush(); blocks.append(('info', (m.group(1).strip(), m.group(2).strip()))); i += 1; continue
        m = re.match(r'\[CTA-(hero|mid|final):\s*(.+)\]$', ln)
        if m: flush(); blocks.append(('cta_'+m.group(1), m.group(2))); i += 1; continue
        if ln.startswith('|'):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            blocks.append(('table', rows)); continue
        if re.match(r'^[-*] ', ln):
            flush(); items = []
            while i < len(lines) and re.match(r'^[-*] ', lines[i]):
                items.append(lines[i][2:].strip()); i += 1
            blocks.append(('ul', items)); continue
        if re.match(r'^\d+\. ', ln):
            flush(); items = []
            while i < len(lines) and re.match(r'^\d+\. ', lines[i]):
                items.append(re.sub(r'^\d+\. ', '', lines[i]).strip()); i += 1
            blocks.append(('ol', items)); continue
        buf.append(ln); i += 1
    flush()
    return meta, blocks

def render_cta(kind, payload):
    parts = [p.strip() for p in payload.split('|')]
    btns = []
    for j, p in enumerate(parts):
        p = re.sub(r'\s*→\s*(форма|сессия.*|демо)$', '', p).strip()
        m = re.search(r'(.*?):?\s*→\s*(/\S+)$', p)
        href, label = (u(m.group(2)), m.group(1)) if m else (u('/kontakty/'), p)
        if kind == 'cta_hero' and len(label) > 38:
            short = label.split(':')[0].strip()
            label = short if len(short) <= 38 else 'Оставить заявку'
        cls = 'btn--primary' if j == 0 else 'btn--outline'
        btns.append(f'<a class="btn {cls}" href="{href}">{esc(label)}</a>')
    if kind == 'cta_hero':
        return '<div class="page-hero__actions">' + ' '.join(btns) + '</div>'
    title = 'Обсудим вашу задачу' if kind == 'cta_final' else parts[0].split(':')[0]
    text = parts[0]
    return (f'<div class="cta-horizontal step-up"><div class="cta-horizontal__text">'
            f'<h3>{inline(text)}</h3></div>'
            f'<a href="{u("/kontakty/")}" class="btn btn--primary">Оставить заявку</a></div>')

def render_blocks(blocks, slug):
    """Основной рендер: hero отдельно, FAQ собирается в accordion + schema."""
    out, faq, in_faq = [], [], False
    h1 = ''
    i = 0
    while i < len(blocks):
        t, v = blocks[i]
        if t == 'h1': h1 = v; i += 1; continue
        if t == 'h2':
            in_faq = bool(re.match(r'(Вопрос|Частые вопрос)', v))
            out.append(f'<h2 class="heading2 step-up">{inline(v)}</h2>')
            if in_faq: out.append('<div class="faq-list step-up">')
            i += 1; continue
        if in_faq and t == 'p':
            m = re.match(r'\*\*(.+?)\*\*\s*(.+)', v, re.S)
            if m:
                q, a = m.group(1), m.group(2)
                faq.append((q, a))
                out.append(f'<div class="faq-item"><button class="faq-question">{esc(q)}</button>'
                           f'<div class="faq-answer"><p>{inline(a)}</p></div></div>')
                i += 1; continue
        if t == 'h3': out.append(f'<h3 class="page-h3">{inline(v)}</h3>')
        elif t == 'p': out.append(f'<p>{inline(v)}</p>')
        elif t == 'ul': out.append('<ul class="page-list">' + ''.join(f'<li>{inline(x)}</li>' for x in v) + '</ul>')
        elif t == 'ol': out.append('<ol class="page-list page-list--num">' + ''.join(f'<li>{inline(x)}</li>' for x in v) + '</ol>')
        elif t == 'table':
            head, *rows = [r for r in v if not all(re.match(r'^:?-+:?$', c) for c in r)]
            thead = '<tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr>'
            tbody = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows)
            out.append(f'<div class="table-wrap"><table class="page-table"><thead>{thead}</thead><tbody>{tbody}</tbody></table></div>')
        elif t == 'img':
            path, alt = v
            src = u('/assets/img/' + os.path.basename(path))
            out.append(f'<figure class="page-figure"><img src="{src}" alt="{esc(alt)}" loading="lazy" width="1600" height="1067"></figure>')
        elif t == 'info':
            path, cap = v
            src = u('/assets/infographics/' + os.path.basename(path))
            out.append(f'<figure class="page-figure page-figure--info"><img src="{src}" alt="{esc(cap)}" loading="lazy">'
                       f'<figcaption>{esc(cap)}</figcaption></figure>')
        elif t.startswith('cta_'):
            out.append(render_cta(t, v))
        i += 1
    if in_faq or faq:
        # закрыть faq-list (он последний содержательный блок перед финальным CTA)
        # вставляем закрытие перед последним CTA если тот после FAQ
        for j in range(len(out)-1, -1, -1):
            if 'faq-item' in out[j]:
                out.insert(j+1, '</div>'); break
    return h1, out, faq

def crumbs(slug):
    url, title, parent = PAGES[slug]
    trail = [("Главная", "/")]
    if url.startswith('/uslugi/'): trail.append(("Услуги", "/uslugi/"))
    if parent: trail.append((PAGES[parent][1], PAGES[parent][0]))
    items_html = ''.join(f'<a href="{u(p)}">{esc(n)}</a><span>/</span>' for n, p in trail)
    ld = [{"@type":"ListItem","position":k+1,"name":n,"item":SITE + p} for k,(n,p) in enumerate(trail)]
    ld.append({"@type":"ListItem","position":len(trail)+1,"name":title,"item":SITE + url})
    return f'<nav class="breadcrumbs" aria-label="Хлебные крошки">{items_html}<span aria-current="page">{esc(title)}</span></nav>', ld

def schema(slug, meta, faq, bc_ld):
    url, title, parent = PAGES[slug]
    g = [
      {"@type":"Organization","@id":SITE+"/#org","name":"Skill Dev","url":SITE+"/",
       "logo":SITE+"/assets/ui/skilldev-logo.svg"},
      {"@type":"WebPage","@id":SITE+url,"url":SITE+url,"name":meta.get("title",title),
       "description":meta.get("description",""),"inLanguage":"ru","isPartOf":{"@id":SITE+"/#org"}},
      {"@type":"BreadcrumbList","itemListElement":bc_ld},
    ]
    if url.startswith('/uslugi/') :
        g.append({"@type":"Service","name":title,"provider":{"@id":SITE+"/#org"},
                  "areaServed":"RU","url":SITE+url})
    if faq:
        g.append({"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r'\[\[TBD[^\]]*\]\]','уточняется',a)}}
            for q,a in faq]})
    return '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@graph":g}, ensure_ascii=False) + '</script>'

def header_html():
    mega_groups = [
        ("Искусственный интеллект", ["vnedrenie-ii","ii-agenty","chat-boty","golosovye-boty"]),
        ("Разработка", ["razrabotka-saitov","internet-magazin","veb-prilozheniya","sait-s-ii"]),
        ("Продажи и трафик", ["vnedrenie-crm","bitrix24","seo-prodvizhenie","seo-audit","geo-aeo"]),
    ]
    cols = ''.join(
        f'<div class="mega__col"><h4>{esc(g)}</h4><ul>' +
        ''.join(f'<li><a href="{u(PAGES[k][0])}">{esc(PAGES[k][1])}</a></li>' for k in kids) +
        '</ul></div>'
        for g, kids in mega_groups)
    return f'''<header class="header" id="siteHeader">
    <div class="header-global-line">
      <div class="container header-global-line__inner">
        <div class="header-global-line__sites">
          <a href="{u(PAGES["vnedrenie-ii"][0])}" class="hgl-link"><span class="hgl-icon hgl-icon--ai"></span>Skill Dev AI</a>
          <a href="{u(PAGES["razrabotka-saitov"][0])}" class="hgl-link"><span class="hgl-icon hgl-icon--web"></span>Skill Dev Web</a>
        </div>
        <a href="mailto:hello@skill-dev.ai" class="header-global-line__contact">
          <img src="{u('/assets/ui/email-icon.svg')}" alt="" width="18" height="12">hello@skill-dev.ai
        </a>
      </div>
    </div>
    <div class="container header__inner">
      <a href="{u('/')}" class="logo"><img src="{u('/assets/ui/skilldev-logo.svg')}" alt="Skill Dev" class="logo__img" width="196" height="36"></a>
      <nav class="nav" id="mainNav">
        <div class="nav__item has-mega">
          <a class="nav__link" href="{u('/uslugi/')}">Услуги</a>
          <div class="mega mega--wide"><div class="container mega__grid">{cols}
            <div class="mega__promo"><h4>С чего начать?</h4><p>Бесплатный аудит одного процесса покажет расчёт экономии до внедрения.</p><a href="{u('/kontakty/')}" class="btn btn--primary btn--sm">Обсудить задачу</a></div>
          </div></div>
        </div>
        <div class="nav__item"><a class="nav__link" href="{u('/o-kompanii/')}">О компании</a></div>
        <div class="nav__item"><a class="nav__link" href="{u('/')}#industries">Отрасли</a></div>
        <div class="nav__item"><a class="nav__link" href="{u('/')}#full-cycle">Как мы работаем</a></div>
        <div class="nav__item"><a class="nav__link" href="{u('/kontakty/')}">Контакты</a></div>
      </nav>
      <div class="nav__actions"><a href="{u(PAGES["seo-audit"][0])}" class="btn btn--accent">Бесплатный аудит</a></div>
      <button class="menu-toggle" id="menuToggle" aria-label="Меню"><span></span><span></span><span></span></button>
    </div>
  </header>'''

def footer_html():
    cols = []
    for h in HUBS:
        kid_links = ''.join(f'<li><a href="{u(PAGES[k][0])}">{esc(PAGES[k][1])}</a></li>' for k in KIDS[h])
        cols.append(f'<div><h4><a href="{u(PAGES[h][0])}">{esc(PAGES[h][1])}</a></h4><ul>{kid_links}</ul></div>')
    return f'''<footer class="footer"><div class="container">
    <div class="footer__top">
      <div class="footer__brand"><div class="footer__logo">Skill Dev</div></div>
      <div class="footer__contacts"><p><strong>Контакты</strong></p><p>hello@skill-dev.ai</p><p>Работаем по всей России</p></div>
    </div>
    <div class="footer__grid footer__grid--silo">{''.join(cols)}
      <div><h4>Компания</h4><ul><li><a href="{u('/o-kompanii/')}">О нас</a></li><li><a href="{u('/kontakty/')}">Контакты</a></li><li><a href="{u('/uslugi/')}">Все услуги</a></li></ul></div>
    </div>
    <div class="footer__bottom"><span>© 2026 Skill Dev. Все права защищены.</span><span>hello@skill-dev.ai</span></div>
  </div></footer>'''

def page_shell(slug, meta, hero_html, body_html, faq, bc_ld):
    url, title, parent = PAGES[slug]
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(meta.get("title", title))}</title>
  <meta name="description" content="{esc(meta.get("description",""))}">
  {noindex}
  <link rel="canonical" href="{SITE}{url}">
  <meta property="og:title" content="{esc(meta.get("og_title", meta.get("title", title)))}">
  <meta property="og:description" content="{esc(meta.get("og_desc", meta.get("description","")))}">
  <meta property="og:type" content="website">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Sumana&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{u('/css/styles.css')}?v=6">
  <link rel="stylesheet" href="{u('/css/pages.css')}?v=6">
  {schema(slug, meta, faq, bc_ld)}
</head>
<body class="inner-page">
{header_html()}
<main class="page-main page-article">
  {hero_html}
  <div class="container page-content">
    {body_html}
  </div>
</main>
{footer_html()}
<script src="{u('/js/main.js')}?v=6"></script>
</body>
</html>'''

def build_page(slug):
    md = open(os.path.join(ROOT, 'content', slug + '.md'), encoding='utf-8').read()
    meta, blocks = parse(md)
    h1, out, faq = render_blocks(blocks, slug)
    bc_html, bc_ld = crumbs(slug)
    # hero: крошки + h1 + первый p + hero-CTA + hero-img выносим наверх
    lead, cta_hero, hero_img, rest = '', '', '', []
    for b in out:
        if not lead and b.startswith('<p>'): lead = b; continue
        if not cta_hero and 'page-hero__actions' in b: cta_hero = b; continue
        if not hero_img and 'page-figure' in b and 'hero' in b: hero_img = b; continue
        rest.append(b)
    hero = f'''<section class="page-hero"><div class="container">
      {bc_html}
      <h1 class="heading1 page-hero__title">{inline(h1)}</h1>
      <div class="page-hero__lead">{lead}</div>
      {cta_hero}
    </div></section>'''
    body = (hero_img or '') + '\n'.join(rest)
    html_doc = page_shell(slug, meta, hero, body, faq, bc_ld)
    url = PAGES[slug][0]
    dst = os.path.join(ROOT, url.strip('/').replace('/', os.sep) or '.', 'index.html')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(html_doc)
    return url

def build_uslugi_catalog():
    cards = []
    DESCR = {
     "vnedrenie-ii":"Аудит процессов, пилот, метрики до и после. Флагманская услуга.",
     "ii-agenty":"Цифровые сотрудники: заявки, документы, поддержка, продажи.",
     "chat-boty":"ИИ-боты для сайта, Telegram и WhatsApp: лиды в CRM за секунды.",
     "razrabotka-saitov":"От визитки до микросервисной AI-экосистемы.",
     "vnedrenie-crm":"Битрикс24 и amoCRM: заявки перестают теряться.",
     "seo-prodvizhenie":"Лиды из Яндекса и Google, которые дешевеют со временем.",
    }
    for h in HUBS:
        kid_links = ' · '.join(f'<a href="{u(PAGES[k][0])}">{esc(PAGES[k][1])}</a>' for k in KIDS[h])
        cards.append(f'''<div class="catalog-card">
          <h2 class="catalog-card__title"><a href="{u(PAGES[h][0])}">{esc(PAGES[h][1])}</a></h2>
          <p>{esc(DESCR[h])}</p>
          <p class="catalog-card__kids">{kid_links if kid_links else ''}</p>
        </div>''')
    bc = f'<nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="{u("/")}">Главная</a><span>/</span><span aria-current="page">Услуги</span></nav>'
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    doc = f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Услуги Skill Dev: внедрение ИИ, разработка, CRM, SEO</title>
<meta name="description" content="Шесть направлений: внедрение ИИ, ИИ-агенты, чат-боты, разработка сайтов, CRM и SEO. Внутри направлений 13 услуг под конкретные задачи.">{noindex}
<link rel="canonical" href="{SITE}/uslugi/">
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Sumana&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/css/styles.css')}?v=6"><link rel="stylesheet" href="{u('/css/pages.css')}?v=6"></head>
<body class="inner-page">{header_html()}
<main class="page-main page-article">
<section class="page-hero"><div class="container">{bc}
<h1 class="heading1 page-hero__title">Услуги</h1>
<div class="page-hero__lead"><p>Мы сокращаем расходы бизнеса технологиями: внедряем ИИ, строим сайты любой сложности, наводим порядок в продажах и приводим трафик. Выберите направление, внутри каждого есть услуги под конкретные задачи.</p></div>
</div></section>
<div class="container page-content"><div class="catalog-grid">{''.join(cards)}</div></div>
</main>{footer_html()}<script src="{u('/js/main.js')}?v=6"></script></body></html>'''
    os.makedirs(os.path.join(ROOT, 'uslugi'), exist_ok=True)
    open(os.path.join(ROOT, 'uslugi', 'index.html'), 'w', encoding='utf-8').write(doc)

def build_kontakty():
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    bc = f'<nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="{u("/")}">Главная</a><span>/</span><span aria-current="page">Контакты</span></nav>'
    doc = f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Контакты — Skill Dev</title><meta name="description" content="Свяжитесь с командой Skill Dev: обсудим задачу и вернёмся с расчётом за 2 дня.">{noindex}
<link rel="canonical" href="{SITE}/kontakty/">
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Sumana&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/css/styles.css')}?v=6"><link rel="stylesheet" href="{u('/css/pages.css')}?v=6"></head>
<body class="inner-page">{header_html()}
<main class="page-main page-article">
<section class="page-hero"><div class="container">{bc}
<h1 class="heading1 page-hero__title">Контакты</h1>
<div class="page-hero__lead"><p>Опишите задачу своими словами, и мы вернёмся с расчётом за 2 дня. Сроки и цены обсуждаем индивидуально, с вами будет работать персональный менеджер.</p></div></div></section>
<section class="contact-section" id="contact"><div class="container"><div class="contact-grid">
<div class="contact-info"><h2 class="heading2">Нужна консультация?</h2><p>hello@skill-dev.ai</p><p>Работаем по всей России, удалённо.</p></div>
<form class="contact-form" id="contactForm">
<div class="form-group"><label for="msg">Чем помочь?</label><textarea id="msg" rows="4" required placeholder="Опишите задачу..."></textarea></div>
<div class="form-row"><div class="form-group"><label>Имя</label><input type="text" required></div>
<div class="form-group"><label>Email или Telegram</label><input type="text" required></div></div>
<button type="submit" class="btn btn--primary" style="width:100%">Отправить</button></form>
</div></div></section>
</main>{footer_html()}<script src="{u('/js/main.js')}?v=6"></script></body></html>'''
    os.makedirs(os.path.join(ROOT, 'kontakty'), exist_ok=True)
    open(os.path.join(ROOT, 'kontakty', 'index.html'), 'w', encoding='utf-8').write(doc)

def build_sitemap(urls):
    items = ''.join(f'<url><loc>{SITE}{p}</loc></url>' for p in urls)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE}/</loc></url>{items}</urlset>')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(
        f"User-agent: *\n{'Disallow: /' if NOINDEX else 'Allow: /'}\nSitemap: {SITE}/sitemap.xml\n")

def patch_home():
    """Единые header/footer на главной: заменяем блоки сгенерированными."""
    p = os.path.join(ROOT, 'index.html')
    h = open(p, encoding='utf-8').read()
    h = re.sub(r'<header class="header[^"]*" id="siteHeader">.*?</header>', header_html(), h, count=1, flags=re.S)
    h = re.sub(r'<footer class="footer">.*?</footer>', footer_html(), h, count=1, flags=re.S)
    h = re.sub(r'href="[^"]*css/(styles|pages)\.css[^"]*"', lambda m: f'href="{u("/css/"+m.group(1)+".css")}?v=6"', h)
    h = re.sub(r'src="[^"]*/js/main\.js[^"]*"', f'src="{u("/js/main.js")}?v=6"', h)
    open(p, 'w', encoding='utf-8').write(h)
    print('patched index.html (header/footer unified)')

if __name__ == '__main__':
    patch_home()
    urls = ['/uslugi/']
    build_uslugi_catalog()
    build_kontakty(); urls.append('/kontakty/')
    for slug in PAGES:
        if slug == 'home': continue
        urls.append(build_page(slug))
        print('built', PAGES[slug][0])
    build_sitemap(urls)
    print(f'\nDONE: {len(urls)} страниц · BASE={BASE!r} · NOINDEX={NOINDEX}')
