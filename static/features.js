// ═══════════════════════════════════════════════════════════════════════════
// features.js — Learning Intelligence & Social features
// Loaded after app.js; shares the same state, api(), toast(), openModal()
// ═══════════════════════════════════════════════════════════════════════════

// ── Extend NAV ──────────────────────────────────────────────────────────────
// Called once app.js has loaded NAV_KEYS / NAV_I18N and navigate()
document.addEventListener('DOMContentLoaded', () => {
  // Student extra nav
  if (window.NAV_KEYS) {
    NAV_KEYS.student.splice(-1, 0, 'sr', 'graph');   // before 'settings'
    NAV_KEYS.teacher.splice(-1, 0, 'graph');
    NAV_KEYS.admin.splice(-1, 0, 'graph');
    Object.assign(NAV_I18N, { sr: 'nav_sr', graph: 'nav_graph' });
  }
  // Extend i18n
  ['en', 'ur'].forEach(lang => {
    if (!i18n[lang]) return;
    const extras = lang === 'en' ? {
      nav_sr:    'My Reviews',
      nav_graph: 'Knowledge Map',
      // SR
      sr_due:       'Due for Review',
      sr_mastered:  'Mastered',
      sr_total:     'Total Cards',
      sr_review:    'Review',
      sr_no_cards:  'No cards due — great job!',
      sr_quality:   'How well did you recall this?',
      sr_again:     'Forgot (0)',
      sr_hard:      'Hard (2)',
      sr_good:      'Good (4)',
      sr_perfect:   'Perfect (5)',
      // Help board
      help_board:      'Help Board',
      ask_question:    'Ask a Question',
      post_anon:       'Post anonymously',
      mark_resolved:   'Mark resolved',
      endorse:         'Endorse ',
      endorsed:        ' Endorsed',
      answer:          'Answer',
      post_answer:     'Post Answer',
      no_questions:    'No questions yet — be the first to ask!',
      resolved:        'Resolved',
      open_q:          'Open',
      upvote:          '',
      upvoted:         'Upvoted ',
      upvote_it:       ' Upvote',
      // Knowledge Graph
      knowledge_graph: 'Knowledge Map',
      add_concept:     '+ Add Concept',
      add_link:        '+ Add Link',
      tag_course:      'Tag Course',
      concept_name:    'Concept Name',
      link_label:      'Relationship label',
      no_concepts:     'No concepts yet. Add one to start building the graph.',
      // Study Groups
      study_groups:    'Study Groups',
      new_group:       '+ New Group',
      auto_match:      ' Auto-Match',
      join_group:      'Join',
      leave_group:     'Leave',
      group_size:      'Group size',
      members:         'members',
      auto_matched:    'Auto-matched',
      // Confusion
      confused_btn:    ' I\'m confused',
      clear_btn:       ' I\'m following',
      confusion_meter: 'Confusion Meter',
      confused_pct:    '% confused',
      reset_signals:   'Reset',
      my_signal:       'Your signal',
    } : {
      nav_sr:    'میرے کارڈز',
      nav_graph: 'علمی نقشہ',
      sr_due:       'آج کا جائزہ',
      sr_mastered:  'مہارت حاصل',
      sr_total:     'کل کارڈز',
      sr_review:    'جائزہ لیں',
      sr_no_cards:  'آج کوئی کارڈ باقی نہیں — شاباش!',
      sr_quality:   'آپ نے کتنا یاد کیا؟',
      sr_again:     'بھول گئے (0)',
      sr_hard:      'مشکل (2)',
      sr_good:      'ٹھیک (4)',
      sr_perfect:   'بالکل درست (5)',
      help_board:      'مدد بورڈ',
      ask_question:    'سوال پوچھیں',
      post_anon:       'گمنام پوسٹ کریں',
      mark_resolved:   'حل شدہ',
      endorse:         'تصدیق کریں',
      endorsed:        ' تصدیق شدہ',
      answer:          'جواب',
      post_answer:     'جواب دیں',
      no_questions:    'ابھی کوئی سوال نہیں — پہلے پوچھیں!',
      resolved:        'حل ہو گیا',
      open_q:          'جاری',
      upvote:          '',
      upvoted:         'پسند کیا ',
      upvote_it:       ' پسند کریں',
      knowledge_graph: 'علمی نقشہ',
      add_concept:     '+ تصور شامل کریں',
      add_link:        '+ ربط شامل کریں',
      tag_course:      'کورس ٹیگ کریں',
      concept_name:    'تصور کا نام',
      link_label:      'تعلق کا عنوان',
      no_concepts:     'ابھی کوئی تصور نہیں۔',
      study_groups:    'مطالعہ گروہ',
      new_group:       '+ نیا گروہ',
      auto_match:      ' خودکار میل',
      join_group:      'شامل ہوں',
      leave_group:     'چھوڑیں',
      group_size:      'گروہ کا حجم',
      members:         'اراکین',
      auto_matched:    'خودکار',
      confused_btn:    ' سمجھ نہیں آئی',
      clear_btn:       ' سمجھ آ گئی',
      confusion_meter: 'الجھن میٹر',
      confused_pct:    '٪ الجھے ہوئے',
      reset_signals:   'ری سیٹ',
      my_signal:       'آپ کا اشارہ',
    };
    Object.assign(i18n[lang], extras);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 1. SPACED REPETITION
// ═══════════════════════════════════════════════════════════════════════════
async function renderSRReview(el) {
  loading(el);
  try {
    const [stats, cards] = await Promise.all([
      api('GET', '/sr/stats'),
      api('GET', '/sr/due'),
    ]);

    el.innerHTML = `
      <div class="page-header">
        <h2>${t('nav_sr')}</h2>
      </div>
      <div class="stats-grid" style="max-width:420px">
        <div class="stat-card"><div class="stat-number">${stats.due_today}</div><div class="stat-label">${t('sr_due')}</div></div>
        <div class="stat-card"><div class="stat-number">${stats.mastered}</div><div class="stat-label">${t('sr_mastered')}</div></div>
        <div class="stat-card"><div class="stat-number">${stats.total}</div><div class="stat-label">${t('sr_total')}</div></div>
      </div>
      ${cards.length === 0 ? `<div class="card"><div class="card-body"><p class="text-muted">${t('sr_no_cards')}</p></div></div>`
        : `<div id="sr-deck">${renderSRCard(cards, 0)}</div>`}
    `;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

window._srCards = [];
window._srIdx   = 0;

function renderSRCard(cards, idx) {
  window._srCards = cards;
  window._srIdx   = idx;
  if (idx >= cards.length) {
    return `<div class="card"><div class="card-body text-muted">${t('sr_no_cards')} </div></div>`;
  }
  const c = cards[idx];
  const progress = `${idx + 1} / ${cards.length}`;
  const opts = c.options.map(o => `
    <div class="quiz-option" onclick="selectSROpt(this, ${o.id})" data-opt-id="${o.id}">
      <input type="radio" name="sr-opt" value="${o.id}"><label>${o.option_text}</label>
    </div>`).join('');

  return `
    <div class="card">
      <div class="card-header">
        <h3>${t('sr_review')} <span class="text-muted" style="font-weight:400">${progress}</span></h3>
      </div>
      <div class="card-body">
        <p class="quiz-q-text">${c.question_text}</p>
        ${c.question_type !== 'short_answer' ? `<div class="quiz-options" id="sr-opts">${opts}</div>` : `
          <textarea id="sr-text" class="form-control" rows="4" placeholder="Your answer…"></textarea>`}
        <div id="sr-quality-row" class="hidden" style="margin-top:16px">
          <p style="font-weight:600;margin-bottom:10px">${t('sr_quality')}</p>
          <div class="flex-gap">
            <button class="btn btn-danger"  onclick="submitSRReview(${c.card_id}, 0)">${t('sr_again')}</button>
            <button class="btn"             onclick="submitSRReview(${c.card_id}, 2)">${t('sr_hard')}</button>
            <button class="btn btn-primary" onclick="submitSRReview(${c.card_id}, 4)">${t('sr_good')}</button>
            <button class="btn btn-success" onclick="submitSRReview(${c.card_id}, 5)">${t('sr_perfect')}</button>
          </div>
        </div>
        ${c.question_type !== 'short_answer' ? '' : `
          <button class="btn btn-primary" style="margin-top:10px" onclick="document.getElementById('sr-quality-row').classList.remove('hidden')">
            Show quality rating
          </button>`}
      </div>
    </div>`;
}

function selectSROpt(el, optId) {
  document.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  document.getElementById('sr-quality-row').classList.remove('hidden');
}

async function submitSRReview(cardId, quality) {
  try {
    await api('POST', `/sr/${cardId}/review`, { quality });
    const next = window._srIdx + 1;
    document.getElementById('sr-deck').innerHTML = renderSRCard(window._srCards, next);
  } catch(err) { toast(err.message, 'error'); }
}

// ═══════════════════════════════════════════════════════════════════════════
// 2. CONFUSION HEATMAP  (shown inside session cards)
// ═══════════════════════════════════════════════════════════════════════════
let _confusionPoll = null;

function renderConfusionWidget(sessionId, role) {
  if (role === 'student') {
    return `
      <div class="confusion-widget">
        <span class="text-muted" style="font-size:12px">${t('my_signal')}:</span>
        <button class="btn btn-sm" onclick="sendConfusion(${sessionId},'confused')" id="conf-btn-${sessionId}">${t('confused_btn')}</button>
        <button class="btn btn-sm btn-success" onclick="sendConfusion(${sessionId},'clear')" id="clear-btn-${sessionId}">${t('clear_btn')}</button>
      </div>`;
  }
  return `
    <div class="confusion-widget" id="confusion-${sessionId}">
      <span class="text-muted" style="font-size:12px">${t('confusion_meter')}:</span>
      <span id="conf-stat-${sessionId}" class="conf-bar">loading…</span>
      <button class="btn btn-sm" onclick="resetConfusion(${sessionId})">${t('reset_signals')}</button>
    </div>`;
}

async function sendConfusion(sessionId, signal) {
  try {
    await api('POST', `/confusion/${sessionId}/signal`, { signal });
    const confBtn  = document.getElementById(`conf-btn-${sessionId}`);
    const clearBtn = document.getElementById(`clear-btn-${sessionId}`);
    if (confBtn)  confBtn.classList.toggle('btn-danger',   signal === 'confused');
    if (clearBtn) clearBtn.classList.toggle('btn-success', signal === 'clear');
    toast(signal === 'confused' ? t('confused_btn') : t('clear_btn'));
  } catch(err) { toast(err.message, 'error'); }
}

async function pollConfusion(sessionId) {
  try {
    const data = await api('GET', `/confusion/${sessionId}/stats`);
    const el   = document.getElementById(`conf-stat-${sessionId}`);
    if (!el) { clearInterval(_confusionPoll); return; }
    el.innerHTML = `
      <span class="badge ${data.confusion_pct > 40 ? 'badge-danger' : 'badge-success'}">
        ${data.confusion_pct}% ${t('confused_pct')}
      </span>
      <span class="text-muted">(${data.total_signals} signals)</span>`;
  } catch(_) {}
}

async function resetConfusion(sessionId) {
  await api('DELETE', `/confusion/${sessionId}/clear`);
  toast(t('reset_signals'));
}

// ═══════════════════════════════════════════════════════════════════════════
// 4. ANONYMOUS HELP BOARD  (tab in course detail)
// ═══════════════════════════════════════════════════════════════════════════
async function renderHelpBoardTab(courseId) {
  const posts = await api('GET', `/help/course/${courseId}`);
  const role  = state.user.role;
  return `
    <div class="card">
      <div class="card-header"><h3>${t('help_board')}</h3>
        <button class="btn btn-sm btn-primary" onclick="openAskQuestionModal(${courseId})">${t('ask_question')}</button>
      </div>
      <div class="card-body">
        ${posts.length === 0 ? `<p class="text-muted">${t('no_questions')}</p>` : ''}
        ${posts.map(p => `
          <div class="help-post ${p.is_resolved ? 'resolved' : ''}">
            <div class="help-post-votes">
              <button class="btn-vote ${p.has_voted ? 'active' : ''}" onclick="votePost(${p.id})">${t('upvote')}</button>
              <span class="vote-count">${p.upvotes}</span>
            </div>
            <div class="help-post-body" onclick="openPostDetail(${p.id}, ${courseId})">
              <div class="help-post-title">
                ${p.is_resolved ? `<span class="badge badge-success">${t('resolved')}</span>` : `<span class="badge badge-info">${t('open_q')}</span>`}
                <strong>${htmlEsc(p.title)}</strong>
              </div>
              <div class="help-post-meta">
                <small>${htmlEsc(p.author)} &bull; ${fmtDate(p.created_at)} &bull; ${p.answer_count} answer(s)</small>
              </div>
            </div>
          </div>`).join('')}
      </div>
    </div>`;
}

function openAskQuestionModal(courseId) {
  openModal(t('ask_question'), `
    <form id="modal-form">
      <div class="form-group"><label>Title *</label>
        <input name="title" class="form-control" required placeholder="What do you want to know?"></div>
      <div class="form-group"><label>Details</label>
        <textarea name="body" class="form-control" rows="5" placeholder="Explain your question in detail…"></textarea></div>
      <div class="form-group">
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer">
          <input type="checkbox" name="is_anonymous" checked> ${t('post_anon')}
        </label>
      </div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('ask_question')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        const res = await api('POST', `/help/course/${courseId}`, {
          title:        fd.get('title'),
          body:         fd.get('body') || '',
          is_anonymous: fd.get('is_anonymous') === 'on',
        });
        closeModal(); toast(t('ask_question') + '!'); navigate('course', { id: courseId });
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function openPostDetail(postId, courseId) {
  const post = await api('GET', `/help/post/${postId}`);
  const role = state.user.role;
  const canEndorse = role === 'admin' || role === 'teacher';

  openModal(htmlEsc(post.title), `
    <div>
      <p style="white-space:pre-wrap;margin-bottom:12px">${htmlEsc(post.body)}</p>
      <small class="text-muted">${htmlEsc(post.author)} &bull; ${fmtDate(post.created_at)}</small>
      <div class="flex-gap" style="margin-top:10px">
        <button class="btn btn-sm ${post.is_resolved ? 'btn-success' : ''}" onclick="toggleResolve(${postId}, ${courseId})">${t('mark_resolved')}</button>
      </div>
      <hr style="margin:16px 0">
      <h4 style="margin-bottom:10px">${post.answers.length} Answer(s)</h4>
      ${post.answers.map(a => `
        <div class="help-answer ${a.is_endorsed ? 'endorsed' : ''}">
          <div class="help-answer-meta">
            <strong>${htmlEsc(a.author)}</strong>
            ${a.is_endorsed ? `<span class="badge badge-success">${t('endorsed')}</span>` : ''}
            <small class="text-muted">${fmtDate(a.created_at)}</small>
          </div>
          <p style="white-space:pre-wrap;margin:8px 0">${htmlEsc(a.body)}</p>
          <div class="flex-gap">
            <button class="btn btn-sm ${a.has_voted ? 'btn-primary' : ''}" onclick="voteAnswer(${a.id})">${t('upvote')} ${a.upvotes}</button>
            ${canEndorse ? `<button class="btn btn-sm ${a.is_endorsed ? 'btn-success' : ''}" onclick="endorseAnswer(${a.id})">${a.is_endorsed ? t('endorsed') : t('endorse')}</button>` : ''}
          </div>
        </div>`).join('')}
      <hr style="margin:16px 0">
      <div class="form-group"><label>${t('post_answer')}</label>
        <textarea id="answer-body" class="form-control" rows="4"></textarea>
        <label style="display:flex;align-items:center;gap:8px;margin-top:8px;cursor:pointer">
          <input type="checkbox" id="answer-anon"> ${t('post_anon')}
        </label>
      </div>
      <button class="btn btn-primary" onclick="postAnswer(${postId}, ${courseId})">${t('post_answer')}</button>
    </div>`);
}

async function postAnswer(postId, courseId) {
  const body = document.getElementById('answer-body').value.trim();
  if (!body) { toast('Write an answer first', 'error'); return; }
  const anon = document.getElementById('answer-anon').checked;
  try {
    await api('POST', `/help/post/${postId}/answer`, { body, is_anonymous: anon });
    toast(t('post_answer') + '!'); closeModal(); navigate('course', { id: courseId });
  } catch(err) { toast(err.message, 'error'); }
}

async function votePost(postId) {
  try { await api('POST', `/help/post/${postId}/vote`); }
  catch(err) { toast(err.message, 'error'); }
}

async function voteAnswer(answerId) {
  try { await api('POST', `/help/answer/${answerId}/vote`); }
  catch(err) { toast(err.message, 'error'); }
}

async function endorseAnswer(answerId) {
  try { await api('POST', `/help/answer/${answerId}/endorse`); closeModal(); toast(t('endorse')); }
  catch(err) { toast(err.message, 'error'); }
}

async function toggleResolve(postId, courseId) {
  try { await api('PUT', `/help/post/${postId}/resolve`); closeModal(); navigate('course', { id: courseId }); }
  catch(err) { toast(err.message, 'error'); }
}

// ═══════════════════════════════════════════════════════════════════════════
// 5. KNOWLEDGE GRAPH  (full-page with Canvas visualization)
// ═══════════════════════════════════════════════════════════════════════════
// Module-level cache so onclick handlers don't embed serialised data in HTML
let _kgNodes   = [];
let _kgCourses = [];

async function renderKnowledgeGraph(el) {
  loading(el);
  try {
    const graph   = await api('GET', '/graph/');
    const courses = await api('GET', '/courses/');
    // Store for use by openAddLinkModal / openTagCourseModal
    _kgNodes   = graph.nodes   || [];
    _kgCourses = courses       || [];

    const role    = state.user.role;
    const canEdit = role === 'admin' || role === 'teacher';

    el.innerHTML = `
      <div class="page-header">
        <h2>${t('knowledge_graph')}</h2>
        ${canEdit ? `
          <div class="flex-gap">
            <button class="btn btn-primary btn-sm" onclick="openAddConceptModal()">${t('add_concept')}</button>
            <button class="btn btn-sm" onclick="openAddLinkModal()">${t('add_link')}</button>
          </div>` : ''}
      </div>
      ${graph.nodes.length === 0
        ? `<div class="card"><div class="card-body"><p class="text-muted">${t('no_concepts')}</p></div></div>`
        : `<div class="graph-canvas-wrap"><canvas id="knowledge-canvas"></canvas></div>`}
      <div class="card" style="margin-top:16px">
        <div class="card-header"><h3>Concepts (${graph.nodes.length})</h3></div>
        <div class="card-body">
          ${graph.nodes.map(n => `
            <div class="concept-row">
              <div class="concept-dot" style="background:${n.color}"></div>
              <div style="flex:1">
                <strong>${n.name}</strong>
                ${n.description ? `<span class="text-muted"> — ${n.description}</span>` : ''}
                ${n.courses.map(c=>`<span class="badge badge-info" style="margin-left:4px">${c.title}</span>`).join('')}
              </div>
              ${canEdit ? `
                <button class="btn btn-sm" onclick="openTagCourseModal(${n.id})">${t('tag_course')}</button>
                <button class="btn btn-sm btn-danger" onclick="deleteConcept(${n.id})">${t('delete')}</button>` : ''}
            </div>`).join('')}
        </div>
      </div>`;

    if (graph.nodes.length > 0) {
      drawGraph(graph);
    }
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function drawGraph(graph) {
  const canvas = document.getElementById('knowledge-canvas');
  if (!canvas) return;
  const W = canvas.parentElement.clientWidth;
  const H = Math.min(420, Math.max(250, graph.nodes.length * 60));
  canvas.width  = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d');

  // Assign positions in a circle
  const cx = W / 2, cy = H / 2, r = Math.min(cx, cy) - 60;
  const positions = {};
  graph.nodes.forEach((n, i) => {
    const angle = (2 * Math.PI * i) / graph.nodes.length - Math.PI / 2;
    positions[n.id] = {
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
    };
  });

  // Draw edges
  ctx.strokeStyle = '#94a3b8';
  ctx.lineWidth   = 1.5;
  ctx.font        = '11px sans-serif';
  ctx.fillStyle   = '#64748b';
  graph.edges.forEach(e => {
    const from = positions[e.from];
    const to   = positions[e.to];
    if (!from || !to) return;
    ctx.beginPath();
    ctx.moveTo(from.x, from.y);
    ctx.lineTo(to.x, to.y);
    ctx.stroke();
    // Arrow head
    const angle = Math.atan2(to.y - from.y, to.x - from.x);
    const ax = to.x - 14 * Math.cos(angle);
    const ay = to.y - 14 * Math.sin(angle);
    ctx.beginPath();
    ctx.moveTo(ax, ay);
    ctx.lineTo(ax - 8 * Math.cos(angle - 0.4), ay - 8 * Math.sin(angle - 0.4));
    ctx.lineTo(ax - 8 * Math.cos(angle + 0.4), ay - 8 * Math.sin(angle + 0.4));
    ctx.closePath();
    ctx.fillStyle = '#94a3b8';
    ctx.fill();
    // Edge label
    const mx = (from.x + to.x) / 2, my = (from.y + to.y) / 2;
    ctx.fillStyle = '#64748b';
    ctx.fillText(e.label, mx, my - 4);
  });

  // Draw nodes
  graph.nodes.forEach(n => {
    const { x, y } = positions[n.id];
    ctx.beginPath();
    ctx.arc(x, y, 22, 0, Math.PI * 2);
    ctx.fillStyle = n.color;
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth   = 2;
    ctx.stroke();
    // Label
    ctx.fillStyle   = '#fff';
    ctx.font        = 'bold 11px sans-serif';
    ctx.textAlign   = 'center';
    ctx.textBaseline= 'middle';
    const label = n.name.length > 12 ? n.name.substring(0, 11) + '…' : n.name;
    ctx.fillText(label, x, y);
  });
}

function openAddConceptModal() {
  const colours = ['#2563eb','#059669','#d97706','#dc2626','#7c3aed','#0891b2'];
  openModal(t('add_concept'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('concept_name')} *</label>
        <input name="name" class="form-control" required placeholder="e.g. Quadratic Equations"></div>
      <div class="form-group"><label>${t('description')}</label>
        <input name="description" class="form-control" placeholder="Brief description…"></div>
      <div class="form-group"><label>Colour</label>
        <div class="flex-gap">
          ${colours.map((c,i)=>`<label style="cursor:pointer">
            <input type="radio" name="color" value="${c}" ${i===0?'checked':''} style="display:none">
            <div style="width:28px;height:28px;border-radius:50%;background:${c};border:2px solid transparent"
              onclick="this.previousElementSibling.checked=true;document.querySelectorAll('.color-swatch').forEach(s=>s.style.border='2px solid transparent');this.style.border='2px solid #000';" class="color-swatch"></div>
          </label>`).join('')}
        </div>
      </div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('add')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', '/graph/concepts', {
          name: fd.get('name'), description: fd.get('description') || null, color: fd.get('color') || '#2563eb',
        });
        closeModal(); toast(t('add_concept') + '!'); navigate('graph');
      } catch(err) { toast(err.message, 'error'); }
    });
}

function openAddLinkModal() {
  const nodes = _kgNodes;
  const opts = nodes.map(n => `<option value="${n.id}">${n.name}</option>`).join('');
  openModal(t('add_link'), `
    <form id="modal-form">
      <div class="form-row">
        <div class="form-group"><label>From *</label><select name="from_id" class="form-control">${opts}</select></div>
        <div class="form-group"><label>To *</label><select name="to_id" class="form-control">${opts}</select></div>
      </div>
      <div class="form-group"><label>${t('link_label')}</label>
        <input name="label" class="form-control" value="relates to"></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('add')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', '/graph/links', {
          from_id: parseInt(fd.get('from_id')), to_id: parseInt(fd.get('to_id')), label: fd.get('label'),
        });
        closeModal(); toast(t('add_link') + '!'); navigate('graph');
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function deleteConcept(id) {
  if (!await showConfirm(t('delete') + '?')) return;
  try { await api('DELETE', `/graph/concepts/${id}`); toast(t('delete')); navigate('graph'); }
  catch(err) { toast(err.message, 'error'); }
}

function openTagCourseModal(conceptId) {
  const opts = _kgCourses.map(c => `<option value="${c.id}">${c.title}</option>`).join('');
  openModal(t('tag_course'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('courses')} *</label>
        <select name="course_id" class="form-control">${opts}</select></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('tag_course')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', `/graph/concepts/${conceptId}/tag`, { course_id: parseInt(fd.get('course_id')) });
        closeModal(); toast(t('tag_course') + '!'); navigate('graph');
      } catch(err) { toast(err.message, 'error'); }
    });
}

// ═══════════════════════════════════════════════════════════════════════════
// 6. STUDY GROUP AUTO-MATCHER  (tab in course detail)
// ═══════════════════════════════════════════════════════════════════════════
async function renderStudyGroupsTab(courseId, canManage) {
  const groups = await api('GET', `/study-groups/course/${courseId}`);
  const role   = state.user.role;

  return `
    <div class="card">
      <div class="card-header"><h3>${t('study_groups')}</h3>
        <div class="flex-gap">
          <button class="btn btn-sm btn-primary" onclick="openNewGroupModal(${courseId})">${t('new_group')}</button>
          ${canManage ? `<button class="btn btn-sm btn-success" onclick="autoMatchGroups(${courseId})">${t('auto_match')}</button>` : ''}
        </div>
      </div>
      <div class="card-body">
        ${groups.length === 0 ? `<p class="text-muted">No study groups yet — create one or ask your teacher to auto-match.</p>` : ''}
        <div class="study-groups-grid">
          ${groups.map(g => `
            <div class="study-group-card">
              <div class="sg-header">
                <strong>${g.name}</strong>
                ${g.is_auto_matched ? `<span class="badge badge-info">${t('auto_matched')}</span>` : ''}
              </div>
              <p class="text-muted" style="font-size:12px">${g.member_count} ${t('members')}</p>
              <div class="sg-members">
                ${g.members.map(m => `<span class="sg-avatar" title="${m.name}">${m.name[0]}</span>`).join('')}
              </div>
              <div class="flex-gap" style="margin-top:10px">
                ${role === 'student' && !g.i_am_member
                  ? `<button class="btn btn-sm btn-primary" onclick="joinGroup(${g.id}, ${courseId})">${t('join_group')}</button>` : ''}
                ${role === 'student' && g.i_am_member
                  ? `<button class="btn btn-sm btn-danger" onclick="leaveGroup(${g.id}, ${courseId})">${t('leave_group')}</button>` : ''}
                ${canManage ? `<button class="btn btn-sm btn-danger" onclick="deleteGroup(${g.id}, ${courseId})">${t('delete')}</button>` : ''}
              </div>
            </div>`).join('')}
        </div>
      </div>
    </div>`;
}

function openNewGroupModal(courseId) {
  openModal(t('new_group'), `
    <form id="modal-form">
      <div class="form-group"><label>Group Name *</label>
        <input name="name" class="form-control" required placeholder="e.g. Team Alpha"></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', `/study-groups/course/${courseId}`, { name: fd.get('name') });
        closeModal(); toast(t('create') + '!'); navigate('course', { id: courseId });
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function autoMatchGroups(courseId) {
  if (!await showConfirm(`${t('auto_match')} — this will regenerate auto-matched groups. Continue?`)) return;
  try {
    const res = await api('POST', `/study-groups/course/${courseId}/auto-match?group_size=3`);
    toast(`${res.groups_created} groups created!`);
    navigate('course', { id: courseId });
  } catch(err) { toast(err.message, 'error'); }
}

async function joinGroup(groupId, courseId) {
  try { await api('POST', `/study-groups/${groupId}/join`); toast(t('join_group') + '!'); navigate('course', { id: courseId }); }
  catch(err) { toast(err.message, 'error'); }
}

async function leaveGroup(groupId, courseId) {
  if (!await showConfirm(t('leave_group') + '?')) return;
  try { await api('DELETE', `/study-groups/${groupId}/leave`); toast(t('leave_group')); navigate('course', { id: courseId }); }
  catch(err) { toast(err.message, 'error'); }
}

async function deleteGroup(groupId, courseId) {
  if (!await showConfirm(t('delete') + '?')) return;
  try { await api('DELETE', `/study-groups/${groupId}`); toast(t('delete')); navigate('course', { id: courseId }); }
  catch(err) { toast(err.message, 'error'); }
}
