#!/usr/bin/env python3
"""Генератор страниц skill-dev.ai из content/*.md (RU) и content/en/*.md (EN).

Использование:
  python3 tools/build_pages.py                     # тестовая (BASE=/site, noindex)
  BASE="" NOINDEX=0 SITE=https://skill-dev.ai python3 tools/build_pages.py

Для каждого URL пишет index.html (RU) и index.en.html (EN). Язык не меняет путь.
"""
import os, re, sys, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("BASE", "/site")
SITE = os.environ.get("SITE", "https://geeedy.github.io/site")
# Индексация по домену: тестовые/локальные — закрыты, боевой домен — открыт.
# Явный NOINDEX=1/0 всегда перекрывает автоопределение.
_is_test = ("geeedy.github.io" in SITE) or ("localhost" in SITE) or ("127.0.0.1" in SITE) or (BASE == "/site")
NOINDEX = os.environ.get("NOINDEX", "1" if _is_test else "0") == "1"

# ---------- реестр: url, titles{ru,en}, parent ----------
PAGES = {
 "vnedrenie-ii":        ("/uslugi/vnedrenie-ii/", {"ru":"Внедрение ИИ","en":"AI Implementation"}, None),
 "ii-agenty":           ("/uslugi/ii-agenty/", {"ru":"ИИ-агенты","en":"AI Agents"}, None),
 "chat-boty":           ("/uslugi/chat-boty/", {"ru":"Чат-боты с ИИ","en":"AI Chatbots"}, None),
 "razrabotka-saitov":   ("/uslugi/razrabotka-saitov/", {"ru":"Разработка сайтов","en":"Website Development"}, None),
 "vnedrenie-crm":       ("/uslugi/vnedrenie-crm/", {"ru":"Внедрение CRM","en":"CRM Implementation"}, None),
 "seo-prodvizhenie":    ("/uslugi/seo-prodvizhenie/", {"ru":"SEO-продвижение","en":"SEO Services"}, None),
 "golosovye-boty":      ("/uslugi/golosovye-boty/", {"ru":"Голосовые боты","en":"Voice Bots"}, "chat-boty"),
 "agenty-dlya-prodazh": ("/uslugi/ii-agenty/dlya-prodazh/", {"ru":"ИИ-агент для продаж","en":"AI Sales Agent"}, "ii-agenty"),
 "agenty-dlya-yuristov":("/uslugi/ii-agenty/dlya-yuristov/", {"ru":"ИИ для юристов","en":"AI for Legal Teams"}, "ii-agenty"),
 "ii-analitika":        ("/uslugi/ii-agenty/ii-analitika/", {"ru":"ИИ-аналитика","en":"AI Analytics"}, "ii-agenty"),
 "korporativnyi-sait":  ("/uslugi/razrabotka-saitov/korporativnyi-sait/", {"ru":"Корпоративный сайт","en":"Corporate Website"}, "razrabotka-saitov"),
 "internet-magazin":    ("/uslugi/razrabotka-saitov/internet-magazin/", {"ru":"Интернет-магазин","en":"Online Store"}, "razrabotka-saitov"),
 "lending":             ("/uslugi/razrabotka-saitov/lending/", {"ru":"Лендинг","en":"Landing Page"}, "razrabotka-saitov"),
 "sait-s-ii":           ("/uslugi/razrabotka-saitov/sait-s-ii/", {"ru":"Сайт с ИИ","en":"AI-Powered Website"}, "razrabotka-saitov"),
 "sait-na-tilde":       ("/uslugi/razrabotka-saitov/sait-na-tilde/", {"ru":"Сайт на Тильде","en":"Tilda Website"}, "razrabotka-saitov"),
 "veb-prilozheniya":    ("/uslugi/razrabotka-saitov/veb-prilozheniya/", {"ru":"Веб-приложения","en":"Web Applications"}, "razrabotka-saitov"),
 "bitrix24":            ("/uslugi/vnedrenie-crm/bitrix24/", {"ru":"Битрикс24","en":"Bitrix24"}, "vnedrenie-crm"),
 "amocrm":              ("/uslugi/vnedrenie-crm/amocrm/", {"ru":"amoCRM","en":"amoCRM"}, "vnedrenie-crm"),
 "seo-audit":           ("/uslugi/seo-prodvizhenie/seo-audit/", {"ru":"SEO-аудит","en":"SEO Audit"}, "seo-prodvizhenie"),
 "geo-aeo":             ("/uslugi/seo-prodvizhenie/geo-aeo/", {"ru":"GEO/AEO-продвижение","en":"GEO/AEO Optimization"}, "seo-prodvizhenie"),
 "o-kompanii":          ("/o-kompanii/", {"ru":"О компании","en":"About Us"}, None),
 "audit-ii-strategiya":  ("/uslugi/vnedrenie-ii/audit-ii-strategiya/", {"ru":"Аудит и ИИ-стратегия","en":"AI Audit & Strategy"}, "vnedrenie-ii"),
 "avtomatizatsiya-dokumentooborota": ("/uslugi/vnedrenie-ii/avtomatizatsiya-dokumentooborota/", {"ru":"Автоматизация документооборота","en":"Document Workflow Automation"}, "vnedrenie-ii"),
 "ii-v-1c":              ("/uslugi/vnedrenie-ii/ii-v-1c/", {"ru":"ИИ в 1С","en":"AI for 1C"}, "vnedrenie-ii"),
 "obuchenie-ii":         ("/uslugi/vnedrenie-ii/obuchenie-ii/", {"ru":"Обучение команды ИИ","en":"AI Team Training"}, "vnedrenie-ii"),
 "dlya-hr":              ("/uslugi/ii-agenty/dlya-hr/", {"ru":"ИИ в HR","en":"AI for HR"}, "ii-agenty"),
 "bot-na-sait":          ("/uslugi/chat-boty/bot-na-sait/", {"ru":"Чат-бот на сайт","en":"Website Chatbot"}, "chat-boty"),
 "telegram-bot":         ("/uslugi/chat-boty/telegram-bot/", {"ru":"Телеграм-бот","en":"Telegram Bot"}, "chat-boty"),
 "skvoznaya-analitika":  ("/uslugi/vnedrenie-crm/skvoznaya-analitika/", {"ru":"Сквозная аналитика","en":"End-to-End Analytics"}, "vnedrenie-crm"),
}
HUBS = ["vnedrenie-ii","ii-agenty","chat-boty","razrabotka-saitov","vnedrenie-crm","seo-prodvizhenie"]
KIDS = {h: [s for s,(u,t,p) in PAGES.items() if p==h] for h in HUBS}

STRINGS = {
  "ru": {
    "home": "Главная", "services": "Услуги", "about": "О компании",
    "industries": "Отрасли", "how_we_work": "Как мы работаем", "contacts": "Контакты",
    "free_audit": "Бесплатный аудит", "menu": "Меню", "breadcrumbs": "Хлебные крошки",
    "mega_ai": "Искусственный интеллект", "mega_dev": "Разработка", "mega_sales": "Продажи и трафик",
    "mega_start": "С чего начать?",
    "mega_start_p": "Бесплатный аудит одного процесса покажет расчёт экономии до внедрения.",
    "mega_discuss": "Обсудить задачу",
    "contacts_label": "Контакты", "worldwide": "Работаем по всему миру",
    "company": "Компания", "about_us": "О нас", "all_services": "Все услуги",
    "rights": "© 2026 Skill Dev. Все права защищены.",
    "cta_discuss": "Обсудим вашу задачу", "cta_apply": "Оставить заявку",
    "tbd": "уточняется",
    "catalog_title": "Услуги Skill Dev: внедрение ИИ, разработка, CRM, SEO",
    "catalog_desc": "Шесть направлений: внедрение ИИ, ИИ-агенты, чат-боты, разработка сайтов, CRM и SEO. Внутри направлений 13 услуг под конкретные задачи.",
    "catalog_h1": "Услуги",
    "catalog_lead": "Мы сокращаем расходы бизнеса технологиями: внедряем ИИ, строим сайты любой сложности, наводим порядок в продажах и приводим трафик. Выберите направление, внутри каждого есть услуги под конкретные задачи.",
    "catalog_descr": {
      "vnedrenie-ii": "Аудит процессов, пилот, метрики до и после. Флагманская услуга.",
      "ii-agenty": "Цифровые сотрудники: заявки, документы, поддержка, продажи.",
      "chat-boty": "ИИ-боты для сайта, Telegram и WhatsApp: лиды в CRM за секунды.",
      "razrabotka-saitov": "От визитки до микросервисной AI-экосистемы.",
      "vnedrenie-crm": "Битрикс24 и amoCRM: заявки перестают теряться.",
      "seo-prodvizhenie": "Лиды из Яндекса и Google, которые дешевеют со временем.",
    },
    "kontakty_title": "Контакты — Skill Dev",
    "kontakty_desc": "Свяжитесь с командой Skill Dev: обсудим задачу и вернёмся с расчётом за 2 дня.",
    "kontakty_h1": "Контакты",
    "kontakty_lead": "Опишите задачу своими словами, и мы вернёмся с расчётом за 2 дня. Сроки и цены обсуждаем индивидуально, с вами будет работать персональный менеджер.",
    "cases_nav": "Кейсы",
    "cases_title": "Кейсы Skill Dev: выполненные проекты",
    "cases_desc": "Реальные проекты команды Skill Dev: инфраструктура, автоматизация, разработка. Каждый кейс с задачей, решением и результатом.",
    "cases_h1": "Кейсы",
    "cases_lead": "Мы показываем работу как есть: задача клиента, что мы сделали и какой получился результат. Список будет пополняться по мере новых проектов.",
    "cases_read": "Читать кейс",
    "cases_soon": "Скоро здесь появятся новые кейсы.",
    "kontakty_need": "Нужна консультация?",
    "kontakty_remote": "Работаем по всему миру, удалённо.",
    "form_help": "Чем помочь?", "form_placeholder": "Опишите задачу...",
    "form_name": "Имя", "form_contact": "Email или Telegram", "form_send": "Отправить",
  },
  "en": {
    "home": "Home", "services": "Services", "about": "About",
    "industries": "Industries", "how_we_work": "How we work", "contacts": "Contact",
    "free_audit": "Free audit", "menu": "Menu", "breadcrumbs": "Breadcrumbs",
    "mega_ai": "Artificial intelligence", "mega_dev": "Development", "mega_sales": "Sales & traffic",
    "mega_start": "Where to start?",
    "mega_start_p": "A free audit of one process shows the savings estimate before you pay for implementation.",
    "mega_discuss": "Discuss your project",
    "contacts_label": "Contact", "worldwide": "We work worldwide",
    "company": "Company", "about_us": "About us", "all_services": "All services",
    "rights": "© 2026 Skill Dev. All rights reserved.",
    "cta_discuss": "Let's discuss your project", "cta_apply": "Send a request",
    "tbd": "TBD",
    "catalog_title": "Skill Dev Services: AI Implementation, Development, CRM, SEO",
    "catalog_desc": "Six practice areas: AI implementation, AI agents, chatbots, website development, CRM, and SEO — with focused services inside each.",
    "catalog_h1": "Services",
    "catalog_lead": "We cut business costs with technology: AI implementation, websites of any complexity, sales systems, and organic traffic. Pick a practice area — each one has services for specific jobs.",
    "catalog_descr": {
      "vnedrenie-ii": "Process audit, pilot, before/after metrics. Our flagship service.",
      "ii-agenty": "Digital coworkers: leads, documents, support, sales.",
      "chat-boty": "AI bots for your site, Telegram, and WhatsApp — leads into CRM in seconds.",
      "razrabotka-saitov": "From a brochure site to a microservice AI ecosystem.",
      "vnedrenie-crm": "Bitrix24 and amoCRM so leads stop getting lost.",
      "seo-prodvizhenie": "Leads from Yandex and Google that get cheaper over time.",
    },
    "kontakty_title": "Contact — Skill Dev",
    "kontakty_desc": "Contact the Skill Dev team: we'll discuss your project and return with an estimate within 2 days.",
    "kontakty_h1": "Contact",
    "kontakty_lead": "Describe your project in your own words — we'll return with an estimate in 2 days. Timelines and pricing are tailored; you'll work with a dedicated manager.",
    "cases_nav": "Cases",
    "cases_title": "Skill Dev Cases: Delivered Projects",
    "cases_desc": "Real projects by the Skill Dev team: infrastructure, automation, development. Every case has the task, the solution, and the outcome.",
    "cases_h1": "Cases",
    "cases_lead": "We show the work as it is: the client's task, what we did, and the outcome. The list grows as new projects ship.",
    "cases_read": "Read the case",
    "cases_soon": "More cases coming soon.",
    "kontakty_need": "Need a consultation?",
    "kontakty_remote": "We work worldwide, remotely.",
    "form_help": "How can we help?", "form_placeholder": "Describe your project...",
    "form_name": "Name", "form_contact": "Email or Telegram", "form_send": "Send",
  },
}

def page_title(slug, lang):
    return PAGES[slug][1][lang]

def u(path):
    return BASE + path

def esc(s):
    return html.escape(s, quote=True)

def content_path(slug, lang):
    if lang == "en":
        return os.path.join(ROOT, "content", "en", slug + ".md")
    return os.path.join(ROOT, "content", slug + ".md")

def out_html_name(lang):
    return "index.en.html" if lang == "en" else "index.html"

def page_dir(url):
    rel = url.strip("/").replace("/", os.sep)
    return os.path.join(ROOT, rel) if rel else ROOT

# ---------- markdown ----------
def inline(md, lang="ru"):
    tbd = STRINGS[lang]["tbd"]
    md = esc(md)
    md = re.sub(r'\[\[TBD[^\]]*\]\]', f'<mark class="tbd">{tbd}</mark>', md)
    def link(m):
        text, url = m.group(1), m.group(2)
        if url.startswith('/'):
            return f'<a href="{u(url)}">{text}</a>'
        return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'
    md = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, md)
    md = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', md)
    return md

def parse(md_text):
    meta = {}
    for k, key in (("Title","title"),("Meta description","description"),
                   ("OG title","og_title"),("OG description","og_desc")):
        m = re.search(rf'\*\*{k}:\*\*\s*(.+)', md_text)
        if m: meta[key] = m.group(1).strip()
    if '\n---\n' not in md_text:
        raise ValueError("missing --- separator after meta")
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

def render_cta(kind, payload, lang):
    S = STRINGS[lang]
    parts = [p.strip() for p in payload.split('|')]
    btns = []
    for j, p in enumerate(parts):
        p = re.sub(r'\s*→\s*(форма|сессия.*|демо|form|session.*|demo)$', '', p, flags=re.I).strip()
        m = re.search(r'(.*?):?\s*→\s*(/\S+)$', p)
        href, label = (u(m.group(2)), m.group(1)) if m else (u('/kontakty/'), p)
        if kind == 'cta_hero' and len(label) > 38:
            short = label.split(':')[0].strip()
            label = short if len(short) <= 38 else S["cta_apply"]
        cls = 'btn--primary' if j == 0 else 'btn--outline'
        btns.append(f'<a class="btn {cls}" href="{href}">{esc(label)}</a>')
    if kind == 'cta_hero':
        return '<div class="page-hero__actions">' + ' '.join(btns) + '</div>'
    text = parts[0]
    return (f'<div class="cta-horizontal step-up"><div class="cta-horizontal__text">'
            f'<p class="cta-horizontal__title">{inline(text, lang)}</p></div>'
            f'<a href="{u("/kontakty/")}" class="btn btn--primary">{esc(S["cta_apply"])}</a></div>')

def render_blocks(blocks, slug, lang):
    out, faq, in_faq = [], [], False
    h1 = ''
    i = 0
    while i < len(blocks):
        t, v = blocks[i]
        if t == 'h1': h1 = v; i += 1; continue
        if t == 'h2':
            in_faq = bool(re.match(r'(Вопрос|Частые вопрос|FAQ|Frequently asked)', v, re.I))
            out.append(f'<h2 class="heading2 step-up">{inline(v, lang)}</h2>')
            if in_faq: out.append('<div class="faq-list step-up">')
            i += 1; continue
        if in_faq and t == 'p':
            m = re.match(r'\*\*(.+?)\*\*\s*(.+)', v, re.S)
            if m:
                q, a = m.group(1), m.group(2)
                faq.append((q, a))
                out.append(f'<div class="faq-item"><button class="faq-question">{esc(q)}</button>'
                           f'<div class="faq-answer"><p>{inline(a, lang)}</p></div></div>')
                i += 1; continue
        if t == 'h3': out.append(f'<h3 class="page-h3">{inline(v, lang)}</h3>')
        elif t == 'p': out.append(f'<p>{inline(v, lang)}</p>')
        elif t == 'ul': out.append('<ul class="page-list">' + ''.join(f'<li>{inline(x, lang)}</li>' for x in v) + '</ul>')
        elif t == 'ol': out.append('<ol class="page-list page-list--num">' + ''.join(f'<li>{inline(x, lang)}</li>' for x in v) + '</ol>')
        elif t == 'table':
            head, *rows = [r for r in v if not all(re.match(r'^:?-+:?$', c) for c in r)]
            thead = '<tr>' + ''.join(f'<th>{inline(c, lang)}</th>' for c in head) + '</tr>'
            tbody = ''.join('<tr>' + ''.join(f'<td>{inline(c, lang)}</td>' for c in r) + '</tr>' for r in rows)
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
            out.append(render_cta(t, v, lang))
        i += 1
    if in_faq or faq:
        for j in range(len(out)-1, -1, -1):
            if 'faq-item' in out[j]:
                out.insert(j+1, '</div>'); break
    return h1, out, faq

def crumbs(slug, lang):
    S = STRINGS[lang]
    url, titles, parent = PAGES[slug]
    title = titles[lang]
    trail = [(S["home"], "/")]
    if url.startswith('/uslugi/'): trail.append((S["services"], "/uslugi/"))
    if parent: trail.append((PAGES[parent][1][lang], PAGES[parent][0]))
    items_html = ''.join(f'<a href="{u(p)}">{esc(n)}</a><span>/</span>' for n, p in trail)
    ld = [{"@type":"ListItem","position":k+1,"name":n,"item":SITE + p} for k,(n,p) in enumerate(trail)]
    ld.append({"@type":"ListItem","position":len(trail)+1,"name":title,"item":SITE + url})
    return f'<nav class="breadcrumbs" aria-label="{esc(S["breadcrumbs"])}">{items_html}<span aria-current="page">{esc(title)}</span></nav>', ld

def schema(slug, meta, faq, bc_ld, lang):
    url, titles, parent = PAGES[slug]
    title = titles[lang]
    tbd = STRINGS[lang]["tbd"]
    area = "Worldwide" if lang == "en" else "RU"
    g = [
      {"@type":"Organization","@id":SITE+"/#org","name":"Skill Dev","url":SITE+"/",
       "logo":SITE+"/assets/ui/logo-full.png"},
      {"@type":"WebPage","@id":SITE+url,"url":SITE+url,"name":meta.get("title",title),
       "description":meta.get("description",""),"inLanguage":lang,"isPartOf":{"@id":SITE+"/#org"}},
      {"@type":"BreadcrumbList","itemListElement":bc_ld},
    ]
    if url.startswith('/uslugi/'):
        g.append({"@type":"Service","name":title,"provider":{"@id":SITE+"/#org"},
                  "areaServed":area,"url":SITE+url})
    if faq:
        g.append({"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r'\[\[TBD[^\]]*\]\]', tbd, a)}}
            for q,a in faq]})
    return '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@graph":g}, ensure_ascii=False) + '</script>'

def lang_switcher(lang):
    ru_cls = 'lang-switch__btn is-active' if lang == 'ru' else 'lang-switch__btn'
    en_cls = 'lang-switch__btn is-active' if lang == 'en' else 'lang-switch__btn'
    return (
      f'<div class="lang-switch" role="group" aria-label="Language">'
      f'<button type="button" class="{ru_cls}" data-lang="ru" aria-pressed="{str(lang=="ru").lower()}">RU</button>'
      f'<span class="lang-switch__sep" aria-hidden="true">/</span>'
      f'<button type="button" class="{en_cls}" data-lang="en" aria-pressed="{str(lang=="en").lower()}">EN</button>'
      f'</div>'
    )

def yandex_metrika_html():
    """Yandex.Metrika — один раз в head на все страницы."""
    return '''  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=110912791', 'ym');

    ym(110912791, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/110912791" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->'''

def favicon_links_html():
    return f'''  <link rel="icon" href="{u('/favicon.ico')}" sizes="48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="{u('/assets/ui/favicon-32.png')}">
  <link rel="icon" type="image/png" sizes="192x192" href="{u('/assets/ui/favicon-192.png')}">
  <link rel="apple-touch-icon" href="{u('/assets/ui/apple-touch-icon.png')}">'''

def head_common():
    """Верификации ПС + фавиконки + Metrika — на все страницы обеих локалей."""
    return f'''<meta name="yandex-verification" content="bac091f33d55ea2c">
  <meta name="google-site-verification" content="a6Kww_ZoTqDVduplocAADN3G1dHjxKny1sv1Y1ag_f0">
{favicon_links_html()}
{yandex_metrika_html()}'''

def header_html(lang="ru"):
    S = STRINGS[lang]
    mega_groups = [
        (S["mega_ai"], ["vnedrenie-ii","ii-agenty","chat-boty","golosovye-boty"]),
        (S["mega_dev"], ["razrabotka-saitov","internet-magazin","veb-prilozheniya","sait-s-ii"]),
        (S["mega_sales"], ["vnedrenie-crm","bitrix24","seo-prodvizhenie","seo-audit","geo-aeo"]),
    ]
    cols = ''.join(
        f'<div class="mega__col"><div class="mega__h">{esc(g)}</div><ul>' +
        ''.join(f'<li><a href="{u(PAGES[k][0])}">{esc(page_title(k, lang))}</a></li>' for k in kids) +
        '</ul></div>'
        for g, kids in mega_groups)
    return f'''<header class="header" id="siteHeader">
    <div class="header-global-line">
      <div class="container header-global-line__inner">
        <div class="header-global-line__sites">
          <a href="{u(PAGES["vnedrenie-ii"][0])}" class="hgl-link"><span class="hgl-icon hgl-icon--ai"></span>Skill Dev AI</a>
          <a href="{u(PAGES["razrabotka-saitov"][0])}" class="hgl-link"><span class="hgl-icon hgl-icon--web"></span>Skill Dev Web</a>
        </div>
        <div class="header-global-line__right">
          {lang_switcher(lang)}
          <a href="mailto:hello@skill-dev.ai" class="header-global-line__contact">
            <img src="{u('/assets/ui/email-icon.svg')}" alt="" width="18" height="12">hello@skill-dev.ai
          </a>
        </div>
      </div>
    </div>
    <div class="container header__inner">
      <a href="{u('/')}" class="logo"><img src="{u('/assets/ui/logo-icon.png')}" alt="" class="logo__icon" width="36" height="40"><img src="{u('/assets/ui/logo-word.png')}" alt="skill-dev" class="logo__word" width="106" height="22"></a>
      <nav class="nav" id="mainNav">
        <div class="nav__item has-mega">
          <a class="nav__link" href="{u('/uslugi/')}">{esc(S["services"])}</a>
          <div class="mega mega--wide"><div class="container mega__grid">{cols}
            <div class="mega__promo"><div class="mega__h">{esc(S["mega_start"])}</div><p>{esc(S["mega_start_p"])}</p><a href="{u('/kontakty/')}" class="btn btn--primary btn--sm">{esc(S["mega_discuss"])}</a></div>
          </div></div>
        </div>
        <div class="nav__item"><a class="nav__link" href="{u('/o-kompanii/')}">{esc(S["about"])}</a></div>
        <div class="nav__item"><a class="nav__link" href="{u('/kejsy/')}">{esc(S["cases_nav"])}</a></div>
        <div class="nav__item"><a class="nav__link" href="{u('/')}#industries">{esc(S["industries"])}</a></div>
        <div class="nav__item"><a class="nav__link" href="{u('/')}#full-cycle">{esc(S["how_we_work"])}</a></div>
        <div class="nav__item"><a class="nav__link" href="{u('/kontakty/')}">{esc(S["contacts"])}</a></div>
      </nav>
      <div class="nav__actions"><a href="{u(PAGES["seo-audit"][0])}" class="btn btn--accent">{esc(S["free_audit"])}</a></div>
      <button class="menu-toggle" id="menuToggle" aria-label="{esc(S["menu"])}"><span></span><span></span><span></span></button>
    </div>
  </header>'''

def footer_html(lang="ru"):
    S = STRINGS[lang]
    cols = []
    for h in HUBS:
        kid_links = ''.join(f'<li><a href="{u(PAGES[k][0])}">{esc(page_title(k, lang))}</a></li>' for k in KIDS[h])
        cols.append(f'<div><div class="footer__h"><a href="{u(PAGES[h][0])}">{esc(page_title(h, lang))}</a></div><ul>{kid_links}</ul></div>')
    return f'''<footer class="footer"><div class="container">
    <div class="footer__top">
      <div class="footer__brand"><div class="footer__logo">Skill Dev</div></div>
      <div class="footer__contacts"><p><strong>{esc(S["contacts_label"])}</strong></p><p>hello@skill-dev.ai</p><p>{esc(S["worldwide"])}</p></div>
    </div>
    <div class="footer__grid footer__grid--silo">{''.join(cols)}
      <div><div class="footer__h">{esc(S["company"])}</div><ul><li><a href="{u('/o-kompanii/')}">{esc(S["about_us"])}</a></li><li><a href="{u('/kejsy/')}">{esc(S["cases_nav"])}</a></li><li><a href="{u('/kontakty/')}">{esc(S["contacts"])}</a></li><li><a href="{u('/uslugi/')}">{esc(S["all_services"])}</a></li></ul></div>
    </div>
    <div class="footer__bottom"><span>{esc(S["rights"])}</span><span>hello@skill-dev.ai</span></div>
  </div></footer>'''

def page_shell(slug, meta, hero_html, body_html, faq, bc_ld, lang):
    url, titles, parent = PAGES[slug]
    title = titles[lang]
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {head_common()}
  <title>{esc(meta.get("title", title))}</title>
  <meta name="description" content="{esc(meta.get("description",""))}">
  <meta http-equiv="content-language" content="{lang}">
  {noindex}
  <link rel="canonical" href="{SITE}{url}">
  <meta property="og:title" content="{esc(meta.get("og_title", meta.get("title", title)))}">
  <meta property="og:description" content="{esc(meta.get("og_desc", meta.get("description","")))}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE}{url}">
  <meta property="og:image" content="{SITE}/assets/ui/og-cover.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta property="og:locale" content="{"en_US" if lang=="en" else "ru_RU"}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Sumana&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{u('/css/styles.css')}?v=10">
  <link rel="stylesheet" href="{u('/css/pages.css')}?v=10">
  {schema(slug, meta, faq, bc_ld, lang)}
</head>
<body class="inner-page">
{header_html(lang)}
<main class="page-main page-article">
  {hero_html}
  <div class="container page-content">
    {body_html}
  </div>
</main>
{footer_html(lang)}
<script src="{u('/js/main.js')}?v=10"></script>
</body>
</html>'''

def build_page(slug, lang):
    path = content_path(slug, lang)
    if not os.path.isfile(path):
        print(f'  SKIP {lang} {slug}: missing {path}', file=sys.stderr)
        return None
    md = open(path, encoding='utf-8').read()
    meta, blocks = parse(md)
    h1, out, faq = render_blocks(blocks, slug, lang)
    bc_html, bc_ld = crumbs(slug, lang)
    lead, cta_hero, hero_img, rest = '', '', '', []
    for b in out:
        if not lead and b.startswith('<p>'): lead = b; continue
        if not cta_hero and 'page-hero__actions' in b: cta_hero = b; continue
        if not hero_img and 'page-figure' in b and 'hero' in b: hero_img = b; continue
        rest.append(b)
    hero = f'''<section class="page-hero"><div class="container">
      {bc_html}
      <h1 class="heading1 page-hero__title">{inline(h1, lang)}</h1>
      <div class="page-hero__lead">{lead}</div>
      {cta_hero}
    </div></section>'''
    body = (hero_img or '') + '\n'.join(rest)
    html_doc = page_shell(slug, meta, hero, body, faq, bc_ld, lang)
    url = PAGES[slug][0]
    d = page_dir(url)
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, out_html_name(lang))
    open(dst, 'w', encoding='utf-8').write(html_doc)
    return url

def build_uslugi_catalog(lang):
    S = STRINGS[lang]
    cards = []
    for h in HUBS:
        kid_links = ' · '.join(f'<a href="{u(PAGES[k][0])}">{esc(page_title(k, lang))}</a>' for k in KIDS[h])
        cards.append(f'''<div class="catalog-card">
          <h2 class="catalog-card__title"><a href="{u(PAGES[h][0])}">{esc(page_title(h, lang))}</a></h2>
          <p>{esc(S["catalog_descr"][h])}</p>
          <p class="catalog-card__kids">{kid_links if kid_links else ''}</p>
        </div>''')
    bc = f'<nav class="breadcrumbs" aria-label="{esc(S["breadcrumbs"])}"><a href="{u("/")}">{esc(S["home"])}</a><span>/</span><span aria-current="page">{esc(S["services"])}</span></nav>'
    itemlist = ",".join(
        f'{{"@type":"ListItem","position":{i+1},"name":{json.dumps(page_title(h, lang), ensure_ascii=False)},"url":"{SITE}{PAGES[h][0]}"}}'
        for i, h in enumerate(HUBS))
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    doc = f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  {head_common()}
<title>{esc(S["catalog_title"])}</title>
<meta name="description" content="{esc(S["catalog_desc"])}">
<meta http-equiv="content-language" content="{lang}">{noindex}
<link rel="canonical" href="{SITE}/uslugi/">
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"CollectionPage","@id":"{SITE}/uslugi/","url":"{SITE}/uslugi/","name":{json.dumps(S["catalog_title"], ensure_ascii=False)},"inLanguage":"{lang}"}},{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":{json.dumps(S["home"], ensure_ascii=False)},"item":"{SITE}/"}},{{"@type":"ListItem","position":2,"name":{json.dumps(S["services"], ensure_ascii=False)},"item":"{SITE}/uslugi/"}}]}},{{"@type":"ItemList","itemListElement":[{itemlist}]}}]}}</script>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Sumana&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/css/styles.css')}?v=10"><link rel="stylesheet" href="{u('/css/pages.css')}?v=10"></head>
<body class="inner-page">{header_html(lang)}
<main class="page-main page-article">
<section class="page-hero"><div class="container">{bc}
<h1 class="heading1 page-hero__title">{esc(S["catalog_h1"])}</h1>
<div class="page-hero__lead"><p>{esc(S["catalog_lead"])}</p></div>
</div></section>
<div class="container page-content"><div class="catalog-grid">{''.join(cards)}</div></div>
</main>{footer_html(lang)}<script src="{u('/js/main.js')}?v=10"></script></body></html>'''
    d = os.path.join(ROOT, 'uslugi')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, out_html_name(lang)), 'w', encoding='utf-8').write(doc)

def build_kontakty(lang):
    S = STRINGS[lang]
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    bc = f'<nav class="breadcrumbs" aria-label="{esc(S["breadcrumbs"])}"><a href="{u("/")}">{esc(S["home"])}</a><span>/</span><span aria-current="page">{esc(S["contacts"])}</span></nav>'
    doc = f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  {head_common()}
<title>{esc(S["kontakty_title"])}</title><meta name="description" content="{esc(S["kontakty_desc"])}">
<meta http-equiv="content-language" content="{lang}">{noindex}
<link rel="canonical" href="{SITE}/kontakty/">
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Sumana&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/css/styles.css')}?v=10"><link rel="stylesheet" href="{u('/css/pages.css')}?v=10"></head>
<body class="inner-page">{header_html(lang)}
<main class="page-main page-article">
<section class="page-hero"><div class="container">{bc}
<h1 class="heading1 page-hero__title">{esc(S["kontakty_h1"])}</h1>
<div class="page-hero__lead"><p>{esc(S["kontakty_lead"])}</p></div></div></section>
<section class="contact-section" id="contact"><div class="container"><div class="contact-grid">
<div class="contact-info"><h2 class="heading2">{esc(S["kontakty_need"])}</h2><p>hello@skill-dev.ai</p><p>{esc(S["kontakty_remote"])}</p></div>
<form class="contact-form" id="contactForm">
<div class="form-group"><label for="msg">{esc(S["form_help"])}</label><textarea id="msg" rows="4" required placeholder="{esc(S["form_placeholder"])}"></textarea></div>
<div class="form-row"><div class="form-group"><label>{esc(S["form_name"])}</label><input type="text" required></div>
<div class="form-group"><label>{esc(S["form_contact"])}</label><input type="text" required></div></div>
<button type="submit" class="btn btn--primary" style="width:100%">{esc(S["form_send"])}</button></form>
</div></div></section>
</main>{footer_html(lang)}<script src="{u('/js/main.js')}?v=10"></script></body></html>'''
    d = os.path.join(ROOT, 'kontakty')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, out_html_name(lang)), 'w', encoding='utf-8').write(doc)


def build_404():
    """Брендированная страница ошибки (serve_i18n использует её как error page)."""
    doc = f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  {head_common()}
<title>Страница не найдена | Skill Dev</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{u('/css/styles.css')}?v=10"><link rel="stylesheet" href="{u('/css/pages.css')}?v=10"></head>
<body class="inner-page">{header_html("ru")}
<main class="page-main page-article">
<section class="page-hero"><div class="container">
<h1 class="heading1 page-hero__title">Страница не найдена</h1>
<div class="page-hero__lead"><p>Такого адреса нет или страница переехала. Вот куда можно пойти отсюда.</p></div>
<div class="page-hero__actions"><a class="btn btn--primary" href="{u('/')}">На главную</a> <a class="btn btn--outline" href="{u('/uslugi/')}">Все услуги</a></div>
</div></section>
</main>{footer_html("ru")}<script src="{u('/js/main.js')}?v=10"></script></body></html>'''
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(doc)

# ==================== КЕЙСЫ ====================
CASES = ["claude-vps-sreda"]  # порядок на хабе (новые сверху)

CASE_META = {
  "claude-vps-sreda": {
    "url": "/kejsy/claude-vps-sreda/",
    "ru": {
      "card_title": "Изолированная среда командной разработки на VPS",
      "card_tag": "Инфраструктура · DevOps",
      "card_descr": "Развернули общий VPS для распределённой SEO-команды: безопасный доступ по SSH, единый workspace, автоматизация SEO-пайплайнов.",
    },
    "en": {
      "card_title": "Isolated team dev environment on a VPS",
      "card_tag": "Infrastructure · DevOps",
      "card_descr": "A shared VPS for a distributed SEO team: secure SSH access, a single workspace, and automated SEO pipelines.",
    },
  },
}

def build_cases_hub(lang):
    S = STRINGS[lang]
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    bc = f'<nav class="breadcrumbs" aria-label="{esc(S["breadcrumbs"])}"><a href="{u("/")}">{esc(S["home"])}</a><span>/</span><span aria-current="page">{esc(S["cases_h1"])}</span></nav>'
    cards = []
    for slug in CASES:
        m = CASE_META[slug]; c = m[lang]
        cards.append(f'''<a class="case-card" href="{u(m['url'])}">
          <div class="case-card__tag">{esc(c['card_tag'])}</div>
          <h2 class="case-card__title">{esc(c['card_title'])}</h2>
          <p class="case-card__descr">{esc(c['card_descr'])}</p>
          <span class="case-card__more">{esc(S['cases_read'])} →</span>
        </a>''')
    items_ld = ",".join(
        f'{{"@type":"ListItem","position":{i+1},"url":"{SITE}{CASE_META[slug]["url"]}","name":{json.dumps(CASE_META[slug][lang]["card_title"], ensure_ascii=False)}}}'
        for i, slug in enumerate(CASES))
    doc = f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  {head_common()}
<title>{esc(S["cases_title"])}</title><meta name="description" content="{esc(S["cases_desc"])}">
<meta http-equiv="content-language" content="{lang}">{noindex}
<link rel="canonical" href="{SITE}/kejsy/">
<meta property="og:title" content="{esc(S["cases_title"])}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}/kejsy/"><meta property="og:image" content="{SITE}/assets/ui/og-cover.png">
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"CollectionPage","@id":"{SITE}/kejsy/","url":"{SITE}/kejsy/","name":{json.dumps(S["cases_title"], ensure_ascii=False)},"inLanguage":"{lang}"}},{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":{json.dumps(S["home"], ensure_ascii=False)},"item":"{SITE}/"}},{{"@type":"ListItem","position":2,"name":{json.dumps(S["cases_h1"], ensure_ascii=False)},"item":"{SITE}/kejsy/"}}]}},{{"@type":"ItemList","itemListElement":[{items_ld}]}}]}}</script>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Sumana&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/css/styles.css')}?v=10"><link rel="stylesheet" href="{u('/css/pages.css')}?v=10"></head>
<body class="inner-page">{header_html(lang)}
<main class="page-main page-article">
<section class="page-hero"><div class="container">{bc}
<h1 class="heading1 page-hero__title">{esc(S["cases_h1"])}</h1>
<div class="page-hero__lead"><p>{esc(S["cases_lead"])}</p></div></div></section>
<div class="container page-content"><div class="case-grid">{''.join(cards)}</div></div>
</main>{footer_html(lang)}<script src="{u('/js/main.js')}?v=10"></script></body></html>'''
    d = os.path.join(ROOT, 'kejsy')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, out_html_name(lang)), 'w', encoding='utf-8').write(doc)


def build_case_vps(lang):
    S = STRINGS[lang]
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    sfx = "" if lang == "ru" else "-en"
    def img(n, alt): return f'<figure class="page-figure"><img src="{u("/assets/img/case-vps-"+n+sfx+".jpg")}" alt="{esc(alt)}" loading="lazy" width="1600" height="1066"></figure>'
    url = "/kejsy/claude-vps-sreda/"
    if lang == "ru":
        title = "Кейс: изолированная среда командной разработки на VPS | Skill Dev"
        desc = "Развернули общий VPS для распределённой SEO-команды: безопасный SSH-доступ, единый workspace, автоматизация SEO-пайплайнов. Три оператора работают одновременно."
        h1 = "Изолированная среда командной разработки на VPS"
        lead = "SEO-команде нужен был стабильный и безопасный доступ нескольких операторов к общей рабочей среде с ИИ-инструментами. Мы собрали такую среду на выделенном VPS и передали её в эксплуатацию."
        body = f'''
<div class="case-meta"><span class="case-card__tag">Инфраструктура · DevOps</span><span class="case-meta__item">Ubuntu 22.04/24.04 LTS</span><span class="case-meta__item">3 оператора одновременно</span></div>
{img("hero", "Рабочие места распределённой команды разработки")}
<h2>Задача</h2>
<p>Команда SEO-специалистов работала распределённо, из разных точек, но над общими проектами. Каждый оператор держал свой набор инструментов на своём компьютере, конфигурации расходились, а общий контекст работы терялся между людьми.</p>
<p>Нужна была одна стабильная и безопасная среда, где несколько операторов работают одновременно: с общими проектами, единым Git, общей историей и одинаковым набором инструментов у всех.</p>
<h2>Что мы развернули</h2>
<p>На выделенном VPS (Ubuntu 22.04/24.04 LTS) собрали изолированную рабочую среду и настроили удалённую разработку через Remote-SSH в VS Code. Операторы подключаются к одному серверу и работают в общем пространстве проектов.</p>
<ul>
<li>Единый workspace с общими проектами сайтов, Git-репозиториями и историей работы.</li>
<li>Три одновременных SSH-подключения: два с рабочих машин заказчика и одно с ПК руководителя.</li>
<li>Общий набор инструментов и окружение, одинаковое у всех операторов.</li>
</ul>
<h2>Архитектура</h2>
{img("arch", "Схема: рабочие места подключаются к общему VPS")}
<p>В центре схемы выделенный VPS, к которому по защищённым SSH-каналам подключаются рабочие места команды из разных локаций. Все работают в едином user-пространстве сервера, поэтому проекты, репозитории и история остаются общими, а не разъезжаются по личным компьютерам.</p>
<h2>Безопасность</h2>
<p>Доступ к серверу закрыт по-взрослому, без паролей и лишних открытых дверей:</p>
<ul>
<li>Вход только по SSH-ключам (ed25519), парольная аутентификация отключена.</li>
<li>Файрвол UFW и fail2ban против перебора и подозрительной активности.</li>
<li>Автоматические обновления системы и безопасности.</li>
<li>Открыт только нужный минимум портов, всё остальное закрыто.</li>
</ul>
<h2>Стабильность подключений</h2>
<p>Чтобы длинные рабочие сессии не рвались, настроили autossh для автоматического восстановления соединений и tmux/screen для долгоживущих сессий. Оператор может отключиться и вернуться к работе ровно там, где остановился, а фоновые задачи продолжают идти.</p>
{img("rack", "Серверная инфраструктура проекта")}
<h2>Производительность</h2>
<p>Под параллельную работу нескольких операторов и инструменты с длинным контекстом выделили ресурсы с запасом: 8–16 vCPU, 32+ ГБ RAM, SSD. Среда не тормозит, даже когда несколько человек работают одновременно и гоняют тяжёлые задачи.</p>
<h2>Автоматизация SEO-работ</h2>
{img("work", "Рабочее место оператора с несколькими мониторами")}
<p>Поверх среды собрали рабочие пайплайны под задачи команды и связали их с привычными инструментами:</p>
<ul>
<li>Интеграция с Git и локальными базами семантики.</li>
<li>Подключение SEO-инструментов: выгрузки Screaming Frog, Ahrefs API, Google Search Console.</li>
<li>Пайплайны генерации контента с проверкой уникальности и последующим SEO-структурированием.</li>
</ul>
<h2>Результат</h2>
<p>Заказчик получил рабочий и масштабируемый инструмент. Три оператора работают в единой среде одновременно, без расхождения конфигураций и потери контекста между людьми. Скорость и предсказуемость SEO-работ заметно выросли: генерация и оптимизация страниц, техническая проработка, кластеризация запросов идут в общем конвейере.</p>
<h2>Наша роль</h2>
<p>Полный цикл: архитектура, развёртывание инфраструктуры, настройка безопасных подключений, тестирование под нагрузкой и передача инструкций по поддержке и масштабированию. Проект запущен в продакшен и работает.</p>
<div class="cta-horizontal step-up"><div class="cta-horizontal__text"><p class="cta-horizontal__title">Нужна похожая среда или своя инфраструктура под команду?</p></div><a href="{u('/kontakty/')}" class="btn btn--primary">{esc(S['cta_apply'])}</a></div>
'''
    else:
        title = "Case: isolated team dev environment on a VPS | Skill Dev"
        desc = "We built a shared VPS for a distributed SEO team: secure SSH access, a single workspace, and automated SEO pipelines. Three operators work at the same time."
        h1 = "Isolated team dev environment on a VPS"
        lead = "An SEO team needed stable, secure, simultaneous access for several operators to one shared working environment with AI tooling. We built that environment on a dedicated VPS and handed it over to production."
        body = f'''
<div class="case-meta"><span class="case-card__tag">Infrastructure · DevOps</span><span class="case-meta__item">Ubuntu 22.04/24.04 LTS</span><span class="case-meta__item">3 operators at once</span></div>
{img("hero", "Distributed development team workstations")}
<h2>The task</h2>
<p>A team of SEO specialists worked remotely, from different places, but on shared projects. Every operator kept their own toolset on their own machine, configs drifted apart, and the shared context of the work got lost between people.</p>
<p>They needed one stable, secure environment where several operators work at the same time: shared projects, a single Git, shared history, and the same toolset for everyone.</p>
<h2>What we deployed</h2>
<p>On a dedicated VPS (Ubuntu 22.04/24.04 LTS) we built an isolated working environment and set up remote development through Remote-SSH in VS Code. Operators connect to one server and work in a shared project space.</p>
<ul>
<li>A single workspace with shared site projects, Git repositories, and work history.</li>
<li>Three simultaneous SSH connections: two from the client's work machines and one from the lead's PC.</li>
<li>One shared toolset and environment, identical for every operator.</li>
</ul>
<h2>Architecture</h2>
{img("arch", "Diagram: workstations connect to a shared VPS")}
<p>At the center is a dedicated VPS, and the team's workstations from different locations connect to it over secured SSH channels. Everyone works in one user space on the server, so projects, repositories, and history stay shared instead of scattering across personal computers.</p>
<h2>Security</h2>
<p>Access to the server is locked down properly, no passwords and no extra open doors:</p>
<ul>
<li>SSH keys only (ed25519); password authentication disabled.</li>
<li>UFW firewall and fail2ban against brute force and suspicious activity.</li>
<li>Automatic system and security updates.</li>
<li>Only the minimum required ports are open; everything else is closed.</li>
</ul>
<h2>Connection stability</h2>
<p>So long working sessions don't drop, we set up autossh to restore connections automatically and tmux/screen for long-lived sessions. An operator can disconnect and come back exactly where they left off, while background tasks keep running.</p>
{img("rack", "Project server infrastructure")}
<h2>Performance</h2>
<p>For several operators working in parallel and tools with long context, we provisioned resources with headroom: 8–16 vCPU, 32+ GB RAM, SSD. The environment stays responsive even when several people work at once and run heavy jobs.</p>
<h2>SEO automation</h2>
{img("work", "Operator workstation with multiple monitors")}
<p>On top of the environment we built working pipelines for the team's tasks and wired them into familiar tools:</p>
<ul>
<li>Integration with Git and local semantic-core databases.</li>
<li>SEO tools connected: Screaming Frog exports, Ahrefs API, Google Search Console.</li>
<li>Content generation pipelines with uniqueness checks and downstream SEO structuring.</li>
</ul>
<h2>The outcome</h2>
<p>The client got a working, scalable tool. Three operators work in one environment at the same time, without config drift or lost context between people. The speed and predictability of SEO work grew noticeably: page generation and optimization, technical work, and query clustering all run through a shared pipeline.</p>
<h2>Our role</h2>
<p>The full cycle: architecture, infrastructure deployment, secure connection setup, load testing, and handover with support and scaling instructions. The project is in production and running.</p>
<div class="cta-horizontal step-up"><div class="cta-horizontal__text"><p class="cta-horizontal__title">Need a similar environment or your own team infrastructure?</p></div><a href="{u('/kontakty/')}" class="btn btn--primary">{esc(S['cta_apply'])}</a></div>
'''
    bc = f'<nav class="breadcrumbs" aria-label="{esc(S["breadcrumbs"])}"><a href="{u("/")}">{esc(S["home"])}</a><span>/</span><a href="{u("/kejsy/")}">{esc(S["cases_h1"])}</a><span>/</span><span aria-current="page">{esc(h1)}</span></nav>'
    ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":h1,"inLanguage":lang,"image":SITE+"/assets/ui/og-cover.png","author":{"@type":"Organization","name":"Skill Dev"},"publisher":{"@type":"Organization","name":"Skill Dev"},"mainEntityOfPage":SITE+url}, ensure_ascii=False)
    doc = f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  {head_common()}
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<meta http-equiv="content-language" content="{lang}">{noindex}
<link rel="canonical" href="{SITE}{url}">
<meta property="og:title" content="{esc(h1)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="article"><meta property="og:url" content="{SITE}{url}"><meta property="og:image" content="{SITE}/assets/img/case-vps-hero{sfx}.jpg"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ld}</script>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Sumana&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/css/styles.css')}?v=10"><link rel="stylesheet" href="{u('/css/pages.css')}?v=10"></head>
<body class="inner-page">{header_html(lang)}
<main class="page-main page-article">
<section class="page-hero"><div class="container">{bc}
<h1 class="heading1 page-hero__title">{esc(h1)}</h1>
<div class="page-hero__lead"><p>{esc(lead)}</p></div></div></section>
<div class="container page-content">{body}</div>
</main>{footer_html(lang)}<script src="{u('/js/main.js')}?v=10"></script></body></html>'''
    d = os.path.join(ROOT, 'kejsy', 'claude-vps-sreda')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, out_html_name(lang)), 'w', encoding='utf-8').write(doc)


def build_sitemap(urls):
    import datetime
    today = datetime.date.today().isoformat()
    items = ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod></url>' for p in urls)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE}/</loc><lastmod>{today}</lastmod></url>{items}</urlset>')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(
        f"User-agent: *\n{'Disallow: /' if NOINDEX else 'Allow: /'}\nSitemap: {SITE}/sitemap.xml\n")

def patch_home(lang="ru"):
    """Единые header/footer на главной. Для EN читает index.en.html если есть, иначе копирует RU."""
    name = out_html_name(lang)
    p = os.path.join(ROOT, name)
    if lang == "en" and not os.path.isfile(p):
        # bootstrap from RU once; content translation lives in index.en.html separately
        src = os.path.join(ROOT, "index.html")
        if not os.path.isfile(src):
            print("skip EN home: no index.html", file=sys.stderr)
            return
        open(p, "w", encoding="utf-8").write(open(src, encoding="utf-8").read())
    if not os.path.isfile(p):
        print(f"skip home {lang}: missing {p}", file=sys.stderr)
        return
    h = open(p, encoding='utf-8').read()
    if NOINDEX:
        if 'name="robots"' not in h:
            h = h.replace('</title>', '</title>\n  <meta name="robots" content="noindex,nofollow">')
    else:
        h = re.sub(r'\s*<meta name="robots" content="noindex,nofollow">(<!--[^>]*-->)?', '', h)
        h = re.sub(r'\s*<!--[^>]*снять при запуске[^>]*-->', '', h)
    if 'yandex-verification' not in h:
        h = h.replace('</head>', '  ' + head_common() + '\n</head>')
    h = re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{lang}"', h, count=1)
    if 'http-equiv="content-language"' not in h:
        h = h.replace('<meta charset="UTF-8">',
                      f'<meta charset="UTF-8">\n  <meta http-equiv="content-language" content="{lang}">', 1)
    else:
        h = re.sub(r'content-language" content="[^"]*"', f'content-language" content="{lang}"', h, count=1)
    h = re.sub(r'<header class="header[^"]*" id="siteHeader">.*?</header>', header_html(lang), h, count=1, flags=re.S)
    h = re.sub(r'<footer class="footer">.*?</footer>', footer_html(lang), h, count=1, flags=re.S)
    h = re.sub(r'href="[^"]*css/(styles|pages)\.css[^"]*"', lambda m: f'href="{u("/css/"+m.group(1)+".css")}?v=10"', h)
    h = re.sub(r'src="[^"]*/js/main\.js[^"]*"', f'src="{u("/js/main.js")}?v=10"', h)
    h = re.sub(
        r'  <link rel="icon" href="[^"]*" sizes="48x48">\n'
        r'  <link rel="icon" type="image/png" sizes="32x32" href="[^"]*">\n'
        r'  <link rel="icon" type="image/png" sizes="192x192" href="[^"]*">\n'
        r'  <link rel="apple-touch-icon" href="[^"]*">',
        favicon_links_html().rstrip(),
        h,
        count=1,
    )
    h = re.sub(r'\s*<!-- Yandex\.Metrika counter -->.*?<!-- /Yandex\.Metrika counter -->\s*', '\n', h, flags=re.S)
    if '110912791' not in h:
        h = h.replace('</head>', '\n' + yandex_metrika_html() + '\n</head>')
    open(p, 'w', encoding='utf-8').write(h)
    print(f'patched {name} (header/footer unified, lang={lang})')

if __name__ == '__main__':
    urls = ['/uslugi/', '/kontakty/', '/kejsy/', '/kejsy/claude-vps-sreda/']
    for lang in ("ru", "en"):
        patch_home(lang)
        build_uslugi_catalog(lang)
        build_kontakty(lang)
        build_cases_hub(lang)
        build_case_vps(lang)
        for slug in PAGES:
            built = build_page(slug, lang)
            if built and lang == "ru":
                urls.append(built)
                print('built', lang, built)
            elif built:
                print('built', lang, built)
    # unique preserve order
    seen, uniq = set(), []
    for p in urls:
        if p not in seen:
            seen.add(p); uniq.append(p)
    build_404()
    build_sitemap(uniq)
    print(f'\nDONE: {len(uniq)} URLs · BASE={BASE!r} · NOINDEX={NOINDEX}')
