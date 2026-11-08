/* GalA-Consult site script: header, menu, rotating globe, waving flags, copy buttons */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };

  /* ---------- header state ---------- */
  var hdr = document.querySelector('.hdr');
  function onScroll() { if (hdr) hdr.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  function setMenu(open) {
    if (!burger || !menu) return;
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    menu.hidden = !open;
    document.body.classList.toggle('menu-open', open);
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(burger.getAttribute('aria-expanded') !== 'true'); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 900) setMenu(false); });
  }

  /* ---------- active section in nav (home) ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  if (navLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    navLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        navLinks.forEach(function (l) { l.classList.remove('is-active'); });
        var a = map[en.target.id];
        if (a) a.classList.add('is-active');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Array.prototype.forEach.call(document.querySelectorAll('main > section'), function (s) { io.observe(s); });
  }

  /* ---------- request form (modal) ---------- */
  var modal = document.getElementById('rq');
  if (modal) {
    var panel = modal.querySelector('.modal__panel');
    var form = modal.querySelector('form.rq');
    var done = modal.querySelector('.done');
    var sendBtn = form.querySelector('.rq__send');
    var fail = form.querySelector('.rq__fail');
    var opener = null, timers = [], busy = false, finished = false;
    var LIVE = /(^|\.)galaconsult\.kz$/i.test(location.hostname) || /\.netlify\.app$/i.test(location.hostname);
    var q = function (sel) { return modal.querySelector(sel); };
    var focusables = function () {
      return Array.prototype.filter.call(modal.querySelectorAll('button, [href], input:not([type="hidden"]):not([tabindex="-1"]), select, textarea'), function (el) {
        return !el.disabled && el.offsetParent !== null && !el.closest('[hidden]');
      });
    };
    var clearTimers = function () { timers.forEach(clearTimeout); timers = []; };
    var reset = function () {
      clearTimers();
      modal.classList.remove('st-1', 'st-2', 'st-3', 'st-4', 'st-5');
      form.hidden = false; done.hidden = true; done.classList.remove('is-in');
      panel.style.height = '';
      sendBtn.classList.remove('is-loading');
      fail.hidden = true;
      busy = false;
      if (finished) { form.reset(); finished = false; }
      Array.prototype.forEach.call(form.querySelectorAll('.is-bad'), function (el) { el.classList.remove('is-bad'); });
      Array.prototype.forEach.call(form.querySelectorAll('.field__err, .topics__err'), function (el) { el.textContent = ''; });
    };
    var open = function (trigger) {
      reset();
      opener = trigger || null;
      var topic = trigger && trigger.getAttribute('data-topic');
      if (topic) {
        Array.prototype.forEach.call(form.querySelectorAll('input[name="topic"]'), function (r) { r.checked = (r.value === topic); });
      }
      form.elements.project.value = (trigger && trigger.getAttribute('data-project')) || '';
      form.elements.page.value = document.title;
      modal.hidden = false;
      document.documentElement.classList.add('modal-open');
      void modal.offsetWidth;
      modal.classList.add('is-open');
      setTimeout(function () { var f = form.elements.name; if (f) f.focus({ preventScroll: true }); }, 60);
    };
    var close = function () {
      if (modal.hidden) return;
      modal.classList.remove('is-open');
      document.documentElement.classList.remove('modal-open');
      setTimeout(function () { modal.hidden = true; reset(); }, reduce ? 0 : 360);
      if (opener && opener.focus) opener.focus({ preventScroll: true });
    };
    document.addEventListener('click', function (e) {
      var t = e.target.closest('[data-form]');
      if (t) { e.preventDefault(); open(t); return; }
      if (!modal.hidden && e.target.closest('[data-close]')) { e.preventDefault(); close(); }
    });
    document.addEventListener('keydown', function (e) {
      if (modal.hidden) return;
      if (e.key === 'Escape') { close(); return; }
      if (e.key === 'Tab') {
        var f = focusables(); if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    var setErr = function (name, msg) {
      var box = name === 'topic' ? q('#f-topic') : q('#f-' + name);
      if (!box) return;
      box.classList.toggle('is-bad', !!msg);
      var out = box.querySelector('.field__err, .topics__err'); if (out) out.textContent = msg || '';
    };
    var validate = function () {
      var ok = true, firstBad = null;
      var name = form.elements.name.value.trim();
      var contact = form.elements.contact.value.trim();
      var topic = form.querySelector('input[name="topic"]:checked');
      if (!name) { setErr('name', 'Укажите имя'); ok = false; firstBad = firstBad || form.elements.name; } else setErr('name', '');
      var digits = contact.replace(/\D/g, '').length;
      var isMail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(contact);
      if (!contact) { setErr('contact', 'Укажите телефон или email, чтобы мы могли ответить'); ok = false; firstBad = firstBad || form.elements.contact; }
      else if (!isMail && digits < 7) { setErr('contact', 'Проверьте номер телефона или адрес почты'); ok = false; firstBad = firstBad || form.elements.contact; }
      else setErr('contact', '');
      if (!topic) { setErr('topic', 'Выберите тему запроса'); ok = false; firstBad = firstBad || form.querySelector('input[name="topic"]'); } else setErr('topic', '');
      if (firstBad) firstBad.focus();
      return ok;
    };
    ['name', 'contact'].forEach(function (n) {
      form.elements[n].addEventListener('input', function () { if (q('#f-' + n).classList.contains('is-bad')) setErr(n, ''); });
    });
    form.addEventListener('change', function (e) { if (e.target.name === 'topic') setErr('topic', ''); });
    var send = function () {
      var t = form.querySelector('input[name="topic"]:checked');
      form.elements.subject.value = 'Запрос с сайта: ' + (t ? t.value : 'без темы') + ' - ' + form.elements.name.value.trim();
      if (!LIVE) return new Promise(function (res) { setTimeout(function () { res(true); }, 450); });
      var body = new URLSearchParams(new FormData(form)).toString();
      return fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body })
        .then(function (r) { return r.ok; }, function () { return false; });
    };
    var at = function (ms, fn) { timers.push(setTimeout(fn, ms)); };
    var showDone = function () {
      var h0 = panel.offsetHeight;
      form.hidden = true; done.hidden = false;
      var h1 = done.offsetHeight;
      panel.style.height = h0 + 'px';
      void panel.offsetHeight;
      panel.style.height = h1 + 'px';
      at(520, function () { panel.style.height = ''; });
      requestAnimationFrame(function () { done.classList.add('is-in'); });
      var b = done.querySelector('.btn'); if (b) setTimeout(function () { b.focus({ preventScroll: true }); }, 700);
    };
    var play = function () {
      var fd = new FormData(form);
      var topicEl = form.querySelector('input[name="topic"]:checked');
      q('[data-fx="topic"]').textContent = 'Запрос: ' + (topicEl ? topicEl.value : '');
      q('[data-fx="name"]').textContent = (fd.get('name') || '').toString().trim();
      q('[data-fx="company"]').textContent = (fd.get('company') || '').toString().trim();
      q('[data-fx="who"]').textContent = (fd.get('name') || '').toString().trim().split(/\s+/)[0] || '';
      finished = true;
      if (reduce) { showDone(); return; }
      panel.style.height = panel.offsetHeight + 'px';
      var env = q('.fx__env');
      var w = panel.clientWidth, h = panel.clientHeight;
      env.style.setProperty('--dx', Math.round(w * .44) + 'px');
      env.style.setProperty('--dy', Math.round(-h * .5) + 'px');
      var trail = q('.fx__trail'), tp = trail.querySelector('path');
      trail.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
      tp.setAttribute('d', 'M' + (w * .5) + ',' + (h * .56) + ' C' + (w * .64) + ',' + (h * .54) + ' ' + (w * .84) + ',' + (h * .4) + ' ' + (w * .94) + ',' + (h * .06));
      modal.classList.add('st-1');
      at(480, function () { modal.classList.add('st-2'); });
      at(1150, function () { modal.classList.add('st-3'); });
      at(2150, function () { modal.classList.add('st-4'); });
      at(3150, function () { modal.classList.add('st-5'); showDone(); });
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (busy) return;
      fail.hidden = true;
      if (!validate()) return;
      busy = true;
      sendBtn.classList.add('is-loading');
      send().then(function (ok) {
        sendBtn.classList.remove('is-loading');
        if (ok) { play(); }
        else { busy = false; fail.hidden = false; }
      });
    });
  }

  /* ---------- waving flags (canvas) ---------- */
  var flags = Array.prototype.slice.call(document.querySelectorAll('.flag[data-src]'));
  if (flags.length && !reduce && document.createElement('canvas').getContext) {
    var states = [];
    var anyVisible = true;
    flags.forEach(function (el, i) {
      var canvas = el.querySelector('canvas');
      if (!canvas) return;
      var s = { el: el, canvas: canvas, ctx: canvas.getContext('2d'), img: new Image(), ready: false, off: null, seed: i * 1.9, W: 0, H: 0, A: 0, fh: 0 };
      s.img.decoding = 'async';
      s.img.onload = function () { s.ready = true; sizeFlag(s); drawFlag(s, performance.now() / 1000); el.classList.add('is-live'); };
      s.img.src = el.getAttribute('data-src');
      states.push(s);
    });
    var sizeFlag = function (s) {
      var r = s.el.getBoundingClientRect();
      var dpr = Math.min(2, window.devicePixelRatio || 1);
      var fw = Math.max(1, Math.round(r.width * dpr)), fh = Math.max(1, Math.round(r.height * dpr));
      var A = Math.round(fh * 0.1);
      s.W = fw; s.H = fh + 2 * A; s.A = A; s.fh = fh;
      s.canvas.width = s.W; s.canvas.height = s.H;
      var off = document.createElement('canvas'); off.width = fw; off.height = fh;
      var octx = off.getContext('2d');
      octx.drawImage(s.img, 0, 0, fw, fh);
      s.off = off;
    };
    var drawFlag = function (s, t) {
      var ctx = s.ctx, W = s.W, A = s.A, fh = s.fh, x, u, k, ph, dy;
      ctx.clearRect(0, 0, W, s.H);
      var amp = A * 0.72;
      for (x = 0; x < W; x++) {
        u = x / W; k = 0.12 + 0.88 * u;
        ph = u * 2.1 * Math.PI - t * 2.2 + s.seed;
        dy = Math.sin(ph) * amp * k + u * A * 0.18;
        ctx.drawImage(s.off, x, 0, 1, fh, x, A + dy, 1, fh);
      }
      ctx.globalCompositeOperation = 'source-atop';
      for (x = 0; x < W; x += 2) {
        u = x / W; k = 0.12 + 0.88 * u;
        ph = u * 2.1 * Math.PI - t * 2.2 + s.seed;
        var shade = Math.cos(ph) * k;
        ctx.fillStyle = shade > 0 ? 'rgba(255,255,255,' + (shade * 0.16).toFixed(3) + ')' : 'rgba(6,16,40,' + (-shade * 0.2).toFixed(3) + ')';
        ctx.fillRect(x, 0, 2, s.H);
      }
      ctx.globalCompositeOperation = 'source-over';
    };
    var wrapEl = document.querySelector('.flags');
    if (wrapEl && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { anyVisible = es[0].isIntersecting; }, { rootMargin: '120px' }).observe(wrapEl);
    }
    var lastF = 0;
    var flagTick = function (now) {
      if (anyVisible && !document.hidden && now - lastF > 30) {
        lastF = now;
        var t = now / 1000;
        for (var i = 0; i < states.length; i++) if (states[i].ready) drawFlag(states[i], t);
      }
      raf(flagTick);
    };
    raf(flagTick);
    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { var t = performance.now() / 1000; states.forEach(function (s) { if (s.ready) { sizeFlag(s); drawFlag(s, t); } }); }, 150);
    });
  }

  /* ---------- map: stop SMIL motion for reduced motion ---------- */
  if (reduce) {
    Array.prototype.forEach.call(document.querySelectorAll('svg[data-smil]'), function (svg) {
      if (svg.pauseAnimations) { svg.pauseAnimations(); }
      Array.prototype.forEach.call(svg.querySelectorAll('.route-dot'), function (d) { d.style.display = 'none'; });
    });
  }

  /* ---------- copy buttons ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-copy]'), function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var done = function () {
        btn.classList.add('is-done');
        btn.setAttribute('aria-label', 'Скопировано');
        setTimeout(function () { btn.classList.remove('is-done'); btn.setAttribute('aria-label', 'Скопировать'); }, 1600);
      };
      var fallback = function () {
        var target = document.getElementById(btn.getAttribute('aria-controls'));
        if (target && window.getSelection) {
          var range = document.createRange(); range.selectNodeContents(target);
          var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
        }
      };
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, fallback);
        } else { fallback(); }
      } catch (e) { fallback(); }
    });
  });
})();
