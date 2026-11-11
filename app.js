/* Gmail Cleaner PWA — talks directly to the Gmail API from the browser.
   Auth: Google Identity Services token client (access token lives ~1 hour). */
(() => {
  'use strict';

  const SCOPE = 'https://mail.google.com/'; // required for permanent delete
  const API = 'https://gmail.googleapis.com/gmail/v1/users/me';
  const PAGE_SIZE = 25;
  const CONCURRENCY = 8;

  /* ---------------- i18n ---------------- */
  const I18N = {
    en: {
      appName: 'Gmail Cleaner', install: 'Install', refresh: 'Refresh', settings: 'Settings', signOut: 'Sign out',
      offline: "You're offline — connect to load or delete mail.",
      setupTitle: 'One-time setup',
      setupBody: "Paste the OAuth Client ID (Web application) from your Google Cloud project. It's saved on this device only.",
      clientId: 'Client ID', setupOrigin: 'Authorized JavaScript origin to add in Google Cloud:', save: 'Save',
      signInTitle: 'Clean your Gmail', signInBody: 'Sign in to view and permanently delete mail in Trash and Spam.',
      signIn: 'Sign in with Google', privacy: 'Runs entirely on your device — it talks only to Google.',
      trash: 'Trash', spam: 'Spam', selectAll: 'Select all', deleteSelected: 'Delete',
      emptyFolder: 'Nothing here. All clean.', loadMore: 'Load more', cancel: 'Cancel', deleteForever: 'Delete forever',
      deleting: 'Deleting…', emptyTrash: 'Empty Trash now', emptySpam: 'Empty Spam now',
      confirmDelTitle: 'Delete {n} email(s) forever?',
      confirmDelBody: 'They will be permanently removed from Gmail. This cannot be undone.',
      confirmEmptyTitle: 'Empty {folder}?',
      confirmEmptyBody: 'All {n} emails in {folder} will be permanently deleted. This cannot be undone.',
      deletedN: 'Deleted {n} email(s).', emptied: '{folder} emptied — {n} deleted.',
      partial: 'Stopped after deleting {n}.', progress: '{done} of {total}',
      sessionExpired: 'Your session expired (Google sign-ins last 1 hour). Sign in again to continue.',
      popupClosed: 'The sign-in window was closed.',
      scopeMissing: "Gmail access wasn't granted. Sign in again and allow full Gmail access — it's needed to delete permanently.",
      gisFail: "Couldn't load Google sign-in. Check your connection.",
      networkError: 'Network error — try again.', noSubject: '(no subject)', unknownSender: '(unknown sender)',
      invalidClient: "That doesn't look like a Client ID (it should end in .apps.googleusercontent.com).",
      saved: 'Saved.', alreadyEmpty: '{folder} is already empty.'
    },
    ar: {
      appName: 'منظّف Gmail', install: 'تثبيت', refresh: 'تحديث', settings: 'الإعدادات', signOut: 'تسجيل الخروج',
      offline: 'أنت غير متصل — اتصل بالإنترنت لعرض الرسائل أو حذفها.',
      setupTitle: 'إعداد لمرة واحدة',
      setupBody: 'الصق معرّف عميل OAuth (تطبيق ويب) من مشروعك في Google Cloud. يُحفظ على هذا الجهاز فقط.',
      clientId: 'معرّف العميل (Client ID)', setupOrigin: 'المصدر المصرّح به (Authorized JavaScript origin) لإضافته في Google Cloud:', save: 'حفظ',
      signInTitle: 'نظّف بريدك في Gmail', signInBody: 'سجّل الدخول لعرض رسائل المهملات وغير المرغوب فيه وحذفها نهائيًا.',
      signIn: 'تسجيل الدخول باستخدام Google', privacy: 'يعمل بالكامل على جهازك ولا يتواصل إلا مع Google.',
      trash: 'المهملات', spam: 'غير المرغوب فيه', selectAll: 'تحديد الكل', deleteSelected: 'حذف',
      emptyFolder: 'لا يوجد شيء هنا. كل شيء نظيف.', loadMore: 'تحميل المزيد', cancel: 'إلغاء', deleteForever: 'حذف نهائي',
      deleting: 'جارٍ الحذف…', emptyTrash: 'إفراغ المهملات الآن', emptySpam: 'إفراغ غير المرغوب فيه الآن',
      confirmDelTitle: 'حذف {n} رسالة نهائيًا؟',
      confirmDelBody: 'ستُحذف نهائيًا من Gmail ولا يمكن التراجع عن ذلك.',
      confirmEmptyTitle: 'إفراغ {folder}؟',
      confirmEmptyBody: 'سيتم حذف جميع الرسائل ({n}) في {folder} نهائيًا. لا يمكن التراجع عن ذلك.',
      deletedN: 'تم حذف {n} رسالة.', emptied: 'تم إفراغ {folder} — حُذفت {n} رسالة.',
      partial: 'توقف بعد حذف {n} رسالة.', progress: '{done} من {total}',
      sessionExpired: 'انتهت الجلسة (تسجيل دخول Google يستمر ساعة واحدة). سجّل الدخول مرة أخرى للمتابعة.',
      popupClosed: 'تم إغلاق نافذة تسجيل الدخول.',
      scopeMissing: 'لم تُمنح صلاحية الوصول إلى Gmail. سجّل الدخول مرة أخرى واسمح بالوصول الكامل — فهو مطلوب للحذف النهائي.',
      gisFail: 'تعذّر تحميل تسجيل الدخول من Google. تحقق من الاتصال.',
      networkError: 'خطأ في الشبكة — حاول مرة أخرى.', noSubject: '(بدون عنوان)', unknownSender: '(مرسل غير معروف)',
      invalidClient: 'هذا لا يبدو معرّف عميل صحيحًا (يجب أن ينتهي بـ ‎.apps.googleusercontent.com).',
      saved: 'تم الحفظ.', alreadyEmpty: '{folder} فارغ بالفعل.'
    }
  };

  /* ---------------- helpers ---------------- */
  const $ = (id) => document.getElementById(id);
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* storage unavailable */ } },
    del(k) { try { localStorage.removeItem(k); } catch { /* ignore */ } }
  };
  class AuthError extends Error {}

  const state = {
    lang: store.get('gc.lang') || ((navigator.language || '').toLowerCase().startsWith('ar') ? 'ar' : 'en'),
    clientId: store.get('gc.clientId') || (window.GC_CONFIG && window.GC_CONFIG.CLIENT_ID) || '',
    token: null, tokenExp: 0,
    email: store.get('gc.email') || '',
    folder: 'TRASH', items: [], nextPage: null, selected: new Set(),
    counts: { TRASH: null, SPAM: null }, loading: false, loadSeq: 0, busy: false
  };
  const savedTok = store.get('gc.token');
  if (savedTok && savedTok.exp > Date.now() + 60000) { state.token = savedTok.token; state.tokenExp = savedTok.exp; }

  function t(key, vars) {
    let s = (I18N[state.lang] && I18N[state.lang][key]) || I18N.en[key] || key;
    if (vars) for (const [k, v] of Object.entries(vars)) s = s.split('{' + k + '}').join(v);
    return s;
  }
  const locale = () => (state.lang === 'ar' ? 'ar-SA-u-nu-latn-ca-gregory' : 'en-GB');
  const fmtNum = (n) => (n == null ? '–' : Number(n).toLocaleString(locale()));
  const folderName = (f) => t(f === 'TRASH' ? 'trash' : 'spam');

  function fmtDate(ms) {
    if (!ms) return '';
    const d = new Date(ms), now = new Date();
    const sameDay = d.toDateString() === now.toDateString();
    const opts = sameDay ? { hour: '2-digit', minute: '2-digit' }
      : d.getFullYear() === now.getFullYear() ? { day: 'numeric', month: 'short' }
      : { day: 'numeric', month: 'short', year: 'numeric' };
    return new Intl.DateTimeFormat(locale(), opts).format(d);
  }

  const decoder = document.createElement('textarea');
  function decodeEntities(s) { decoder.innerHTML = s || ''; return decoder.value; }

  function parseFrom(v) {
    if (!v) return t('unknownSender');
    const m = v.match(/^\s*"?([^"<]*?)"?\s*<([^>]+)>/);
    return (m && (m[1].trim() || m[2])) || v;
  }

  async function mapLimit(arr, limit, fn) {
    const out = new Array(arr.length); let i = 0;
    const worker = async () => { while (i < arr.length) { const idx = i++; out[idx] = await fn(arr[idx], idx); } };
    await Promise.all(Array.from({ length: Math.min(limit, arr.length) }, worker));
    return out;
  }

  /* ---------------- Gmail API ---------------- */
  async function api(path, { method = 'GET', body } = {}) {
    for (let attempt = 0; ; attempt++) {
      if (!state.token || Date.now() > state.tokenExp - 30000) { expireSession(); throw new AuthError(); }
      let r;
      try {
        r = await fetch(API + path, {
          method,
          headers: Object.assign({ Authorization: 'Bearer ' + state.token }, body ? { 'Content-Type': 'application/json' } : {}),
          body: body ? JSON.stringify(body) : undefined
        });
      } catch {
        throw new Error(navigator.onLine ? t('networkError') : t('offline'));
      }
      if (r.status === 401) { expireSession(); throw new AuthError(); }
      if (r.ok) { const txt = await r.text(); return txt ? JSON.parse(txt) : null; }
      let msg = '';
      try { const j = await r.json(); msg = (j.error && j.error.message) || ''; } catch { /* no body */ }
      const retryable = r.status === 429 || r.status >= 500 || (r.status === 403 && /rate|quota/i.test(msg));
      if (retryable && attempt < 4) { await sleep(600 * 2 ** attempt + Math.random() * 400); continue; }
      const err = new Error(msg || 'HTTP ' + r.status); err.status = r.status; throw err;
    }
  }

  /* ---------------- Auth (Google Identity Services) ---------------- */
  let gisPromise = null, tokenClient = null, tokenWaiter = null;

  function loadGis() {
    if (window.google && google.accounts && google.accounts.oauth2) return Promise.resolve();
    if (!gisPromise) {
      gisPromise = new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = 'https://accounts.google.com/gsi/client';
        s.async = true;
        s.onload = () => resolve();
        s.onerror = () => { gisPromise = null; s.remove(); reject(new Error(t('gisFail'))); };
        document.head.appendChild(s);
      });
    }
    return gisPromise;
  }

  function settleAuth(err) {
    const w = tokenWaiter; tokenWaiter = null;
    if (w) err ? w.reject(err) : w.resolve();
  }

  function ensureTokenClient() {
    if (tokenClient) return tokenClient;
    tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: state.clientId,
      scope: SCOPE,
      callback: (resp) => {
        if (resp.error) return settleAuth(new Error(resp.error_description || resp.error));
        if (!google.accounts.oauth2.hasGrantedAllScopes(resp, SCOPE)) return settleAuth(new Error(t('scopeMissing')));
        state.token = resp.access_token;
        state.tokenExp = Date.now() + (Number(resp.expires_in) || 3600) * 1000;
        store.set('gc.token', { token: state.token, exp: state.tokenExp });
        settleAuth(null);
      },
      error_callback: (err) => settleAuth(new Error(err && err.type === 'popup_closed' ? t('popupClosed') : (err && (err.message || err.type)) || 'Sign-in failed'))
    });
    return tokenClient;
  }

  async function signIn() {
    const btn = $('signInBtn');
    btn.disabled = true;
    try {
      await loadGis();
      ensureTokenClient();
      const done = new Promise((resolve, reject) => { tokenWaiter = { resolve, reject }; });
      const opts = { prompt: state.email ? '' : 'consent' };
      if (state.email) opts.login_hint = state.email;
      tokenClient.requestAccessToken(opts);
      await done;
      await enterMain();
    } catch (e) {
      toast(e.message, 'error');
    } finally {
      btn.disabled = false;
    }
  }

  function expireSession() {
    state.token = null; state.tokenExp = 0;
    store.del('gc.token');
  }

  function signOut() {
    const tok = state.token;
    if (tok && window.google && google.accounts && google.accounts.oauth2) {
      try { google.accounts.oauth2.revoke(tok, () => {}); } catch { /* ignore */ }
    }
    expireSession();
    state.email = ''; store.del('gc.email');
    state.items = []; state.selected.clear(); state.counts = { TRASH: null, SPAM: null };
    showView('signedOut');
  }

  function handleErr(e) {
    if (e instanceof AuthError) { showView('signedOut', t('sessionExpired')); return; }
    toast(e.message || String(e), 'error');
  }

  /* ---------------- Views ---------------- */
  function showView(name, signInMessage) {
    $('setupView').hidden = name !== 'setup';
    $('signedOutView').hidden = name !== 'signedOut';
    $('mainView').hidden = name !== 'main';
    $('menuSignOut').hidden = name !== 'main';
    $('menuRefresh').hidden = name !== 'main';
    $('account').textContent = name === 'main' ? state.email : '';
    if (name === 'signedOut') {
      const msg = $('signInMsg');
      msg.textContent = signInMessage || t('signInBody');
      msg.dataset.custom = signInMessage ? '1' : '';
    }
    if (name === 'setup') {
      $('clientIdInput').value = state.clientId;
      $('originText').textContent = location.origin;
    }
  }

  async function enterMain() {
    showView('main');
    try {
      if (!state.email) {
        const p = await api('/profile');
        state.email = p.emailAddress || '';
        store.set('gc.email', state.email);
        $('account').textContent = state.email;
      }
    } catch (e) { return handleErr(e); }
    refreshCounts();
    loadFolder(true);
  }

  /* ---------------- Data ---------------- */
  async function refreshCounts() {
    try {
      const [tr, sp] = await Promise.all([api('/labels/TRASH'), api('/labels/SPAM')]);
      state.counts.TRASH = tr.messagesTotal || 0;
      state.counts.SPAM = sp.messagesTotal || 0;
    } catch (e) { if (e instanceof AuthError) return handleErr(e); }
    renderCounts();
  }

  function parseMsg(m) {
    const h = {};
    for (const x of (m.payload && m.payload.headers) || []) h[x.name.toLowerCase()] = x.value;
    return {
      id: m.id,
      from: parseFrom(h.from),
      subject: h.subject || '',
      snippet: decodeEntities(m.snippet),
      date: Number(m.internalDate) || (h.date ? Date.parse(h.date) : 0)
    };
  }

  async function loadFolder(reset) {
    const seq = ++state.loadSeq;
    if (reset) { state.items = []; state.nextPage = null; state.selected.clear(); }
    state.loading = true; renderList();
    try {
      const q = new URLSearchParams({ labelIds: state.folder, includeSpamTrash: 'true', maxResults: String(PAGE_SIZE) });
      if (!reset && state.nextPage) q.set('pageToken', state.nextPage);
      const res = await api('/messages?' + q);
      if (seq !== state.loadSeq) return;
      const ids = (res.messages || []).map((m) => m.id);
      const fields = 'id,snippet,internalDate,payload/headers';
      const msgs = await mapLimit(ids, CONCURRENCY, (id) =>
        api('/messages/' + id + '?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date&fields=' + encodeURIComponent(fields))
          .catch((e) => { if (e instanceof AuthError) throw e; return null; }));
      if (seq !== state.loadSeq) return;
      const have = new Set(state.items.map((m) => m.id));
      for (const m of msgs) if (m && !have.has(m.id)) state.items.push(parseMsg(m));
      state.nextPage = res.nextPageToken || null;
    } catch (e) {
      if (seq === state.loadSeq) handleErr(e);
    } finally {
      if (seq === state.loadSeq) { state.loading = false; renderList(); }
    }
  }

  async function deleteIds(ids) {
    for (let i = 0; i < ids.length; i += 1000) {
      const chunk = ids.slice(i, i + 1000);
      if (chunk.length === 1) await api('/messages/' + chunk[0], { method: 'DELETE' });
      else await api('/messages/batchDelete', { method: 'POST', body: { ids: chunk } });
    }
  }

  async function deleteSome(ids) {
    if (!ids.length || state.busy) return;
    const ok = await confirmDialog(t('confirmDelTitle', { n: fmtNum(ids.length) }), t('confirmDelBody'));
    if (!ok) return;
    state.busy = true;
    try {
      await deleteIds(ids);
      const gone = new Set(ids);
      document.querySelectorAll('.item').forEach((li) => { if (gone.has(li.dataset.id)) li.classList.add('removing'); });
      await sleep(200);
      state.items = state.items.filter((m) => !gone.has(m.id));
      ids.forEach((id) => state.selected.delete(id));
      const c = state.counts[state.folder];
      if (c != null) state.counts[state.folder] = Math.max(0, c - ids.length);
      renderCounts(); renderList();
      toast(t('deletedN', { n: fmtNum(ids.length) }), 'ok');
      if (!state.items.length && state.nextPage) loadFolder(true);
      refreshCounts();
    } catch (e) {
      handleErr(e);
    } finally {
      state.busy = false;
    }
  }

  async function emptyFolder() {
    if (state.busy) return;
    const folder = state.folder, fname = folderName(folder);
    const total = state.counts[folder];
    if (total === 0 && !state.items.length) { toast(t('alreadyEmpty', { folder: fname })); return; }
    const ok = await confirmDialog(
      t('confirmEmptyTitle', { folder: fname }),
      t('confirmEmptyBody', { n: total == null ? '?' : fmtNum(total), folder: fname })
    );
    if (!ok) return;

    state.busy = true;
    let deleted = 0, lastFirst = null;
    setProgress(0, total);
    $('progressOverlay').hidden = false;
    try {
      for (let round = 0; round < 1000; round++) {
        const q = new URLSearchParams({ labelIds: folder, includeSpamTrash: 'true', maxResults: '500', fields: 'messages/id,nextPageToken' });
        const res = await api('/messages?' + q);
        const ids = (res.messages || []).map((m) => m.id);
        if (!ids.length) break;
        if (ids[0] === lastFirst) throw new Error('Gmail did not remove the messages — stopping.');
        lastFirst = ids[0];
        await deleteIds(ids);
        deleted += ids.length;
        setProgress(deleted, Math.max(total || 0, deleted));
      }
      toast(t('emptied', { folder: fname, n: fmtNum(deleted) }), 'ok');
    } catch (e) {
      handleErr(e);
      if (deleted && !(e instanceof AuthError)) toast(t('partial', { n: fmtNum(deleted) }) + ' ' + (e.message || ''), 'error');
    } finally {
      $('progressOverlay').hidden = true;
      state.busy = false;
      if (state.token) { refreshCounts(); if (state.folder === folder) loadFolder(true); }
    }
  }

  /* ---------------- Rendering ---------------- */
  const TRASH_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>';

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function renderCounts() {
    $('countTRASH').textContent = fmtNum(state.counts.TRASH);
    $('countSPAM').textContent = fmtNum(state.counts.SPAM);
    $('emptyBtnLabel').textContent = t(state.folder === 'TRASH' ? 'emptyTrash' : 'emptySpam');
    $('emptyBtn').disabled = state.counts[state.folder] === 0 && !state.items.length;
  }

  function renderList() {
    const ul = $('list');
    const frag = document.createDocumentFragment();
    for (const m of state.items) {
      const sel = state.selected.has(m.id);
      const li = el('li', 'item' + (sel ? ' selected' : ''));
      li.dataset.id = m.id;
      const cb = el('input'); cb.type = 'checkbox'; cb.checked = sel; cb.className = 'sel';
      cb.setAttribute('aria-label', m.subject || t('noSubject'));
      const body = el('div', 'body');
      const row1 = el('div', 'row1');
      row1.append(el('div', 'from', m.from), el('div', 'date', fmtDate(m.date)));
      body.append(row1, el('div', 'subject', m.subject || t('noSubject')));
      if (m.snippet) body.append(el('div', 'snippet', m.snippet));
      const del = el('button', 'del-one');
      del.type = 'button'; del.innerHTML = TRASH_SVG; del.setAttribute('aria-label', t('deleteForever'));
      li.append(cb, body, del);
      frag.append(li);
    }
    ul.replaceChildren(frag);
    $('loading').hidden = !state.loading;
    $('emptyState').hidden = state.loading || state.items.length > 0;
    $('loadMoreBtn').hidden = state.loading || !state.nextPage;
    renderCounts();
    updateSelectionUI();
  }

  function updateSelectionUI() {
    const n = state.selected.size, total = state.items.length;
    $('selCount').textContent = fmtNum(n);
    $('deleteSelectedBtn').disabled = n === 0;
    const all = $('selectAll');
    all.checked = total > 0 && n === total;
    all.indeterminate = n > 0 && n < total;
    all.disabled = total === 0;
    document.querySelectorAll('.item').forEach((li) => {
      const on = state.selected.has(li.dataset.id);
      li.classList.toggle('selected', on);
      li.querySelector('.sel').checked = on;
    });
  }

  function applyLang() {
    const root = document.documentElement;
    root.lang = state.lang;
    root.dir = state.lang === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-i18n]').forEach((n) => { n.textContent = t(n.dataset.i18n); });
    const msg = $('signInMsg');
    if (!msg.dataset.custom) msg.textContent = t('signInBody');
    $('langBtn').textContent = state.lang === 'ar' ? 'EN' : 'ع';
    document.title = t('appName');
    renderList();
  }

  /* ---------------- UI bits ---------------- */
  let toastTimer = null;
  function toast(text, kind) {
    const tEl = $('toast');
    tEl.textContent = text;
    tEl.className = 'toast' + (kind ? ' ' + kind : '');
    tEl.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { tEl.hidden = true; }, kind === 'error' ? 6000 : 3200);
  }

  function confirmDialog(title, body) {
    return new Promise((resolve) => {
      $('confirmTitle').textContent = title;
      $('confirmBody').textContent = body;
      const ov = $('confirmOverlay');
      ov.hidden = false;
      const done = (v) => {
        ov.hidden = true;
        $('confirmOk').onclick = $('confirmCancel').onclick = ov.onclick = null;
        resolve(v);
      };
      $('confirmOk').onclick = () => done(true);
      $('confirmCancel').onclick = () => done(false);
      ov.onclick = (e) => { if (e.target === ov) done(false); };
      $('confirmCancel').focus();
    });
  }

  function setProgress(done, total) {
    const pct = total ? Math.min(100, (done / total) * 100) : 0;
    $('progressBar').style.width = pct + '%';
    $('progressText').textContent = t('progress', { done: fmtNum(done), total: total == null ? '?' : fmtNum(total) });
  }

  /* ---------------- Events ---------------- */
  $('signInBtn').addEventListener('click', signIn);

  $('saveClientBtn').addEventListener('click', () => {
    const v = $('clientIdInput').value.trim();
    if (!/\.apps\.googleusercontent\.com$/.test(v)) { toast(t('invalidClient'), 'error'); return; }
    if (v !== state.clientId) { tokenClient = null; expireSession(); }
    state.clientId = v; store.set('gc.clientId', v);
    toast(t('saved'), 'ok');
    route();
  });

  $('langBtn').addEventListener('click', () => {
    state.lang = state.lang === 'ar' ? 'en' : 'ar';
    store.set('gc.lang', state.lang);
    applyLang();
  });

  const menu = $('menu');
  $('menuBtn').addEventListener('click', (e) => { e.stopPropagation(); menu.hidden = !menu.hidden; });
  document.addEventListener('click', (e) => { if (!menu.hidden && !menu.contains(e.target)) menu.hidden = true; });
  $('menuRefresh').addEventListener('click', () => { menu.hidden = true; refreshCounts(); loadFolder(true); });
  $('menuSettings').addEventListener('click', () => { menu.hidden = true; showView('setup'); });
  $('menuSignOut').addEventListener('click', () => { menu.hidden = true; signOut(); });

  document.querySelectorAll('.tab').forEach((tab) => tab.addEventListener('click', () => {
    if (tab.dataset.folder === state.folder) return;
    document.querySelectorAll('.tab').forEach((x) => x.classList.toggle('active', x === tab));
    state.folder = tab.dataset.folder;
    loadFolder(true);
  }));

  $('list').addEventListener('click', (e) => {
    const li = e.target.closest('.item');
    if (!li) return;
    const id = li.dataset.id;
    if (e.target.closest('.del-one')) { deleteSome([id]); return; }
    if (state.selected.has(id)) state.selected.delete(id); else state.selected.add(id);
    updateSelectionUI();
  });

  $('selectAll').addEventListener('change', (e) => {
    if (e.target.checked) state.items.forEach((m) => state.selected.add(m.id));
    else state.selected.clear();
    updateSelectionUI();
  });

  $('deleteSelectedBtn').addEventListener('click', () => deleteSome([...state.selected]));
  $('emptyBtn').addEventListener('click', emptyFolder);
  $('loadMoreBtn').addEventListener('click', () => loadFolder(false));

  const syncOnline = () => { $('offlineBanner').hidden = navigator.onLine; };
  window.addEventListener('online', () => { syncOnline(); loadGis().catch(() => {}); });
  window.addEventListener('offline', syncOnline);

  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && !$('mainView').hidden && Date.now() > state.tokenExp - 30000) {
      expireSession();
      showView('signedOut', t('sessionExpired'));
    }
  });

  // Install prompt (Android / desktop Chrome & Edge)
  let deferredInstall = null;
  window.addEventListener('beforeinstallprompt', (e) => { e.preventDefault(); deferredInstall = e; $('installBtn').hidden = false; });
  $('installBtn').addEventListener('click', async () => {
    if (!deferredInstall) return;
    deferredInstall.prompt();
    try { await deferredInstall.userChoice; } catch { /* ignore */ }
    deferredInstall = null; $('installBtn').hidden = true;
  });
  window.addEventListener('appinstalled', () => { $('installBtn').hidden = true; });

  /* ---------------- Boot ---------------- */
  function route() {
    if (!state.clientId) { showView('setup'); return; }
    if (state.token && state.tokenExp > Date.now() + 60000) enterMain();
    else showView('signedOut');
    if (navigator.onLine) loadGis().catch(() => {}); // preload so the sign-in popup opens instantly
  }

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => { navigator.serviceWorker.register('sw.js').catch(() => {}); });
  }

  syncOnline();
  applyLang();
  route();
})();
