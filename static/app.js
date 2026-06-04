// ═══════════════════════════════════════════════════════════
// i18n  ─  English & Urdu translations
// ═══════════════════════════════════════════════════════════
const i18n = {
  en: {
    app_name:'School LMS',
    // Nav
    nav_dashboard:'Dashboard', nav_courses:'Courses', nav_users:'Users',
    nav_announcements:'Announcements', nav_settings:'Settings',
    nav_gradebook:'Gradebook', nav_analytics:'Analytics',
    nav_calendar:'Calendar', nav_badges:'Badges',
    nav_messages:'Messages', nav_question_banks:'Question Banks',
    nav_portfolio:'Portfolio',
    // Auth
    sign_in:'Sign In', sign_out:'Sign out', email:'Email', password:'Password',
    login_hint:'Default admin: admin@school.edu / admin123',
    // Common
    back:'← Back', save:'Save', cancel:'Cancel', delete:'Delete',
    create:'Create', add:'Add', edit:'Edit', submit:'Submit', loading:'Loading…',
    by:'By', yes:'Yes', no:'No',
    // Dashboard
    welcome:'Welcome back',
    // Courses
    courses:'Courses', new_course:'+ New Course', enroll:'Enroll',
    unenroll:'Unenroll', enrolled:'Enrolled', no_courses:'No courses yet.',
    my_courses:'My Courses', browse_courses:'Browse Courses',
    subject:'Subject', grade_level:'Grade Level', description:'Description',
    teacher:'Teacher', students:'Students', student_count:'students',
    all_courses:'All Courses',
    // Materials
    materials:'Materials', course_materials:'Course Materials',
    add_material:'+ Add Material', title_label:'Title', content:'Content',
    url_label:'URL (optional)', no_materials:'No materials yet.',
    upload_file:'Upload File', link_text:'Link / Text',
    file_upload_hint:'Any file type (PDF, video, image, document…) — max 200 MB',
    download:'Download', view_file:'View',
    // Assignments
    assignments:'Assignments', new_assignment:'+ New Assignment',
    instructions:'Instructions', due_date:'Due', max_score:'Max Score',
    pts:'pts', submit_assignment:'Submit Assignment',
    your_submission:'Your Submission', resubmit:'Resubmit',
    edit_resubmit:'Edit / Resubmit', not_graded:'Not graded yet.',
    not_submitted:'Not submitted', submissions:'Submissions',
    no_submissions:'No submissions yet.', feedback:'Feedback',
    score:'Score', save_grade:'Save Grade', graded:'Graded',
    // Quizzes
    quizzes:'Quizzes', new_quiz:'+ New Quiz', quiz_builder:'Quiz Builder',
    add_question:'+ Add Question', question_type:'Question Type',
    multiple_choice:'Multiple Choice', true_false:'True / False',
    short_answer:'Short Answer', question_text:'Question', points:'Points',
    correct_answer:'Correct', start_quiz:'Start Quiz', submit_quiz:'Submit Quiz',
    quiz_results:'View Results', time_limit:'Time Limit (min)',
    minutes:'min', time_remaining:'Time remaining', no_quizzes:'No quizzes yet.',
    attempt_count:'attempts', not_attempted:'Not attempted',
    attempted:'Attempted', q_num:'Question', of:'of',
    short_manual:'Short answer — graded manually by teacher.',
    quiz_submitted:'Quiz submitted!', your_score:'Your Score',
    correct:'Correct', wrong:'Wrong', your_answer:'Your answer',
    // Sessions
    sessions:'Sessions', new_session:'+ New Session', virtual:'Virtual',
    physical:'In-Person', session_type:'Session Type', meeting_link:'Meeting Link / URL',
    location:'Room / Location', duration:'Duration (minutes)', notes:'Notes',
    join:'Join', no_sessions:'No sessions scheduled.', upcoming:'Upcoming',
    past:'Past', mins:'mins',
    // Announcements
    announcements:'Announcements', school_announcements:'School Announcements',
    post_announcement:'+ Post Announcement', course_announcements:'Course Announcements',
    no_announcements:'No announcements yet.',
    // Users
    user_management:'User Management', add_user:'+ Add User',
    full_name:'Full Name', role:'Role', all:'All', admins:'Admins',
    teachers:'Teachers', you:'You',
    // Settings
    settings:'Settings', language:'Language', language_desc:'Choose your preferred language',
    profile:'My Profile', profile_desc:'Update your display name or password',
    update_profile:'Update Profile', new_password:'New Password (leave blank to keep current)',
    profile_saved:'Profile updated!',
    // New features
    gradebook:'Gradebook', my_grades:'My Grades', weighted_avg:'Weighted Avg',
    letter_grade:'Letter Grade', gpa:'GPA', cumulative_gpa:'Cumulative GPA',
    categories:'Categories', new_category:'+ Category', weight:'Weight',
    drop_lowest:'Drop Lowest', category:'Category',
    calendar:'Calendar', upcoming_events:'Upcoming Events', no_events:'No upcoming events.',
    event_assignment:'Assignment Due', event_session:'Session', event_quiz:'Quiz Due',
    overdue:'Overdue', due_soon:'Due Soon',
    messages:'Messages', inbox:'Inbox', sent:'Sent', compose:'+ Compose',
    compose_message:'Compose Message', recipient:'Recipient', subject:'Subject',
    message_body:'Message', send:'Send', no_messages:'No messages.',
    analytics:'Analytics', grade_distribution:'Grade Distribution',
    submission_rate:'Submission Rate', avg_score:'Avg Score', active_students:'Active Students',
    total_users:'Total Users', total_courses:'Total Courses', submissions_this_week:'Submissions This Week',
    badges:'Badges', my_badges:'My Badges', award_badge:'Award Badge', create_badge:'+ Create Badge',
    badge_icon:'Icon (emoji)', no_badges:'No badges yet.', earned_on:'Earned on',
    portfolio:'Portfolio', my_portfolio:'My Portfolio', add_item:'+ Add Item',
    portfolio_title:'Portfolio Title', bio:'Bio', make_public:'Make Public',
    portfolio_items:'Portfolio Items', no_items:'No items yet.',
    question_banks:'Question Banks', new_bank:'+ New Bank', import_to_quiz:'Import to Quiz',
    add_questions:'+ Add Question', no_banks:'No question banks yet.',
    modules:'Modules', new_module:'+ New Module', add_module_item:'+ Add Item',
    mark_complete:'Mark Complete', completed:'Completed', progress:'Progress',
    discussions:'Discussions', new_board:'+ New Board', reply:'Reply',
    endorse:'Endorse', no_boards:'No discussion boards yet.', post:'Post',
    surveys:'Surveys', new_survey:'+ New Survey', take_survey:'Take Survey',
    view_results:'View Results', submit_survey:'Submit Survey',
    // Dark mode
    theme:'Theme', theme_desc:'Switch between light and dark mode',
    light_mode:'☀️ Light', dark_mode:'🌙 Dark',
    // Leaderboard
    leaderboard:'Leaderboard', nav_leaderboard:'Leaderboard',
    your_rank:'Your Rank', rank:'Rank', top_students:'Top Students',
    no_leaderboard_data:'No grades recorded yet.',
    course_leaderboard:'Course Leaderboard', school_leaderboard:'School Leaderboard',
    // Certificates
    download_certificate:'⬇ Download Certificate',
    cert_not_eligible:'Certificate not available yet',
    cert_requirements:'Submit all assignments & complete all quizzes (avg ≥ 50%) to earn your certificate.',
    cert_ready:'🎓 Your certificate is ready to download!',
    // Retake limits
    max_attempts:'Max Attempts', unlimited:'Unlimited',
    attempts_remaining:'attempts left', no_attempts_left:'No attempts remaining',
    // Quiz publish / edit
    quiz_published:'Published', quiz_draft:'Draft',
    publish_quiz:'Publish to Students', unpublish_quiz:'Unpublish',
    edit_quiz:'Edit Details', quiz_edit_saved:'Quiz updated!',
    urgent_quizzes:'⚡ Urgent: Quizzes & Tests',
    no_urgent:'No pending quizzes — you\'re all caught up!',
    start_now:'Start Now', resume_quiz:'Resume',
    urgent:'Urgent',
    // Post-quiz results popup
    quiz_score_result:'Your Result',
    outstanding_quizzes:'Outstanding Quizzes & Tests',
    no_outstanding_quizzes:'No outstanding quizzes or tests! 🎉 Well done!',
    outstanding_quizzes_msg:'You still have these quizzes / tests to complete:',
    pending_grading:'Awaiting teacher grading',
    // Post-submit assignment check
    outstanding_assignments:'Outstanding Assignments',
    no_outstanding:'No outstanding assignments! Well done! 🎉',
    outstanding_msg:'You still have assignments to complete:',
    go_to_assignment:'Go to Assignment',
    well_done:'Well done!',
    // Misc
    enrolled_courses:'Enrolled Courses', available_courses:'Available',
    total_students:'Total Students', manage_courses:'Manage Courses',
    // AI Tutor
    nav_ai_tutor:'AI Tutor', ai_tutor:'AI Tutor',
    new_chat:'+ New Chat', study_session:'Study Session',
    assignment_help:'Assignment Help', chat_send:'Send',
    chat_placeholder:'Ask a question…',
    chat_empty:'Ask me anything about your course materials!',
    chat_hint_note:'I\'m in hint-only mode — I\'ll guide you without giving away answers.',
    chat_locked:'🔒 AI Tutor is locked while a quiz is in progress. Submit or finish the quiz first.',
    chat_attach:'Attach file',
    no_chat_sessions:'No chat sessions yet. Click + New Chat to get started.',
  },
  ur: {
    app_name:'اسکول ایل ایم ایس',
    // Nav
    nav_dashboard:'ڈیش بورڈ', nav_courses:'کورسز', nav_users:'صارفین',
    nav_announcements:'اعلانات', nav_settings:'ترتیبات',
    // Auth
    sign_in:'سائن اِن', sign_out:'سائن آوٹ', email:'ای میل', password:'پاس ورڈ',
    login_hint:'پہلا منتظم: admin@school.edu / admin123',
    // Common
    back:'→ واپس', save:'محفوظ کریں', cancel:'منسوخ', delete:'حذف کریں',
    create:'بنائیں', add:'شامل کریں', edit:'ترمیم', submit:'جمع کریں', loading:'لوڈ ہو رہا ہے…',
    by:'از', yes:'ہاں', no:'نہیں',
    // Dashboard
    welcome:'خوش آمدید',
    // Courses
    courses:'کورسز', new_course:'+ نیا کورس', enroll:'داخلہ لیں',
    unenroll:'نام خارج کریں', enrolled:'داخل شدہ', no_courses:'ابھی کوئی کورس نہیں۔',
    my_courses:'میرے کورسز', browse_courses:'کورسز دیکھیں',
    subject:'مضمون', grade_level:'جماعت', description:'تفصیل',
    teacher:'استاد', students:'طلبا', student_count:'طلبا',
    all_courses:'تمام کورسز',
    // Materials
    materials:'مواد', course_materials:'کورس مواد',
    add_material:'+ مواد شامل کریں', title_label:'عنوان', content:'مواد',
    url_label:'لنک (اختیاری)', no_materials:'ابھی کوئی مواد نہیں۔',
    upload_file:'فائل اپ لوڈ کریں', link_text:'لنک / متن',
    file_upload_hint:'کوئی بھی فائل (پی ڈی ایف، ویڈیو، تصویر...) — زیادہ سے زیادہ 200 ایم بی',
    download:'ڈاؤن لوڈ', view_file:'دیکھیں',
    // Assignments
    assignments:'اسائنمنٹس', new_assignment:'+ نیا اسائنمنٹ',
    instructions:'ہدایات', due_date:'آخری تاریخ', max_score:'زیادہ سے زیادہ',
    pts:'نمبر', submit_assignment:'اسائنمنٹ جمع کریں',
    your_submission:'آپ کی جمع شدہ کاپی', resubmit:'دوبارہ جمع کریں',
    edit_resubmit:'ترمیم / دوبارہ جمع کریں', not_graded:'ابھی تک گریڈ نہیں ہوئی۔',
    not_submitted:'جمع نہیں کی گئی', submissions:'جمع شدہ کاپیاں',
    no_submissions:'ابھی کوئی کاپی نہیں۔', feedback:'رائے',
    score:'نمبر', save_grade:'گریڈ محفوظ کریں', graded:'گریڈ ہو گئی',
    // Quizzes
    quizzes:'کوئز', new_quiz:'+ نیا کوئز', quiz_builder:'کوئز بنائیں',
    add_question:'+ سوال شامل کریں', question_type:'سوال کی قسم',
    multiple_choice:'چار انتخابی', true_false:'درست / غلط',
    short_answer:'مختصر جواب', question_text:'سوال', points:'نمبر',
    correct_answer:'درست', start_quiz:'کوئز شروع کریں', submit_quiz:'کوئز جمع کریں',
    quiz_results:'نتائج دیکھیں', time_limit:'وقت کی حد (منٹ)',
    minutes:'منٹ', time_remaining:'باقی وقت', no_quizzes:'ابھی کوئی کوئز نہیں۔',
    attempt_count:'کوششیں', not_attempted:'کوشش نہیں کی',
    attempted:'کوشش کی گئی', q_num:'سوال', of:'میں سے',
    short_manual:'مختصر جواب — استاد خود گریڈ دیں گے۔',
    quiz_submitted:'کوئز جمع ہو گیا!', your_score:'آپ کا سکور',
    correct:'درست', wrong:'غلط', your_answer:'آپ کا جواب',
    // Sessions
    sessions:'سیشنز', new_session:'+ نیا سیشن', virtual:'آن لائن',
    physical:'ذاتی حاضری', session_type:'سیشن کی قسم',
    meeting_link:'میٹنگ لنک / یو آر ایل', location:'کمرہ / مقام',
    duration:'مدت (منٹ)', notes:'نوٹس',
    join:'شامل ہوں', no_sessions:'کوئی سیشن شیڈول نہیں۔',
    upcoming:'آنے والے', past:'گزرے ہوئے', mins:'منٹ',
    // Announcements
    announcements:'اعلانات', school_announcements:'اسکول کے اعلانات',
    post_announcement:'+ اعلان پوسٹ کریں',
    course_announcements:'کورس کے اعلانات', no_announcements:'کوئی اعلان نہیں۔',
    // Users
    user_management:'صارف انتظام', add_user:'+ صارف شامل کریں',
    full_name:'پورا نام', role:'کردار', all:'سب', admins:'منتظمین',
    teachers:'اساتذہ', you:'آپ',
    // Settings
    settings:'ترتیبات', language:'زبان', language_desc:'اپنی پسندیدہ زبان منتخب کریں',
    profile:'میری پروفائل', profile_desc:'اپنا نام یا پاس ورڈ تبدیل کریں',
    update_profile:'پروفائل اپڈیٹ کریں',
    new_password:'نیا پاس ورڈ (خالی چھوڑیں تو پرانا رہے گا)',
    profile_saved:'پروفائل اپڈیٹ ہو گئی!',
    // New features (Urdu)
    nav_gradebook:'گریڈ بک', nav_analytics:'تجزیات', nav_calendar:'کیلنڈر',
    nav_badges:'بیجز', nav_messages:'پیغامات', nav_question_banks:'سوال بینک',
    nav_portfolio:'پورٹ فولیو',
    gradebook:'گریڈ بک', my_grades:'میرے نمبر', weighted_avg:'وزنی اوسط',
    letter_grade:'حروفی گریڈ', gpa:'جی پی اے', cumulative_gpa:'مجموعی جی پی اے',
    calendar:'کیلنڈر', upcoming_events:'آنے والے واقعات', no_events:'کوئی واقعات نہیں۔',
    messages:'پیغامات', inbox:'ان باکس', sent:'بھیجے گئے', compose:'+ لکھیں',
    compose_message:'پیغام لکھیں', send:'بھیجیں', no_messages:'کوئی پیغام نہیں۔',
    analytics:'تجزیات', grade_distribution:'نمبروں کی تقسیم',
    badges:'بیجز', my_badges:'میرے بیجز', create_badge:'+ بیج بنائیں',
    portfolio:'پورٹ فولیو', my_portfolio:'میرا پورٹ فولیو',
    modules:'ماڈیولز', discussions:'بحث', surveys:'سروے',
    question_banks:'سوال بینک',
    // Dark mode (Urdu)
    theme:'تھیم', theme_desc:'لائٹ یا ڈارک موڈ منتخب کریں',
    light_mode:'☀️ روشن', dark_mode:'🌙 تاریک',
    // Leaderboard (Urdu)
    leaderboard:'لیڈر بورڈ', nav_leaderboard:'لیڈر بورڈ',
    your_rank:'آپ کی پوزیشن', rank:'پوزیشن', top_students:'اعلیٰ طلبا',
    no_leaderboard_data:'ابھی کوئی گریڈ نہیں۔',
    course_leaderboard:'کورس لیڈر بورڈ', school_leaderboard:'اسکول لیڈر بورڈ',
    // Certificates (Urdu)
    download_certificate:'⬇ سرٹیفکیٹ ڈاؤن لوڈ کریں',
    cert_not_eligible:'سرٹیفکیٹ ابھی دستیاب نہیں',
    cert_requirements:'تمام اسائنمنٹس اور کوئز مکمل کریں (اوسط ≥ ۵۰٪)۔',
    cert_ready:'🎓 آپ کا سرٹیفکیٹ ڈاؤن لوڈ کے لیے تیار ہے!',
    // Retake (Urdu)
    max_attempts:'زیادہ سے زیادہ کوششیں', unlimited:'لامحدود',
    attempts_remaining:'کوششیں باقی', no_attempts_left:'کوئی کوشش باقی نہیں',
    // Quiz publish / edit (Urdu)
    quiz_published:'شائع شدہ', quiz_draft:'مسودہ',
    publish_quiz:'طلبا کو دکھائیں', unpublish_quiz:'چھپائیں',
    edit_quiz:'تفصیل ترمیم', quiz_edit_saved:'کوئز اپڈیٹ ہو گئی!',
    urgent_quizzes:'⚡ ضروری: کوئز اور ٹیسٹ',
    no_urgent:'کوئی زیر التواء کوئز نہیں — آپ نے سب مکمل کر لیے!',
    start_now:'ابھی شروع کریں', resume_quiz:'جاری رکھیں',
    urgent:'ضروری',
    // Post-quiz results (Urdu)
    quiz_score_result:'آپ کا نتیجہ',
    outstanding_quizzes:'باقی کوئز اور ٹیسٹ',
    no_outstanding_quizzes:'کوئی کوئز یا ٹیسٹ باقی نہیں! 🎉 شاباش!',
    outstanding_quizzes_msg:'آپ کے ابھی یہ کوئز / ٹیسٹ باقی ہیں:',
    pending_grading:'استاد کی جانب سے گریڈنگ کا انتظار ہے',
    // Post-submit assignment check (Urdu)
    outstanding_assignments:'باقی اسائنمنٹس',
    no_outstanding:'کوئی اسائنمنٹ باقی نہیں! شاباش! 🎉',
    outstanding_msg:'آپ کے ابھی یہ اسائنمنٹس مکمل کرنے ہیں:',
    go_to_assignment:'اسائنمنٹ دیکھیں',
    well_done:'شاباش!',
    // Misc
    enrolled_courses:'داخل شدہ کورسز', available_courses:'دستیاب',
    total_students:'کل طلبا', manage_courses:'کورسز منظم کریں',
  }
};

function t(key) {
  const lang = state.lang || 'en';
  return (i18n[lang] && i18n[lang][key]) || i18n.en[key] || key;
}

// ═══════════════════════════════════════════════════════════
// State
// ═══════════════════════════════════════════════════════════
const state = {
  token: null, user: null, lang: 'en', theme: 'light',
  currentPage: null, currentParams: {},
  quizTimer: null, notifInterval: null,
};

// ═══════════════════════════════════════════════════════════
// API helper
// ═══════════════════════════════════════════════════════════
async function api(method, path, body) {
  const headers = {};
  if (state.token) headers['Authorization'] = `Bearer ${state.token}`;
  const opts = { method, headers };
  if (body) { headers['Content-Type'] = 'application/json'; opts.body = JSON.stringify(body); }
  const res = await fetch('/api' + path, opts);
  if (res.status === 401) { logout(); return null; }
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    const detail = err.detail;
    const msg = Array.isArray(detail)
      ? detail.map(e => e.msg || JSON.stringify(e)).join('; ')
      : (typeof detail === 'string' ? detail : 'Request failed');
    throw new Error(msg);
  }
  return res.json().catch(() => null);
}

// ═══════════════════════════════════════════════════════════
// Auth
// ═══════════════════════════════════════════════════════════
async function login(email, password) {
  const form = new FormData();
  form.append('username', email); form.append('password', password);
  const res = await fetch('/api/auth/login', { method: 'POST', body: form });
  if (!res.ok) { const e = await res.json(); throw new Error(e.detail || 'Login failed'); }
  const data = await res.json();
  state.token = data.access_token;
  state.user  = { id: data.user_id, name: data.name, role: data.role };
  localStorage.setItem('lms_token', state.token);
  localStorage.setItem('lms_user',  JSON.stringify(state.user));
  return data;
}

function logout() {
  if (state.quizTimer) clearInterval(state.quizTimer);
  if (state.notifInterval) clearInterval(state.notifInterval);
  state.token = null; state.user = null;
  localStorage.removeItem('lms_token'); localStorage.removeItem('lms_user');
  document.getElementById('app').classList.add('hidden');
  document.getElementById('login-page').classList.remove('hidden');
}

function restoreSession() {
  const token = localStorage.getItem('lms_token');
  const user  = localStorage.getItem('lms_user');
  const lang  = localStorage.getItem('lms_lang') || 'en';
  const theme = localStorage.getItem('lms_theme') || 'light';
  applyTheme(theme); // always apply saved theme, even before login
  if (token && user) {
    state.token = token; state.user = JSON.parse(user);
    state.lang = lang;
    applyLang(lang);
    return true;
  }
  return false;
}

// ═══════════════════════════════════════════════════════════
// Language
// ═══════════════════════════════════════════════════════════
function applyLang(lang) {
  document.documentElement.lang = lang;
  document.documentElement.dir  = lang === 'ur' ? 'rtl' : 'ltr';
}

function setLanguage(lang) {
  state.lang = lang;
  localStorage.setItem('lms_lang', lang);
  applyLang(lang);
  updateSidebarNav();
  navigate(state.currentPage || 'dashboard', state.currentParams);
}

// ── Theme (dark / light mode) ────────────────────────────────────────────────
function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  state.theme = theme;
}

function setTheme(theme) {
  applyTheme(theme);
  localStorage.setItem('lms_theme', theme);
  // Re-render settings so the active button updates
  if (state.currentPage === 'settings') {
    navigate('settings', state.currentParams);
  }
}

// ═══════════════════════════════════════════════════════════
// Notifications & Modal
// ═══════════════════════════════════════════════════════════
function toast(msg, type = 'success') {
  const el = document.createElement('div');
  el.className = `toast toast-${type}`; el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3200);
}

function openModal(title, html, onSubmit) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = html;
  document.getElementById('modal-overlay').classList.remove('hidden');
  if (onSubmit) {
    const form = document.getElementById('modal-form');
    if (form) form.onsubmit = async (e) => { e.preventDefault(); await onSubmit(new FormData(form)); };
  }
}
function closeModal() { document.getElementById('modal-overlay').classList.add('hidden'); }

function loading(el) {
  el.innerHTML = `<div class="loading"><div class="spinner"></div><p>${t('loading')}</p></div>`;
}

// ═══════════════════════════════════════════════════════════
// Navigation
// ═══════════════════════════════════════════════════════════
const NAV_KEYS = {
  admin:   ['dashboard','courses','users','announcements','gradebook','analytics','leaderboard','calendar','badges','graph','settings'],
  teacher: ['dashboard','courses','announcements','gradebook','analytics','leaderboard','calendar','messages','question_banks','graph','settings'],
  student: ['dashboard','courses','announcements','gradebook','leaderboard','calendar','messages','ai_tutor','portfolio','badges','sr','graph','settings'],
  parent:  ['dashboard','settings'],
};
const NAV_I18N = {
  dashboard:'nav_dashboard', courses:'nav_courses', users:'nav_users',
  announcements:'nav_announcements', settings:'nav_settings',
  gradebook:'nav_gradebook', analytics:'nav_analytics', calendar:'nav_calendar',
  badges:'nav_badges', messages:'nav_messages', question_banks:'nav_question_banks',
  portfolio:'nav_portfolio', sr:'nav_sr', graph:'nav_graph',
  leaderboard:'nav_leaderboard', ai_tutor:'nav_ai_tutor',
};
const NAV_ICONS = {
  dashboard:'🏠', courses:'📚', users:'👥', announcements:'📢',
  gradebook:'📊', analytics:'📈', calendar:'📅', badges:'🏅',
  messages:'✉️', question_banks:'🗃️', portfolio:'🗂️',
  sr:'🃏', graph:'🕸️', settings:'⚙️', leaderboard:'🏆', ai_tutor:'🤖',
};

// ── Subject → accent colour (used on course cards) ─────────────────────────
function subjectAccent(subject, title) {
  const s = ((subject || '') + ' ' + (title || '')).toLowerCase();
  if (/math|algebra|calculus|geometry|arithmetic|trig|stat/.test(s)) return '#2563eb';
  if (/science|biology|chem|physics|ecology|zoology/.test(s))        return '#059669';
  if (/english|lit|writing|reading|grammar|poetry/.test(s))          return '#7c3aed';
  if (/history|social|civics|geo|economic|politic/.test(s))          return '#d97706';
  if (/art|music|drama|creative|design|craft/.test(s))               return '#db2777';
  if (/computer|tech|it|coding|program|digital/.test(s))             return '#0891b2';
  if (/urdu|arabic|islamiat|quran|religion|ethic/.test(s))           return '#ea580c';
  if (/physical|sport|health|pe|gym|fitness/.test(s))                return '#0d9488';
  return '#4f46e5'; // default indigo
}

function updateSidebarNav() {
  if (!state.user) return;
  const r = state.user.role;
  document.getElementById('sidebar-nav').innerHTML = NAV_KEYS[r].map(p =>
    `<a class="nav-item${state.currentPage===p?' active':''}" data-page="${p}" onclick="navigate('${p}')">
      <span class="nav-icon">${NAV_ICONS[p]||'•'}</span>
      <span class="nav-label">${t(NAV_I18N[p])}</span>
    </a>`
  ).join('');
}

function showApp() {
  document.getElementById('login-page').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  document.getElementById('user-name').textContent = state.user.name;
  document.getElementById('user-avatar').textContent = state.user.name[0].toUpperCase();
  document.getElementById('user-role-badge').textContent = state.user.role;
  updateSidebarNav();
  navigate('dashboard');
  // Start polling notifications every 30s
  refreshNotifCount();
  if (state.notifInterval) clearInterval(state.notifInterval);
  state.notifInterval = setInterval(refreshNotifCount, 30000);
}

async function refreshNotifCount() {
  try {
    const data = await api('GET', '/notifications/unread-count');
    if (data === null) return;
    const badge = document.getElementById('notif-count-badge');
    if (badge) badge.textContent = data.count || '';
    if (badge) badge.style.display = data.count ? 'inline' : 'none';
  } catch(e) { /* silent */ }
}

let _notifOpen = false;
async function toggleNotifDropdown() {
  const dd = document.getElementById('notif-dropdown');
  if (!dd) return;
  _notifOpen = !_notifOpen;
  if (_notifOpen) {
    dd.classList.remove('hidden');
    try {
      const notifs = await api('GET', '/notifications/?limit=10');
      if (!notifs) return;
      dd.innerHTML = notifs.length
        ? notifs.map(n => `
          <div class="notif-item${n.is_read ? '' : ' unread'}" onclick="markNotifRead(${n.id})">
            <div class="notif-title">${n.title}</div>
            ${n.body ? `<div class="notif-body">${n.body.substring(0,60)}</div>` : ''}
            <div class="notif-time">${fmtDateTime(n.created_at)}</div>
          </div>`).join('')
        : `<div class="notif-empty">No notifications</div>`;
    } catch(e) { dd.innerHTML = '<div class="notif-empty">Error loading</div>'; }
  } else {
    dd.classList.add('hidden');
  }
}

async function markNotifRead(id) {
  try {
    await api('PUT', `/notifications/${id}/read`);
    refreshNotifCount();
    toggleNotifDropdown(); toggleNotifDropdown(); // refresh
  } catch(e) { /* silent */ }
}

function navigate(page, params = {}) {
  if (state.quizTimer) { clearInterval(state.quizTimer); state.quizTimer = null; }
  state.currentPage = page; state.currentParams = params;
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const a = document.querySelector(`.nav-item[data-page="${page}"]`);
  if (a) a.classList.add('active');
  const el = document.getElementById('page-content');
  const pages = {
    dashboard: renderDashboard, courses: renderCourses,
    users: renderUsers, announcements: renderAnnouncements, settings: renderSettings,
    gradebook: renderGradebook, calendar: renderCalendar, messages: renderMessages,
    analytics: renderAnalytics, badges: renderBadges, portfolio: renderPortfolio,
    question_banks: renderQuestionBanks, ai_tutor: renderAiTutor,
  };
  if      (page === 'course')        renderCourseDetail(params.id, el);
  else if (page === 'assignment')    renderAssignmentDetail(params.id, el);
  else if (page === 'quiz-builder')  renderQuizBuilder(params.id, el);
  else if (page === 'quiz-take')     renderQuizTake(params.id, el);
  else if (page === 'discussion-board') renderDiscussionBoard(params.id, el);
  else if (page === 'ai-chat')       renderAiChat(params.id, el);
  // ── Learning Intelligence & Social ───────────────────────────────────────
  else if (page === 'sr')          { if (typeof renderSRReview       !== 'undefined') renderSRReview(el); }
  else if (page === 'graph')       { if (typeof renderKnowledgeGraph  !== 'undefined') renderKnowledgeGraph(el); }
  else if (page === 'leaderboard') renderLeaderboard(el);
  else if (pages[page])            pages[page](el);
}

/** Escape a string for safe insertion into HTML attribute values or text nodes. */
function htmlEsc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function fmtDate(d) {
  if (!d) return '—';
  return new Date(d).toLocaleDateString('en-GB', { day:'numeric', month:'short', year:'numeric' });
}
function fmtDateTime(d) {
  if (!d) return '—';
  return new Date(d).toLocaleString('en-GB', { day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
}
function isPast(d) { return d && new Date(d) < new Date(); }

// ═══════════════════════════════════════════════════════════
// Profile Update
// ═══════════════════════════════════════════════════════════
async function updateProfile() {
  const name = document.getElementById('profile-name').value.trim();
  const pw   = document.getElementById('profile-password').value;
  const body = {};
  if (name) body.name = name;
  if (pw)   body.password = pw;
  try {
    const updated = await api('PUT', '/users/me', body);
    state.user.name = updated.name;
    localStorage.setItem('lms_user', JSON.stringify(state.user));
    document.getElementById('user-name').textContent = updated.name;
    document.getElementById('user-avatar').textContent = updated.name[0].toUpperCase();
    toast(t('profile_saved'));
  } catch(err) { toast(err.message, 'error'); }
}

// ═══════════════════════════════════════════════════════════
// Settings Page
// ═══════════════════════════════════════════════════════════
function renderSettings(el) {
  el.innerHTML = `
    <div class="page-header"><h2>${t('settings')}</h2></div>

    <div class="card settings-section">
      <div class="card-header"><h3>${t('language')}</h3></div>
      <div class="card-body">
        <p class="text-muted">${t('language_desc')}</p>
        <div class="lang-buttons">
          <button class="lang-btn${state.lang==='en'?' active':''}" onclick="setLanguage('en')">
            🇬🇧&nbsp; English
          </button>
          <button class="lang-btn${state.lang==='ur'?' active':''}" onclick="setLanguage('ur')">
            🇵🇰&nbsp; اردو
          </button>
        </div>
      </div>
    </div>

    <div class="card settings-section">
      <div class="card-header"><h3>🌓 ${t('theme')}</h3></div>
      <div class="card-body">
        <p class="text-muted">${t('theme_desc')}</p>
        <div class="lang-buttons">
          <button class="lang-btn${state.theme==='light'?' active':''}" onclick="setTheme('light')">${t('light_mode')}</button>
          <button class="lang-btn${state.theme==='dark'?' active':''}" onclick="setTheme('dark')">${t('dark_mode')}</button>
        </div>
      </div>
    </div>

    <div class="card settings-section">
      <div class="card-header"><h3>${t('profile')}</h3></div>
      <div class="card-body">
        <p class="text-muted" style="margin-bottom:16px">${t('profile_desc')}</p>
        <div class="form-group">
          <label>${t('full_name')}</label>
          <input id="profile-name" class="form-control" value="${htmlEsc(state.user.name)}">
        </div>
        <div class="form-group">
          <label>${t('new_password')}</label>
          <input id="profile-password" type="password" class="form-control" placeholder="••••••••">
        </div>
        <button class="btn btn-primary" onclick="updateProfile()">${t('update_profile')}</button>
      </div>
    </div>`;
}

// ═══════════════════════════════════════════════════════════
// Dashboard
// ═══════════════════════════════════════════════════════════
async function renderDashboard(el) {
  loading(el);
  const role = state.user.role;
  try {
    if (role === 'admin') {
      const [users, courses, anns] = await Promise.all([
        api('GET','/users/'), api('GET','/courses/'), api('GET','/announcements/')
      ]);
      el.innerHTML = `
        <div class="welcome-banner">
          <h2>👋 ${t('welcome')}, ${state.user.name}!</h2>
          <p>${t('nav_dashboard')} — EduPortal School Management</p>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card-blue"   data-icon="🎓"><div class="stat-number">${users.filter(u=>u.role==='student').length}</div><div class="stat-label">${t('students')}</div></div>
          <div class="stat-card stat-card-purple" data-icon="🧑‍🏫"><div class="stat-number">${users.filter(u=>u.role==='teacher').length}</div><div class="stat-label">${t('teachers')}</div></div>
          <div class="stat-card stat-card-green"  data-icon="📚"><div class="stat-number">${courses.length}</div><div class="stat-label">${t('courses')}</div></div>
          <div class="stat-card stat-card-gold"   data-icon="📢"><div class="stat-number">${anns.length}</div><div class="stat-label">${t('announcements')}</div></div>
        </div>
        <div class="card"><div class="card-header ch-gold"><h3>📢 ${t('announcements')}</h3>
          <button class="btn btn-sm btn-primary" onclick="navigate('announcements')">${t('nav_announcements')}</button></div>
          <div class="card-body">
            ${anns.length ? anns.slice(0,4).map(a=>`
              <div class="announcement-item"><strong>${htmlEsc(a.title)}</strong><p>${htmlEsc(a.content)}</p>
              <small>${t('by')} ${htmlEsc(a.author_name)} &bull; ${fmtDate(a.created_at)}</small></div>`).join('')
            : `<p class="text-muted">${t('no_announcements')}</p>`}
          </div>
        </div>`;

    } else if (role === 'teacher') {
      const [courses] = await Promise.all([api('GET','/courses/')]);
      const mine = courses.filter(c => c.teacher_id === state.user.id);
      el.innerHTML = `
        <div class="welcome-banner">
          <h2>👋 ${t('welcome')}, ${state.user.name}!</h2>
          <p>🧑‍🏫 ${t('teachers')} Dashboard — EduPortal</p>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card-blue"  data-icon="📚"><div class="stat-number">${mine.length}</div><div class="stat-label">${t('my_courses')}</div></div>
          <div class="stat-card stat-card-green" data-icon="🎓"><div class="stat-number">${mine.reduce((s,c)=>s+c.student_count,0)}</div><div class="stat-label">${t('total_students')}</div></div>
        </div>
        <div class="card"><div class="card-header ch-green"><h3>📚 ${t('my_courses')}</h3>
          <button class="btn btn-sm btn-primary" onclick="openNewCourseModal()">${t('new_course')}</button></div>
          <div class="card-body">
            ${mine.length ? mine.map(c=>`
              <div class="course-item" onclick="navigate('course',{id:${c.id}})">
                <div><strong>${c.title}</strong><small>${c.subject||''} ${c.grade_level?'· '+c.grade_level:''}</small></div>
                <span class="badge badge-info">${c.student_count} ${t('student_count')}</span>
              </div>`).join('') : `<p class="text-muted">${t('no_courses')}</p>`}
          </div>
        </div>`;

    } else {
      const [courses, anns] = await Promise.all([api('GET','/courses/'), api('GET','/announcements/')]);
      const enrolled = courses.filter(c => c.enrolled);
      el.innerHTML = `
        <div class="welcome-banner">
          <h2>👋 ${t('welcome')}, ${state.user.name}!</h2>
          <p>🎓 ${t('students')} Dashboard — EduPortal</p>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card-green"  data-icon="📚"><div class="stat-number">${enrolled.length}</div><div class="stat-label">${t('enrolled_courses')}</div></div>
          <div class="stat-card stat-card-teal"   data-icon="🔍"><div class="stat-number">${courses.length-enrolled.length}</div><div class="stat-label">${t('available_courses')}</div></div>
        </div>
        <!-- Urgent quizzes panel (populated async below) -->
        <div class="card" id="urgent-quizzes-card">
          <div class="card-header ch-red"><h3>${t('urgent_quizzes')}</h3></div>
          <div class="card-body" id="urgent-quizzes-body">
            <div class="loading"><div class="spinner"></div></div>
          </div>
        </div>
        <div class="card"><div class="card-header ch-green"><h3>📚 ${t('my_courses')}</h3>
          <button class="btn btn-sm btn-primary" onclick="navigate('courses')">${t('browse_courses')}</button></div>
          <div class="card-body">
            ${enrolled.length ? enrolled.map(c=>`
              <div class="course-item" onclick="navigate('course',{id:${c.id}})">
                <div><strong>${c.title}</strong><small>${t('teacher')}: ${c.teacher_name||'?'}</small></div>
                <span class="badge badge-success">${t('enrolled')}</span>
              </div>`).join('') : `<p class="text-muted">${t('no_courses')}</p>`}
          </div>
        </div>
        ${anns.length ? `<div class="card"><div class="card-header"><h3>${t('announcements')}</h3></div>
          <div class="card-body">${anns.slice(0,3).map(a=>`
            <div class="announcement-item"><strong>${htmlEsc(a.title)}</strong><p>${htmlEsc(a.content)}</p>
            <small>${t('by')} ${htmlEsc(a.author_name)} &bull; ${fmtDate(a.created_at)}</small></div>`).join('')}
          </div></div>` : ''}`;
      // Populate urgent quizzes asynchronously
      loadUrgentQuizzes(enrolled);
    }
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

// ═══════════════════════════════════════════════════════════
// Courses
// ═══════════════════════════════════════════════════════════
async function renderCourses(el) {
  loading(el);
  try {
    const courses = await api('GET','/courses/');
    el.innerHTML = `
      <div class="page-header">
        <h2>${t('all_courses')}</h2>
        ${state.user.role !== 'student' ? `<button class="btn btn-primary" onclick="openNewCourseModal()">${t('new_course')}</button>` : ''}
      </div>
      <div class="courses-grid">${courses.map(courseCard).join('') || `<p class="text-muted">${t('no_courses')}</p>`}</div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function courseCard(c) {
  const role = state.user.role;
  const canManage = role === 'admin' || (role === 'teacher' && c.teacher_id === state.user.id);
  const accent = subjectAccent(c.subject, c.title);
  return `
    <div class="course-card" style="--accent:${accent}" onclick="navigate('course',{id:${c.id}})">
      <div class="course-card-header">
        <h3>${c.title}</h3>
        ${c.grade_level ? `<span class="badge badge-info">${c.grade_level}</span>` : ''}
      </div>
      <div class="course-card-body">
        ${c.subject ? `<p style="color:${accent};font-weight:600;font-size:12px">${c.subject}</p>` : ''}
        ${c.description ? `<p>${c.description.substring(0,90)}${c.description.length>90?'…':''}</p>` : ''}
        <div class="course-meta">
          <small>🧑‍🏫 ${c.teacher_name||'?'}</small>
          <small>👥 ${c.student_count} ${t('student_count')}</small>
        </div>
      </div>
      <div class="course-card-footer" onclick="event.stopPropagation()">
        ${role==='student'
          ? (c.enrolled
            ? `<button class="btn btn-sm btn-danger" onclick="unenrollCourse(${c.id})">${t('unenroll')}</button>`
            : `<button class="btn btn-sm btn-primary" onclick="enrollCourse(${c.id})">${t('enroll')}</button>`)
          : ''}
        ${canManage ? `<button class="btn btn-sm btn-danger" onclick="deleteCourse(${c.id})">${t('delete')}</button>` : ''}
      </div>
    </div>`;
}

function openNewCourseModal() {
  openModal(t('new_course'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required placeholder="e.g. Mathematics Grade 8"></div>
      <div class="form-row">
        <div class="form-group"><label>${t('subject')}</label>
          <input name="subject" class="form-control" placeholder="Mathematics"></div>
        <div class="form-group"><label>${t('grade_level')}</label>
          <input name="grade_level" class="form-control" placeholder="Grade 8"></div>
      </div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control"></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST','/courses/',{ title:fd.get('title'), subject:fd.get('subject')||null,
          grade_level:fd.get('grade_level')||null, description:fd.get('description')||null });
        closeModal(); toast(t('new_course')); navigate('courses');
      } catch(err) { toast(err.message,'error'); }
    });
}

async function enrollCourse(id) {
  try { await api('POST',`/courses/${id}/enroll`); toast(t('enrolled')+'!'); navigate('courses'); }
  catch(err) { toast(err.message,'error'); }
}
async function unenrollCourse(id) {
  if (!confirm(t('unenroll')+'?')) return;
  try { await api('DELETE',`/courses/${id}/enroll`); toast(t('unenroll')); navigate('courses'); }
  catch(err) { toast(err.message,'error'); }
}
async function deleteCourse(id) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE',`/courses/${id}`); toast(t('delete')); navigate('courses'); }
  catch(err) { toast(err.message,'error'); }
}

// ═══════════════════════════════════════════════════════════
// Course Detail
// ═══════════════════════════════════════════════════════════
async function renderCourseDetail(courseId, el) {
  loading(el);
  try {
    const [course, materials, assignments, anns, sessions, quizzes] = await Promise.all([
      api('GET',`/courses/${courseId}`),
      api('GET',`/courses/${courseId}/materials`),
      api('GET',`/assignments/course/${courseId}`),
      api('GET',`/announcements/?course_id=${courseId}`),
      api('GET',`/sessions/course/${courseId}`),
      api('GET',`/quizzes/course/${courseId}`),
    ]);
    const role = state.user.role;
    const canManage = role==='admin' || (role==='teacher' && course.teacher_id===state.user.id);
    const now = new Date();

    el.innerHTML = `
      <div class="page-header">
        <div>
          <button class="btn btn-sm" onclick="navigate('courses')" style="margin-bottom:8px">${t('back')}</button>
          <h2>${course.title}</h2>
          <div class="flex-gap mt-8">
            ${course.subject    ? `<span class="badge badge-info">${course.subject}</span>`     : ''}
            ${course.grade_level? `<span class="badge badge-info">${course.grade_level}</span>` : ''}
          </div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px">
          <small class="text-muted">${t('teacher')}: ${course.teacher_name||'?'}</small>
          ${role === 'student' ? `<button class="btn btn-sm btn-success" onclick="downloadCertificate(${courseId})">
            ${t('download_certificate')}
          </button>` : ''}
        </div>
      </div>
      ${course.description ? `<div class="card"><div class="card-body"><p>${course.description}</p></div></div>` : ''}

      <div class="tabs">
        <button class="tab active" onclick="showTab('materials',this)">${t('materials')} (${materials.length})</button>
        <button class="tab" onclick="showTab('assignments',this)">${t('assignments')} (${assignments.length})</button>
        <button class="tab" onclick="showTab('quizzes',this)">${t('quizzes')} (${quizzes.length})</button>
        <button class="tab" onclick="showTab('sessions',this)">${t('sessions')} (${sessions.length})</button>
        <button class="tab" onclick="showTab('modules',this);renderModulesTab(${courseId},document.getElementById('tab-modules'),${canManage})">${t('modules')}</button>
        <button class="tab" onclick="showTab('discussions',this);renderDiscussionsTab(${courseId},document.getElementById('tab-discussions'),${canManage})">${t('discussions')}</button>
        <button class="tab" onclick="showTab('surveys',this);renderSurveysTab(${courseId},document.getElementById('tab-surveys'),${canManage})">${t('surveys')}</button>
        <!-- ── New feature tabs ── -->
        <button class="tab" onclick="showTab('helpboard',this);renderHelpBoardTab(${courseId}).then(h=>document.getElementById('tab-helpboard').innerHTML=h)">${t('help_board')}</button>
        <button class="tab" onclick="showTab('teachback',this);renderTeachBackTab(${courseId},${canManage}).then(h=>document.getElementById('tab-teachback').innerHTML=h)">${t('teach_back')}</button>
        <button class="tab" onclick="showTab('studygroups',this);renderStudyGroupsTab(${courseId},${canManage}).then(h=>document.getElementById('tab-studygroups').innerHTML=h)">${t('study_groups')}</button>
        ${canManage ? `<button class="tab" onclick="showTab('students',this)">${t('students')} (${course.students.length})</button>` : ''}
        ${canManage ? `<button class="tab" onclick="showTab('anns',this)">${t('announcements')}</button>` : ''}
      </div>

      <!-- MATERIALS -->
      <div id="tab-materials">
        <div class="card">
          <div class="card-header"><h3>${t('course_materials')}</h3>
            ${canManage ? `<button class="btn btn-sm btn-primary" onclick="openAddMaterialModal(${courseId})">${t('add_material')}</button>` : ''}</div>
          <div class="card-body">
            ${materials.length ? materials.map(m => {
              const mtype = m.material_type || (m.url ? 'link' : 'text');
              const icon = mtype === 'file' ? fileMimeIcon(m.file_mime) : (mtype === 'link' ? '🔗' : '📝');
              const badge = `<span class="mat-type-badge mat-type-${mtype}">${mtype}</span>`;
              const isViewable = m.file_mime && (
                m.file_mime.startsWith('image/') || m.file_mime.startsWith('video/') ||
                m.file_mime.startsWith('audio/') || m.file_mime === 'application/pdf' ||
                m.file_mime.startsWith('text/')
              );
              let body = '';
              if (mtype === 'file') {
                const sz = formatFileSize(m.file_size);
                const btnLabel = isViewable ? `👁 ${t('view_file')}` : `⬇ ${t('download')}`;
                body = `
                  <div class="mat-file-info">
                    <span class="mat-filename">${m.file_name || ''}</span>
                    ${sz ? `<span class="mat-filesize">${sz}</span>` : ''}
                  </div>
                  <div class="mat-actions-inline">
                    <a class="btn btn-sm btn-primary" href="#"
                       onclick="return viewMaterialFile(event,this)"
                       data-course="${courseId}"
                       data-mid="${m.id}"
                       data-fname="${(m.file_name||'download').replace(/"/g,'&quot;')}"
                       data-mime="${(m.file_mime||'').replace(/"/g,'&quot;')}"
                    >${btnLabel}</a>
                  </div>`;
              } else if (mtype === 'link') {
                body = (m.content ? `<p class="mat-content">${m.content}</p>` : '') +
                       `<a class="link mat-link" href="${m.url}" target="_blank" rel="noopener">${m.url}</a>`;
              } else {
                body = m.content ? `<p class="mat-content">${m.content}</p>` : '';
              }
              return `
                <div class="material-item">
                  <div class="material-icon">${icon}</div>
                  <div class="material-body">
                    <div class="material-title"><strong>${m.title}</strong>${badge}</div>
                    ${body}
                    <small class="text-muted">${fmtDate(m.created_at)}</small>
                  </div>
                  ${canManage ? `<button class="btn btn-sm btn-danger" onclick="deleteMaterial(${courseId},${m.id})">${t('delete')}</button>` : ''}
                </div>`;
            }).join('') : `<p class="text-muted">${t('no_materials')}</p>`}
          </div>
        </div>
      </div>

      <!-- ASSIGNMENTS -->
      <div id="tab-assignments" class="hidden">
        <div class="card">
          <div class="card-header"><h3>${t('assignments')}</h3>
            ${canManage ? `<button class="btn btn-sm btn-primary" onclick="openNewAssignmentModal(${courseId})">${t('new_assignment')}</button>` : ''}</div>
          <div class="card-body">
            ${assignments.length ? assignments.map(a=>`
              <div class="list-item clickable" onclick="navigate('assignment',{id:${a.id}})">
                <div>
                  <strong>${a.title}</strong>
                  <div class="assignment-meta">
                    ${a.due_date ? `<small>${t('due_date')}: ${fmtDate(a.due_date)}</small>` : ''}
                    <small>${t('max_score')}: ${a.max_score} ${t('pts')}</small>
                    ${canManage && a.submission_count!=null ? `<small>${a.submission_count} ${t('submissions')}</small>` : ''}
                  </div>
                  ${a.my_submission
                    ? `<span class="badge ${a.my_submission.score!=null?'badge-success':'badge-warning'}">
                        ${a.my_submission.score!=null?`${t('score')}: ${a.my_submission.score}/${a.max_score}`:t('submitted_assignment')}</span>`
                    : (role==='student'?`<span class="badge badge-danger">${t('not_submitted')}</span>`:'')}
                </div>
              </div>`).join('') : `<p class="text-muted">${t('no_submissions')}</p>`}
          </div>
        </div>
      </div>

      <!-- QUIZZES -->
      <div id="tab-quizzes" class="hidden">
        <div class="card">
          <div class="card-header"><h3>${t('quizzes')}</h3>
            ${canManage ? `<button class="btn btn-sm btn-primary" onclick="openNewQuizModal(${courseId})">${t('new_quiz')}</button>` : ''}</div>
          <div class="card-body">
            ${quizzes.length ? quizzes.map(q=>quizCard(q, canManage, courseId)).join('')
                             : `<p class="text-muted">${t('no_quizzes')}</p>`}
          </div>
        </div>
      </div>

      <!-- SESSIONS -->
      <div id="tab-sessions" class="hidden">
        <div class="card">
          <div class="card-header"><h3>${t('sessions')}</h3>
            ${canManage ? `<button class="btn btn-sm btn-primary" onclick="openNewSessionModal(${courseId})">${t('new_session')}</button>` : ''}</div>
          <div class="card-body">
            ${sessions.length ? sessions.map(s=>sessionCard(s, canManage)).join('')
                              : `<p class="text-muted">${t('no_sessions')}</p>`}
          </div>
        </div>
      </div>

      <!-- MODULES -->
      <div id="tab-modules" class="hidden">
        <div class="card"><div class="card-body"><p class="text-muted">Loading modules…</p></div></div>
      </div>

      <!-- DISCUSSIONS -->
      <div id="tab-discussions" class="hidden">
        <div class="card"><div class="card-body"><p class="text-muted">Loading discussions…</p></div></div>
      </div>

      <!-- SURVEYS -->
      <div id="tab-surveys" class="hidden">
        <div class="card"><div class="card-body"><p class="text-muted">Loading surveys…</p></div></div>
      </div>

      <!-- HELP BOARD (async rendered by features.js) -->
      <div id="tab-helpboard" class="hidden">
        <div class="loading"><div class="spinner"></div></div>
      </div>

      <!-- TEACH-BACK (async rendered by features.js) -->
      <div id="tab-teachback" class="hidden">
        <div class="loading"><div class="spinner"></div></div>
      </div>

      <!-- STUDY GROUPS (async rendered by features.js) -->
      <div id="tab-studygroups" class="hidden">
        <div class="loading"><div class="spinner"></div></div>
      </div>

      <!-- STUDENTS (teacher/admin) -->
      ${canManage ? `
      <div id="tab-students" class="hidden">
        <div class="card">
          <div class="card-header"><h3>${t('students')}</h3></div>
          <div class="card-body">
            ${course.students.length ? `
              <table class="table">
                <thead><tr><th>${t('full_name')}</th><th>${t('email')}</th></tr></thead>
                <tbody>${course.students.map(s=>`<tr><td>${s.name}</td><td>${s.email}</td></tr>`).join('')}</tbody>
              </table>` : `<p class="text-muted">${t('students')} — 0</p>`}
          </div>
        </div>
      </div>
      <div id="tab-anns" class="hidden">
        <div class="card">
          <div class="card-header"><h3>${t('course_announcements')}</h3>
            <button class="btn btn-sm btn-primary" onclick="openAnnouncementModal(${courseId})">${t('post_announcement')}</button></div>
          <div class="card-body">
            ${anns.length ? anns.map(a=>`
              <div class="announcement-item">
                <div class="announcement-header"><strong>${htmlEsc(a.title)}</strong>
                  <button class="btn btn-sm btn-danger" onclick="deleteAnnouncement(${a.id},${courseId})">${t('delete')}</button></div>
                <p>${htmlEsc(a.content)}</p>
                <small>${htmlEsc(a.author_name)} &bull; ${fmtDate(a.created_at)}</small>
              </div>`).join('') : `<p class="text-muted">${t('no_announcements')}</p>`}
          </div>
        </div>
      </div>` : ''}
    `;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function showTab(name, btn) {
  document.querySelectorAll('[id^="tab-"]').forEach(t => t.classList.add('hidden'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  const tabEl = document.getElementById(`tab-${name}`);
  if (tabEl) tabEl.classList.remove('hidden');
  btn.classList.add('active');
}

// ── Quiz card (in course detail list) ──
function quizCard(q, canManage, courseId) {
  const attempted  = q.my_attempt && q.my_attempt.submitted_at;
  const inProgress = q.my_attempt && !q.my_attempt.submitted_at;
  const scoreLabel = attempted
    ? `${t('score')}: ${q.my_attempt.score!=null ? q.my_attempt.score : '?'}/${q.total_points}`
    : (inProgress ? t('attempted') : t('not_attempted'));
  const attemptBadgeCls = attempted ? 'badge-success' : (inProgress ? 'badge-warning' : 'badge-secondary');

  // Students: flag unpublished-but-not-attempted as urgent
  const isUrgent = !canManage && q.is_published && !attempted && !inProgress;

  return `
    <div class="quiz-card${isUrgent ? ' quiz-urgent' : ''}">
      <div class="quiz-card-body">
        <div class="quiz-title-row">
          <strong>${q.title}</strong>
          ${isUrgent ? `<span class="badge badge-danger">⚡ ${t('urgent')}</span>` : ''}
          ${canManage
            ? (q.is_published
              ? `<span class="badge badge-success">✓ ${t('quiz_published')}</span>`
              : `<span class="badge badge-warning">✏️ ${t('quiz_draft')}</span>`)
            : ''}
        </div>
        ${q.description ? `<p class="text-muted" style="margin-top:4px;font-size:13px">${q.description}</p>` : ''}
        <div class="quiz-meta">
          <small>${q.question_count} ${t('question_text')}(s) &bull; ${q.total_points} ${t('pts')}</small>
          ${q.time_limit ? `<small>⏱ ${q.time_limit} ${t('minutes')}</small>` : ''}
          ${q.due_date ? `<small>📅 ${t('due_date')}: ${fmtDate(q.due_date)}</small>` : ''}
          ${canManage && q.attempt_count!=null ? `<small>👥 ${q.attempt_count} ${t('attempt_count')}</small>` : ''}
          ${canManage && q.max_attempts ? `<small>🔁 ${t('max_attempts')}: ${q.max_attempts}</small>` : ''}
          ${!canManage && q.max_attempts ? (() => {
            const left = q.max_attempts - (q.attempts_used || 0);
            return left > 0
              ? `<small style="color:var(--warning)">🔁 ${left} ${t('attempts_remaining')}</small>`
              : `<small style="color:var(--danger)">🚫 ${t('no_attempts_left')}</small>`;
          })() : ''}
        </div>
      </div>
      <div class="quiz-card-actions">
        ${!canManage ? `<span class="badge ${attemptBadgeCls}">${scoreLabel}</span>` : ''}
        ${!canManage && !attempted && !inProgress && q.question_count > 0
          && !(q.max_attempts && (q.attempts_used || 0) >= q.max_attempts)
          ? `<button class="btn btn-sm btn-primary" onclick="startQuiz(${q.id})">▶ ${t('start_quiz')}</button>` : ''}
        ${!canManage && inProgress
          ? `<button class="btn btn-sm btn-warning" onclick="navigate('quiz-take',{id:${q.id}})">▶ ${t('resume_quiz')}</button>` : ''}
        ${!canManage && attempted
          ? `<button class="btn btn-sm" onclick="navigate('quiz-take',{id:${q.id}})">${t('quiz_results')}</button>` : ''}
        ${canManage ? `
          <button class="btn btn-sm ${q.is_published ? 'btn-warning' : 'btn-success'}"
            onclick="togglePublishQuiz(${q.id},${q.is_published},${courseId})">
            ${q.is_published ? t('unpublish_quiz') : t('publish_quiz')}
          </button>
          <button class="btn btn-sm btn-primary" onclick="navigate('quiz-builder',{id:${q.id}})">${t('quiz_builder')}</button>
          <button class="btn btn-sm btn-danger" onclick="deleteQuiz(${q.id},${courseId})">${t('delete')}</button>
        ` : ''}
      </div>
    </div>`;
}

// ── Session card ──
function sessionCard(s, canManage) {
  const isVirtual = s.session_type === 'virtual';
  const icon = isVirtual ? '💻' : '🏫';
  const past = isPast(s.date);
  return `
    <div class="session-card">
      <div class="session-icon ${s.session_type}">${icon}</div>
      <div class="session-body">
        <strong>${s.title}</strong>
        <div class="session-meta">
          <span class="badge badge-${s.session_type}">${t(s.session_type)}</span>
          <small>📅 ${fmtDateTime(s.date)}</small>
          <small>⏱ ${s.duration_minutes} ${t('mins')}</small>
          ${s.location ? (isVirtual
            ? `<a class="link" href="${s.location}" target="_blank">${t('join')}</a>`
            : `<small>📍 ${s.location}</small>`) : ''}
        </div>
        ${s.notes ? `<p class="text-muted" style="font-size:12px;margin-top:4px">${s.notes}</p>` : ''}
      </div>
      <div class="session-actions">
        ${isVirtual && s.location && !past
          ? `<a href="${s.location}" target="_blank" class="btn btn-sm btn-primary">${t('join')}</a>` : ''}
        ${canManage ? `<button class="btn btn-sm btn-danger" onclick="deleteSession(${s.id},${s.course_id||0})">${t('delete')}</button>` : ''}
      </div>
    </div>`;
}

// ═══════════════════════════════════════════════════════════
// Material helpers
// ═══════════════════════════════════════════════════════════
function fileMimeIcon(mime) {
  if (!mime) return '📄';
  if (mime.startsWith('image/')) return '🖼️';
  if (mime.startsWith('video/')) return '🎬';
  if (mime.startsWith('audio/')) return '🎵';
  if (mime === 'application/pdf') return '📕';
  if (mime.includes('word') || mime.includes('msword') || mime.includes('document')) return '📝';
  if (mime.includes('excel') || mime.includes('spreadsheet') || mime.includes('sheet')) return '📊';
  if (mime.includes('powerpoint') || mime.includes('presentation')) return '📊';
  if (mime.includes('zip') || mime.includes('compressed') || mime.includes('archive') || mime.includes('tar')) return '🗜️';
  if (mime.startsWith('text/')) return '📃';
  return '📄';
}

function formatFileSize(bytes) {
  if (!bytes) return '';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
}

function switchMatMode(mode, btn) {
  document.querySelectorAll('.mat-mode-tab').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('mat-link-sect').classList.toggle('hidden', mode === 'file');
  document.getElementById('mat-file-sect').classList.toggle('hidden', mode === 'link');
  document.getElementById('modal-form').dataset.mode = mode;
}

function viewMaterialFile(event, el) {
  event.preventDefault();
  // Values come from data-* attributes to avoid double-quote conflicts
  // that would break onclick="..." when JSON.stringify embeds its own quotes.
  const courseId   = el.dataset.course;
  const materialId = el.dataset.mid;
  const fileName   = el.dataset.fname;
  const mime       = el.dataset.mime;

  // Append the JWT as a query param so the browser can open/stream the URL
  // directly without needing a custom Authorization header.
  // This is essential for videos: the browser must stream via Range requests,
  // not download the whole file as a blob first.
  const fileUrl = `/api/courses/${courseId}/materials/${materialId}/file?dl_token=${encodeURIComponent(state.token)}`;

  const isVideo = mime && mime.startsWith('video/');
  const isAudio = mime && mime.startsWith('audio/');
  const isImage = mime && mime.startsWith('image/');
  const isPdf   = mime === 'application/pdf';

  if (isVideo || isAudio) {
    // Embed a native player in a modal so it streams without leaving the page
    const tag  = isVideo ? 'video' : 'audio';
    const icon = isVideo ? '🎬' : '🎵';
    openModal(`${icon} ${fileName || 'Media'}`,
      `<div style="text-align:center;padding:8px 0">
        <${tag} controls autoplay
          style="max-width:100%;max-height:60vh;border-radius:8px;background:#000"
          src="${fileUrl}">
          Your browser does not support this media type.
        </${tag}>
        <br><br>
        <a class="btn btn-sm btn-primary" href="${fileUrl}" download="${fileName||'download'}">
          ⬇ Download
        </a>
      </div>`
    );
  } else if (isPdf || isImage) {
    // PDFs and images open natively in a new browser tab
    window.open(fileUrl, '_blank');
  } else {
    // Everything else: force download via a hidden <a>
    const a = document.createElement('a');
    a.href = fileUrl;
    a.download = fileName || 'download';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
  return false;
}

// ═══════════════════════════════════════════════════════════
// Materials
// ═══════════════════════════════════════════════════════════
function openAddMaterialModal(courseId) {
  openModal(t('add_material'), `
    <div class="mat-mode-tabs">
      <button type="button" class="mat-mode-tab active" onclick="switchMatMode('link',this)">🔗 ${t('link_text')}</button>
      <button type="button" class="mat-mode-tab" onclick="switchMatMode('file',this)">📁 ${t('upload_file')}</button>
    </div>
    <form id="modal-form" data-mode="link">
      <!-- Link / Text section -->
      <div id="mat-link-sect">
        <div class="form-group"><label>${t('title_label')} *</label>
          <input name="title" class="form-control" placeholder="e.g. Chapter 3 Notes"></div>
        <div class="form-group"><label>${t('content')}</label>
          <textarea name="content" class="form-control" rows="4" placeholder="Optional description or notes…"></textarea></div>
        <div class="form-group"><label>${t('url_label')}</label>
          <input name="url" type="url" class="form-control" placeholder="https://…"></div>
      </div>
      <!-- File upload section -->
      <div id="mat-file-sect" class="hidden">
        <div class="form-group"><label>${t('title_label')} *</label>
          <input name="file_title" class="form-control" placeholder="e.g. Lecture Slides Week 3"></div>
        <div class="form-group"><label>File *</label>
          <input name="file" type="file" class="form-control" accept="*/*"
            onchange="const t=document.querySelector('[name=file_title]');if(!t.value)t.value=this.files[0]?.name||''">
          <small class="text-muted">${t('file_upload_hint')}</small>
        </div>
      </div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('add')}</button>
      </div>
    </form>`,
    async (fd) => {
      const form = document.getElementById('modal-form');
      const mode = form.dataset.mode;
      if (mode !== 'file') {
        // Link / Text
        const title = (fd.get('title') || '').trim();
        if (!title) { toast(t('title_label') + ' is required', 'error'); return; }
        try {
          await api('POST', `/courses/${courseId}/materials`,
            { title, content: fd.get('content') || null, url: fd.get('url') || null });
          closeModal(); toast(t('add') + '!'); navigate('course', { id: courseId });
        } catch(err) { toast(err.message, 'error'); }
      } else {
        // File upload — must use multipart/form-data, not JSON
        const fileTitle = (fd.get('file_title') || '').trim();
        const file = fd.get('file');
        if (!fileTitle) { toast(t('title_label') + ' is required', 'error'); return; }
        if (!file || !file.size) { toast('Please select a file', 'error'); return; }
        const uploadFd = new FormData();
        uploadFd.append('title', fileTitle);
        uploadFd.append('file', file);
        try {
          const resp = await fetch(`/api/courses/${courseId}/materials/upload`, {
            method: 'POST',
            headers: { Authorization: 'Bearer ' + state.token },
            body: uploadFd,
          });
          if (!resp.ok) { const e = await resp.json(); throw new Error(e.detail || 'Upload failed'); }
          closeModal(); toast('File uploaded!'); navigate('course', { id: courseId });
        } catch(err) { toast(err.message, 'error'); }
      }
    });
}

async function deleteMaterial(courseId, matId) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE',`/courses/${courseId}/materials/${matId}`); toast(t('delete')); navigate('course',{id:courseId}); }
  catch(err) { toast(err.message,'error'); }
}

// ═══════════════════════════════════════════════════════════
// Assignments
// ═══════════════════════════════════════════════════════════
function openNewAssignmentModal(courseId) {
  openModal(t('new_assignment'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required></div>
      <div class="form-group"><label>${t('instructions')}</label>
        <textarea name="description" class="form-control" rows="4"></textarea></div>
      <div class="form-row">
        <div class="form-group"><label>${t('due_date')}</label>
          <input name="due_date" type="datetime-local" class="form-control"></div>
        <div class="form-group"><label>${t('max_score')}</label>
          <input name="max_score" type="number" class="form-control" value="100" min="1"></div>
      </div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST',`/assignments/course/${courseId}`,
          { title:fd.get('title'), description:fd.get('description')||null,
            due_date:fd.get('due_date')||null, max_score:parseFloat(fd.get('max_score'))||100 });
        closeModal(); toast(t('create')+'!'); navigate('course',{id:courseId});
      } catch(err) { toast(err.message,'error'); }
    });
}

async function renderAssignmentDetail(assignmentId, el) {
  loading(el);
  try {
    const a = await api('GET',`/assignments/${assignmentId}`);
    const canGrade = state.user.role==='admin' || state.user.role==='teacher';
    el.innerHTML = `
      <div class="page-header">
        <div>
          <button class="btn btn-sm" onclick="navigate('course',{id:${a.course_id}})" style="margin-bottom:8px">${t('back')}</button>
          <h2>${a.title}</h2>
        </div>
        <div style="text-align:right">
          ${a.due_date ? `<small class="text-muted">${t('due_date')}: ${fmtDateTime(a.due_date)}</small><br>` : ''}
          <small class="text-muted">${t('max_score')}: ${a.max_score} ${t('pts')}</small>
        </div>
      </div>
      ${a.description ? `<div class="card"><div class="card-header"><h3>${t('instructions')}</h3></div>
        <div class="card-body"><p style="white-space:pre-wrap">${a.description}</p></div></div>` : ''}
      ${!canGrade ? `
        <div class="card"><div class="card-header">
          <h3>${a.my_submission ? t('your_submission') : t('submit_assignment')}</h3></div>
          <div class="card-body">
            ${a.my_submission ? `
              <div style="margin-bottom:12px">
                <div class="submission-content"><p>${htmlEsc(a.my_submission.content)}</p></div>
                <small class="text-muted">${fmtDateTime(a.my_submission.submitted_at)}</small>
                ${a.my_submission.score!=null
                  ? `<div class="grade-result mt-8"><strong>${t('score')}: ${a.my_submission.score} / ${a.max_score}</strong>
                      ${a.my_submission.feedback?`<p>${a.my_submission.feedback}</p>`:''}</div>`
                  : `<p class="text-muted mt-8">${t('not_graded')}</p>`}
              </div>
              <button class="btn btn-sm" onclick="document.getElementById('sub-area').classList.toggle('hidden')">${t('edit_resubmit')}</button>
              <div id="sub-area" class="hidden" style="margin-top:14px">` : `<div id="sub-area">`}
            <div class="form-group" style="margin-top:${a.my_submission?'12px':'0'}"><label></label>
              <textarea id="sub-content" class="form-control" rows="8">${htmlEsc(a.my_submission ? a.my_submission.content : '')}</textarea></div>
            <button class="btn btn-primary" onclick="submitAssignment(${assignmentId})">
              ${a.my_submission?t('resubmit'):t('submit_assignment')}</button>
            </div>
          </div>
        </div>` : `
        <div class="card"><div class="card-header"><h3>${t('submissions')} (${a.submissions.length})</h3></div>
          <div class="card-body">
            ${a.submissions.length ? a.submissions.map(s=>`
              <div class="submission-item">
                <div class="submission-header">
                  <strong>${s.student_name}</strong>
                  <small class="text-muted">${fmtDateTime(s.submitted_at)}</small>
                  ${s.score!=null ? `<span class="badge badge-success">${s.score}/${a.max_score}</span>`
                                  : `<span class="badge badge-warning">${t('not_graded')}</span>`}
                </div>
                <div class="submission-content"><p>${htmlEsc(s.content)}</p></div>
                <div class="grade-form">
                  <div class="form-row">
                    <div class="form-group"><label>${t('score')} (max ${a.max_score})</label>
                      <input type="number" id="score-${s.id}" class="form-control" value="${s.score??''}" min="0" max="${a.max_score}" step="0.5"></div>
                    <div class="form-group" style="flex:2"><label>${t('feedback')}</label>
                      <input type="text" id="fb-${s.id}" class="form-control" value="${s.feedback??''}"></div>
                  </div>
                  <button class="btn btn-sm btn-primary" onclick="gradeSubmission(${s.id},${assignmentId})">${t('save_grade')}</button>
                </div>
              </div>`).join('') : `<p class="text-muted">${t('no_submissions')}</p>`}
          </div>
        </div>`}`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

async function submitAssignment(id) {
  const content = document.getElementById('sub-content').value.trim();
  if (!content) { toast(t('submit_assignment'),'error'); return; }
  try {
    await api('POST',`/assignments/${id}/submit`,{content});
    toast(t('submit_assignment')+'!');
    navigate('assignment',{id});
    // Show outstanding-assignments window after a brief pause so the page re-renders first
    setTimeout(() => showPostSubmitModal(id), 400);
  }
  catch(err) { toast(err.message,'error'); }
}

// ── Post-submission: show remaining assignments across all enrolled courses ──
async function showPostSubmitModal(submittedId) {
  try {
    const courses = await api('GET', '/courses/');
    if (!courses) return;
    const enrolled = courses.filter(c => c.enrolled);
    const pending = [];

    // Fetch assignments for every enrolled course in parallel
    const perCourse = await Promise.all(
      enrolled.map(c =>
        api('GET', `/assignments/course/${c.id}`)
          .then(asgns => ({ course: c, asgns: asgns || [] }))
          .catch(() => ({ course: c, asgns: [] }))
      )
    );

    perCourse.forEach(({ course, asgns }) => {
      asgns.forEach(a => {
        // Exclude the one just submitted, and any already submitted
        if (a.id !== submittedId && !a.my_submission) {
          pending.push({ ...a, course_title: course.title, course_id: course.id });
        }
      });
    });

    // Sort: overdue first, then by due date ascending, then undated
    pending.sort((a, b) => {
      const da = a.due_date ? new Date(a.due_date) : null;
      const db = b.due_date ? new Date(b.due_date) : null;
      if (!da && !db) return 0;
      if (!da) return 1;
      if (!db) return -1;
      return da - db;
    });

    if (pending.length === 0) {
      openModal(t('well_done'), `
        <div class="post-submit-empty">
          <div class="post-submit-trophy">🏆</div>
          <p class="post-submit-congrats">${t('no_outstanding')}</p>
        </div>
        <div class="form-actions" style="justify-content:center">
          <button class="btn btn-primary" onclick="closeModal()">OK</button>
        </div>`);
    } else {
      const now = new Date();
      openModal(t('outstanding_assignments'), `
        <p class="post-submit-subtitle">${t('outstanding_msg')}</p>
        <div class="outstanding-list">
          ${pending.map(a => {
            const due = a.due_date ? new Date(a.due_date) : null;
            const isOverdue = due && due < now;
            const dueTxt = due
              ? `${t('due_date')}: <strong class="${isOverdue?'text-danger':''}">${fmtDate(a.due_date)}</strong>${isOverdue?' ⚠️':''}`
              : '';
            return `
              <div class="outstanding-item">
                <div class="outstanding-info">
                  <span class="outstanding-title">${a.title}</span>
                  <span class="outstanding-course">📚 ${a.course_title}</span>
                  ${dueTxt ? `<span class="outstanding-due">${dueTxt}</span>` : ''}
                </div>
                <button class="btn btn-sm btn-primary"
                  onclick="closeModal();navigate('assignment',{id:${a.id}})">
                  ${t('go_to_assignment')}
                </button>
              </div>`;
          }).join('')}
        </div>
        <div class="form-actions">
          <button class="btn" onclick="closeModal()">${t('cancel')}</button>
        </div>`);
    }
  } catch(e) { /* silent — don't block the user if the lookup fails */ }
}

async function gradeSubmission(subId, aId) {
  const score = parseFloat(document.getElementById(`score-${subId}`).value);
  const fb    = document.getElementById(`fb-${subId}`).value;
  if (isNaN(score)) { toast(t('score'),'error'); return; }
  try { await api('PUT',`/assignments/submissions/${subId}/grade`,{score,feedback:fb||null}); toast(t('save_grade')+'!'); navigate('assignment',{id:aId}); }
  catch(err) { toast(err.message,'error'); }
}

// ═══════════════════════════════════════════════════════════
// Sessions
// ═══════════════════════════════════════════════════════════
function openNewSessionModal(courseId) {
  openModal(t('new_session'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required placeholder="e.g. Week 3 Lecture"></div>
      <div class="form-group"><label>${t('session_type')} *</label>
        <select name="session_type" class="form-control" onchange="updateSessionForm(this.value)">
          <option value="virtual">💻 ${t('virtual')}</option>
          <option value="physical">🏫 ${t('physical')}</option>
        </select>
      </div>
      <div class="form-group"><label>📅 Date &amp; Time *</label>
        <input name="date" type="datetime-local" class="form-control" required></div>
      <div class="form-group"><label>${t('duration')}</label>
        <input name="duration_minutes" type="number" class="form-control" value="60" min="10"></div>
      <div class="form-group" id="location-group">
        <label id="location-label">${t('meeting_link')}</label>
        <input name="location" id="location-input" class="form-control" placeholder="https://meet.google.com/…"></div>
      <div class="form-group"><label>${t('notes')}</label>
        <textarea name="notes" class="form-control" rows="2"></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST',`/sessions/course/${courseId}`,{
          title: fd.get('title'), session_type: fd.get('session_type'),
          date: fd.get('date'), duration_minutes: parseInt(fd.get('duration_minutes'))||60,
          location: fd.get('location')||null, notes: fd.get('notes')||null,
        });
        closeModal(); toast(t('new_session')+'!'); navigate('course',{id:courseId});
      } catch(err) { toast(err.message,'error'); }
    });
}

function updateSessionForm(type) {
  const label = document.getElementById('location-label');
  const input = document.getElementById('location-input');
  if (type === 'virtual') {
    label.textContent = t('meeting_link');
    input.placeholder = 'https://meet.google.com/…';
    input.type = 'url';
  } else {
    label.textContent = t('location');
    input.placeholder = 'Room 204 / Building A';
    input.type = 'text';
  }
}

async function deleteSession(sessionId, courseId) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE',`/sessions/${sessionId}`); toast(t('delete')); navigate('course',{id:courseId}); }
  catch(err) { toast(err.message,'error'); }
}

// ═══════════════════════════════════════════════════════════
// Quizzes  —  Create / Delete
// ═══════════════════════════════════════════════════════════
function openNewQuizModal(courseId) {
  openModal(t('new_quiz'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required placeholder="e.g. Chapter 2 Quiz"></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="3"></textarea></div>
      <div class="form-row">
        <div class="form-group"><label>${t('time_limit')} <small class="text-muted">(0 = none)</small></label>
          <input name="time_limit" type="number" class="form-control" value="0" min="0"></div>
        <div class="form-group"><label>${t('due_date')}</label>
          <input name="due_date" type="datetime-local" class="form-control"></div>
      </div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        const tl = parseInt(fd.get('time_limit')) || 0;
        const res = await api('POST',`/quizzes/course/${courseId}`,{
          title: fd.get('title'), description: fd.get('description')||null,
          time_limit: tl > 0 ? tl : null, due_date: fd.get('due_date')||null,
        });
        closeModal(); toast(t('create')+'!');
        navigate('quiz-builder',{id: res.id});
      } catch(err) { toast(err.message,'error'); }
    });
}

async function deleteQuiz(quizId, courseId) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE',`/quizzes/${quizId}`); toast(t('delete')); navigate('course',{id:courseId}); }
  catch(err) { toast(err.message,'error'); }
}

// ═══════════════════════════════════════════════════════════
// Quiz Builder (teacher)
// ═══════════════════════════════════════════════════════════
async function renderQuizBuilder(quizId, el) {
  loading(el);
  try {
    const quiz = await api('GET',`/quizzes/${quizId}`);
    const pubBadge = quiz.is_published
      ? `<span class="badge badge-success">✓ ${t('quiz_published')}</span>`
      : `<span class="badge badge-warning">✏️ ${t('quiz_draft')}</span>`;
    el.innerHTML = `
      <div class="page-header">
        <div>
          <button class="btn btn-sm" onclick="navigate('course',{id:${quiz.course_id}})" style="margin-bottom:8px">${t('back')}</button>
          <h2>${t('quiz_builder')}: ${quiz.title}</h2>
          <div style="display:flex;gap:8px;margin-top:6px;align-items:center">
            ${pubBadge}
            <small class="text-muted">${quiz.question_count} ${t('question_text')}(s) &bull; ${quiz.total_points} ${t('pts')}${quiz.time_limit ? ` &bull; ${quiz.time_limit} ${t('minutes')}` : ''}</small>
          </div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <button class="btn btn-sm" onclick="openEditQuizModal(${quizId})">${t('edit_quiz')}</button>
          <button class="btn btn-sm ${quiz.is_published ? 'btn-warning' : 'btn-success'}"
            onclick="togglePublishQuiz(${quizId},${quiz.is_published},${quiz.course_id})">
            ${quiz.is_published ? t('unpublish_quiz') : t('publish_quiz')}
          </button>
          <button class="btn btn-primary" onclick="openAddQuestionModal(${quizId})">${t('add_question')}</button>
        </div>
      </div>
      ${!quiz.is_published ? `
        <div class="alert alert-warning" style="margin-bottom:16px">
          📋 ${t('quiz_draft')} — ${t('publish_quiz').toLowerCase()} when you\'re ready for students to see it.
        </div>` : ''}
      <div id="question-list">
        ${quiz.questions.length ? quiz.questions.map((q,i)=>questionBuilderCard(q,i,quizId)).join('')
                                : `<div class="card"><div class="card-body"><p class="text-muted">No questions yet — click "${t('add_question')}" to get started.</p></div></div>`}
      </div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

// ── Edit quiz metadata (title / description / time limit / due date) ──
async function openEditQuizModal(quizId) {
  const quiz = await api('GET', `/quizzes/${quizId}`);
  if (!quiz) return;
  const dueFmt = quiz.due_date ? quiz.due_date.replace(' ','T').slice(0,16) : '';
  openModal(t('edit_quiz'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required value="${htmlEsc(quiz.title)}"></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="3">${htmlEsc(quiz.description||'')}</textarea></div>
      <div class="form-row">
        <div class="form-group"><label>${t('time_limit')} <small class="text-muted">(0 = ${t('no')} limit)</small></label>
          <input name="time_limit" type="number" class="form-control" value="${quiz.time_limit||0}" min="0"></div>
        <div class="form-group"><label>${t('due_date')}</label>
          <input name="due_date" type="datetime-local" class="form-control" value="${dueFmt}"></div>
      </div>
      <div class="form-group"><label>${t('max_attempts')} <small class="text-muted">(0 = ${t('unlimited')})</small></label>
        <input name="max_attempts" type="number" class="form-control" value="${quiz.max_attempts||0}" min="0"></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('save')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        const tl = parseInt(fd.get('time_limit')) || 0;
        const ma = parseInt(fd.get('max_attempts')) || 0;
        await api('PUT', `/quizzes/${quizId}`, {
          title: fd.get('title'),
          description: fd.get('description') || null,
          time_limit: tl > 0 ? tl : null,
          due_date: fd.get('due_date') || null,
          max_attempts: ma,   // 0 = clear limit (backend treats as unlimited)
        });
        closeModal();
        toast(t('quiz_edit_saved'));
        navigate('quiz-builder', {id: quizId});
      } catch(err) { toast(err.message, 'error'); }
    });
}

// ── Publish / unpublish toggle ──
async function togglePublishQuiz(quizId, isPublished, courseId) {
  try {
    await api('PATCH', `/quizzes/${quizId}/publish`, { is_published: !isPublished });
    toast(!isPublished ? '✅ ' + t('publish_quiz') : t('unpublish_quiz'));
    if (state.currentPage === 'quiz-builder') {
      navigate('quiz-builder', {id: quizId});
    } else {
      navigate('course', {id: courseId});
    }
  } catch(err) { toast(err.message, 'error'); }
}

function questionBuilderCard(q, idx, quizId) {
  const typeLabel = { multiple_choice: t('multiple_choice'), true_false: t('true_false'), short_answer: t('short_answer') };
  return `
    <div class="question-card">
      <div class="question-card-header">
        <div>
          <span class="text-muted" style="font-size:11px;text-transform:uppercase">${t('q_num')} ${idx+1} &bull; ${typeLabel[q.question_type]||q.question_type} &bull; ${q.points} ${t('pts')}</span>
          <strong style="display:block;margin-top:2px">${q.question_text}</strong>
        </div>
        <button class="btn btn-sm btn-danger" onclick="deleteQuestion(${q.id},${quizId})">${t('delete')}</button>
      </div>
      ${q.options.length ? `<div class="question-options">
        ${q.options.map(o=>`
          <div class="option-row${o.is_correct?' correct':''}">
            <span>${o.is_correct ? '✓' : '○'}</span> ${o.option_text}
          </div>`).join('')}
      </div>` : `<p class="text-muted" style="font-size:12px;margin-top:4px">${t('short_manual')}</p>`}
    </div>`;
}

function openAddQuestionModal(quizId) {
  openModal(t('add_question'), `
    <div>
      <div class="form-group"><label>${t('question_type')} *</label>
        <select id="q-type" class="form-control" onchange="updateQTypeUI()">
          <option value="multiple_choice">${t('multiple_choice')}</option>
          <option value="true_false">${t('true_false')}</option>
          <option value="short_answer">${t('short_answer')}</option>
        </select>
      </div>
      <div class="form-group"><label>${t('question_text')} *</label>
        <textarea id="q-text" class="form-control" rows="3" required></textarea></div>
      <div class="form-group"><label>${t('points')}</label>
        <input id="q-pts" type="number" class="form-control" value="1" min="0.5" step="0.5"></div>
      <div id="q-options-area"></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="button" class="btn btn-primary" onclick="submitAddQuestion(${quizId})">${t('add')}</button>
      </div>
    </div>`);
  updateQTypeUI();
}

function updateQTypeUI() {
  const type = document.getElementById('q-type')?.value;
  const area = document.getElementById('q-options-area');
  if (!area) return;
  if (type === 'short_answer') {
    area.innerHTML = `<p class="text-muted" style="font-size:13px;padding:8px 0">${t('short_manual')}</p>`;
  } else if (type === 'true_false') {
    area.innerHTML = `
      <div class="form-group"><label>${t('correct_answer')}</label>
        <div class="tf-options">
          <label><input type="radio" name="tf-correct" value="0" checked> ${t('yes')} (True)</label>
          <label><input type="radio" name="tf-correct" value="1"> ${t('no')} (False)</label>
        </div>
      </div>`;
  } else {
    area.innerHTML = `
      <div class="form-group"><label>${t('options')} <small class="text-muted">(mark correct with ○)</small></label>
        ${[0,1,2,3].map(i=>`
          <div class="mc-option">
            <input type="radio" name="mc-correct" value="${i}">
            <input type="text" id="mc-opt-${i}" class="form-control" placeholder="${t('options')} ${i+1}">
          </div>`).join('')}
      </div>`;
  }
}

async function submitAddQuestion(quizId) {
  const type = document.getElementById('q-type').value;
  const text = document.getElementById('q-text').value.trim();
  const pts  = parseFloat(document.getElementById('q-pts').value) || 1;
  if (!text) { toast(t('question_text'),'error'); return; }

  let options = [];
  if (type === 'true_false') {
    const correct = document.querySelector('input[name="tf-correct"]:checked')?.value || '0';
    options = [
      { option_text: 'True',  is_correct: correct === '0' },
      { option_text: 'False', is_correct: correct === '1' },
    ];
  } else if (type === 'multiple_choice') {
    const correct = document.querySelector('input[name="mc-correct"]:checked')?.value;
    for (let i = 0; i < 4; i++) {
      const val = document.getElementById(`mc-opt-${i}`)?.value.trim();
      if (val) options.push({ option_text: val, is_correct: String(i) === correct });
    }
    if (options.length < 2) { toast('Add at least 2 options','error'); return; }
  }

  try {
    await api('POST',`/quizzes/${quizId}/questions`,{ question_text:text, question_type:type, points:pts, options });
    closeModal(); toast(t('add')+'!'); navigate('quiz-builder',{id:quizId});
  } catch(err) { toast(err.message,'error'); }
}

async function deleteQuestion(questionId, quizId) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE',`/quizzes/questions/${questionId}`); toast(t('delete')); navigate('quiz-builder',{id:quizId}); }
  catch(err) { toast(err.message,'error'); }
}

// ═══════════════════════════════════════════════════════════
// Quiz Taking (student) & Results
// ═══════════════════════════════════════════════════════════
async function startQuiz(quizId) {
  try {
    await api('POST',`/quizzes/${quizId}/start`);
    navigate('quiz-take',{id:quizId});
  } catch(err) { toast(err.message,'error'); }
}

async function renderQuizTake(quizId, el) {
  loading(el);
  try {
    const quiz = await api('GET',`/quizzes/${quizId}`);
    const submitted = quiz.my_attempt && quiz.my_attempt.submitted_at;

    if (submitted) {
      // Show results
      renderQuizResults(quiz, el);
      return;
    }

    // Taking mode
    let timerHtml = '';
    if (quiz.time_limit && quiz.my_attempt) {
      timerHtml = `<div class="quiz-timer" id="quiz-timer">--:--</div>`;
    }

    el.innerHTML = `
      <div class="quiz-header">
        <div>
          <button class="btn btn-sm" onclick="navigate('course',{id:${quiz.course_id}})">${t('back')}</button>
          <strong style="margin-left:12px">${quiz.title}</strong>
        </div>
        <div style="display:flex;align-items:center;gap:12px">
          <small class="text-muted">${quiz.question_count} ${t('question_text')}(s) &bull; ${quiz.total_points} ${t('pts')}</small>
          ${timerHtml}
        </div>
      </div>
      ${quiz.questions.map((q,i) => `
        <div class="quiz-question-block">
          <div class="quiz-q-num">${t('q_num')} ${i+1} ${t('of')} ${quiz.question_count} &bull; ${q.points} ${t('pts')}</div>
          <div class="quiz-q-text">${q.question_text}</div>
          ${q.question_type === 'short_answer' ? `
            <textarea class="form-control" id="sa-${q.id}" rows="4" placeholder="…"></textarea>` : `
            <div class="quiz-options">
              ${q.options.map(o=>`
                <div class="quiz-option">
                  <input type="radio" name="q-${q.id}" id="opt-${o.id}" value="${o.id}">
                  <label for="opt-${o.id}">${o.option_text}</label>
                </div>`).join('')}
            </div>`}
        </div>`).join('')}
      <div style="display:flex;gap:10px;margin-top:8px">
        <button class="btn" onclick="navigate('course',{id:${quiz.course_id}})">${t('cancel')}</button>
        <button class="btn btn-primary" onclick="submitQuiz(${quizId},${quiz.course_id})">${t('submit_quiz')}</button>
      </div>`;

    // Start timer if needed
    if (quiz.time_limit && quiz.my_attempt) {
      const elapsed = (Date.now() - new Date(quiz.my_attempt.started_at)) / 1000;
      const remaining = Math.max(0, quiz.time_limit * 60 - elapsed);
      startQuizTimer(Math.floor(remaining), () => submitQuiz(quizId, quiz.course_id));
    }
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function startQuizTimer(seconds, onExpire) {
  let rem = seconds;
  const tick = () => {
    const el = document.getElementById('quiz-timer');
    if (!el) { clearInterval(state.quizTimer); return; }
    const m = Math.floor(rem / 60), s = rem % 60;
    el.textContent = `${m}:${String(s).padStart(2,'0')}`;
    el.style.color = rem < 60 ? 'var(--danger)' : 'var(--text)';
    if (rem <= 0) { clearInterval(state.quizTimer); onExpire(); }
    rem--;
  };
  tick();
  state.quizTimer = setInterval(tick, 1000);
}

async function submitQuiz(quizId, courseId) {
  if (state.quizTimer) { clearInterval(state.quizTimer); state.quizTimer = null; }
  // Collect answers from the live DOM
  const quiz = await api('GET',`/quizzes/${quizId}`).catch(() => null);
  if (!quiz) return;
  const answers = quiz.questions.map(q => {
    if (q.question_type === 'short_answer') {
      return { question_id: q.id, text_answer: document.getElementById(`sa-${q.id}`)?.value || '' };
    }
    const sel = document.querySelector(`input[name="q-${q.id}"]:checked`);
    return { question_id: q.id, selected_option_id: sel ? parseInt(sel.value) : null };
  });
  try {
    const result = await api('POST',`/quizzes/${quizId}/submit`,{ answers });
    toast(t('quiz_submitted'));
    navigate('quiz-take',{id:quizId}); // re-render page as results view
    setTimeout(() => showPostQuizModal(quizId, result), 450);
  } catch(err) { toast(err.message,'error'); }
}

// ── Post-quiz popup: score + outstanding quizzes across all courses ──
async function showPostQuizModal(quizId, result) {
  try {
    // Fetch all enrolled-course quiz lists in parallel
    const courses = await api('GET', '/courses/');
    if (!courses) return;
    const enrolled = courses.filter(c => c.enrolled);

    const perCourse = await Promise.all(
      enrolled.map(c =>
        api('GET', `/quizzes/course/${c.id}`)
          .then(quizzes => ({ course: c, quizzes: quizzes || [] }))
          .catch(() => ({ course: c, quizzes: [] }))
      )
    );

    const pending = [];
    const now = new Date();
    perCourse.forEach(({ course, quizzes }) => {
      quizzes.forEach(q => {
        // Outstanding = published, not this quiz, and not yet fully submitted
        if (q.id !== quizId && q.is_published && !(q.my_attempt && q.my_attempt.submitted_at)) {
          pending.push({ ...q, course_title: course.title, course_id: course.id });
        }
      });
    });

    // Sort: overdue first → nearest due date → undated
    pending.sort((a, b) => {
      const da = a.due_date ? new Date(a.due_date) : null;
      const db = b.due_date ? new Date(b.due_date) : null;
      if (!da && !db) return 0;
      if (!da) return 1;
      if (!db) return -1;
      return da - db;
    });

    // ── Score section ──
    const score    = result.score;
    const total    = result.total_possible;
    const hasShort = result.has_short_answer;
    const pct      = (!hasShort && total > 0 && score != null) ? Math.round(score / total * 100) : null;
    const ringColor = pct === null ? 'var(--muted)'
                    : pct >= 80   ? 'var(--success)'
                    : pct >= 50   ? 'var(--warning)'
                    : 'var(--danger)';

    const scoreHtml = hasShort
      ? `<div class="pq-score-pending">
           <span class="pq-pending-icon">📝</span>
           <p>${t('pending_grading')}</p>
         </div>`
      : `<div class="pq-score-ring" style="--ring-clr:${ringColor};--ring-pct:${pct}">
           <svg class="pq-ring-svg" viewBox="0 0 80 80">
             <circle cx="40" cy="40" r="34" fill="none" stroke="#e5e7eb" stroke-width="8"/>
             <circle cx="40" cy="40" r="34" fill="none" stroke="${ringColor}" stroke-width="8"
               stroke-dasharray="${Math.round(2*Math.PI*34*pct/100)} 214"
               stroke-linecap="round" transform="rotate(-90 40 40)"/>
           </svg>
           <div class="pq-ring-inner">
             <span class="pq-score-num">${score}</span>
             <span class="pq-score-slash">/ ${total}</span>
           </div>
         </div>
         <p class="pq-score-pct" style="color:${ringColor}">${pct}%</p>`;

    // ── Outstanding section ──
    const outHtml = pending.length === 0
      ? `<div class="post-submit-empty" style="padding:16px 0 8px">
           <div class="post-submit-trophy">🎉</div>
           <p class="post-submit-congrats">${t('no_outstanding_quizzes')}</p>
         </div>`
      : `<p class="post-submit-subtitle">${t('outstanding_quizzes_msg')}</p>
         <div class="outstanding-list">
           ${pending.map(q => {
             const due = q.due_date ? new Date(q.due_date) : null;
             const overdue = due && due < now;
             const dueTxt = due
               ? `${t('due_date')}: <strong class="${overdue?'text-danger':''}">${fmtDate(q.due_date)}${overdue?' ⚠️':''}</strong>`
               : '';
             const resume = q.my_attempt && !q.my_attempt.submitted_at;
             return `
               <div class="outstanding-item">
                 <div class="outstanding-info">
                   <span class="outstanding-title">📋 ${q.title}</span>
                   <span class="outstanding-course">📚 ${q.course_title}</span>
                   ${dueTxt ? `<span class="outstanding-due">${dueTxt}</span>` : ''}
                 </div>
                 <button class="btn btn-sm btn-primary"
                   onclick="closeModal();${resume ? `navigate('quiz-take',{id:${q.id}})` : `startQuiz(${q.id})`}">
                   ${resume ? t('resume_quiz') : t('start_now')}
                 </button>
               </div>`;
           }).join('')}
         </div>`;

    openModal(t('quiz_score_result'), `
      <div class="pq-modal">
        <div class="pq-result-section">
          ${scoreHtml}
        </div>
        <div class="pq-divider"></div>
        <div class="pq-outstanding-section">
          <h4 class="pq-section-title">📋 ${t('outstanding_quizzes')}</h4>
          ${outHtml}
        </div>
      </div>
      <div class="form-actions">
        <button class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button class="btn btn-primary" onclick="closeModal();navigate('quiz-take',{id:${quizId}})">${t('quiz_results')}</button>
      </div>`);
  } catch(e) { /* silent — never block the user if the lookup fails */ }
}

// ── Load urgent quizzes into student dashboard panel ──
async function loadUrgentQuizzes(enrolled) {
  const body = document.getElementById('urgent-quizzes-body');
  const card = document.getElementById('urgent-quizzes-card');
  if (!body) return;
  try {
    const perCourse = await Promise.all(
      enrolled.map(c =>
        api('GET', `/quizzes/course/${c.id}`)
          .then(qs => ({ course: c, quizzes: qs || [] }))
          .catch(() => ({ course: c, quizzes: [] }))
      )
    );

    const now = new Date();
    const urgent = [];
    perCourse.forEach(({ course, quizzes }) => {
      quizzes.forEach(q => {
        if (q.is_published && !(q.my_attempt && q.my_attempt.submitted_at)) {
          urgent.push({ ...q, course_title: course.title, course_id: course.id });
        }
      });
    });

    // Sort: overdue → nearest due date → undated
    urgent.sort((a, b) => {
      const da = a.due_date ? new Date(a.due_date) : null;
      const db = b.due_date ? new Date(b.due_date) : null;
      if (!da && !db) return 0;
      if (!da) return 1;
      if (!db) return -1;
      return da - db;
    });

    if (urgent.length === 0) {
      if (card) card.classList.add('hidden');
      return;
    }

    body.innerHTML = urgent.map(q => {
      const due     = q.due_date ? new Date(q.due_date) : null;
      const overdue = due && due < now;
      const resume  = q.my_attempt && !q.my_attempt.submitted_at;
      return `
        <div class="urgent-quiz-item">
          <div class="urgent-quiz-info">
            <span class="urgent-quiz-title">📋 ${q.title}</span>
            <span class="urgent-quiz-course">📚 ${q.course_title}</span>
            ${due ? `<span class="urgent-quiz-due${overdue?' text-danger':''}">
              ${t('due_date')}: ${fmtDate(q.due_date)}${overdue?' ⚠️':''}
            </span>` : ''}
          </div>
          <button class="btn btn-sm btn-primary"
            onclick="${resume ? `navigate('quiz-take',{id:${q.id}})` : `startQuiz(${q.id})`}">
            ⚡ ${resume ? t('resume_quiz') : t('start_now')}
          </button>
        </div>`;
    }).join('');
  } catch(e) {
    if (body) body.innerHTML = `<p class="text-muted">—</p>`;
  }
}

function renderQuizResults(quiz, el) {
  const attempt = quiz.my_attempt;
  const answers = attempt?.answers || [];
  const answerMap = {};
  answers.forEach(a => { answerMap[a.question_id] = a; });

  el.innerHTML = `
    <div class="page-header">
      <div>
        <button class="btn btn-sm" onclick="navigate('course',{id:${quiz.course_id}})" style="margin-bottom:8px">${t('back')}</button>
        <h2>${quiz.title} — ${t('quiz_results')}</h2>
      </div>
      ${attempt?.score != null
        ? `<div class="stat-card" style="min-width:120px;text-align:center">
            <div class="stat-number">${attempt.score}</div>
            <div class="stat-label">${t('your_score')} / ${quiz.total_points}</div>
           </div>`
        : `<span class="badge badge-warning">${t('short_manual')}</span>`}
    </div>
    ${quiz.questions.map((q,i) => {
      const myAns = answerMap[q.id];
      const myOptId = myAns?.selected_option_id;
      const myText = myAns?.text_answer;
      return `
        <div class="quiz-question-block">
          <div class="quiz-q-num">${t('q_num')} ${i+1} &bull; ${q.points} ${t('pts')}</div>
          <div class="quiz-q-text">${q.question_text}</div>
          ${q.question_type === 'short_answer' ? `
            <div class="alert alert-success" style="margin-top:8px">
              <strong>${t('your_answer')}:</strong> ${myText || '—'}
            </div>
            <p class="text-muted" style="font-size:12px">${t('short_manual')}</p>` : `
            <div class="quiz-options" style="pointer-events:none">
              ${q.options.map(o => {
                let cls = '';
                if (o.is_correct && myOptId === o.id) cls = 'result-correct';
                else if (o.is_correct)               cls = 'result-correct';
                else if (myOptId === o.id)            cls = 'result-wrong';
                return `<div class="quiz-option ${cls}">
                  <input type="radio" ${myOptId===o.id?'checked':''} disabled>
                  <label>${o.option_text}
                    ${o.is_correct ? ' ✓' : ''}
                    ${myOptId===o.id && !o.is_correct ? ' ✗' : ''}
                  </label>
                </div>`;
              }).join('')}
            </div>`}
        </div>`;
    }).join('')}`;
}

// ═══════════════════════════════════════════════════════════
// Announcements
// ═══════════════════════════════════════════════════════════
async function renderAnnouncements(el) {
  loading(el);
  try {
    const anns = await api('GET','/announcements/');
    const role = state.user.role;
    el.innerHTML = `
      <div class="page-header"><h2>${t('school_announcements')}</h2>
        ${role!=='student' ? `<button class="btn btn-primary" onclick="openAnnouncementModal(null)">${t('post_announcement')}</button>` : ''}
      </div>
      <div class="card"><div class="card-body">
        ${anns.length ? anns.map(a=>`
          <div class="announcement-item">
            <div class="announcement-header"><strong>${htmlEsc(a.title)}</strong>
              ${role!=='student' ? `<button class="btn btn-sm btn-danger" onclick="deleteAnnouncement(${a.id},null)">${t('delete')}</button>` : ''}</div>
            <p>${htmlEsc(a.content)}</p>
            <small>${t('by')} ${htmlEsc(a.author_name)} &bull; ${fmtDate(a.created_at)}</small>
          </div>`).join('') : `<p class="text-muted">${t('no_announcements')}</p>`}
      </div></div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function openAnnouncementModal(courseId) {
  openModal(t('post_announcement'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required></div>
      <div class="form-group"><label>${t('content')} *</label>
        <textarea name="content" class="form-control" rows="5" required></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('post_announcement')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST','/announcements/',{title:fd.get('title'),content:fd.get('content'),course_id:courseId||null});
        closeModal(); toast(t('post_announcement')+'!');
        courseId ? navigate('course',{id:courseId}) : navigate('announcements');
      } catch(err) { toast(err.message,'error'); }
    });
}

async function deleteAnnouncement(id, courseId) {
  if (!confirm(t('delete')+'?')) return;
  try {
    await api('DELETE',`/announcements/${id}`); toast(t('delete'));
    courseId ? navigate('course',{id:courseId}) : navigate('announcements');
  } catch(err) { toast(err.message,'error'); }
}

// ═══════════════════════════════════════════════════════════
// Users (Admin)
// ═══════════════════════════════════════════════════════════
async function renderUsers(el) {
  loading(el);
  try {
    const users = await api('GET','/users/');
    window._users = users;
    el.innerHTML = `
      <div class="page-header"><h2>${t('user_management')}</h2>
        <button class="btn btn-primary" onclick="openNewUserModal()">${t('add_user')}</button>
      </div>
      <div class="tabs">
        <button class="tab active" onclick="filterUsers('all',this)">${t('all')} (${users.length})</button>
        <button class="tab" onclick="filterUsers('admin',this)">${t('admins')} (${users.filter(u=>u.role==='admin').length})</button>
        <button class="tab" onclick="filterUsers('teacher',this)">${t('teachers')} (${users.filter(u=>u.role==='teacher').length})</button>
        <button class="tab" onclick="filterUsers('student',this)">${t('students')} (${users.filter(u=>u.role==='student').length})</button>
      </div>
      <div class="card"><div class="card-body">
        <table class="table">
          <thead><tr><th>${t('full_name')}</th><th>${t('email')}</th><th>${t('role')}</th><th></th></tr></thead>
          <tbody id="users-tbody">${usersRows(users,'all')}</tbody>
        </table>
      </div></div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function usersRows(users, filter) {
  const list = filter==='all' ? users : users.filter(u=>u.role===filter);
  return list.map(u=>`
    <tr>
      <td>${u.name}</td><td>${u.email}</td>
      <td><span class="badge badge-${u.role}">${u.role}</span></td>
      <td>${u.id!==state.user.id
        ? `<button class="btn btn-sm btn-danger" onclick="deleteUser(${u.id})">${t('delete')}</button>`
        : `<span class="text-muted">${t('you')}</span>`}</td>
    </tr>`).join('');
}

function filterUsers(filter, btn) {
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('users-tbody').innerHTML = usersRows(window._users,filter);
}

function openNewUserModal() {
  openModal(t('add_user'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('full_name')} *</label>
        <input name="name" class="form-control" required placeholder="Jane Doe"></div>
      <div class="form-group"><label>${t('email')} *</label>
        <input name="email" type="email" class="form-control" required></div>
      <div class="form-group"><label>${t('password')} *</label>
        <input name="password" type="password" class="form-control" required minlength="6"></div>
      <div class="form-group"><label>${t('role')} *</label>
        <select name="role" class="form-control">
          <option value="student">${t('students')}</option>
          <option value="teacher">${t('teachers')}</option>
          <option value="admin">${t('admins')}</option>
        </select>
      </div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST','/users/',{name:fd.get('name'),email:fd.get('email'),
          password:fd.get('password'),role:fd.get('role')});
        closeModal(); toast(t('add_user')+'!'); navigate('users');
      } catch(err) { toast(err.message,'error'); }
    });
}

async function deleteUser(id) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE',`/users/${id}`); toast(t('delete')); navigate('users'); }
  catch(err) { toast(err.message,'error'); }
}

// ═══════════════════════════════════════════════════════════
// Gradebook Page
// ═══════════════════════════════════════════════════════════
async function renderGradebook(el) {
  loading(el);
  const role = state.user.role;
  try {
    if (role === 'student') {
      const data = await api('GET', '/gradebook/my');
      if (!data) return;
      el.innerHTML = `
        <div class="page-header"><h2>${t('my_grades')}</h2>
          <div class="stat-card" style="min-width:120px;text-align:center">
            <div class="stat-number">${data.cumulative_gpa}</div>
            <div class="stat-label">${t('cumulative_gpa')}</div>
          </div>
        </div>
        ${data.courses.map(c => `
          <div class="card">
            <div class="card-header">
              <h3>${c.course_title}</h3>
              <div style="display:flex;gap:10px;align-items:center">
                <span class="grade-cell grade-${c.letter}">${c.letter} (${c.weighted_pct}%)</span>
                <small class="text-muted">GPA: ${c.gpa}</small>
              </div>
            </div>
            <div class="card-body">
              <table class="table">
                <thead><tr><th>${t('title_label')}</th><th>${t('score')}</th><th>${t('max_score')}</th><th>%</th></tr></thead>
                <tbody>
                  ${Object.values(c.scores).map(s => `
                    <tr>
                      <td>${s.title}</td>
                      <td>${s.score !== null ? s.score : '<span class="text-muted">—</span>'}</td>
                      <td>${s.max_score}</td>
                      <td>${s.score !== null && s.max_score ? Math.round(s.score/s.max_score*100)+'%' : '—'}</td>
                    </tr>`).join('')}
                </tbody>
              </table>
            </div>
          </div>`).join('')}`;

    } else {
      // Teacher/Admin: pick course
      const courses = await api('GET', '/courses/');
      const mine = role === 'admin' ? courses : courses.filter(c => c.teacher_id === state.user.id);
      if (!state.currentParams.course_id && mine.length > 0) {
        state.currentParams.course_id = mine[0].id;
      }
      const cid = state.currentParams.course_id;
      let gb = null;
      if (cid) {
        gb = await api('GET', `/gradebook/course/${cid}`);
      }

      el.innerHTML = `
        <div class="page-header"><h2>${t('gradebook')}</h2>
          <select class="form-control" style="max-width:280px" onchange="navigate('gradebook',{course_id:parseInt(this.value)})">
            ${mine.map(c => `<option value="${c.id}" ${c.id==cid?'selected':''}>${c.title}</option>`).join('')}
          </select>
        </div>
        ${gb ? renderGradebookTable(gb) : '<div class="card"><div class="card-body"><p class="text-muted">Select a course to view gradebook.</p></div></div>'}`;
    }
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function renderGradebookTable(gb) {
  if (!gb.students.length) return '<div class="card"><div class="card-body"><p class="text-muted">No students enrolled.</p></div></div>';
  const assignments = gb.assignments;
  return `
    <div class="card">
      <div class="card-header"><h3>${gb.course_title}</h3></div>
      <div class="card-body" style="padding:0">
        <div class="gradebook-table-wrapper">
          <table class="gradebook-table">
            <thead>
              <tr>
                <th>Student</th>
                ${assignments.map(a => `<th title="${a.title}">${a.title.substring(0,12)}${a.title.length>12?'…':''}${a.is_extra_credit?' ⭐':''}</th>`).join('')}
                <th>Avg%</th><th>Grade</th>
              </tr>
            </thead>
            <tbody>
              ${gb.students.map(s => `
                <tr>
                  <td>${s.student_name}</td>
                  ${assignments.map(a => {
                    const sc = s.scores[a.id];
                    if (!sc || sc.score === null) return `<td><span class="text-muted">—</span></td>`;
                    const pct = a.max_score ? Math.round(sc.score/a.max_score*100) : 0;
                    return `<td>${sc.score}</td>`;
                  }).join('')}
                  <td><strong>${s.weighted_pct}%</strong></td>
                  <td><span class="grade-cell grade-${s.letter}">${s.letter}</span></td>
                </tr>`).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </div>`;
}

// ═══════════════════════════════════════════════════════════
// Calendar Page
// ═══════════════════════════════════════════════════════════
async function renderCalendar(el) {
  loading(el);
  try {
    const courses = await api('GET', '/courses/');
    const enrolled = state.user.role === 'student'
      ? courses.filter(c => c.enrolled)
      : (state.user.role === 'teacher' ? courses.filter(c => c.teacher_id === state.user.id) : courses);

    const events = [];
    const now = new Date();

    for (const c of enrolled) {
      const [asgns, sessions, quizzes] = await Promise.all([
        api('GET', `/assignments/course/${c.id}`),
        api('GET', `/sessions/course/${c.id}`),
        api('GET', `/quizzes/course/${c.id}`),
      ]);
      (asgns||[]).forEach(a => {
        if (a.due_date) events.push({ date: new Date(a.due_date), title: a.title, course: c.title, type: 'assignment' });
      });
      (sessions||[]).forEach(s => {
        if (s.date) events.push({ date: new Date(s.date), title: s.title, course: c.title, type: 'session' });
      });
      (quizzes||[]).forEach(q => {
        if (q.due_date) events.push({ date: new Date(q.due_date), title: q.title, course: c.title, type: 'quiz' });
      });
    }

    events.sort((a, b) => a.date - b.date);
    const upcoming = events.filter(e => e.date >= now);

    el.innerHTML = `
      <div class="page-header"><h2>${t('calendar')}</h2></div>
      <div class="calendar-list">
        ${upcoming.length ? upcoming.map(ev => {
          const msLeft = ev.date - now;
          const dayLeft = msLeft / 86400000;
          const cls = dayLeft < 0 ? 'overdue' : dayLeft < 3 ? 'soon' : '';
          const mon = ev.date.toLocaleString('en-GB', { month: 'short' });
          const day = ev.date.getDate();
          const typeIcon = { assignment: '📋', session: '📅', quiz: '📝' }[ev.type] || '📌';
          return `
            <div class="calendar-event ${cls}">
              <div class="calendar-event-date"><span class="cal-day">${day}</span>${mon}</div>
              <div class="calendar-event-info">
                <div class="calendar-event-title">${typeIcon} ${ev.title}</div>
                <div class="calendar-event-course">${ev.course}</div>
              </div>
              <span class="calendar-event-type">${ev.type}</span>
            </div>`;
        }).join('') : `<div class="card"><div class="card-body"><p class="text-muted">${t('no_events')}</p></div></div>`}
      </div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

// ═══════════════════════════════════════════════════════════
// Messages Page
// ═══════════════════════════════════════════════════════════
async function renderMessages(el) {
  loading(el);
  const tab = state.currentParams.tab || 'inbox';
  try {
    const data = await api('GET', tab === 'sent' ? '/messages/sent' : '/messages/');
    el.innerHTML = `
      <div class="page-header"><h2>${t('messages')}</h2>
        <button class="btn btn-primary" onclick="openComposeModal()">${t('compose')}</button>
      </div>
      <div class="tabs">
        <button class="tab${tab==='inbox'?' active':''}" onclick="navigate('messages',{tab:'inbox'})">${t('inbox')}</button>
        <button class="tab${tab==='sent'?' active':''}" onclick="navigate('messages',{tab:'sent'})">${t('sent')}</button>
      </div>
      <div class="card"><div class="card-body">
        ${(data||[]).length ? (data||[]).map(m => {
          const other = tab === 'sent' ? m.recipient_name : m.sender_name;
          const isUnread = !m.is_read && tab === 'inbox';
          return `
            <div class="message-item${isUnread?' unread':''}" onclick="openMessageModal(${m.id},'${tab}')">
              <div class="message-avatar">${(other||'?')[0].toUpperCase()}</div>
              <div class="message-info">
                <div class="message-from">${other||'?'}</div>
                <div class="message-subject">${m.subject}</div>
              </div>
              <div>
                <div class="message-time">${fmtDate(m.sent_at)}</div>
                ${isUnread ? '<div class="message-dot" style="margin-left:auto"></div>' : ''}
              </div>
            </div>`;
        }).join('') : `<p class="text-muted">${t('no_messages')}</p>`}
      </div></div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

async function openMessageModal(id, tab) {
  try {
    const m = await api('GET', `/messages/${id}`);
    if (!m) return;
    openModal(m.subject, `
      <div>
        <p><strong>From:</strong> ${htmlEsc(m.sender_name)}</p>
        <p><strong>To:</strong> ${htmlEsc(m.recipient_name)}</p>
        <p><strong>Sent:</strong> ${fmtDateTime(m.sent_at)}</p>
        <hr style="margin:12px 0;border-color:var(--border)">
        <div style="white-space:pre-wrap;font-size:14px;line-height:1.6">${htmlEsc(m.body)}</div>
        <div class="form-actions" style="margin-top:16px">
          <button class="btn" onclick="closeModal();navigate('messages',{tab:'${tab}'})">Close</button>
          <button class="btn btn-primary" onclick="openReplyModal(${m.sender_id},${JSON.stringify(m.subject)})">↩ Reply</button>
          <button class="btn btn-danger" onclick="deleteMsg(${id},'${tab}')">Delete</button>
        </div>
      </div>`);
  } catch(err) { toast(err.message, 'error'); }
}

async function openReplyModal(recipientId, originalSubject) {
  const subject = originalSubject.startsWith('Re: ') ? originalSubject : `Re: ${originalSubject}`;
  closeModal();
  openModal(t('compose_message'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('subject')}</label>
        <input name="subject" class="form-control" value="${htmlEsc(subject)}"></div>
      <div class="form-group"><label>${t('message_body')}</label>
        <textarea name="body" class="form-control" rows="5" required></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('send')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', '/messages/', { recipient_id: recipientId, subject: fd.get('subject'), body: fd.get('body') });
        closeModal(); toast(t('send') + '!'); navigate('messages', { tab: 'sent' });
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function deleteMsg(id, tab) {
  if (!confirm('Delete this message?')) return;
  try {
    await api('DELETE', `/messages/${id}`);
    closeModal(); toast('Deleted'); navigate('messages', { tab });
  } catch(err) { toast(err.message, 'error'); }
}

async function openComposeModal() {
  let recipientField = `<div class="form-group"><label>${t('recipient')} ID *</label>
    <input name="recipient_id" type="number" class="form-control" required placeholder="Enter user ID"></div>`;

  try {
    let persons = [];
    if (state.user.role === 'admin') {
      const users = await api('GET', '/users/') || [];
      persons = users.filter(u => u.id !== state.user.id);
    } else {
      // Teachers see their enrolled students; students see teachers of their courses
      const courses = await api('GET', '/courses/') || [];
      const relevant = state.user.role === 'teacher'
        ? courses.filter(c => c.teacher_id === state.user.id)
        : courses.filter(c => c.enrolled);
      const map = {};
      await Promise.all(relevant.map(async c => {
        const detail = await api('GET', `/courses/${c.id}`).catch(() => null);
        if (!detail) return;
        if (state.user.role === 'teacher') {
          (detail.students || []).forEach(s => { map[s.id] = { id: s.id, name: s.name, email: s.email, role: 'student' }; });
        } else if (detail.teacher_id) {
          map[detail.teacher_id] = { id: detail.teacher_id, name: detail.teacher_name || '?', email: '', role: 'teacher' };
        }
      }));
      persons = Object.values(map).filter(p => p.id !== state.user.id);
    }

    if (persons.length) {
      recipientField = `
        <div class="form-group"><label>${t('recipient')} *</label>
          <select name="recipient_id" class="form-control" required>
            <option value="">— Select recipient —</option>
            ${persons.map(p => `<option value="${p.id}">${htmlEsc(p.name)}${p.email ? ` (${htmlEsc(p.email)})` : ''} — ${p.role}</option>`).join('')}
          </select>
        </div>`;
    }
  } catch(_) { /* fall back to ID input */ }

  openModal(t('compose_message'), `
    <form id="modal-form">
      ${recipientField}
      <div class="form-group"><label>${t('subject')} *</label>
        <input name="subject" class="form-control" required></div>
      <div class="form-group"><label>${t('message_body')}</label>
        <textarea name="body" class="form-control" rows="5" required></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('send')}</button>
      </div>
    </form>`,
    async (fd) => {
      const recipId = fd.get('recipient_id');
      if (!recipId) { toast('Please select a recipient', 'error'); return; }
      try {
        await api('POST', '/messages/', { recipient_id: parseInt(recipId), subject: fd.get('subject'), body: fd.get('body') });
        closeModal(); toast(t('send') + '!'); navigate('messages', { tab: 'sent' });
      } catch(err) { toast(err.message, 'error'); }
    });
}

// ═══════════════════════════════════════════════════════════
// Analytics Page
// ═══════════════════════════════════════════════════════════
async function renderAnalytics(el) {
  loading(el);
  const role = state.user.role;
  try {
    if (role === 'admin') {
      const data = await api('GET', '/analytics/overview');
      if (!data) return;
      el.innerHTML = `
        <div class="page-header"><h2>${t('analytics')}</h2></div>
        <div class="stats-grid">
          <div class="stat-card"><div class="stat-number">${data.total_users}</div><div class="stat-label">${t('total_users')}</div></div>
          <div class="stat-card"><div class="stat-number">${data.total_students}</div><div class="stat-label">${t('students')}</div></div>
          <div class="stat-card"><div class="stat-number">${data.total_teachers}</div><div class="stat-label">${t('teachers')}</div></div>
          <div class="stat-card"><div class="stat-number">${data.total_courses}</div><div class="stat-label">${t('courses')}</div></div>
          <div class="stat-card"><div class="stat-number">${data.submissions_this_week}</div><div class="stat-label">${t('submissions_this_week')}</div></div>
          <div class="stat-card"><div class="stat-number">${data.avg_grade_pct}%</div><div class="stat-label">${t('avg_score')}</div></div>
        </div>`;
    } else {
      // Teacher: pick course
      const courses = await api('GET', '/courses/');
      const mine = courses.filter(c => c.teacher_id === state.user.id);
      const cid = state.currentParams.course_id || (mine[0] && mine[0].id);
      let data = null;
      if (cid) data = await api('GET', `/analytics/course/${cid}`);

      el.innerHTML = `
        <div class="page-header"><h2>${t('analytics')}</h2>
          <select class="form-control" style="max-width:260px" onchange="navigate('analytics',{course_id:parseInt(this.value)})">
            ${mine.map(c => `<option value="${c.id}" ${c.id==cid?'selected':''}>${c.title}</option>`).join('')}
          </select>
        </div>
        ${data ? `
          <div class="stats-grid">
            <div class="stat-card"><div class="stat-number">${data.enrollment_count}</div><div class="stat-label">${t('students')}</div></div>
            <div class="stat-card"><div class="stat-number">${data.active_students}</div><div class="stat-label">${t('active_students')}</div></div>
          </div>
          <div class="card">
            <div class="card-header"><h3>${t('grade_distribution')}</h3></div>
            <div class="card-body">
              ${Object.entries(data.grade_distribution).map(([letter, count]) => {
                const total = data.enrollment_count || 1;
                const pct = Math.round(count / total * 100);
                return `
                  <div class="chart-bar-container">
                    <div class="chart-bar-label"><span>${letter}</span><span>${count} students</span></div>
                    <div class="chart-bar-track">
                      <div class="chart-bar-fill chart-bar-${letter}" style="width:${pct}%">${pct}%</div>
                    </div>
                  </div>`;
              }).join('')}
            </div>
          </div>
          <div class="card">
            <div class="card-header"><h3>${t('assignments')}</h3></div>
            <div class="card-body">
              <table class="table">
                <thead><tr><th>Assignment</th><th>Submitted</th><th>Rate</th><th>Avg Score</th></tr></thead>
                <tbody>
                  ${data.assignment_stats.map(a => `
                    <tr>
                      <td>${a.title}</td>
                      <td>${a.submission_count}/${a.enrollment_count}</td>
                      <td>${a.submission_rate}%</td>
                      <td>${a.avg_pct}%</td>
                    </tr>`).join('')}
                </tbody>
              </table>
            </div>
          </div>` : '<div class="card"><div class="card-body"><p class="text-muted">Select a course.</p></div></div>'}`;
    }
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

// ═══════════════════════════════════════════════════════════
// Badges Page
// ═══════════════════════════════════════════════════════════
async function renderBadges(el) {
  loading(el);
  const role = state.user.role;
  try {
    const [badges, myBadges] = await Promise.all([
      api('GET', '/badges/'),
      role === 'student' ? api('GET', '/badges/my') : Promise.resolve([]),
    ]);

    if (role === 'student') {
      const earned    = myBadges || [];
      const earnedIds = new Set(earned.map(b => b.badge_id));
      el.innerHTML = `
        <div class="page-header"><h2>🏅 ${t('my_badges')}</h2></div>

        ${earned.length ? `
          <p class="badges-section-title">Earned — ${earned.length} badge${earned.length !== 1 ? 's' : ''}</p>
          <div class="badges-grid">
            ${earned.map(b => `
              <div class="badge-card earned">
                <span class="badge-icon">${b.badge_icon}</span>
                <div class="badge-name">${htmlEsc(b.badge_name)}</div>
                ${b.badge_description ? `<div class="badge-desc">${htmlEsc(b.badge_description)}</div>` : ''}
                <div class="badge-earned-stamp">🏆 ${htmlEsc(b.awarded_by_name)}</div>
                ${b.note ? `<div class="badge-desc" style="font-style:italic">"${htmlEsc(b.note)}"</div>` : ''}
                <div class="badge-meta">${fmtDate(b.awarded_at)}</div>
              </div>`).join('')}
          </div>` : ''}

        <p class="badges-section-title" style="margin-top:${earned.length ? '32px' : '8px'}">
          All Badges — ${(badges||[]).length} available
        </p>
        <div class="badges-grid">
          ${(badges||[]).map(b => `
            <div class="badge-card ${earnedIds.has(b.id) ? 'earned' : ''}">
              <span class="badge-icon">${b.icon}</span>
              <div class="badge-name">${htmlEsc(b.name)}</div>
              ${b.description ? `<div class="badge-desc">${htmlEsc(b.description)}</div>` : ''}
              <div class="badge-meta">${earnedIds.has(b.id) ? '✓ Earned' : `${b.awarded_count} awarded`}</div>
            </div>`).join('')}
          ${!(badges||[]).length
            ? `<p class="text-muted" style="grid-column:1/-1;text-align:center;padding:24px">No badges created yet.</p>`
            : ''}
        </div>`;

    } else {
      el.innerHTML = `
        <div class="page-header">
          <h2>🏅 ${t('badges')}</h2>
          <button class="btn btn-primary" onclick="openCreateBadgeModal()">${t('create_badge')}</button>
        </div>
        ${!(badges||[]).length
          ? `<div class="card"><div class="card-body"><p class="text-muted">${t('no_badges')}</p></div></div>`
          : ''}
        <div class="badges-grid">
          ${(badges||[]).map(b => `
            <div class="badge-card">
              <span class="badge-icon">${b.icon}</span>
              <div class="badge-name">${htmlEsc(b.name)}</div>
              ${b.description ? `<div class="badge-desc">${htmlEsc(b.description)}</div>` : ''}
              <div class="badge-meta">${b.awarded_count} student${b.awarded_count !== 1 ? 's' : ''} earned this</div>
              <div style="margin-top:10px;display:flex;gap:6px;justify-content:center;flex-wrap:wrap">
                <button class="btn btn-sm btn-primary"
                  onclick="openAwardBadgeModal(${b.id},${JSON.stringify(b.name)})">🎖 ${t('award_badge')}</button>
                <button class="btn btn-sm btn-danger" onclick="deleteBadge(${b.id})">${t('delete')}</button>
              </div>
            </div>`).join('')}
        </div>`;
    }
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function openCreateBadgeModal() {
  openModal(t('create_badge'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="name" class="form-control" required placeholder="Excellence Award"></div>
      <div class="form-group"><label>${t('badge_icon')} (emoji)</label>
        <input name="icon" class="form-control" value="🏅" maxlength="4"></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="2"></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', '/badges/', { name: fd.get('name'), icon: fd.get('icon')||'🏅', description: fd.get('description')||null });
        closeModal(); toast(t('create')+'!'); navigate('badges');
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function openAwardBadgeModal(badgeId, badgeName) {
  // Load the students this user can award to
  let students = [];
  try {
    if (state.user.role === 'admin') {
      students = await api('GET', '/users/?role=student') || [];
    } else {
      // Teacher: collect unique students from their courses
      const courses = await api('GET', '/courses/') || [];
      const myCourses = courses.filter(c => c.teacher_id === state.user.id);
      const map = {};
      await Promise.all(myCourses.map(async c => {
        const detail = await api('GET', `/courses/${c.id}`).catch(() => null);
        (detail?.students || []).forEach(s => { map[s.id] = s; });
      }));
      students = Object.values(map);
    }
  } catch(_) { /* fall back to manual entry */ }

  const hasStudents = students.length > 0;
  const studentField = hasStudents
    ? `<div class="form-group"><label>Student *</label>
        <select name="user_id" class="form-control" required>
          <option value="">— Select a student —</option>
          ${students.map(s => `<option value="${s.id}">${htmlEsc(s.name)} (${htmlEsc(s.email)})</option>`).join('')}
        </select></div>`
    : `<div class="form-group"><label>Student User ID *</label>
        <input name="user_id" type="number" class="form-control" required placeholder="Enter user ID"></div>`;

  openModal(`🎖 Award: ${badgeName}`, `
    <form id="modal-form">
      ${studentField}
      <div class="form-group"><label>Note (optional)</label>
        <input name="note" class="form-control" placeholder="Reason for this award…"></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">🎖 Award Badge</button>
      </div>
    </form>`,
    async (fd) => {
      const userId = fd.get('user_id');
      if (!userId) { toast('Please select a student', 'error'); return; }
      try {
        await api('POST', `/badges/${badgeId}/award/${userId}`, { note: fd.get('note')||null });
        closeModal(); toast('Badge awarded! 🏅'); navigate('badges');
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function deleteBadge(id) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE', `/badges/${id}`); toast(t('delete')); navigate('badges'); }
  catch(err) { toast(err.message, 'error'); }
}

// ═══════════════════════════════════════════════════════════
// Portfolio Page
// ═══════════════════════════════════════════════════════════
async function renderPortfolio(el) {
  loading(el);
  try {
    const p = await api('GET', '/portfolio/my');
    if (!p) return;
    el.innerHTML = `
      <div class="page-header"><h2>${t('my_portfolio')}</h2>
        <button class="btn btn-primary" onclick="openAddPortfolioItemModal()">${t('add_item')}</button>
      </div>
      <div class="card">
        <div class="card-header"><h3>${p.title}</h3>
          <button class="btn btn-sm" onclick="openEditPortfolioModal()">${t('edit')}</button>
        </div>
        <div class="card-body">
          ${p.bio ? `<p style="margin-bottom:12px">${p.bio}</p>` : ''}
          <small class="text-muted">${p.is_public ? '🌐 Public' : '🔒 Private'}</small>
        </div>
      </div>
      <div class="portfolio-items-grid">
        ${(p.items||[]).map(item => `
          <div class="portfolio-item-card">
            <h4>${item.title}</h4>
            ${item.description ? `<p>${item.description}</p>` : ''}
            ${item.content ? `<p style="margin-top:6px;font-size:12px;color:var(--text)">${item.content.substring(0,100)}${item.content.length>100?'…':''}</p>` : ''}
            ${item.url ? `<a href="${item.url}" target="_blank" class="link" style="display:block;margin-top:6px">${item.url.substring(0,40)}</a>` : ''}
            ${item.tags ? `<div class="portfolio-tags">${item.tags.split(',').map(tag=>`<span class="portfolio-tag">${tag.trim()}</span>`).join('')}</div>` : ''}
            <div style="margin-top:10px;display:flex;gap:6px">
              <button class="btn btn-sm btn-danger" onclick="deletePortfolioItem(${item.id})">${t('delete')}</button>
            </div>
          </div>`).join('') || `<div class="card" style="grid-column:1/-1"><div class="card-body"><p class="text-muted">${t('no_items')}</p></div></div>`}
      </div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function openEditPortfolioModal() {
  openModal(t('my_portfolio'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('portfolio_title')}</label>
        <input name="title" class="form-control"></div>
      <div class="form-group"><label>${t('bio')}</label>
        <textarea name="bio" class="form-control" rows="3"></textarea></div>
      <div class="form-group"><label>
        <input name="is_public" type="checkbox"> ${t('make_public')}
      </label></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('save')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('PUT', '/portfolio/my', { title: fd.get('title')||undefined, bio: fd.get('bio')||null, is_public: !!fd.get('is_public') });
        closeModal(); toast(t('save')+'!'); navigate('portfolio');
      } catch(err) { toast(err.message, 'error'); }
    });
}

function openAddPortfolioItemModal() {
  openModal(t('add_item'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="2"></textarea></div>
      <div class="form-group"><label>${t('content')}</label>
        <textarea name="content" class="form-control" rows="3"></textarea></div>
      <div class="form-group"><label>URL</label>
        <input name="url" type="url" class="form-control"></div>
      <div class="form-group"><label>Tags (comma-separated)</label>
        <input name="tags" class="form-control" placeholder="design, coding, art"></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('add')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', '/portfolio/my/items', { title: fd.get('title'), description: fd.get('description')||null, content: fd.get('content')||null, url: fd.get('url')||null, tags: fd.get('tags')||null });
        closeModal(); toast(t('add')+'!'); navigate('portfolio');
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function deletePortfolioItem(id) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE', `/portfolio/items/${id}`); toast(t('delete')); navigate('portfolio'); }
  catch(err) { toast(err.message, 'error'); }
}

// ═══════════════════════════════════════════════════════════
// Question Banks Page
// ═══════════════════════════════════════════════════════════
async function renderQuestionBanks(el) {
  loading(el);
  try {
    const banks = await api('GET', '/question-banks/');
    el.innerHTML = `
      <div class="page-header"><h2>${t('question_banks')}</h2>
        <button class="btn btn-primary" onclick="openNewBankModal()">${t('new_bank')}</button>
      </div>
      ${(banks||[]).length ? (banks||[]).map(b => `
        <div class="card">
          <div class="card-header">
            <h3>${b.title}</h3>
            <div style="display:flex;gap:6px">
              <button class="btn btn-sm btn-primary" onclick="viewBank(${b.id})">${t('edit')}</button>
              <button class="btn btn-sm btn-danger" onclick="deleteBank(${b.id})">${t('delete')}</button>
            </div>
          </div>
          <div class="card-body">
            ${b.description ? `<p class="text-muted">${b.description}</p>` : ''}
            <small>${b.question_count} questions</small>
          </div>
        </div>`).join('')
      : `<div class="card"><div class="card-body"><p class="text-muted">${t('no_banks')}</p></div></div>`}`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function openNewBankModal() {
  openModal(t('new_bank'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="2"></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', '/question-banks/', { title: fd.get('title'), description: fd.get('description')||null });
        closeModal(); toast(t('create')+'!'); navigate('question_banks');
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function viewBank(id) {
  const bank = await api('GET', `/question-banks/${id}`);
  if (!bank) return;
  openModal(bank.title, `
    <div>
      <p class="text-muted" style="margin-bottom:12px">${bank.question_count||bank.questions.length} questions</p>
      ${bank.questions.map(q => `
        <div class="bank-question-item">
          <div class="q-text">${q.question_text}</div>
          <div class="q-meta">
            <span>${q.question_type}</span>
            <span>${q.points} pts</span>
            ${q.tags ? `<span>🏷 ${q.tags}</span>` : ''}
          </div>
        </div>`).join('')}
      <div class="form-actions">
        <button class="btn" onclick="closeModal()">Close</button>
        <button class="btn btn-primary" onclick="openAddBankQuestionModal(${id})">+ Add Question</button>
      </div>
    </div>`);
}

function openAddBankQuestionModal(bankId) {
  closeModal();
  openModal(t('add_questions'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('question_type')}</label>
        <select name="question_type" class="form-control">
          <option value="multiple_choice">${t('multiple_choice')}</option>
          <option value="true_false">${t('true_false')}</option>
          <option value="short_answer">${t('short_answer')}</option>
        </select></div>
      <div class="form-group"><label>${t('question_text')} *</label>
        <textarea name="question_text" class="form-control" rows="3" required></textarea></div>
      <div class="form-group"><label>${t('points')}</label>
        <input name="points" type="number" class="form-control" value="1" step="0.5" min="0.5"></div>
      <div class="form-group"><label>Tags</label>
        <input name="tags" class="form-control" placeholder="math, algebra"></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('add')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', `/question-banks/${bankId}/questions`, [{
          question_text: fd.get('question_text'),
          question_type: fd.get('question_type'),
          points: parseFloat(fd.get('points'))||1,
          tags: fd.get('tags')||null,
        }]);
        closeModal(); toast(t('add')+'!'); navigate('question_banks');
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function deleteBank(id) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE', `/question-banks/${id}`); toast(t('delete')); navigate('question_banks'); }
  catch(err) { toast(err.message, 'error'); }
}

// ═══════════════════════════════════════════════════════════
// Course Detail — Modules Tab
// ═══════════════════════════════════════════════════════════
async function renderModulesTab(courseId, container, canManage) {
  container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  try {
    const modules = await api('GET', `/modules/course/${courseId}`);
    container.innerHTML = `
      ${canManage ? `<div style="margin-bottom:12px"><button class="btn btn-sm btn-primary" onclick="openNewModuleModal(${courseId})">${t('new_module')}</button></div>` : ''}
      ${(modules||[]).map(m => `
        <div class="module-card">
          <div class="module-card-header" onclick="this.nextElementSibling.nextElementSibling.classList.toggle('hidden')">
            <h4>${m.title} ${!m.is_published?'<span class="badge badge-warning">Draft</span>':''}</h4>
            <small>${m.progress}% complete</small>
          </div>
          <div class="module-progress-bar"><div class="module-progress-fill" style="width:${m.progress}%"></div></div>
          <div class="module-item-list">
            ${m.items.map(item => `
              <div class="module-item-row">
                ${state.user.role === 'student' ? `
                  <div class="module-item-check${item.completed?' done':''}" onclick="completeModuleItem(${item.id},${courseId})">
                    ${item.completed ? '✓' : ''}
                  </div>` : '<div style="width:20px"></div>'}
                <div class="module-item-title">${item.title}</div>
                <span class="module-item-type">${item.item_type}</span>
                ${!item.is_required ? '<span class="badge badge-info" style="font-size:10px">Optional</span>' : ''}
                ${canManage ? `<button class="btn btn-sm btn-danger" onclick="deleteModuleItem(${item.id},${courseId})" style="margin-left:auto">${t('delete')}</button>` : ''}
              </div>`).join('') || '<p class="text-muted" style="padding:8px 0">No items yet.</p>'}
            ${canManage ? `<div style="margin-top:8px"><button class="btn btn-sm" onclick="openAddModuleItemModal(${m.id},${courseId})">${t('add_module_item')}</button></div>` : ''}
          </div>
        </div>`).join('') || '<p class="text-muted">No modules yet.</p>'}`;
  } catch(err) { container.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

async function completeModuleItem(itemId, courseId) {
  try { await api('POST', `/modules/items/${itemId}/complete`); renderModulesTab(courseId, document.getElementById('tab-modules'), false); }
  catch(err) { toast(err.message, 'error'); }
}

async function deleteModuleItem(itemId, courseId) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE', `/modules/items/${itemId}`); renderModulesTab(courseId, document.getElementById('tab-modules'), true); }
  catch(err) { toast(err.message, 'error'); }
}

function openNewModuleModal(courseId) {
  openModal(t('new_module'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="2"></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', `/modules/course/${courseId}`, { title: fd.get('title'), description: fd.get('description')||null });
        closeModal(); toast(t('create')+'!'); renderModulesTab(courseId, document.getElementById('tab-modules'), true);
      } catch(err) { toast(err.message, 'error'); }
    });
}

function openAddModuleItemModal(moduleId, courseId) {
  openModal(t('add_module_item'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required></div>
      <div class="form-group"><label>Type</label>
        <select name="item_type" class="form-control">
          <option value="assignment">Assignment</option>
          <option value="quiz">Quiz</option>
          <option value="material">Material</option>
          <option value="session">Session</option>
          <option value="page">Page</option>
        </select></div>
      <div class="form-group"><label>Item ID (optional)</label>
        <input name="item_id" type="number" class="form-control"></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('add')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        const itemId = parseInt(fd.get('item_id'))||null;
        await api('POST', `/modules/${moduleId}/items`, { title: fd.get('title'), item_type: fd.get('item_type'), item_id: itemId, is_required: true });
        closeModal(); toast(t('add')+'!'); renderModulesTab(courseId, document.getElementById('tab-modules'), true);
      } catch(err) { toast(err.message, 'error'); }
    });
}

// ═══════════════════════════════════════════════════════════
// Course Detail — Discussions Tab
// ═══════════════════════════════════════════════════════════
async function renderDiscussionsTab(courseId, container, canManage) {
  container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  try {
    const boards = await api('GET', `/discussions/course/${courseId}`);
    container.innerHTML = `
      ${canManage ? `<div style="margin-bottom:12px"><button class="btn btn-sm btn-primary" onclick="openNewBoardModal(${courseId})">${t('new_board')}</button></div>` : ''}
      ${(boards||[]).map(b => `
        <div class="card" style="margin-bottom:12px">
          <div class="card-header">
            <h3>${b.is_pinned?'📌 ':''}${b.title}</h3>
            <div style="display:flex;gap:6px;align-items:center">
              <small class="text-muted">${b.post_count} posts</small>
              <button class="btn btn-sm btn-primary" onclick="navigate('discussion-board',{id:${b.id}})">View Posts</button>
              ${canManage?`<button class="btn btn-sm btn-danger" onclick="deleteBoard(${b.id},${courseId})">${t('delete')}</button>`:''}
            </div>
          </div>
          ${b.description?`<div class="card-body"><p class="text-muted">${b.description}</p></div>`:''}
        </div>`).join('') || `<p class="text-muted">${t('no_boards')}</p>`}`;
  } catch(err) { container.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function openNewBoardModal(courseId) {
  openModal(t('new_board'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="2"></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', `/discussions/course/${courseId}`, { title: fd.get('title'), description: fd.get('description')||null });
        closeModal(); toast(t('create')+'!'); renderDiscussionsTab(courseId, document.getElementById('tab-discussions'), true);
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function deleteBoard(boardId, courseId) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE', `/discussions/boards/${boardId}`); toast(t('delete')); renderDiscussionsTab(courseId, document.getElementById('tab-discussions'), true); }
  catch(err) { toast(err.message, 'error'); }
}

async function renderDiscussionBoard(boardId, el) {
  loading(el);
  try {
    const posts = await api('GET', `/discussions/boards/${boardId}/posts`);
    const canEndorse = state.user.role !== 'student';
    el.innerHTML = `
      <div class="page-header">
        <button class="btn btn-sm" onclick="history.back()">${t('back')}</button>
        <h2>Discussion Board</h2>
      </div>
      <div class="card" style="margin-bottom:16px">
        <div class="card-body">
          <div class="form-group"><textarea id="new-post-content" class="form-control" rows="3" placeholder="Share your thoughts..."></textarea></div>
          <button class="btn btn-primary" onclick="submitPost(${boardId})">${t('post')}</button>
        </div>
      </div>
      <div id="posts-container">
        ${renderPosts(posts||[], canEndorse)}
      </div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function renderPosts(posts, canEndorse) {
  if (!posts.length) return '<p class="text-muted">No posts yet. Be the first!</p>';
  return posts.map(p => `
    <div class="discussion-post${p.is_endorsed?' endorsed':''}">
      <div class="discussion-post-header">
        <div class="discussion-post-author">${htmlEsc(p.author_name)}</div>
        <div class="discussion-post-time">${fmtDateTime(p.created_at)}</div>
        ${p.is_endorsed?'<span class="endorsed-badge">Endorsed</span>':''}
        ${canEndorse?`<button class="btn btn-sm" onclick="endorsePost(${p.id},${p.board_id})">${t('endorse')}</button>`:''}
        <button class="btn btn-sm" onclick="toggleReplyForm(${p.id})">${t('reply')}</button>
      </div>
      <div class="discussion-post-content" style="white-space:pre-wrap">${htmlEsc(p.content)}</div>
      <div id="reply-form-${p.id}" class="hidden" style="margin-top:10px">
        <textarea id="reply-content-${p.id}" class="form-control" rows="2" placeholder="Your reply..."></textarea>
        <button class="btn btn-sm btn-primary" style="margin-top:6px" onclick="submitReply(${p.id},${p.board_id})">${t('reply')}</button>
      </div>
      ${p.replies&&p.replies.length?`<div class="discussion-replies">${renderPosts(p.replies, canEndorse)}</div>`:''}
    </div>`).join('');
}

function toggleReplyForm(postId) {
  document.getElementById(`reply-form-${postId}`)?.classList.toggle('hidden');
}

async function submitPost(boardId) {
  const content = document.getElementById('new-post-content')?.value.trim();
  if (!content) { toast('Write something first', 'error'); return; }
  try {
    await api('POST', `/discussions/boards/${boardId}/posts`, { content });
    toast(t('post')+'!'); navigate('discussion-board', { id: boardId });
  } catch(err) { toast(err.message, 'error'); }
}

async function submitReply(postId, boardId) {
  const content = document.getElementById(`reply-content-${postId}`)?.value.trim();
  if (!content) { toast('Write something first', 'error'); return; }
  try {
    await api('POST', `/discussions/posts/${postId}/reply`, { content });
    toast(t('reply')+'!'); navigate('discussion-board', { id: boardId });
  } catch(err) { toast(err.message, 'error'); }
}

async function endorsePost(postId, boardId) {
  try {
    await api('PUT', `/discussions/posts/${postId}/endorse`);
    navigate('discussion-board', { id: boardId });
  } catch(err) { toast(err.message, 'error'); }
}

// ═══════════════════════════════════════════════════════════
// Course Detail — Surveys Tab
// ═══════════════════════════════════════════════════════════
async function renderSurveysTab(courseId, container, canManage) {
  container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  try {
    const surveys = await api('GET', `/surveys/course/${courseId}`);
    container.innerHTML = `
      ${canManage ? `<div style="margin-bottom:12px"><button class="btn btn-sm btn-primary" onclick="openNewSurveyModal(${courseId})">${t('new_survey')}</button></div>` : ''}
      ${(surveys||[]).map(s => `
        <div class="card" style="margin-bottom:12px">
          <div class="card-header">
            <h3>${s.title}</h3>
            <div style="display:flex;gap:6px;align-items:center">
              <small class="text-muted">${s.question_count} questions &bull; ${s.response_count} responses</small>
              ${!canManage && !s.already_responded ? `<button class="btn btn-sm btn-primary" onclick="takeSurvey(${s.id})">${t('take_survey')}</button>` : ''}
              ${s.already_responded ? '<span class="badge badge-success">Submitted</span>' : ''}
              ${canManage ? `<button class="btn btn-sm" onclick="viewSurveyResults(${s.id})">${t('view_results')}</button>` : ''}
              ${canManage ? `<button class="btn btn-sm btn-danger" onclick="deleteSurvey(${s.id},${courseId})">${t('delete')}</button>` : ''}
            </div>
          </div>
          ${s.description?`<div class="card-body"><p class="text-muted">${s.description}</p></div>`:''}
        </div>`).join('') || '<p class="text-muted">No surveys yet.</p>'}`;
  } catch(err) { container.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

async function takeSurvey(surveyId) {
  const survey = await api('GET', `/surveys/${surveyId}`);
  if (!survey) return;
  const answers = {};
  openModal(survey.title, `
    <div>
      ${survey.questions.map((q, i) => `
        <div class="survey-question-block">
          <h4>${i+1}. ${q.question_text}</h4>
          ${q.question_type === 'text' ? `
            <textarea id="sq-${q.id}" class="form-control" rows="3"></textarea>` :
          q.question_type === 'rating' ? `
            <div class="survey-rating">
              ${[1,2,3,4,5].map(n=>`<button type="button" class="survey-rating-btn" onclick="selectRating(${q.id},${n},this)">${n}</button>`).join('')}
            </div>` :
          `<div>${(q.options||[]).map(opt=>`
            <div class="survey-option-row">
              <input type="radio" name="sq-${q.id}" id="sqo-${q.id}-${opt}" value="${opt}">
              <label for="sqo-${q.id}-${opt}">${opt}</label>
            </div>`).join('')}</div>`}
        </div>`).join('')}
      <div class="form-actions">
        <button class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button class="btn btn-primary" onclick="submitSurvey(${surveyId},'${JSON.stringify(survey.questions.map(q=>q.id)).replace(/'/g,"\\'")}' )">${t('submit_survey')}</button>
      </div>
    </div>`);
}

window._surveyRatings = {};
function selectRating(qId, val, btn) {
  window._surveyRatings[qId] = val;
  btn.closest('.survey-rating').querySelectorAll('.survey-rating-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
}

async function submitSurvey(surveyId, qIdsStr) {
  const qIds = JSON.parse(qIdsStr);
  const answers = [];
  for (const qId of qIds) {
    let answerText = '';
    const textEl = document.getElementById(`sq-${qId}`);
    if (textEl) {
      answerText = textEl.value;
    } else {
      const radioEl = document.querySelector(`input[name="sq-${qId}"]:checked`);
      if (radioEl) answerText = radioEl.value;
      else if (window._surveyRatings[qId]) answerText = String(window._surveyRatings[qId]);
    }
    if (answerText) answers.push({ question_id: qId, answer_text: answerText });
  }
  try {
    await api('POST', `/surveys/${surveyId}/respond`, { answers });
    closeModal(); toast(t('submit_survey')+'!');
  } catch(err) { toast(err.message, 'error'); }
}

async function viewSurveyResults(surveyId) {
  const results = await api('GET', `/surveys/${surveyId}/results`);
  if (!results) return;
  openModal(`Results: ${results.title}`, `
    <div>
      <p class="text-muted" style="margin-bottom:12px">${results.total_responses} responses</p>
      ${results.questions.map(q => `
        <div class="survey-question-block">
          <h4>${q.question_text}</h4>
          <small class="text-muted">${q.response_count} answers</small>
          <div style="margin-top:8px">
            ${q.question_type === 'rating'
              ? `<strong>Average: ${q.summary.avg}</strong>`
              : q.question_type === 'multiple_choice'
              ? Object.entries(q.summary||{}).map(([opt,cnt])=>`<div>${opt}: <strong>${cnt}</strong></div>`).join('')
              : (q.summary.responses||[]).slice(0,5).map(r=>`<div class="bank-question-item" style="padding:6px 10px">${r}</div>`).join('')}
          </div>
        </div>`).join('')}
      <button class="btn" style="margin-top:8px" onclick="closeModal()">Close</button>
    </div>`);
}

async function deleteSurvey(surveyId, courseId) {
  if (!confirm(t('delete')+'?')) return;
  try { await api('DELETE', `/surveys/${surveyId}`); toast(t('delete')); renderSurveysTab(courseId, document.getElementById('tab-surveys'), true); }
  catch(err) { toast(err.message, 'error'); }
}

function openNewSurveyModal(courseId) {
  openModal(t('new_survey'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" required></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="2"></textarea></div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('POST', `/surveys/course/${courseId}`, { title: fd.get('title'), description: fd.get('description')||null, questions: [] });
        closeModal(); toast(t('create')+'!'); renderSurveysTab(courseId, document.getElementById('tab-surveys'), true);
      } catch(err) { toast(err.message, 'error'); }
    });
}

// ═══════════════════════════════════════════════════════════
// Leaderboard
// ═══════════════════════════════════════════════════════════
async function renderLeaderboard(el) {
  loading(el);
  const role = state.user.role;
  try {
    const courses = await api('GET', '/courses/');
    const relevant = role === 'student'
      ? courses.filter(c => c.enrolled)
      : role === 'teacher'
        ? courses.filter(c => c.teacher_id === state.user.id)
        : courses;

    const firstId = state.currentParams.course_id || (relevant[0] && relevant[0].id);
    if (!firstId) {
      el.innerHTML = `<div class="page-header"><h2>🏆 ${t('leaderboard')}</h2></div>
        <div class="card"><div class="card-body"><p class="text-muted">${t('no_leaderboard_data')}</p></div></div>`;
      return;
    }

    const data = await api('GET', `/leaderboard/course/${firstId}`);
    const schoolData = (role === 'admin' || role === 'teacher')
      ? await api('GET', '/leaderboard/school').catch(() => null)
      : null;

    const entries = data.entries || [];
    const top3    = entries.slice(0, 3);
    const rest    = entries.slice(3);
    const medals  = ['🥇','🥈','🥉'];

    el.innerHTML = `
      <div class="page-header">
        <h2>🏆 ${t('leaderboard')}</h2>
        <select class="form-control" style="max-width:260px"
          onchange="navigate('leaderboard',{course_id:parseInt(this.value)})">
          ${relevant.map(c=>`<option value="${c.id}" ${c.id==firstId?'selected':''}>${c.title}</option>`).join('')}
        </select>
      </div>

      <!-- Podium -->
      ${top3.length ? `
      <div class="podium">
        ${[top3[1], top3[0], top3[2]].filter(Boolean).map((e,i) => {
          const podiumRank = e === top3[0] ? 1 : e === top3[1] ? 2 : 3;
          return `
          <div class="podium-slot podium-${podiumRank} ${e.is_me ? 'podium-me' : ''}">
            <div class="podium-medal">${medals[podiumRank-1]}</div>
            <div class="podium-name">${e.name}</div>
            <div class="podium-score">${e.avg_pct}%</div>
            <div class="podium-block p${podiumRank}"></div>
          </div>`;
        }).join('')}
      </div>` : ''}

      <!-- Full table -->
      <div class="card">
        <div class="card-header ch-gold"><h3>📊 ${data.course_title}</h3></div>
        <div class="card-body" style="padding:0">
          <table class="table">
            <thead><tr>
              <th style="width:60px">${t('rank')}</th>
              <th>${t('full_name')}</th>
              <th style="width:100px;text-align:right">${t('avg_score')}</th>
            </tr></thead>
            <tbody>
              ${entries.map(e => `
                <tr class="${e.is_me ? 'lb-my-row' : ''}">
                  <td><strong>${medals[e.rank-1] || '#'+e.rank}</strong></td>
                  <td>${e.name}${e.is_me ? ` <span class="badge badge-info">${t('you')}</span>` : ''}</td>
                  <td style="text-align:right;font-weight:700">${e.avg_pct}%</td>
                </tr>`).join('')}
              ${entries.length === 0 ? `<tr><td colspan="3" class="text-muted" style="text-align:center;padding:20px">${t('no_leaderboard_data')}</td></tr>` : ''}
            </tbody>
          </table>
        </div>
      </div>

      ${schoolData ? `
      <div class="card" style="margin-top:20px">
        <div class="card-header ch-purple"><h3>🏫 ${t('school_leaderboard')}</h3></div>
        <div class="card-body" style="padding:0">
          <table class="table">
            <thead><tr><th>${t('rank')}</th><th>${t('full_name')}</th><th style="text-align:right">${t('avg_score')}</th></tr></thead>
            <tbody>
              ${(schoolData.entries||[]).map(e=>`
                <tr><td>${medals[e.rank-1]||'#'+e.rank}</td><td>${e.name}</td><td style="text-align:right;font-weight:700">${e.avg_pct}%</td></tr>`).join('')}
            </tbody>
          </table>
        </div>
      </div>` : ''}`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

// ═══════════════════════════════════════════════════════════
// Certificates
// ═══════════════════════════════════════════════════════════
async function downloadCertificate(courseId) {
  try {
    const check = await api('GET', `/certificates/course/${courseId}/check`);
    if (!check.eligible) {
      toast(check.reason, 'error'); return;
    }
    // Trigger file download via a hidden link
    const a = document.createElement('a');
    a.href = `/api/certificates/course/${courseId}`;
    a.setAttribute('Authorization', `Bearer ${state.token}`);
    // Use fetch to attach auth header then create blob URL
    const res = await fetch(`/api/certificates/course/${courseId}`, {
      headers: { Authorization: `Bearer ${state.token}` },
    });
    if (!res.ok) { const e = await res.json(); toast(e.detail || 'Error', 'error'); return; }
    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href     = url;
    link.download  = `certificate.pdf`;
    link.click();
    URL.revokeObjectURL(url);
    toast('🎓 Certificate downloaded!');
  } catch(e) { toast(e.message, 'error'); }
}

// ═══════════════════════════════════════════════════════════
// Password Reset
// ═══════════════════════════════════════════════════════════

// All login-card sub-sections. Only one is visible at a time.
const _LOGIN_SECTIONS = [
  'login-form-wrap', 'forgot-wrap', 'forgot-success',
  'reset-form-wrap', 'reset-success', 'reset-invalid',
];

function showLoginSection(id) {
  _LOGIN_SECTIONS.forEach(s => {
    const el = document.getElementById(s);
    if (el) el.classList.toggle('hidden', s !== id);
  });
}

// Kept for backwards compat with the HTML onclick
function showForgotPassword() { showLoginSection('forgot-wrap'); }

async function submitForgotPassword() {
  const email  = document.getElementById('forgot-email').value.trim();
  const errEl  = document.getElementById('forgot-error');
  const btn    = document.getElementById('forgot-btn');
  errEl.classList.add('hidden');
  if (!email) { errEl.textContent = 'Please enter your email address.'; errEl.classList.remove('hidden'); return; }
  btn.disabled = true;
  btn.textContent = '…';
  try {
    await fetch('/api/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    // Always show success — never reveal whether the email exists
    showLoginSection('forgot-success');
  } catch(_) {
    showLoginSection('forgot-success');   // still show success
  } finally {
    btn.disabled = false;
    btn.textContent = 'Send Reset Link';
  }
}

async function submitResetPassword() {
  const token  = document.getElementById('reset-token-val').value;
  const pw     = document.getElementById('reset-pw').value;
  const pw2    = document.getElementById('reset-pw2').value;
  const errEl  = document.getElementById('reset-error');
  errEl.classList.add('hidden');

  if (pw !== pw2) {
    errEl.textContent = 'Passwords do not match.';
    errEl.classList.remove('hidden');
    return;
  }
  try {
    const res = await fetch('/api/auth/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, new_password: pw }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      errEl.textContent = err.detail || 'Something went wrong. Please try again.';
      errEl.classList.remove('hidden');
      return;
    }
    window.history.replaceState({}, '', '/');   // remove ?reset=... from URL
    showLoginSection('reset-success');
  } catch(e) {
    errEl.textContent = e.message;
    errEl.classList.remove('hidden');
  }
}

async function checkResetToken() {
  const params = new URLSearchParams(window.location.search);
  const token  = params.get('reset');
  if (!token) return;

  // Hide everything while we verify
  _LOGIN_SECTIONS.forEach(s => {
    const el = document.getElementById(s);
    if (el) el.classList.add('hidden');
  });

  try {
    const res  = await fetch(`/api/auth/verify-reset-token/${encodeURIComponent(token)}`);
    const data = await res.json();
    if (data.valid) {
      document.getElementById('reset-token-val').value = token;
      showLoginSection('reset-form-wrap');
    } else {
      showLoginSection('reset-invalid');
    }
  } catch(_) {
    showLoginSection('reset-invalid');
  }
}

// ═══════════════════════════════════════════════════════════
// AI Tutor — Session List
// ═══════════════════════════════════════════════════════════
async function renderAiTutor(el) {
  loading(el);
  try {
    const [statusData, sessions] = await Promise.all([
      api('GET', '/ai-tutor/status').catch(() => null),
      api('GET', '/ai-tutor/sessions').catch(() => []),
    ]);

    const ollamaOk = statusData?.available;
    const ollamaBanner = !ollamaOk ? `
      <div class="chat-ollama-banner">
        ⚠️ <strong>Ollama is not running.</strong>
        Start it with: <code>ollama serve</code> and make sure
        <code>ollama pull ${statusData?.model || 'llama3.2'}</code> has been run.
      </div>` : '';

    el.innerHTML = `
      <div class="page-header">
        <h2>🤖 ${t('ai_tutor')}</h2>
        <button class="btn btn-primary" onclick="openNewTutorSessionModal()">${t('new_chat')}</button>
      </div>
      ${ollamaBanner}
      <div id="ai-tutor-sessions" style="margin-top:${ollamaOk ? '0' : '12px'}">
        ${(sessions||[]).length ? (sessions||[]).map(s => `
          <div class="card" style="margin-bottom:10px;cursor:pointer" onclick="navigate('ai-chat',{id:${s.id}})">
            <div class="card-body" style="display:flex;align-items:center;gap:14px;padding:14px 18px">
              <div style="font-size:1.6rem;flex-shrink:0">
                ${s.mode === 'assignment_help' ? '📝' : '📖'}
              </div>
              <div style="flex:1;min-width:0">
                <div style="font-weight:700;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
                  ${htmlEsc(s.title)}
                </div>
                <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
                  <span class="chat-mode-pill ${s.mode === 'assignment_help' ? 'chat-mode-assignment' : 'chat-mode-study'}">
                    ${s.mode === 'assignment_help' ? 'Assignment Help' : 'Study'}
                  </span>
                  ${s.course_title ? `<small class="text-muted">📚 ${htmlEsc(s.course_title)}</small>` : ''}
                  <small class="text-muted">💬 ${s.message_count} message${s.message_count !== 1 ? 's' : ''}</small>
                  <small class="text-muted">${fmtDate(s.created_at)}</small>
                </div>
              </div>
              <button class="btn btn-sm btn-danger" style="flex-shrink:0"
                onclick="event.stopPropagation();deleteTutorSession(${s.id})">🗑</button>
            </div>
          </div>`).join('')
        : `<div class="card"><div class="card-body">
            <p class="text-muted" style="text-align:center;padding:24px">
              ${t('no_chat_sessions')}
            </p></div></div>`}
      </div>`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

// ═══════════════════════════════════════════════════════════
// AI Tutor — Chat View
// ═══════════════════════════════════════════════════════════
async function renderAiChat(sessionId, el) {
  loading(el);
  window._chatUploads = [];
  try {
    const [session, messages, statusData] = await Promise.all([
      api('GET', `/ai-tutor/sessions/${sessionId}`),
      api('GET', `/ai-tutor/sessions/${sessionId}/messages`),
      api('GET', '/ai-tutor/status').catch(() => null),
    ]);
    if (!session) { el.innerHTML = '<div class="alert alert-error">Session not found</div>'; return; }

    const ollamaOk = statusData?.available;

    el.innerHTML = `
      <div style="margin-bottom:12px">
        <button class="btn btn-sm" onclick="navigate('ai_tutor')">${t('back')}</button>
      </div>
      <div class="chat-layout">
        <div class="chat-main">
          <div class="chat-main-header">
            <div style="flex:1;min-width:0">
              <h3 style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:3px">
                ${htmlEsc(session.title)}
              </h3>
              <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
                <span class="chat-mode-pill ${session.mode === 'assignment_help' ? 'chat-mode-assignment' : 'chat-mode-study'}">
                  ${session.mode === 'assignment_help' ? '📝 Hint-Only Mode' : '📖 Study Mode'}
                </span>
                ${session.course_title ? `<small class="text-muted">📚 ${htmlEsc(session.course_title)}</small>` : ''}
              </div>
            </div>
            ${ollamaOk
              ? `<span class="badge badge-success" style="flex-shrink:0">● Online</span>`
              : `<span class="badge badge-warning" style="flex-shrink:0">⚠ Ollama offline</span>`}
          </div>

          ${!ollamaOk ? `<div class="chat-ollama-banner">
            ⚠️ Ollama is not running — messages will fail until you run <code>ollama serve</code>.
          </div>` : ''}

          <div class="chat-messages" id="chat-messages-area">
            ${(messages||[]).length
              ? (messages||[]).map(m => renderChatBubble(m)).join('')
              : `<div class="chat-empty">
                  <div class="chat-empty-icon">🤖</div>
                  <p>${t('chat_empty')}</p>
                  ${session.mode === 'assignment_help'
                    ? `<p style="font-size:12px;color:var(--muted)">${t('chat_hint_note')}</p>`
                    : ''}
                </div>`}
          </div>

          <div class="chat-input-area">
            <div class="chat-file-chips" id="chat-file-chips"></div>
            <div class="chat-input-row">
              <label class="btn btn-sm" title="${t('chat_attach')}" style="cursor:pointer;margin-bottom:0;flex-shrink:0">
                📎
                <input type="file" id="chat-file-input" style="display:none"
                  accept=".txt,.py,.js,.ts,.jsx,.tsx,.java,.c,.cpp,.h,.cs,.go,.rb,.php,.html,.css,.md,.csv,.json,.xml,.yaml,.pdf,.docx,.jpg,.jpeg,.png,.gif,.webp"
                  onchange="handleChatFileSelect(${sessionId},this)">
              </label>
              <textarea id="chat-text-input" placeholder="${t('chat_placeholder')}"
                onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendChatMessage(${sessionId})}"
                oninput="this.style.height='auto';this.style.height=Math.min(this.scrollHeight,140)+'px'"></textarea>
              <button class="btn btn-primary" onclick="sendChatMessage(${sessionId})" id="chat-send-btn" style="flex-shrink:0">
                ${t('chat_send')} ▶
              </button>
            </div>
            <small class="text-muted" style="font-size:11px">Enter to send · Shift+Enter for new line · Max 3 files · 20 MB each</small>
          </div>
        </div>
      </div>`;

    // Scroll to bottom of messages
    const area = document.getElementById('chat-messages-area');
    if (area) area.scrollTop = area.scrollHeight;

    // Focus input
    document.getElementById('chat-text-input')?.focus();
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function renderChatBubble(m) {
  const isUser = m.role === 'user';
  return `
    <div class="chat-bubble-wrap ${isUser ? 'user' : 'assistant'}">
      <div class="chat-bubble ${isUser ? 'user' : 'assistant'}">${htmlEsc(m.content)}</div>
      <div class="chat-bubble-time">${fmtDateTime(m.created_at)}</div>
    </div>`;
}

async function handleChatFileSelect(sessionId, input) {
  if (!input.files || !input.files[0]) return;
  const file = input.files[0];
  input.value = '';

  if ((window._chatUploads || []).length >= 3) {
    toast('Maximum 3 files per message', 'error'); return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    toast('📎 Uploading…');
    const res = await fetch(`/api/ai-tutor/sessions/${sessionId}/upload`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${state.token}` },
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      const detail = err.detail;
      const msg = Array.isArray(detail)
        ? detail.map(e => e.msg || JSON.stringify(e)).join('; ')
        : (typeof detail === 'string' ? detail : 'Upload failed');
      toast(msg, 'error'); return;
    }
    const data = await res.json();
    window._chatUploads = window._chatUploads || [];
    window._chatUploads.push({ upload_id: data.upload_id, filename: data.filename, kind: data.file_kind });
    renderChatChips();
    toast(`📎 ${data.filename} attached`);
  } catch(e) { toast(e.message, 'error'); }
}

function renderChatChips() {
  const el = document.getElementById('chat-file-chips');
  if (!el) return;
  el.innerHTML = (window._chatUploads || []).map((u, i) => `
    <span class="upload-chip">
      ${u.kind === 'image' ? '🖼' : u.kind === 'pdf' ? '📄' : '📎'} ${htmlEsc(u.filename)}
      <span class="chip-remove" onclick="removeChatUpload(${i})">×</span>
    </span>`).join('');
}

function removeChatUpload(i) {
  window._chatUploads = (window._chatUploads || []).filter((_, idx) => idx !== i);
  renderChatChips();
}

async function sendChatMessage(sessionId) {
  const input   = document.getElementById('chat-text-input');
  const sendBtn = document.getElementById('chat-send-btn');
  const content = input?.value.trim();
  const uploads = window._chatUploads || [];

  if (!content && !uploads.length) return;

  const uploadIds = uploads.map(u => u.upload_id);
  const messagesArea = document.getElementById('chat-messages-area');

  // Remove empty-state placeholder if present
  const emptyEl = messagesArea?.querySelector('.chat-empty');
  if (emptyEl) emptyEl.remove();

  // Optimistic user bubble
  const userWrap = document.createElement('div');
  userWrap.innerHTML = renderChatBubble({
    role: 'user',
    content: content || `(${uploads.map(u => u.filename).join(', ')})`,
    created_at: new Date().toISOString(),
  });
  messagesArea?.appendChild(userWrap);

  // Thinking indicator
  const thinkingWrap = document.createElement('div');
  thinkingWrap.className = 'chat-bubble-wrap assistant';
  thinkingWrap.innerHTML = `<div class="chat-thinking"><span></span><span></span><span></span></div>`;
  messagesArea?.appendChild(thinkingWrap);
  if (messagesArea) messagesArea.scrollTop = messagesArea.scrollHeight;

  // Reset input
  if (input) { input.value = ''; input.style.height = 'auto'; }
  window._chatUploads = [];
  renderChatChips();
  if (sendBtn) sendBtn.disabled = true;

  try {
    const reply = await api('POST', `/ai-tutor/sessions/${sessionId}/messages`, {
      content: content || `(see attached file${uploads.length > 1 ? 's' : ''})`,
      upload_ids: uploadIds.length ? uploadIds : undefined,
    });
    thinkingWrap.remove();

    // The endpoint returns the assistant message object directly
    const aiMsg = reply?.assistant_message ?? reply;
    const aiBubble = document.createElement('div');
    aiBubble.innerHTML = renderChatBubble({
      role: 'assistant',
      content: aiMsg?.content ?? JSON.stringify(aiMsg),
      created_at: aiMsg?.created_at ?? new Date().toISOString(),
    });
    messagesArea?.appendChild(aiBubble);
    if (messagesArea) messagesArea.scrollTop = messagesArea.scrollHeight;
  } catch(err) {
    thinkingWrap.remove();
    const isQuizLock = err.message.includes('403') || err.message.toLowerCase().includes('quiz');
    const errBubble = document.createElement('div');
    errBubble.className = 'chat-bubble-wrap assistant';
    errBubble.innerHTML = `
      <div class="chat-bubble assistant" style="color:var(--danger);border-color:var(--danger)">
        ${isQuizLock ? t('chat_locked') : `⚠️ ${htmlEsc(err.message)}`}
      </div>`;
    messagesArea?.appendChild(errBubble);
    if (messagesArea) messagesArea.scrollTop = messagesArea.scrollHeight;
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    document.getElementById('chat-text-input')?.focus();
  }
}

async function deleteTutorSession(id) {
  if (!confirm('Delete this chat session and all its messages?')) return;
  try {
    await api('DELETE', `/ai-tutor/sessions/${id}`);
    toast('Session deleted');
    navigate('ai_tutor');
  } catch(e) { toast(e.message, 'error'); }
}

async function openNewTutorSessionModal() {
  let enrolled = [];
  try {
    const courses = await api('GET', '/courses/') || [];
    enrolled = courses.filter(c => c.enrolled);
  } catch(_) {}

  openModal('🤖 New AI Tutor Session', `
    <form id="modal-form">
      <div class="form-group"><label>Mode *</label>
        <select name="mode" class="form-control" id="tutor-mode-sel" onchange="onTutorModeChange()">
          <option value="study">📖 Study Session</option>
          <option value="assignment_help">📝 Assignment Help (hints only)</option>
        </select>
      </div>
      <div class="form-group"><label>Course</label>
        <select name="course_id" class="form-control" id="tutor-course-sel" onchange="onTutorCourseChange()">
          <option value="">— General (no specific course) —</option>
          ${enrolled.map(c => `<option value="${c.id}">${htmlEsc(c.title)}</option>`).join('')}
        </select>
      </div>
      <div class="form-group hidden" id="tutor-assignment-group"><label>Assignment *</label>
        <select name="assignment_id" class="form-control" id="tutor-assignment-sel">
          <option value="">— Select a course first —</option>
        </select>
      </div>
      <div class="form-group"><label>Session Title <span class="text-muted">(optional)</span></label>
        <input name="title" class="form-control" placeholder="Auto-generated if blank">
      </div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">Start Chat ▶</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        const courseId     = fd.get('course_id')     ? parseInt(fd.get('course_id'))     : null;
        const assignmentId = fd.get('assignment_id') ? parseInt(fd.get('assignment_id')) : null;
        const session = await api('POST', '/ai-tutor/sessions', {
          course_id:     courseId     || undefined,
          assignment_id: assignmentId || undefined,
          title:         fd.get('title') || undefined,
          mode:          fd.get('mode'),
        });
        closeModal();
        navigate('ai-chat', { id: session.id });
      } catch(e) { toast(e.message, 'error'); }
    });
}

function onTutorModeChange() {
  const mode  = document.getElementById('tutor-mode-sel')?.value;
  const group = document.getElementById('tutor-assignment-group');
  if (!group) return;
  if (mode === 'assignment_help') {
    group.classList.remove('hidden');
    onTutorCourseChange();
  } else {
    group.classList.add('hidden');
  }
}

async function onTutorCourseChange() {
  const courseId = document.getElementById('tutor-course-sel')?.value;
  const sel      = document.getElementById('tutor-assignment-sel');
  if (!sel) return;
  if (!courseId) {
    sel.innerHTML = '<option value="">— Select a course first —</option>';
    return;
  }
  sel.innerHTML = '<option>Loading…</option>';
  try {
    const assignments = await api('GET', `/assignments/course/${courseId}`).catch(() => []);
    sel.innerHTML = (assignments||[]).length
      ? (assignments||[]).map(a => `<option value="${a.id}">${htmlEsc(a.title)}</option>`).join('')
      : '<option value="">No assignments in this course</option>';
  } catch(_) {
    sel.innerHTML = '<option value="">Error loading assignments</option>';
  }
}

// ═══════════════════════════════════════════════════════════
// Init
// ═══════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errEl = document.getElementById('login-error');
    errEl.classList.add('hidden');
    try {
      await login(document.getElementById('login-email').value,
                  document.getElementById('login-password').value);
      showApp();
    } catch(err) { errEl.textContent = err.message; errEl.classList.remove('hidden'); }
  });

  document.getElementById('logout-btn').addEventListener('click', logout);
  document.getElementById('modal-overlay').addEventListener('click', (e) => {
    if (e.target === document.getElementById('modal-overlay')) closeModal();
  });

  if (restoreSession()) {
    showApp();
  } else {
    document.getElementById('login-page').classList.remove('hidden');
    checkResetToken();
  }
});
