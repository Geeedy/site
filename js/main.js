(function () {
  'use strict';

  const pageLang = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase() === 'en' ? 'en' : 'ru';

  // Drop legacy same-URL language cookies (no longer used).
  try {
    document.cookie = 'sd_lang=;path=/;max-age=0;SameSite=Lax';
    document.cookie = 'sd_lang=;path=/site;max-age=0;SameSite=Lax';
    localStorage.removeItem('sd_lang');
    localStorage.removeItem('sd_lang_explicit');
  } catch (_) { /* ignore */ }

  const ASSETS = (() => {
    const base = document.querySelector('link[href*="css/styles.css"]')?.getAttribute('href') || '';
    const root = base.replace(/\/css\/styles\.css.*$/, '') || '';
    return `${root}/assets/hero`;
  })();

  const heroTabLabels = pageLang === 'en'
    ? ['E-commerce', 'B2B', 'Finance', 'Other industries']
    : ['E-commerce', 'B2B', 'Финансы', 'Другие отрасли'];

  const heroSlides = [
    { tab: heroTabLabels[0], color: '#0066FF', slide: `${ASSETS}/healthcare-ui-animated.svg`, time: 5000 },
    { tab: heroTabLabels[1], color: '#6F00FF', slide: `${ASSETS}/insurance-ui-animated.svg`, time: 5000 },
    { tab: heroTabLabels[2], color: '#00A6FF', slide: `${ASSETS}/lending-ui-animated.svg`, time: 5000 },
    { tab: heroTabLabels[3], color: '#4000FF', slide: `${ASSETS}/more-industries-ui-animated.svg`, time: 10000 },
  ];

  // Animated hero background (svgator waves)
  initHeroBackground();

  async function initHeroBackground() {
    const wrap = document.querySelector('.wp-hts-bg-wrapper');
    if (!wrap) return;
    try {
      const bgSrc = `${ASSETS}/home-background.svg`;
      const res = await fetch(bgSrc);
      if (!res.ok) throw new Error('bg fetch failed');
      const text = await res.text();
      const doc = new DOMParser().parseFromString(text, 'image/svg+xml');
      const svg = doc.documentElement;
      const scriptEl = doc.querySelector('script');
      wrap.appendChild(document.importNode(svg, true));
      const svgNode = wrap.querySelector('svg');
      if (svgNode) {
        svgNode.classList.add('wp-hts-bg-img');
        svgNode.setAttribute('preserveAspectRatio', 'xMidYMid slice');
        svgNode.style.width = '100%';
        svgNode.style.height = '100%';
      }
      if (scriptEl?.textContent) {
        const runner = document.createElement('script');
        runner.textContent = scriptEl.textContent;
        document.body.appendChild(runner);
      }
    } catch {
      wrap.innerHTML = `<iframe class="wp-hts-bg-img" src="${ASSETS}/home-background.svg" title="" tabindex="-1"></iframe>`;
    }
  }

  // Header scroll + transparent
  const header = document.querySelector('.header');
  const isHome = document.body.classList.contains('home-page');
  const updateHeader = () => {
    const scrolled = window.scrollY > 80;
    header?.classList.toggle('scrolled', scrolled);
    header?.classList.toggle('header-transparent', isHome && !scrolled);
  };
  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();

  // Mobile menu
  document.getElementById('menuToggle')?.addEventListener('click', () => {
    document.getElementById('mainNav')?.classList.toggle('open');
    document.body.classList.toggle('menu-open');
  });

  // Step-up scroll reveal (scnsoft waypoint pattern)
  const stepEls = document.querySelectorAll('.step-up');
  const stepObserver = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        stepObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
  stepEls.forEach((el) => stepObserver.observe(el));

  // Counter animation
  document.querySelectorAll('[data-count]').forEach((el) => {
    const target = el.dataset.count;
    const isNum = /^\d/.test(target);
    const observer = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) return;
      if (!isNum) { el.textContent = target; observer.disconnect(); return; }
      const num = parseInt(target.replace(/\D/g, ''), 10);
      const suffix = target.replace(/[\d]/g, '');
      const duration = 1800;
      const start = performance.now();
      const tick = (now) => {
        const p = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.floor(num * eased) + suffix;
        if (p < 1) requestAnimationFrame(tick);
        else el.textContent = target;
      };
      requestAnimationFrame(tick);
      observer.disconnect();
    }, { threshold: 0.5 });
    observer.observe(el);
  });

  // Hero industry slider — scnsoft wp-hts logic
  const tabsEl = document.getElementById('heroTabs');
  const slidesEl = document.getElementById('heroSlides');
  const overlayEl = document.getElementById('heroOverlay');
  let heroIndex = 0;
  let heroTimer;
  let slideObjects = [];

  async function loadSlideSvg(el, src) {
    if (!el || el.dataset.loaded) return;
    try {
      const res = await fetch(src);
      if (!res.ok) throw new Error('slide fetch failed');
      const text = await res.text();
      const doc = new DOMParser().parseFromString(text, 'image/svg+xml');
      const svg = doc.documentElement;
      const scriptEl = doc.querySelector('script');
      el.replaceChildren(document.importNode(svg, true));
      const svgNode = el.querySelector('svg');
      if (svgNode) {
        svgNode.setAttribute('preserveAspectRatio', 'xMidYMid slice');
        svgNode.style.width = '100%';
        svgNode.style.height = '100%';
        svgNode.style.display = 'block';
      }
      if (scriptEl?.textContent) {
        const runner = document.createElement('script');
        runner.textContent = scriptEl.textContent;
        document.body.appendChild(runner);
      }
      el.dataset.loaded = '1';
    } catch {
      el.replaceChildren(Object.assign(document.createElement('img'), { src, alt: '' }));
      el.dataset.loaded = '1';
    }
  }

  function restartProgress(btn, ms) {
    btn.style.setProperty('--tab-time', ms + 'ms');
    const block = btn.querySelector('.wp-hts-tab-progress-block');
    if (!block) return;
    block.style.animation = 'none';
    block.offsetHeight;
    block.style.animation = '';
  }

  function goHero(i, manual) {
    const prev = heroIndex;
    heroIndex = i;
    const s = heroSlides[i];

    tabsEl?.querySelectorAll('.wp-hts-tab').forEach((t, idx) => {
      t.classList.toggle('active', idx === i);
      if (idx === i) restartProgress(t, s.time);
    });

    slideObjects.forEach((slideEl, idx) => {
      slideEl.classList.remove('active', 'deactive');
      if (idx === i) {
        loadSlideSvg(slideEl, s.slide);
        slideEl.classList.add('active');
      } else if (idx === prev && prev !== i) {
        slideEl.classList.add('deactive');
      }
    });

    if (overlayEl) overlayEl.style.backgroundColor = s.color;

    clearTimeout(heroTimer);
    heroTimer = setTimeout(() => goHero((i + 1) % heroSlides.length, false), s.time);

    // Prefetch next slide
    const next = heroSlides[(i + 1) % heroSlides.length];
    if (slideObjects[(i + 1) % heroSlides.length]) {
      loadSlideSvg(slideObjects[(i + 1) % heroSlides.length], next.slide);
    }
  }

  if (tabsEl && slidesEl) {
    heroSlides.forEach((s, i) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'wp-hts-tab' + (i === 0 ? ' active' : '');
      btn.innerHTML = `${s.tab}<span class="wp-hts-tab-progress-wrap"><span class="wp-hts-tab-progress-block"><span class="wp-hts-tab-progress"></span></span></span>`;
      btn.addEventListener('click', () => goHero(i, true));
      tabsEl.appendChild(btn);

      const slideEl = document.createElement('div');
      slideEl.className = 'wp-hts-slide-img' + (i === 0 ? ' active' : '');
      slideEl.setAttribute('role', 'img');
      slideEl.setAttribute('aria-label', s.tab);
      slideEl.dataset.src = s.slide;
      slidesEl.appendChild(slideEl);
      slideObjects.push(slideEl);
    });

    document.getElementById('heroPrev')?.addEventListener('click', () => {
      goHero((heroIndex - 1 + heroSlides.length) % heroSlides.length, true);
    });
    document.getElementById('heroNext')?.addEventListener('click', () => {
      goHero((heroIndex + 1) % heroSlides.length, true);
    });

    goHero(0, false);
  }

  // Logo drag carousel (owl-style)
  const logoSlider = document.getElementById('logoSlider');
  const swlWrap = logoSlider?.closest('.swl');
  if (logoSlider && swlWrap) {
    let offset = 0;
    let startX = 0;
    let dragging = false;
    let maxOffset = 0;

    const recalc = () => {
      const wrapW = swlWrap.clientWidth;
      const trackW = logoSlider.scrollWidth;
      maxOffset = Math.max(0, trackW - wrapW);
      offset = Math.min(offset, maxOffset);
      offset = Math.max(0, offset);
      logoSlider.style.transform = `translateX(-${offset}px)`;
    };

    const onDown = (x) => {
      dragging = true;
      startX = x - offset;
      swlWrap.classList.add('is-dragging');
    };

    const onMove = (x) => {
      if (!dragging) return;
      offset = Math.min(maxOffset, Math.max(0, startX - x));
      logoSlider.style.transform = `translateX(-${offset}px)`;
    };

    const onUp = (e) => {
      if (!dragging) return;
      dragging = false;
      swlWrap.classList.remove('is-dragging');
    };

    swlWrap.addEventListener('mousedown', (e) => onDown(e.clientX));
    window.addEventListener('mousemove', (e) => onMove(e.clientX));
    window.addEventListener('mouseup', onUp);
    swlWrap.addEventListener('touchstart', (e) => onDown(e.touches[0].clientX), { passive: true });
    swlWrap.addEventListener('touchmove', (e) => onMove(e.touches[0].clientX), { passive: true });
    swlWrap.addEventListener('touchend', onUp);
    window.addEventListener('resize', recalc);
    recalc();
  }

  // Service list tabs
  const sliItems = document.querySelectorAll('.sli-details');
  const sliArticles = document.querySelectorAll('.sli-article');
  sliItems.forEach((item) => {
    item.querySelector('.sli-summary')?.addEventListener('click', () => {
      const id = item.dataset.item;
      sliItems.forEach((i) => i.classList.remove('active'));
      sliArticles.forEach((a) => a.classList.remove('active'));
      item.classList.add('active');
      document.querySelector(`.sli-article[data-item="${id}"]`)?.classList.add('active');
    });
  });

  // Tech tabs
  document.querySelectorAll('.tech-tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      const t = tab.dataset.tech;
      document.querySelectorAll('.tech-tab').forEach((x) => x.classList.remove('active'));
      document.querySelectorAll('.tech-panel').forEach((x) => x.classList.remove('active'));
      tab.classList.add('active');
      document.querySelector(`[data-tech-panel="${t}"]`)?.classList.add('active');
    });
  });

  // Case study filters
  const csdTabs = document.querySelectorAll('.csd-tab');
  const storyCards = document.querySelectorAll('#storiesGrid .story-card');
  let activeFilter = 'all';

  function applyStoryFilter(filter) {
    activeFilter = filter;
    storyCards.forEach((card) => {
      const tags = (card.dataset.tags || '').split(/\s+/);
      const match = filter === 'all' || tags.includes(filter);
      card.classList.toggle('is-filtered-out', !match);
      if (!match) card.classList.remove('story-card--visible');
    });
    updateLoadMoreVisibility();
  }

  csdTabs.forEach((btn) => {
    btn.addEventListener('click', () => {
      csdTabs.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      applyStoryFilter(btn.dataset.filter || 'all');
    });
  });

  function updateLoadMoreVisibility() {
    const btn = document.getElementById('loadMoreStories');
    if (!btn) return;
    const hidden = [...storyCards].filter((c) =>
      !c.classList.contains('is-filtered-out') && c.classList.contains('story-card--hidden')
    );
    btn.style.display = hidden.length ? '' : 'none';
  }

  document.getElementById('loadMoreStories')?.addEventListener('click', () => {
    storyCards.forEach((card) => {
      if (!card.classList.contains('is-filtered-out') && card.classList.contains('story-card--hidden')) {
        card.classList.remove('story-card--hidden');
        card.classList.add('story-card--visible');
      }
    });
    updateLoadMoreVisibility();
  });
  updateLoadMoreVisibility();

  // FAQ
  document.querySelectorAll('.faq-item').forEach((item) => {
    item.querySelector('.faq-question')?.addEventListener('click', () => {
      const open = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach((i) => i.classList.remove('open'));
      if (!open) item.classList.add('open');
    });
  });

  // Testimonials photo carousel
  const track = document.getElementById('testimonialsTrack');
  const testPrev = document.getElementById('testPrev');
  const testNext = document.getElementById('testNext');
  let testIndex = 0;

  if (track) {
    const cards = [...track.children];
    const visibleCount = () => (window.innerWidth < 768 ? 1 : window.innerWidth < 1279 ? 2 : 3);

    function goTestimonial(i) {
      const vis = visibleCount();
      const max = Math.max(0, cards.length - vis);
      testIndex = Math.min(Math.max(0, i), max);
      const card = cards[0];
      const gap = 24;
      const step = card ? card.offsetWidth + gap : 0;
      track.style.transform = `translateX(-${testIndex * step}px)`;
    }

    testPrev?.addEventListener('click', () => goTestimonial(testIndex - 1));
    testNext?.addEventListener('click', () => goTestimonial(testIndex + 1));
    window.addEventListener('resize', () => goTestimonial(testIndex));
    setInterval(() => goTestimonial(testIndex + 1 >= cards.length - visibleCount() + 1 ? 0 : testIndex + 1), 7000);
  }

  // Chat widget
  const chatPanel = document.getElementById('chatPanel');
  const chatTeaser = document.getElementById('chatTeaser');
  document.getElementById('chatOpen')?.addEventListener('click', () => {
    chatPanel?.classList.add('open');
    chatTeaser?.classList.remove('visible');
  });
  document.getElementById('chatClose')?.addEventListener('click', () => chatPanel?.classList.remove('open'));
  document.getElementById('chatTeaserClose')?.addEventListener('click', (e) => {
    e.stopPropagation();
    chatTeaser?.classList.remove('visible');
  });
  chatTeaser?.addEventListener('click', () => {
    chatPanel?.classList.add('open');
    chatTeaser?.classList.remove('visible');
  });

  // Contact form → Telegram leads bot via /api/lead
  const contactForm = document.getElementById('contactForm');
  contactForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;

    const btn = form.querySelector('button[type="submit"]');
    const successEl = form.querySelector('.form-success');
    const fieldsEl = form.querySelector('.form-fields') || form;

    const i18n = pageLang === 'en'
      ? {
          ok: 'Your request has been sent. A manager will contact you shortly.',
          err: 'Could not send the request. Please try again or email hello@skill-dev.ai',
          sending: 'Sending…',
        }
      : {
          ok: 'Заявка отправлена. Менеджер свяжется с вами в ближайшее время.',
          err: 'Не удалось отправить заявку. Попробуйте ещё раз или напишите на hello@skill-dev.ai',
          sending: 'Отправка…',
        };

    const nameInput = form.querySelector('[name="name"]');
    const contactInput = form.querySelector('[name="contact"]');
    const messageInput = form.querySelector('[name="message"], #msg');

    const name = (nameInput && 'value' in nameInput ? nameInput.value : '').trim();
    const contact = (contactInput && 'value' in contactInput ? contactInput.value : '').trim();
    const message = (messageInput && 'value' in messageInput ? messageInput.value : '').trim();
    if (!name || !contact || !message) return;

    const prevLabel = btn ? btn.textContent : '';
    if (btn) {
      btn.disabled = true;
      btn.textContent = i18n.sending;
    }

    const apiBase = (() => {
      const base = document.querySelector('link[href*="css/styles.css"]')?.getAttribute('href') || '';
      const root = base.replace(/\/css\/styles\.css.*$/, '') || '';
      return root;
    })();

    try {
      const res = await fetch(`${apiBase}/api/lead`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, contact, message, lang: pageLang }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || !data.ok) throw new Error(data.error || 'fail');

      form.reset();
      if (successEl) {
        successEl.hidden = false;
        successEl.classList.remove('form-success--error');
        successEl.textContent = i18n.ok;
      } else {
        const note = document.createElement('p');
        note.className = 'form-success';
        note.textContent = i18n.ok;
        fieldsEl.appendChild(note);
      }
      form.querySelectorAll('.form-group, .form-row, button[type="submit"], .form-honeypot').forEach((el) => {
        el.hidden = true;
      });
    } catch (_) {
      if (successEl) {
        successEl.hidden = false;
        successEl.classList.add('form-success--error');
        successEl.textContent = i18n.err;
      } else {
        alert(i18n.err);
      }
      if (btn) {
        btn.disabled = false;
        btn.textContent = prevLabel;
      }
    }
  });

  // Cookies
  const cookieBanner = document.getElementById('cookieBanner');
  if (!localStorage.getItem('cookiesAccepted')) cookieBanner?.classList.add('visible');
  document.getElementById('cookieAccept')?.addEventListener('click', () => {
    localStorage.setItem('cookiesAccepted', '1');
    cookieBanner?.classList.remove('visible');
  });
  document.getElementById('cookieDecline')?.addEventListener('click', () => {
    localStorage.setItem('cookiesAccepted', '0');
    cookieBanner?.classList.remove('visible');
  });
})();
