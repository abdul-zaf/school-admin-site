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
    nav_calendar:'Calendar',
    nav_messages:'Messages',
    // Auth
    sign_in:'Sign In', sign_out:'Sign out', email:'Email', password:'Password',
    login_hint:'Default admin: admin@school.edu / Admin123',
    // Common
    back:'← Back', save:'Save', cancel:'Cancel', delete:'Delete',
    create:'Create', add:'Add', edit:'Edit', submit:'Submit', loading:'Loading…',
    by:'By', yes:'Yes', no:'No',
    // Dashboard
    welcome:'Welcome Back',
    // Courses
    courses:'Courses', new_course:'+ New Course', enroll:'Enroll',
    unenroll:'Unenroll', enrolled:'Enrolled', no_courses:'No courses yet.',
    my_courses:'My Courses', browse_courses:'Browse Courses',
    subject:'Subject', grade_level:'Grade Level', section_number:'Section Number', description:'Description',
    teacher:'Teacher', students:'Students', student_count:'students',
    all_courses:'All Courses',
    // Materials
    materials:'Materials', course_materials:'Course Materials',
    add_material:'+ Add Material', title_label:'Title', content:'Content',
    url_label:'URL (optional)', no_materials:'No materials yet.',
    upload_file:'Upload File', link_text:'Link / Text',
    file_upload_hint:'Any file type (PDF, video, image, document…) — max 200 MB',
    download:'Download', view_file:'View', view_slides:'View Slides',
    // Assignments
    assignments:'Assignments', new_assignment:'+ New Assignment', manual:'Manual', ai_generate:'AI Generate',
    instructions:'Instructions', due_date:'Due', max_score:'Max Score',
    pts:'pts', submit_assignment:'Submit Assignment',
    your_submission:'Your Submission', resubmit:'Resubmit',
    edit_resubmit:'Edit / Resubmit', not_graded:'Not graded yet.',
    not_submitted:'Not submitted', submissions:'Submissions',
    no_submissions:'No submissions yet.', feedback:'Feedback',
    score:'Score', save_grade:'Save Grade', graded:'Graded',
    // Quizzes
    quizzes:'Assessments', new_quiz:'+ New Assessment', quiz_builder:'Assessment Builder',
    add_question:'+ Add Question', question_type:'Question Type',
    multiple_choice:'Multiple Choice', true_false:'True / False',
    short_answer:'Short Answer', question_text:'Question', points:'Points',
    correct_answer:'Correct', start_quiz:'Start Assessment', submit_quiz:'Submit Assessment',
    quiz_results:'View Results', time_limit:'Time Limit (min)',
    minutes:'min', time_remaining:'Time remaining', no_quizzes:'No assessments yet.',
    attempt_count:'attempts', not_attempted:'Not attempted',
    attempted:'Attempted', q_num:'Question', of:'of',
    short_manual:'Short answer — graded manually by teacher.',
    quiz_submitted:'Assessment submitted!', your_score:'Your Score',
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
    event_assignment:'Assignment Due', event_session:'Session', event_quiz:'Assessment Due',
    overdue:'Overdue', due_soon:'Due Soon',
    messages:'Messages', inbox:'Inbox', sent:'Sent', compose:'+ Compose',
    compose_message:'Compose Message', recipient:'Recipient', subject:'Subject',
    message_body:'Message', send:'Send', no_messages:'No messages.',
    analytics:'Analytics', grade_distribution:'Grade Distribution',
    submission_rate:'Submission Rate', avg_score:'Avg Score', active_students:'Active Students',
    total_users:'Total Users', total_courses:'Total Courses', submissions_this_week:'Submissions This Week',
    add_questions:'+ Add Question', no_banks:'No question banks yet.',
    modules:'Modules', new_module:'+ New Module', add_module_item:'+ Add Item',
    mark_complete:'Mark Complete', completed:'Completed', progress:'Progress',
    discussions:'Discussions', new_board:'+ New Board', reply:'Reply',
    endorse:'Endorse', no_boards:'No discussion boards yet.', post:'Post',
    view_results:'View Results',
    // Exams
    exams:'Exams', nav_exams:'Exams',
    new_exam:'+ New Exam', exam_mode:'Exam Mode',
    exam_warning:'This is a locked exam. You cannot navigate away until you submit or the time expires.',
    exam_submit_confirm:'Are you sure you want to submit? You cannot go back.',
    exam_time_up:'Time is up — your exam has been submitted automatically.',
    is_exam:'Mark as Exam (locked environment)',
    unlock_after_all_materials:'Unlock only after student completes ALL course materials',
    exam_locked_all_materials:'Complete all course materials to unlock this exam',
    // Co-teachers
    co_teachers:'Co-Teachers', add_co_teacher:'Add Teacher', no_co_teachers:'No co-teachers assigned yet.',
    // Leaderboard

    your_rank:'Your Rank', rank:'Rank', top_students:'Top Students',
    // Retake limits
    max_attempts:'Max Attempts', unlimited:'Unlimited',
    attempts_remaining:'attempts left', no_attempts_left:'No attempts remaining',
    // Quiz publish / edit
    quiz_published:'Published', quiz_draft:'Draft',
    publish_quiz:'Publish to Students', unpublish_quiz:'Unpublish',
    edit_quiz:'Edit Details', quiz_edit_saved:'Assessment updated!',
    // Material completion / unlock
    mark_complete:'Mark as Complete', completed:'Completed',
    // AI quiz generation
    ai_generate:'AI Generate', ai_generate_title:'Add Questions',
    ai_generate_prompt:'Want AI to generate questions from your course materials?',
    ai_skip:'Skip — add manually',
    select_materials:'Select Materials', select_all:'Select All', deselect_all:'Deselect All',
    num_mc:'Multiple Choice', num_tf:'True / False', num_short:'Short Answer', num_long:'Long Answer',
    generating:'Generating…', ai_generated_ok:'Questions generated!',
    tab_ai_gen:'AI Generate', tab_manual:'Manual',
    add_option:'+ Add Option', mark_correct:'Mark correct',
    long_answer:'Long Answer', long_manual:'Students write a full paragraph response. Teacher grades this.',
    // Teacher grading
    grade_responses:'Grade Responses', grading_panel:'Grading Panel',
    student_answer:'Student Answer', your_score:'Score', feedback_optional:'Feedback (optional)',
    save_grades:'Save Grades', grades_saved:'Grades saved!', needs_grading:'Needs Grading',
    pending_teacher_grade:'Awaiting teacher grading',
    urgent_quizzes:' Urgent: Assessments',
    no_urgent:'No pending assessments — you\'re all caught up!',
    start_now:'Start Now', resume_quiz:'Resume',
    urgent:'Urgent',
    // Post-quiz results popup
    quiz_score_result:'Your Result',
    outstanding_quizzes:'Outstanding Assessments',
    no_outstanding_quizzes:'No assessments remaining! Well done!',
    outstanding_quizzes_msg:'You still have these assessments to complete:',
    pending_grading:'Awaiting teacher grading',
    // Post-submit assignment check
    outstanding_assignments:'Outstanding Assignments',
    no_outstanding:'No outstanding assignments! Well done! ',
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
    chat_locked:' AI Tutor is locked while an assessment is in progress. Submit or finish the assessment first.',
    chat_attach:'Attach file',
    no_chat_sessions:'No chat sessions yet. Click + New Chat to get started.',
    // Due date picker
    dp_today:'Today', dp_tomorrow:'Tomorrow', dp_next_week:'+1 Week',
    dp_clear:'Clear', dp_date:'Date', dp_time:'Time',
    dp_no_due:'No due date',
    // Attendance
    nav_attendance:'Attendance', attendance_title:'Attendance Tracker',
    att_pick_course:'Select a course', att_pick_date:'Date',
    att_mark:'Mark Attendance', att_save:'Save Attendance',
    att_present:'Present', att_absent:'Absent', att_late:'Late',
    att_no_students:'No students enrolled.', att_saved:'Attendance saved.',
    att_history:'History', att_summary:'Summary',
    att_total:'Total', att_present_count:'Present', att_absent_count:'Absent', att_late_count:'Late',
    att_rate:'Attendance Rate',
    // Report Cards
    nav_report_cards:'Report Cards', report_cards_title:'Report Cards',
    rc_generate:'Generate with AI', rc_generating:'Generating…',
    rc_publish:'Publish', rc_unpublish:'Unpublish', rc_delete:'Delete',
    rc_edit:'Edit', rc_save:'Save', rc_cancel:'Cancel',
    rc_published:'Published', rc_draft:'Draft',
    rc_no_cards:'No report cards yet.',
    rc_pick_student:'Select student',
    rc_pick_course:'Select course',
    rc_generated:'Report card generated.',
    rc_deleted:'Report card deleted.',
    rc_view:'View Report Card',
  },
  ur: {
    app_name:'اسکول ایل ایم ایس',
    // Nav
    nav_dashboard:'ڈیش بورڈ', nav_courses:'کورسز', nav_users:'صارفین',
    nav_announcements:'اعلانات', nav_settings:'ترتیبات',
    // Auth
    sign_in:'سائن اِن', sign_out:'سائن آوٹ', email:'ای میل', password:'پاس ورڈ',
    login_hint:'پہلا منتظم: admin@school.edu / Admin123',
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
    subject:'مضمون', grade_level:'جماعت', section_number:'سیکشن نمبر', description:'تفصیل',
    teacher:'استاد', students:'طلبا', student_count:'طلبا',
    all_courses:'تمام کورسز',
    // Materials
    materials:'مواد', course_materials:'کورس مواد',
    add_material:'+ مواد شامل کریں', title_label:'عنوان', content:'مواد',
    url_label:'لنک (اختیاری)', no_materials:'ابھی کوئی مواد نہیں۔',
    upload_file:'فائل اپ لوڈ کریں', link_text:'لنک / متن',
    file_upload_hint:'کوئی بھی فائل (پی ڈی ایف، ویڈیو، تصویر...) — زیادہ سے زیادہ 200 ایم بی',
    download:'ڈاؤن لوڈ', view_file:'دیکھیں', view_slides:'سلائیڈز دیکھیں',
    // Assignments
    assignments:'اسائنمنٹس', new_assignment:'+ نیا اسائنمنٹ', manual:'دستی', ai_generate:'AI سے بنائیں',
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
    nav_messages:'پیغامات',
    gradebook:'گریڈ بک', my_grades:'میرے نمبر', weighted_avg:'وزنی اوسط',
    letter_grade:'حروفی گریڈ', gpa:'جی پی اے', cumulative_gpa:'مجموعی جی پی اے',
    calendar:'کیلنڈر', upcoming_events:'آنے والے واقعات', no_events:'کوئی واقعات نہیں۔',
    messages:'پیغامات', inbox:'ان باکس', sent:'بھیجے گئے', compose:'+ لکھیں',
    compose_message:'پیغام لکھیں', send:'بھیجیں', no_messages:'کوئی پیغام نہیں۔',
    analytics:'تجزیات', grade_distribution:'نمبروں کی تقسیم',
    modules:'ماڈیولز', discussions:'بحث',
    // Exams (Urdu)
    exams:'امتحانات', nav_exams:'امتحانات',
    new_exam:'+ نیا امتحان', exam_mode:'امتحان موڈ',
    exam_warning:'یہ ایک بند امتحان ہے۔ جمع کرنے یا وقت ختم ہونے تک آپ کہیں نہیں جا سکتے۔',
    exam_submit_confirm:'کیا آپ واقعی جمع کرنا چاہتے ہیں؟ واپس نہیں جا سکتے۔',
    exam_time_up:'وقت ختم — آپ کا امتحان خودبخود جمع ہو گیا۔',
    is_exam:'امتحان کے طور پر نشان زد کریں (بند ماحول)',
    unlock_after_all_materials:'تمام کورس مواد مکمل کرنے کے بعد ہی امتحان کھلے گا',
    exam_locked_all_materials:'یہ امتحان کھولنے کے لیے تمام کورس مواد مکمل کریں',
    // Co-teachers (Urdu)
    co_teachers:'معاون اساتذہ', add_co_teacher:'استاد شامل کریں', no_co_teachers:'ابھی کوئی معاون استاد مقرر نہیں۔',
    // Leaderboard (Urdu)

    your_rank:'آپ کی پوزیشن', rank:'پوزیشن', top_students:'اعلیٰ طلبا',
    // Retake (Urdu)
    max_attempts:'زیادہ سے زیادہ کوششیں', unlimited:'لامحدود',
    attempts_remaining:'کوششیں باقی', no_attempts_left:'کوئی کوشش باقی نہیں',
    // Quiz publish / edit (Urdu)
    quiz_published:'شائع شدہ', quiz_draft:'مسودہ',
    publish_quiz:'طلبا کو دکھائیں', unpublish_quiz:'چھپائیں',
    edit_quiz:'تفصیل ترمیم', quiz_edit_saved:'کوئز اپڈیٹ ہو گئی!',
    // Material completion / unlock (Urdu)
    mark_complete:'مکمل کریں', completed:'مکمل',
    // AI quiz generation (Urdu)
    ai_generate:'AI سے بنائیں', ai_generate_title:'سوالات شامل کریں',
    ai_generate_prompt:'کیا AI آپ کے کورس مواد سے سوالات بنائے؟',
    ai_skip:'چھوڑیں — خود شامل کریں',
    select_materials:'مواد منتخب کریں', select_all:'سب منتخب کریں', deselect_all:'سب ہٹائیں',
    num_mc:'کثیر انتخابی', num_tf:'صحیح / غلط', num_short:'مختصر جواب', num_long:'طویل جواب',
    generating:'تیار ہو رہا ہے…', ai_generated_ok:'سوالات تیار ہو گئے!',
    tab_ai_gen:'AI سے بنائیں', tab_manual:'خود لکھیں',
    add_option:'+ آپشن شامل کریں', mark_correct:'درست نشان کریں',
    long_answer:'طویل جواب', long_manual:'طالب علم مکمل جواب لکھتا ہے۔ استاد اسے جانچتا ہے۔',
    // Teacher grading (Urdu)
    grade_responses:'جوابات جانچیں', grading_panel:'جانچ پینل',
    student_answer:'طالب علم کا جواب', your_score:'نمبر', feedback_optional:'رائے (اختیاری)',
    save_grades:'نمبر محفوظ کریں', grades_saved:'نمبر محفوظ!', needs_grading:'جانچ درکار',
    pending_teacher_grade:'استاد کی جانچ کا انتظار',
    urgent_quizzes:' ضروری: کوئز اور ٹیسٹ',
    no_urgent:'کوئی زیر التواء کوئز نہیں — آپ نے سب مکمل کر لیے!',
    start_now:'ابھی شروع کریں', resume_quiz:'جاری رکھیں',
    urgent:'ضروری',
    // Post-quiz results (Urdu)
    quiz_score_result:'آپ کا نتیجہ',
    outstanding_quizzes:'باقی کوئز اور ٹیسٹ',
    no_outstanding_quizzes:'کوئی کوئز یا ٹیسٹ باقی نہیں!  شاباش!',
    outstanding_quizzes_msg:'آپ کے ابھی یہ کوئز / ٹیسٹ باقی ہیں:',
    pending_grading:'استاد کی جانب سے گریڈنگ کا انتظار ہے',
    // Post-submit assignment check (Urdu)
    outstanding_assignments:'باقی اسائنمنٹس',
    no_outstanding:'کوئی اسائنمنٹ باقی نہیں! شاباش! ',
    outstanding_msg:'آپ کے ابھی یہ اسائنمنٹس مکمل کرنے ہیں:',
    go_to_assignment:'اسائنمنٹ دیکھیں',
    well_done:'شاباش!',
    // Misc
    enrolled_courses:'داخل شدہ کورسز', available_courses:'دستیاب',
    total_students:'کل طلبا', manage_courses:'کورسز منظم کریں',
    // Due date picker (Urdu)
    dp_today:'آج', dp_tomorrow:'کل', dp_next_week:'+1 ہفتہ',
    dp_clear:'ہٹائیں', dp_date:'تاریخ', dp_time:'وقت',
    dp_no_due:'کوئی آخری تاریخ نہیں',
    // Attendance (Urdu)
    nav_attendance:'حاضری', attendance_title:'حاضری ٹریکر',
    att_pick_course:'کورس منتخب کریں', att_pick_date:'تاریخ',
    att_mark:'حاضری لگائیں', att_save:'حاضری محفوظ کریں',
    att_present:'حاضر', att_absent:'غیر حاضر', att_late:'دیر سے',
    att_no_students:'کوئی طالب علم داخل نہیں۔', att_saved:'حاضری محفوظ ہو گئی۔',
    att_history:'تاریخ', att_summary:'خلاصہ',
    att_total:'کل', att_present_count:'حاضر', att_absent_count:'غیر حاضر', att_late_count:'دیر سے',
    att_rate:'حاضری شرح',
    // Report Cards (Urdu)
    nav_report_cards:'رپورٹ کارڈ', report_cards_title:'رپورٹ کارڈ',
    rc_generate:'AI سے بنائیں', rc_generating:'بن رہا ہے…',
    rc_publish:'شائع کریں', rc_unpublish:'غیر شائع کریں', rc_delete:'حذف کریں',
    rc_edit:'ترمیم', rc_save:'محفوظ', rc_cancel:'منسوخ',
    rc_published:'شائع شدہ', rc_draft:'مسودہ',
    rc_no_cards:'ابھی کوئی رپورٹ کارڈ نہیں۔',
    rc_pick_student:'طالب علم منتخب کریں',
    rc_pick_course:'کورس منتخب کریں',
    rc_generated:'رپورٹ کارڈ بن گیا۔',
    rc_deleted:'رپورٹ کارڈ حذف ہو گیا۔',
    rc_view:'رپورٹ کارڈ دیکھیں',
  }
};

function t(key) {
  const lang = state.lang || 'en';
  return (i18n[lang] && i18n[lang][key]) || i18n.en[key] || key;
}

// ═══════════════════════════════════════════════════════════
// Due-date picker helper
// ═══════════════════════════════════════════════════════════
// Renders a date + time row with quick-pick shortcuts.
// `id`    — unique id prefix used for the hidden <input name="due_date">
//           and for the date/time sub-inputs.
// `value` — ISO string "YYYY-MM-DDTHH:MM" (or empty) to pre-fill.
function dueDatePicker(id, value) {
  const datePart = value ? value.slice(0, 10) : '';
  const timePart = value ? value.slice(11, 16) : '23:59';
  return `
    <div class="due-date-picker" id="${id}-picker">
      <div class="ddp-shortcuts">
        <button type="button" class="btn btn-sm ddp-btn" onclick="ddpSet('${id}','today')">${t('dp_today')}</button>
        <button type="button" class="btn btn-sm ddp-btn" onclick="ddpSet('${id}','tomorrow')">${t('dp_tomorrow')}</button>
        <button type="button" class="btn btn-sm ddp-btn" onclick="ddpSet('${id}','week')">${t('dp_next_week')}</button>
        <button type="button" class="btn btn-sm ddp-btn ddp-clear" onclick="ddpClear('${id}')">${t('dp_clear')}</button>
      </div>
      <div class="ddp-inputs">
        <div class="ddp-field">
          <label class="ddp-label">${t('dp_date')}</label>
          <input type="date" id="${id}-date" class="form-control ddp-date"
            value="${datePart}" onchange="ddpSync('${id}')">
        </div>
        <div class="ddp-field">
          <label class="ddp-label">${t('dp_time')}</label>
          <input type="time" id="${id}-time" class="form-control ddp-time"
            value="${timePart}" onchange="ddpSync('${id}')">
        </div>
      </div>
      <div id="${id}-preview" class="ddp-preview">${value ? fmtDateTimeLocal(value) : t('dp_no_due')}</div>
      <input type="hidden" name="due_date" id="${id}-val" value="${value||''}">
    </div>`;
}

function ddpSet(id, preset) {
  const now = new Date();
  if (preset === 'today') { /* keep today */ }
  else if (preset === 'tomorrow') now.setDate(now.getDate() + 1);
  else if (preset === 'week') now.setDate(now.getDate() + 7);
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  document.getElementById(id + '-date').value = `${y}-${m}-${d}`;
  document.getElementById(id + '-time').value = '23:59';
  ddpSync(id);
}

function ddpClear(id) {
  document.getElementById(id + '-date').value = '';
  document.getElementById(id + '-time').value = '23:59';
  ddpSync(id);
}

function ddpSync(id) {
  const date = document.getElementById(id + '-date').value;
  const time = document.getElementById(id + '-time').value || '23:59';
  const combined = date ? `${date}T${time}` : '';
  document.getElementById(id + '-val').value = combined;
  document.getElementById(id + '-preview').textContent = combined ? fmtDateTimeLocal(combined) : t('dp_no_due');
}

function fmtPts(n) { return Number.isInteger(n) ? n : parseFloat(n) % 1 === 0 ? parseInt(n) : n; }

function fmtDateTimeLocal(iso) {
  if (!iso) return '';
  const d = new Date(iso.includes('T') ? iso : iso.replace(' ', 'T'));
  if (isNaN(d)) return iso;
  return d.toLocaleDateString(undefined, { weekday:'short', year:'numeric', month:'short', day:'numeric' })
    + ' at ' + d.toLocaleTimeString(undefined, { hour:'2-digit', minute:'2-digit' });
}

// ═══════════════════════════════════════════════════════════
// State
// ═══════════════════════════════════════════════════════════
const state = {
  token: null, user: null, lang: 'en',
  currentPage: null, currentParams: {},
  quizTimer: null, notifInterval: null,
  examLocked: false,
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
  exitExamLock();
  state.token = null; state.user = null;
  localStorage.removeItem('lms_token'); localStorage.removeItem('lms_user');
  document.getElementById('app').classList.add('hidden');
  document.getElementById('login-page').classList.remove('hidden');
}

function restoreSession() {
  const token = localStorage.getItem('lms_token');
  const user  = localStorage.getItem('lms_user');
  const lang  = localStorage.getItem('lms_lang') || 'en';
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

// ═══════════════════════════════════════════════════════════
// Notifications & Modal
// ═══════════════════════════════════════════════════════════
function toast(msg, type = 'success') {
  const el = document.createElement('div');
  el.className = `toast toast-${type}`; el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3200);
}

function openModal(title, html, onSubmitOrOpts) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = html;
  const modalEl = document.querySelector('.modal');
  const isOpts = onSubmitOrOpts && typeof onSubmitOrOpts === 'object';
  if (modalEl) modalEl.classList.toggle('modal-wide', !!(isOpts && onSubmitOrOpts.wide));
  document.getElementById('modal-overlay').classList.remove('hidden');
  const onSubmit = !isOpts ? onSubmitOrOpts : null;
  if (onSubmit) {
    const form = document.getElementById('modal-form');
    if (form) form.onsubmit = async (e) => { e.preventDefault(); await onSubmit(new FormData(form)); };
  }
}
function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
  const modalEl = document.querySelector('.modal');
  if (modalEl) modalEl.classList.remove('modal-wide');
}

// In-app confirm dialog — replaces browser confirm()
// Returns a Promise<boolean>; resolves true on OK, false on Cancel.
function showConfirm(message, { title = 'Confirm', okLabel = 'Confirm', okClass = 'btn-danger' } = {}) {
  return new Promise(resolve => {
    document.getElementById('confirm-title').textContent = title;
    document.getElementById('confirm-message').textContent = message;
    const okBtn = document.getElementById('confirm-ok-btn');
    const cancelBtn = document.getElementById('confirm-cancel-btn');
    okBtn.className = `btn ${okClass}`;
    okBtn.textContent = okLabel;
    const overlay = document.getElementById('confirm-overlay');
    overlay.classList.remove('hidden');
    function cleanup(result) {
      overlay.classList.add('hidden');
      okBtn.onclick = null;
      cancelBtn.onclick = null;
      resolve(result);
    }
    okBtn.onclick = () => cleanup(true);
    cancelBtn.onclick = () => cleanup(false);
  });
}

function loading(el) {
  el.innerHTML = `<div class="loading"><div class="spinner"></div><p>${t('loading')}</p></div>`;
}

// ═══════════════════════════════════════════════════════════
// Navigation
// ═══════════════════════════════════════════════════════════
const NAV_KEYS = {
  admin:   ['dashboard','courses','users','announcements','gradebook','attendance','report_cards','analytics','calendar','messages','settings'],
  teacher: ['dashboard','courses','users','announcements','gradebook','attendance','report_cards','analytics','calendar','messages','settings'],
  student: ['dashboard','courses','announcements','gradebook','report_cards','calendar','messages','ai_tutor','settings'],
  parent:  ['dashboard','settings'],
};
const NAV_I18N = {
  dashboard:'nav_dashboard', courses:'nav_courses', users:'nav_users',
  announcements:'nav_announcements', settings:'nav_settings',
  gradebook:'nav_gradebook', analytics:'nav_analytics', calendar:'nav_calendar',
  messages:'nav_messages', question_banks:'nav_question_banks',
  ai_tutor:'nav_ai_tutor',
  attendance:'nav_attendance', report_cards:'nav_report_cards',
};
const NAV_ICONS = {
  dashboard:'', courses:'', users:'', announcements:'',
  gradebook:'', analytics:'', calendar:'',
  messages:'',
  settings:'', ai_tutor:'',
  attendance:'', report_cards:'',
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
  document.getElementById('sidebar-nav').innerHTML = NAV_KEYS[r].map(p => {
    const isActive = state.currentPage === p || (p === 'courses' && state.currentPage === 'course');
    const hasFlyout = NAV_FLYOUT_PAGES[p] && NAV_FLYOUT_PAGES[p].roles.includes(r);
    const flyoutAttrs = hasFlyout
      ? `onmouseenter="showNavFlyoutFor('${p}',this)" onmouseleave="_scheduleFlyoutHide()"`
      : '';
    return `<a class="nav-item${isActive?' active':''}" data-page="${p}" onclick="navigate('${p}')" ${flyoutAttrs}>
      <span class="nav-icon">${NAV_ICONS[p]||'•'}</span>
      <span class="nav-label">${t(NAV_I18N[p])}</span>
      ${hasFlyout ? '<span class="nav-chevron">›</span>' : ''}
    </a>`;
  }).join('');

  // Bind flyout panel listeners once on first nav render
  const flyout = document.getElementById('nav-flyout');
  if (flyout && !flyout._flyoutBound) {
    flyout.addEventListener('mouseenter', _cancelFlyoutHide);
    flyout.addEventListener('mouseleave', _scheduleFlyoutHide);
    flyout._flyoutBound = true;
  }
}

// ── Shared nav hover flyout system ────────────────────────────────────────────

// Which pages get a flyout and which roles can see it
const NAV_FLYOUT_PAGES = {
  courses:       { roles: ['admin','teacher','student'], endpoint: '/courses/' },
  announcements: { roles: ['admin','teacher','student'], endpoint: '/announcements/' },
  messages:      { roles: ['admin','teacher','student'], endpoint: '/messages/' },
  users:         { roles: ['admin'],                     endpoint: '/users/' },
};

const _flyoutCache   = {};
const _flyoutFetched = {};
const FLYOUT_CACHE_MS = 60_000;

let _flyoutHideTimer = null;
function _cancelFlyoutHide()   { clearTimeout(_flyoutHideTimer); }
function _scheduleFlyoutHide() { _flyoutHideTimer = setTimeout(hideNavFlyout, 220); }

function showNavFlyoutFor(page, item) {
  _cancelFlyoutHide();
  const flyout = document.getElementById('nav-flyout');
  if (!flyout) return;
  const rect = item.getBoundingClientRect();
  flyout.style.top = Math.max(8, Math.min(rect.top, window.innerHeight - 360)) + 'px';
  flyout.classList.add('visible');
  loadNavFlyout(page);
}

function hideNavFlyout() {
  const f = document.getElementById('nav-flyout');
  if (f) f.classList.remove('visible');
}

function invalidateFlyoutCache(page) {
  delete _flyoutCache[page];
  delete _flyoutFetched[page];
}

// Backward-compat alias used by deleteCourse / createCourse
function invalidateCoursesFlyoutCache() { invalidateFlyoutCache('courses'); }

async function loadNavFlyout(page) {
  const flyout = document.getElementById('nav-flyout');
  if (!flyout || !(page in NAV_FLYOUT_PAGES)) return;

  // Show skeleton while loading
  const title = _flyoutTitle(page);
  flyout.innerHTML = `<div class="nav-flyout-header">${title}</div>
    <div class="nav-flyout-list"><div class="nav-flyout-loading">Loading…</div></div>`;

  const now = Date.now();
  if (_flyoutCache[page] && now - (_flyoutFetched[page] || 0) < FLYOUT_CACHE_MS) {
    flyout.innerHTML = _renderFlyout(page, _flyoutCache[page]);
    return;
  }
  try {
    const data = await api('GET', NAV_FLYOUT_PAGES[page].endpoint);
    _flyoutCache[page] = data;
    _flyoutFetched[page] = now;
    flyout.innerHTML = _renderFlyout(page, data);
  } catch (e) {
    flyout.innerHTML = `<div class="nav-flyout-header">${title}</div>
      <div class="nav-flyout-list"><div class="nav-flyout-error">Could not load</div></div>`;
  }
}

function _flyoutTitle(page) {
  return ({
    courses: t('all_courses'),
    announcements: t('school_announcements') || 'Announcements',
    messages: t('messages'),
    users: t('users'),
  })[page] || page;
}

function _renderFlyout(page, data) {
  const title  = _flyoutTitle(page);
  const header = `<div class="nav-flyout-header">${title}</div>`;
  const footer  = `<div class="nav-flyout-footer">
    <span class="nav-flyout-all" onclick="navigate('${page}');hideNavFlyout()">${title} →</span>
  </div>`;

  let items = '';

  if (page === 'courses') {
    if (!data?.length) return header + `<div class="nav-flyout-list"><div class="nav-flyout-empty">${t('no_courses')}</div></div>` + footer;
    const visible = data.slice(0, 10);
    const extra   = data.length - visible.length;
    items = visible.map(c => `
      <div class="nav-flyout-item" onclick="navigate('course',{id:${c.id}});hideNavFlyout()">
        <span class="nav-flyout-dot" style="background:${subjectAccent(c.subject||'',c.title||'')}"></span>
        <div class="nav-flyout-item-text">
          <div class="nav-flyout-item-title">${htmlEsc(c.title)}</div>
          ${c.subject ? `<div class="nav-flyout-item-sub">${htmlEsc(c.subject)}</div>` : ''}
        </div>
      </div>`).join('')
      + (extra > 0 ? `<div class="nav-flyout-more">+${extra} more</div>` : '');
  }

  else if (page === 'announcements') {
    if (!data?.length) return header + `<div class="nav-flyout-list"><div class="nav-flyout-empty">No announcements</div></div>` + footer;
    items = data.slice(0, 5).map(a => `
      <div class="nav-flyout-item" onclick="navigate('announcements');hideNavFlyout()">
        <span class="nav-flyout-dot" style="background:#f59e0b"></span>
        <div class="nav-flyout-item-text">
          <div class="nav-flyout-item-title">${htmlEsc(a.title)}</div>
          <div class="nav-flyout-item-sub">${htmlEsc(a.author_name||'')} · ${fmtDate(a.created_at)}</div>
        </div>
      </div>`).join('');
  }

  else if (page === 'messages') {
    if (!data?.length) return header + `<div class="nav-flyout-list"><div class="nav-flyout-empty">No messages</div></div>` + footer;
    items = data.slice(0, 6).map(m => {
      const other  = m.sender_name === state.user?.name ? m.recipient_name : m.sender_name;
      const unread = !m.is_read && m.recipient_id === state.user?.id;
      return `
        <div class="nav-flyout-item${unread?' nav-flyout-item-unread':''}" onclick="navigate('messages');hideNavFlyout()">
          <span class="nav-flyout-avatar">${htmlEsc((other||'?')[0].toUpperCase())}</span>
          <div class="nav-flyout-item-text">
            <div class="nav-flyout-item-title">${htmlEsc(m.subject||'(no subject)')}</div>
            <div class="nav-flyout-item-sub">${htmlEsc(other||'?')}</div>
          </div>
          ${unread ? '<span class="nav-flyout-unread-dot"></span>' : ''}
        </div>`;
    }).join('');
  }

  else if (page === 'users') {
    if (!data?.length) return header + `<div class="nav-flyout-list"><div class="nav-flyout-empty">No users</div></div>` + footer;
    items = data.slice(0, 8).map(u => `
      <div class="nav-flyout-item" onclick="navigate('users');hideNavFlyout()">
        <span class="nav-flyout-avatar">${htmlEsc((u.name||'?')[0].toUpperCase())}</span>
        <div class="nav-flyout-item-text">
          <div class="nav-flyout-item-title">${htmlEsc(u.name||'')}</div>
          <div class="nav-flyout-item-sub">${htmlEsc(u.role||'')}</div>
        </div>
      </div>`).join('');
  }

  return header + `<div class="nav-flyout-list">${items}</div>` + footer;
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

// ── Notifications hover panel ─────────────────────────────────────────────────

let _notifHideTimer = null;
function _cancelNotifHide()   { clearTimeout(_notifHideTimer); }
function _scheduleNotifHide() { _notifHideTimer = setTimeout(hideNotifPanel, 220); }

function showNotifPanel(bellWrapper) {
  _cancelNotifHide();
  const panel = document.getElementById('notif-panel');
  if (!panel) return;
  const rect = bellWrapper.getBoundingClientRect();
  // Panel grows upward from the bell — available space is rect.top (above bell)
  const panelH = Math.max(220, Math.min(460, rect.top - 12));
  panel.style.maxHeight = panelH + 'px';
  panel.style.bottom = (window.innerHeight - rect.bottom - 2) + 'px';
  panel.classList.add('visible');
  loadNotifPanel();
}

function hideNotifPanel() {
  const p = document.getElementById('notif-panel');
  if (p) p.classList.remove('visible');
}

function _notifIcon(title) {
  const s = (title || '').toLowerCase();
  if (/quiz|test|exam/.test(s))       return '';
  if (/assignment|submit/.test(s))    return '';
  if (/grade|score|mark/.test(s))     return '';
  if (/message|inbox/.test(s))        return '';
  if (/announce|notice/.test(s))      return '';
  if (/enroll|course/.test(s))        return '';
  if (/badge|award/.test(s))          return '';
  return '';
}

function _relTime(iso) {
  const mins = Math.floor((Date.now() - new Date(iso)) / 60000);
  if (mins <  1)  return 'Just now';
  if (mins < 60)  return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs  < 24)  return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days <  7)  return `${days}d ago`;
  return fmtDate(iso);
}

async function loadNotifPanel() {
  const panel = document.getElementById('notif-panel');
  if (!panel) return;
  panel.innerHTML = `
    <div class="notif-panel-header">
      <span class="notif-panel-title"> Notifications</span>
      <button class="notif-mark-all" onclick="markAllNotifsRead()">Mark all read</button>
    </div>
    <div class="notif-list"><div class="notif-empty-state">
      <span class="notif-empty-icon"></span><p>Loading…</p>
    </div></div>`;
  try {
    const notifs = await api('GET', '/notifications/?limit=15');
    const list = panel.querySelector('.notif-list');
    if (!list) return;
    if (!notifs?.length) {
      list.innerHTML = `<div class="notif-empty-state">
        <span class="notif-empty-icon"></span>
        <p>You're all caught up!</p>
      </div>`;
      return;
    }
    list.innerHTML = notifs.map(n => `
      <div class="notif-item${n.is_read ? '' : ' unread'}${n.link ? ' notif-clickable' : ''}"
           onclick="_notifClick(${n.id},'${(n.link||'').replace(/'/g,"\\'")}')">
        <div class="notif-icon">${_notifIcon(n.title)}</div>
        <div class="notif-content">
          <div class="notif-title">${htmlEsc(n.title)}</div>
          ${n.body ? `<div class="notif-body">${htmlEsc(n.body)}</div>` : ''}
          <div class="notif-time">${_relTime(n.created_at)}</div>
        </div>
        ${n.is_read ? '' : '<div class="notif-unread-dot"></div>'}
        ${n.link ? '<div class="notif-arrow">›</div>' : ''}
      </div>`).join('');
    panel.innerHTML += `<div class="notif-panel-footer">
      <button class="notif-view-all" onclick="hideNotifPanel()">Close</button>
    </div>`;
  } catch(e) {
    const list = panel.querySelector('.notif-list');
    if (list) list.innerHTML = `<div class="notif-empty-state">
      <span class="notif-empty-icon"></span><p>Could not load notifications</p>
    </div>`;
  }
}

async function markNotifRead(id) {
  try {
    await api('PUT', `/notifications/${id}/read`);
    refreshNotifCount();
    loadNotifPanel();
  } catch(e) { /* silent */ }
}

async function markAllNotifsRead() {
  try {
    await api('PUT', '/notifications/read-all');
    refreshNotifCount();
    const list = document.querySelector('#notif-panel .notif-list');
    if (list) list.innerHTML = `<div class="notif-empty-state">
      <span class="notif-empty-icon"></span>
      <p>You're all caught up!</p>
    </div>`;
  } catch(e) { /* silent */ }
}

async function _notifClick(id, link) {
  // Mark read (best-effort, don't block navigation)
  api('PUT', `/notifications/${id}/read`).then(() => { refreshNotifCount(); }).catch(() => {});
  hideNotifPanel();
  if (!link) return;
  // Parse link format: "assignment:123", "quiz:456", "course:789", "announcements", "messages"
  const [type, idStr] = link.split(':');
  const targetId = parseInt(idStr, 10);
  if      (type === 'assignment')   navigate('assignment',  { id: targetId });
  else if (type === 'quiz')         navigate('quiz-take',   { id: targetId });
  else if (type === 'course')       navigate('course',      { id: targetId });
  else if (type === 'announcements' || link === 'announcements') navigate('announcements');
  else if (type === 'messages'      || link === 'messages')      navigate('messages');
}

function navigate(page, params = {}) {
  // Block all navigation during an active exam
  if (state.examLocked && page !== 'exam-take') {
    toast(t('exam_warning'), 'error');
    return;
  }
  if (state.quizTimer) { clearInterval(state.quizTimer); state.quizTimer = null; }
  state.currentPage = page; state.currentParams = params;
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  // 'course' is a sub-page of 'courses' — highlight the courses nav item
  const activePage = page === 'course' ? 'courses' : page;
  const a = document.querySelector(`.nav-item[data-page="${activePage}"]`);
  if (a) a.classList.add('active');
  const el = document.getElementById('page-content');
  const pages = {
    dashboard: renderDashboard, courses: renderCourses,
    users: renderUsers, announcements: renderAnnouncements, settings: renderSettings,
    gradebook: renderGradebook, calendar: renderCalendar, messages: renderMessages,
    analytics: renderAnalytics,
    ai_tutor: renderAiTutor,
    attendance: renderAttendance,
    report_cards: renderReportCards,
  };
  if      (page === 'course')        renderCourseDetail(params.id, el);
  else if (page === 'assignment')    renderAssignmentDetail(params.id, el);
  else if (page === 'quiz-builder')  renderQuizBuilder(params.id, el);
  else if (page === 'quiz-take')     renderQuizTake(params.id, el);
  else if (page === 'exam-take')     renderExamTake(params.id, el);
  else if (page === 'discussion-board') renderDiscussionBoard(params.id, el);
  else if (page === 'ai-chat')       renderAiChat(params.id, el);
  // ── Learning Intelligence & Social ───────────────────────────────────────
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
            &nbsp; English
          </button>
          <button class="lang-btn${state.lang==='ur'?' active':''}" onclick="setLanguage('ur')">
            &nbsp; اردو
          </button>
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
          <h2>${t('welcome')}, ${state.user.name}</h2>
          <p>${t('nav_dashboard')} — EduPortal School Management</p>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card-blue"   data-icon=""><div class="stat-number">${users.filter(u=>u.role==='student').length}</div><div class="stat-label">${t('students')}</div></div>
          <div class="stat-card stat-card-purple" data-icon=""><div class="stat-number">${users.filter(u=>u.role==='teacher').length}</div><div class="stat-label">${t('teachers')}</div></div>
          <div class="stat-card stat-card-green"  data-icon=""><div class="stat-number">${courses.length}</div><div class="stat-label">${t('courses')}</div></div>
          <div class="stat-card stat-card-gold"   data-icon=""><div class="stat-number">${anns.length}</div><div class="stat-label">${t('announcements')}</div></div>
        </div>
        <div class="card"><div class="card-header ch-green"><h3> ${t('courses')}</h3>
          <button class="btn btn-sm btn-primary" onclick="openNewCourseModal()">${t('new_course')}</button></div>
          <div class="card-body">
            ${courses.length ? courses.map(c=>`
              <div class="course-item" onclick="navigate('course',{id:${c.id}})">
                <div><strong>${htmlEsc(c.title)}</strong><small>${htmlEsc(c.subject||'')} ${c.grade_level?'· '+htmlEsc(c.grade_level):''}${c.section_number?' · §'+htmlEsc(c.section_number):''}</small></div>
                <span class="badge badge-info">${c.student_count} ${t('student_count')}</span>
              </div>`).join('') : `<p class="text-muted">${t('no_courses')}</p>`}
          </div>
        </div>
        <div class="card"><div class="card-header ch-gold"><h3> ${t('announcements')}</h3>
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
      el.innerHTML = `
        <div class="welcome-banner">
          <h2>${t('welcome')}, ${state.user.name}</h2>
          <p> ${t('teachers')} Dashboard — EduPortal</p>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card-blue"  data-icon=""><div class="stat-number">${courses.length}</div><div class="stat-label">${t('courses')}</div></div>
          <div class="stat-card stat-card-green" data-icon=""><div class="stat-number">${courses.reduce((s,c)=>s+c.student_count,0)}</div><div class="stat-label">${t('total_students')}</div></div>
        </div>
        <div class="card"><div class="card-header ch-green"><h3> ${t('courses')}</h3>
          <button class="btn btn-sm btn-primary" onclick="openNewCourseModal()">${t('new_course')}</button></div>
          <div class="card-body">
            ${courses.length ? courses.map(c=>`
              <div class="course-item" onclick="navigate('course',{id:${c.id}})">
                <div><strong>${htmlEsc(c.title)}</strong><small>${htmlEsc(c.subject||'')} ${c.grade_level?'· '+htmlEsc(c.grade_level):''}${c.section_number?' · §'+htmlEsc(c.section_number):''}</small></div>
                <span class="badge badge-info">${c.student_count} ${t('student_count')}</span>
              </div>`).join('') : `<p class="text-muted">${t('no_courses')}</p>`}
          </div>
        </div>`;

    } else {
      const [courses, anns] = await Promise.all([api('GET','/courses/'), api('GET','/announcements/')]);
      const enrolled = courses.filter(c => c.enrolled);
      el.innerHTML = `
        <div class="welcome-banner">
          <h2>${t('welcome')}, ${state.user.name}</h2>
          <p> ${t('students')} Dashboard — EduPortal</p>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card-green"  data-icon=""><div class="stat-number">${enrolled.length}</div><div class="stat-label">${t('enrolled_courses')}</div></div>
          <div class="stat-card stat-card-teal"   data-icon=""><div class="stat-number">${courses.length-enrolled.length}</div><div class="stat-label">${t('available_courses')}</div></div>
        </div>
        <!-- Urgent quizzes panel (populated async below) -->
        <div class="card" id="urgent-quizzes-card">
          <div class="card-header ch-red"><h3>${t('urgent_quizzes')}</h3></div>
          <div class="card-body" id="urgent-quizzes-body">
            <div class="loading"><div class="spinner"></div></div>
          </div>
        </div>
        <div class="card"><div class="card-header ch-green"><h3> ${t('my_courses')}</h3>
          <button class="btn btn-sm btn-primary" onclick="navigate('courses')">${t('browse_courses')}</button></div>
          <div class="card-body">
            ${enrolled.length ? enrolled.map(c=>`
              <div class="course-item" onclick="navigate('course',{id:${c.id}})">
                <div><strong>${htmlEsc(c.title)}</strong><small>${t('teacher')}: ${htmlEsc(c.teacher_name||'?')}</small></div>
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
  const canManage = role === 'admin' || role === 'teacher';
  const accent = subjectAccent(c.subject, c.title);
  return `
    <div class="course-card" style="--accent:${accent}" onclick="navigate('course',{id:${c.id}})">
      <div class="course-card-header">
        <h3>${htmlEsc(c.title)}</h3>
        ${c.grade_level ? `<span class="badge badge-info">${htmlEsc(c.grade_level)}</span>` : ''}
        ${c.section_number ? `<span class="badge badge-secondary">§ ${htmlEsc(c.section_number)}</span>` : ''}
      </div>
      <div class="course-card-body">
        ${c.subject ? `<p style="color:${accent};font-weight:600;font-size:12px">${htmlEsc(c.subject)}</p>` : ''}
        ${c.description ? `<p>${htmlEsc(c.description).substring(0,90)}${c.description.length>90?'…':''}</p>` : ''}
        <div class="course-meta">
          <small> ${htmlEsc(c.teacher_name||'?')}</small>
          <small> ${c.student_count} ${t('student_count')}</small>
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
      <div class="form-group"><label>${t('section_number')}</label>
        <input name="section_number" class="form-control" placeholder="e.g. A, B, 01, Morning"></div>
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
          grade_level:fd.get('grade_level')||null, section_number:fd.get('section_number')||null,
          description:fd.get('description')||null });
        invalidateCoursesFlyoutCache(); closeModal(); toast(t('new_course')); navigate('courses');
      } catch(err) { toast(err.message,'error'); }
    });
}

async function enrollCourse(id) {
  try { await api('POST',`/courses/${id}/enroll`); toast(t('enrolled')+'!'); navigate('courses'); }
  catch(err) { toast(err.message,'error'); }
}
async function unenrollCourse(id) {
  if (!await showConfirm(t('unenroll')+'?')) return;
  try { await api('DELETE',`/courses/${id}/enroll`); toast(t('unenroll')); navigate('courses'); }
  catch(err) { toast(err.message,'error'); }
}
async function deleteCourse(id) {
  if (!await showConfirm(t('delete')+'?')) return;
  try { await api('DELETE',`/courses/${id}`); invalidateCoursesFlyoutCache(); toast(t('delete')); navigate('courses'); }
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
    const canManage = role==='admin' || role==='teacher';
    const now = new Date();

    el.innerHTML = `
      <div class="page-header">
        <div>
          <button class="btn btn-sm" onclick="navigate('courses')" style="margin-bottom:8px">${t('back')}</button>
          <h2>${htmlEsc(course.title)}</h2>
          <div class="flex-gap mt-8">
            ${course.subject    ? `<span class="badge badge-info">${htmlEsc(course.subject)}</span>`     : ''}
            ${course.grade_level? `<span class="badge badge-info">${htmlEsc(course.grade_level)}</span>` : ''}
          </div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px">
          <small class="text-muted">${t('teacher')}: ${htmlEsc(course.teacher_name||'?')}</small>
        </div>
      </div>
      ${course.description ? `<div class="card"><div class="card-body"><p>${htmlEsc(course.description)}</p></div></div>` : ''}

      <div class="tabs">
        <button class="tab active" onclick="showTab('materials',this)">${t('materials')} (${materials.length})</button>
        <button class="tab" onclick="showTab('assignments',this)">${t('assignments')} (${assignments.length})</button>
        <button class="tab" onclick="showTab('quizzes',this)">${t('quizzes')} (${quizzes.length})</button>
        <button class="tab" onclick="showTab('sessions',this)">${t('sessions')} (${sessions.length})</button>
        <button class="tab" onclick="showTab('modules',this);renderModulesTab(${courseId},document.getElementById('tab-modules'),${canManage})">${t('modules')}</button>
        <button class="tab" onclick="showTab('discussions',this);renderDiscussionsTab(${courseId},document.getElementById('tab-discussions'),${canManage})">${t('discussions')}</button>
        <!-- ── New feature tabs ── -->
        <button class="tab" onclick="showTab('helpboard',this);renderHelpBoardTab(${courseId}).then(h=>document.getElementById('tab-helpboard').innerHTML=h)">${t('help_board')}</button>
        <button class="tab" onclick="showTab('studygroups',this);renderStudyGroupsTab(${courseId},${canManage}).then(h=>document.getElementById('tab-studygroups').innerHTML=h)">${t('study_groups')}</button>
        ${canManage ? `<button class="tab" onclick="showTab('students',this)">${t('students')} (${course.students.length})</button>` : ''}
        ${canManage ? `<button class="tab" onclick="showTab('coteachers',this);renderCoTeachersTab(${courseId},document.getElementById('tab-coteachers'),${JSON.stringify(course.co_teachers||[])})">${t('co_teachers')} (${(course.co_teachers||[]).length})</button>` : ''}
        ${canManage ? `<button class="tab" onclick="showTab('anns',this)">${t('announcements')}</button>` : ''}
      </div>

      <!-- MATERIALS -->
      <div id="tab-materials">
        <div class="card">
          <div class="card-header"><h3>${t('course_materials')}</h3>
            ${canManage ? `<button class="btn btn-sm btn-primary" onclick="openAddMaterialModal(${courseId})">${t('add_material')}</button>` : ''}</div>
          <div class="card-body">
            ${(() => { window._matData = {}; window._ytPendingInit = []; materials.forEach(m => { window._matData[m.id] = m; }); return ''; })()}
            ${materials.length ? materials.map(m => {
              const mtype = m.material_type || (m.url ? 'link' : 'text');
              const icon = mtype === 'file' ? fileMimeIcon(m.file_mime) : (mtype === 'link' ? '' : '');
              const badge = `<span class="mat-type-badge mat-type-${mtype}">${mtype}</span>`;
              const isViewable = m.file_mime && (
                m.file_mime.startsWith('image/') || m.file_mime.startsWith('video/') ||
                m.file_mime.startsWith('audio/') || m.file_mime === 'application/pdf' ||
                m.file_mime.startsWith('text/')
              );
              let body = '';
              if (mtype === 'file') {
                const sz = formatFileSize(m.file_size);
                const isPdf = m.file_mime === 'application/pdf';
                const btnLabel = isPdf ? ` ${t('view_file')}` : (isViewable ? ` ${t('view_file')}` : ` ${t('download')}`);
                body = `
                  <div class="mat-file-info">
                    <span class="mat-filename">${htmlEsc(m.file_name || '')}</span>
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
                const linkAutoComplete = (role === 'student' && !m.completed)
                  ? ` onclick="completeMaterial(${courseId},${m.id})"` : '';
                const ytId = getYouTubeId(m.url);
                if (ytId) {
                  const ytIframeId = `yt-player-${m.id}`;
                  if (role === 'student' && !m.completed) {
                    window._ytPendingInit.push({iframeId: ytIframeId, courseId, matId: m.id});
                  }
                  body = (m.content ? `<p class="mat-content">${htmlEsc(m.content)}</p>` : '') +
                    `<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;margin-top:8px">
                      <iframe id="${ytIframeId}"
                        src="https://www.youtube.com/embed/${ytId}?enablejsapi=1"
                        style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;border-radius:8px"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen>
                      </iframe>
                    </div>`;
                } else {
                  body = (m.content ? `<p class="mat-content">${htmlEsc(m.content)}</p>` : '') +
                         `<a class="link mat-link" href="${htmlEsc(m.url)}" target="_blank" rel="noopener"${linkAutoComplete}>${htmlEsc(m.url)}</a>`;
                }
              } else {
                body = m.content ? `<p class="mat-content">${htmlEsc(m.content)}</p>` : '';
              }
              const completedBadge = (role === 'student' && m.completed)
                ? `<span class="badge badge-success" id="mat-done-${m.id}"> ${t('completed')}</span>` : '';
              return `
                <div class="material-item" id="mat-item-${m.id}" data-cid="${courseId}" data-mid="${m.id}" data-completed="${m.completed ? '1' : '0'}">
                  <div class="material-icon">${icon}</div>
                  <div class="material-body">
                    <div class="material-title"><strong>${htmlEsc(m.title)}</strong>${badge}${completedBadge}</div>
                    ${body}
                    <small class="text-muted">${fmtDate(m.created_at)}</small>
                  </div>
                  <div style="display:flex;gap:6px;align-items:center">
                    ${canManage ? `<button class="btn btn-sm btn-secondary" onclick="openEditMaterialModal(${courseId},${m.id},window._matData[${m.id}])"> Edit</button>` : ''}
                    ${canManage ? `<button class="btn btn-sm btn-danger" onclick="deleteMaterial(${courseId},${m.id})">${t('delete')}</button>` : ''}
                  </div>
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
              <div class="list-item" style="display:flex;align-items:center;justify-content:space-between;gap:8px">
                <div class="clickable" style="flex:1;min-width:0" onclick="navigate('assignment',{id:${a.id}})">
                  <strong>${htmlEsc(a.title)}</strong>
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
                ${canManage ? `<button class="btn btn-sm btn-danger" style="flex-shrink:0" onclick="event.stopPropagation();deleteAssignment(${a.id},${courseId})">Delete</button>` : ''}
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

      <!-- HELP BOARD (async rendered by features.js) -->
      <div id="tab-helpboard" class="hidden">
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
                <tbody>${course.students.map(s=>`<tr><td>${htmlEsc(s.name)}</td><td>${htmlEsc(s.email)}</td></tr>`).join('')}</tbody>
              </table>` : `<p class="text-muted">${t('students')} — 0</p>`}
          </div>
        </div>
      </div>
      <div id="tab-coteachers" class="hidden"></div>
      <div id="tab-anns" class="hidden">
        <div class="card">
          <div class="card-header"><h3>${t('course_announcements')}</h3>
            ${state.user.role !== 'student' ? `<button class="btn btn-sm btn-primary" onclick="openAnnouncementModal(${courseId})">${t('post_announcement')}</button>` : ''}</div>
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
    // Auto-mark text-type materials complete for students (they're immediately visible)
    if (state.user && state.user.role === 'student') {
      materials.forEach(m => {
        if (!m.completed && (m.material_type === 'text' || (!m.material_type && !m.url && !m.file_name))) {
          completeMaterial(courseId, m.id);
        }
      });
      // Init YouTube tracking now that iframes are in the DOM
      (window._ytPendingInit || []).forEach(p => attachYTPlayer(p.iframeId, p.courseId, p.matId));
      window._ytPendingInit = [];
    }
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function showTab(name, btn) {
  document.querySelectorAll('[id^="tab-"]').forEach(t => t.classList.add('hidden'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  const tabEl = document.getElementById(`tab-${name}`);
  if (tabEl) tabEl.classList.remove('hidden');
  btn.classList.add('active');
}

// ── Co-teacher management tab ──
async function renderCoTeachersTab(courseId, el, initialList) {
  const isOwnerOrAdmin = state.user.role === 'admin' ||
    (state.user.role === 'teacher');  // all teachers can manage if they're on this course

  let coTeachers = initialList || [];

  function draw() {
    el.innerHTML = `
      <div class="card">
        <div class="card-header">
          <h3>${t('co_teachers')}</h3>
          <button class="btn btn-sm btn-primary" onclick="openAddCoTeacherModal(${courseId})">${t('add_co_teacher')}</button>
        </div>
        <div class="card-body">
          ${coTeachers.length ? `
            <table class="table">
              <thead><tr><th>${t('full_name')}</th><th>${t('email')}</th><th></th></tr></thead>
              <tbody>${coTeachers.map(ct => `
                <tr>
                  <td>${htmlEsc(ct.name)}</td>
                  <td>${htmlEsc(ct.email)}</td>
                  <td><button class="btn btn-sm btn-danger" onclick="removeCoTeacher(${courseId},${ct.id},this)">${t('delete')}</button></td>
                </tr>`).join('')}
              </tbody>
            </table>` : `<p class="text-muted">${t('no_co_teachers')}</p>`}
        </div>
      </div>`;
  }

  draw();

  window._coTeacherState = window._coTeacherState || {};
  window._coTeacherState[courseId] = { coTeachers, draw: () => draw() };
}

async function openAddCoTeacherModal(courseId) {
  let teachers = [];
  try {
    teachers = await api('GET', '/users/?role=teacher');
  } catch(e) { teachers = []; }

  // Fetch current co-teachers to exclude them
  let current = [];
  try { current = await api('GET', `/courses/${courseId}/teachers`); } catch(e) {}
  const currentIds = new Set(current.map(t => t.id));

  // Also get course owner to exclude
  let course;
  try { course = await api('GET', `/courses/${courseId}`); } catch(e) {}
  const ownerId = course ? course.teacher_id : null;

  const available = teachers.filter(t => !currentIds.has(t.id) && t.id !== ownerId);

  openModal(`
    <h3>${t('add_co_teacher')}</h3>
    <div class="form-group">
      <label>${t('teacher')}</label>
      <select id="co-teacher-select" class="form-control">
        <option value="">— Select —</option>
        ${available.map(t => `<option value="${t.id}">${htmlEsc(t.name)} (${htmlEsc(t.email)})</option>`).join('')}
      </select>
    </div>
    <div style="display:flex;gap:8px;margin-top:16px">
      <button class="btn btn-primary" onclick="confirmAddCoTeacher(${courseId})">${t('add_co_teacher')}</button>
      <button class="btn" onclick="closeModal()">${t('cancel')}</button>
    </div>`);
}

async function confirmAddCoTeacher(courseId) {
  const sel = document.getElementById('co-teacher-select');
  const teacherId = sel ? parseInt(sel.value) : 0;
  if (!teacherId) return;
  try {
    await api('POST', `/courses/${courseId}/teachers/${teacherId}`);
    closeModal();
    // Refresh tab
    const el = document.getElementById('tab-coteachers');
    if (el) {
      const updated = await api('GET', `/courses/${courseId}/teachers`);
      if (window._coTeacherState && window._coTeacherState[courseId]) {
        window._coTeacherState[courseId].coTeachers = updated;
        window._coTeacherState[courseId].draw();
      }
    }
  } catch(e) { toast(e.message, 'error'); }
}

async function removeCoTeacher(courseId, teacherId, btn) {
  if (!await showConfirm('Remove this teacher from the course?')) return;
  try {
    await api('DELETE', `/courses/${courseId}/teachers/${teacherId}`);
    if (window._coTeacherState && window._coTeacherState[courseId]) {
      window._coTeacherState[courseId].coTeachers =
        window._coTeacherState[courseId].coTeachers.filter(t => t.id !== teacherId);
      window._coTeacherState[courseId].draw();
    }
  } catch(e) { toast(e.message, 'error'); }
}

// ── Quiz card (in course detail list) ──
function quizCard(q, canManage, courseId) {
  const attempted  = q.my_attempt && q.my_attempt.submitted_at;
  const inProgress = q.my_attempt && !q.my_attempt.submitted_at;
  const scoreLabel = attempted
    ? `${t('score')}: ${q.my_attempt.score!=null ? fmtPts(q.my_attempt.score) : '?'}/${fmtPts(q.total_points)}`
    : (inProgress ? t('attempted') : t('not_attempted'));
  const attemptBadgeCls = attempted ? 'badge-success' : (inProgress ? 'badge-warning' : 'badge-secondary');

  // Students: flag published-but-not-attempted as urgent
  const isUrgent = !canManage && q.is_published && !attempted && !inProgress;

  return `
    <div class="quiz-card${isUrgent ? ' quiz-urgent' : ''}">
      <div class="quiz-card-body">
        <div class="quiz-title-row">
          <strong>${htmlEsc(q.title)}</strong>
          ${q.is_exam ? `<span class="exam-badge">EXAM</span>` : ''}
          ${isUrgent ? `<span class="badge badge-danger"> ${t('urgent')}</span>` : ''}
          ${canManage
            ? (q.is_published
              ? `<span class="badge badge-success"> ${t('quiz_published')}</span>`
              : `<span class="badge badge-warning"> ${t('quiz_draft')}</span>`)
            : ''}
        </div>
        ${q.description ? `<p class="text-muted" style="margin-top:4px;font-size:13px">${htmlEsc(q.description)}</p>` : ''}
        <div class="quiz-meta">
          <small>${q.question_count} ${t('question_text')}(s) &bull; ${q.total_points} ${t('pts')}</small>
          ${q.time_limit ? `<small> ${q.time_limit} ${t('minutes')}</small>` : ''}
          ${q.due_date ? `<small> ${t('due_date')}: ${fmtDate(q.due_date)}</small>` : ''}
          ${canManage && q.attempt_count!=null ? `<small> ${q.attempt_count} ${t('attempt_count')}</small>` : ''}
          ${canManage && q.max_attempts ? `<small> ${t('max_attempts')}: ${q.max_attempts}</small>` : ''}
          ${!canManage && q.max_attempts ? (() => {
            const left = q.max_attempts - (q.attempts_used || 0);
            return left > 0
              ? `<small style="color:var(--warning)"> ${left} ${t('attempts_remaining')}</small>`
              : `<small style="color:var(--danger)"> ${t('no_attempts_left')}</small>`;
          })() : ''}
        </div>
      </div>
      <div class="quiz-card-actions">
        ${!canManage ? `<span class="badge ${attemptBadgeCls}">${scoreLabel}</span>` : ''}
        ${!canManage && !attempted && !inProgress && q.question_count > 0
          && !(q.max_attempts && (q.attempts_used || 0) >= q.max_attempts)
          ? (q.is_exam
            ? `<button class="btn btn-sm btn-primary" onclick="startExam(${q.id})"> ${t('start_quiz')}</button>`
            : `<button class="btn btn-sm btn-primary" onclick="startQuiz(${q.id})"> ${t('start_quiz')}</button>`) : ''}
        ${!canManage && inProgress
          ? (q.is_exam
            ? `<button class="btn btn-sm btn-warning" onclick="navigate('exam-take',{id:${q.id}})"> ${t('resume_quiz')}</button>`
            : `<button class="btn btn-sm btn-warning" onclick="navigate('quiz-take',{id:${q.id}})"> ${t('resume_quiz')}</button>`) : ''}
        ${!canManage && attempted
          ? (q.is_exam
            ? `<button class="btn btn-sm" onclick="navigate('exam-take',{id:${q.id}})">${t('quiz_results')}</button>`
            : `<button class="btn btn-sm" onclick="navigate('quiz-take',{id:${q.id}})">${t('quiz_results')}</button>`) : ''}
        ${canManage ? `
          ${q.unlock_all_materials ? `<span class="badge badge-info" style="font-size:11px"> ${t('unlock_after_all_materials')}</span>` : ''}
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
  const icon = isVirtual ? '' : '';
  const past = isPast(s.date);
  return `
    <div class="session-card">
      <div class="session-icon ${s.session_type}">${icon}</div>
      <div class="session-body">
        <strong>${htmlEsc(s.title)}</strong>
        <div class="session-meta">
          <span class="badge badge-${s.session_type}">${t(s.session_type)}</span>
          <small> ${fmtDateTime(s.date)}</small>
          <small> ${s.duration_minutes} ${t('mins')}</small>
          ${s.location ? (isVirtual
            ? `<a class="link" href="${htmlEsc(s.location)}" target="_blank" rel="noopener">${t('join')}</a>`
            : `<small> ${htmlEsc(s.location)}</small>`) : ''}
        </div>
        ${s.notes ? `<p class="text-muted" style="font-size:12px;margin-top:4px">${htmlEsc(s.notes)}</p>` : ''}
      </div>
      <div class="session-actions">
        ${isVirtual && s.location && !past
          ? `<a href="${htmlEsc(s.location)}" target="_blank" rel="noopener" class="btn btn-sm btn-primary">${t('join')}</a>` : ''}
        ${canManage ? `<button class="btn btn-sm btn-danger" onclick="deleteSession(${s.id},${s.course_id||0})">${t('delete')}</button>` : ''}
      </div>
    </div>`;
}

// ═══════════════════════════════════════════════════════════
// Material helpers
// ═══════════════════════════════════════════════════════════
function fileMimeIcon(mime) {
  if (!mime) return '';
  if (mime.startsWith('image/')) return '';
  if (mime.startsWith('video/')) return '';
  if (mime.startsWith('audio/')) return '';
  if (mime === 'application/pdf') return '';
  if (mime.includes('word') || mime.includes('msword') || mime.includes('document')) return '';
  if (mime.includes('excel') || mime.includes('spreadsheet') || mime.includes('sheet')) return '';
  if (mime.includes('powerpoint') || mime.includes('presentation')) return '';
  if (mime.includes('zip') || mime.includes('compressed') || mime.includes('archive') || mime.includes('tar')) return '';
  if (mime.startsWith('text/')) return '';
  return '';
}

function getYouTubeId(url) {
  if (!url) return null;
  try {
    const u = new URL(url);
    if (u.hostname === 'youtu.be') return u.pathname.slice(1).split('?')[0] || null;
    if (u.hostname.includes('youtube.com')) {
      if (u.pathname.startsWith('/embed/')) return u.pathname.split('/')[2] || null;
      return u.searchParams.get('v') || null;
    }
  } catch (_) {}
  return null;
}

// YouTube IFrame API — loaded once, players registered after API ready
window._ytApiLoaded = false;
window._ytApiReady = false;
window._ytPendingPlayers = []; // [{iframeId, courseId, matId}]

window.onYouTubeIframeAPIReady = function() {
  window._ytApiReady = true;
  window._ytPendingPlayers.forEach(p => _initYTPlayer(p.iframeId, p.courseId, p.matId));
  window._ytPendingPlayers = [];
};

function _loadYTApi() {
  if (window._ytApiLoaded) return;
  window._ytApiLoaded = true;
  const s = document.createElement('script');
  s.src = 'https://www.youtube.com/iframe_api';
  document.head.appendChild(s);
}

function _initYTPlayer(iframeId, courseId, matId) {
  let marked = false;
  function markDone() {
    if (marked) return;
    marked = true;
    completeMaterial(courseId, matId);
  }
  const player = new YT.Player(iframeId, {
    events: {
      onStateChange(e) {
        if (e.data === YT.PlayerState.ENDED) { markDone(); return; }
        // PAUSED (2): if seeked to within last 10 s, treat as done
        if (e.data === 2) {
          const dur = player.getDuration ? player.getDuration() : 0;
          const cur = player.getCurrentTime ? player.getCurrentTime() : 0;
          if (dur > 0 && (dur - cur) <= 10) markDone();
        }
      }
    }
  });
}

function attachYTPlayer(iframeId, courseId, matId) {
  _loadYTApi();
  if (window._ytApiReady) {
    _initYTPlayer(iframeId, courseId, matId);
  } else {
    window._ytPendingPlayers.push({iframeId, courseId, matId});
  }
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

  // Auto-mark complete for students when they open/view the material
  if (state.user && state.user.role === 'student') {
    const item = document.getElementById(`mat-item-${materialId}`);
    if (item && item.dataset.completed === '0') completeMaterial(courseId, materialId);
  }

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
    const icon = isVideo ? '' : '';
    openModal(`${icon} ${fileName || 'Media'}`,
      `<div style="text-align:center;padding:8px 0">
        <${tag} controls
          style="max-width:100%;max-height:60vh;border-radius:8px;background:#000"
          onloadstart="this.muted=false;this.volume=1.0"
          src="${fileUrl}">
          Your browser does not support this media type.
        </${tag}>
      </div>`
    );
  } else if (isPdf) {
    // Fetch the PDF with auth headers and render via a blob URL so the iframe
    // never tries to load from localhost directly (which browsers may refuse).
    openModal(` ${htmlEsc(fileName || 'Document')}`,
      `<div style="display:flex;flex-direction:column;align-items:center;gap:10px;padding:4px 0">
        <div id="pdf-frame-wrap" style="width:100%;height:70vh;border-radius:6px;background:#f5f5f5;display:flex;align-items:center;justify-content:center">
          <span class="text-muted">Loading…</span>
        </div>
        <a class="btn btn-sm btn-primary" id="pdf-dl-link" href="#"> Download PDF</a>
      </div>`,
      {wide: true}
    );
    fetch(`/api/courses/${courseId}/materials/${materialId}/file`, {
      headers: { Authorization: `Bearer ${state.token}` }
    }).then(r => r.blob()).then(blob => {
      const url = URL.createObjectURL(blob);
      const wrap = document.getElementById('pdf-frame-wrap');
      if (wrap) wrap.innerHTML = `<iframe src="${url}" style="width:100%;height:70vh;border:none;border-radius:6px"></iframe>`;
      const dl = document.getElementById('pdf-dl-link');
      if (dl) { dl.href = url; dl.download = fileName || 'document.pdf'; }
    }).catch(() => {
      const wrap = document.getElementById('pdf-frame-wrap');
      if (wrap) wrap.innerHTML = `<p class="text-muted">Could not load PDF.</p>`;
    });
  } else if (isImage) {
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
async function openAddMaterialModal(courseId) {
  openModal(t('add_material'), `
    <div class="mat-mode-tabs">
      <button type="button" class="mat-mode-tab active" onclick="switchMatMode('link',this)"> ${t('link_text')}</button>
      <button type="button" class="mat-mode-tab" onclick="switchMatMode('file',this)"> ${t('upload_file')}</button>
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
  if (!await showConfirm(t('delete')+'?')) return;
  try { await api('DELETE',`/courses/${courseId}/materials/${matId}`); toast(t('delete')); navigate('course',{id:courseId}); }
  catch(err) { toast(err.message,'error'); }
}

async function openEditMaterialModal(courseId, matId, mat) {
  openModal(' Edit Material', `
    <form id="edit-mat-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" value="${htmlEsc(mat.title)}" required></div>
      ${mat.material_type === 'link' ? `
      <div class="form-group"><label>URL</label>
        <input name="url" type="url" class="form-control" value="${htmlEsc(mat.url)}"></div>` : ''}
      <div class="form-group"><label>${t('description') || 'Description'}</label>
        <textarea name="content" class="form-control" rows="3">${htmlEsc(mat.content)}</textarea></div>
      <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
        <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" class="btn btn-primary">Save</button>
      </div>
    </form>
  `);
  document.getElementById('edit-mat-form').onsubmit = async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const payload = {
      title: fd.get('title'),
      content: fd.get('content') || null,
      url: fd.get('url') || null,
    };
    try {
      await api('PUT', `/courses/${courseId}/materials/${matId}`, payload);
      toast('Material updated.');
      closeModal();
      navigate('course', { id: courseId });
    } catch(err) { toast(err.message, 'error'); }
  };
}

async function completeMaterial(courseId, matId) {
  try {
    await api('POST', `/courses/${courseId}/materials/${matId}/complete`);
    const item = document.getElementById(`mat-item-${matId}`);
    if (item) {
      item.dataset.completed = '1';
      const titleRow = item.querySelector('.material-title');
      if (titleRow && !document.getElementById(`mat-done-${matId}`)) {
        const span = document.createElement('span');
        span.id = `mat-done-${matId}`;
        span.className = 'badge badge-success';
        span.textContent = ` ${t('completed')}`;
        titleRow.appendChild(span);
      }
    }
    // Re-fetch quizzes tab to reflect newly unlocked assessments
    const quizzesTab = document.getElementById('tab-quizzes');
    if (quizzesTab && !quizzesTab.classList.contains('hidden')) {
      navigate('course', { id: courseId });
    }
  } catch(_) {}
}

// ═══════════════════════════════════════════════════════════
// Assignments
// ═══════════════════════════════════════════════════════════
function openNewAssignmentModal(courseId) {
  openModal(t('new_assignment'), `
    <div class="tabs" style="margin-bottom:16px">
      <button class="tab active" id="asgn-tab-manual" onclick="asgnSwitchTab('manual')">${t('manual')}</button>
      <button class="tab" id="asgn-tab-ai" onclick="asgnSwitchTab('ai')"> ${t('ai_generate')}</button>
    </div>

    <form id="modal-form">
      <!-- Manual tab -->
      <div id="asgn-pane-manual">
        <div class="form-group"><label>${t('title_label')} *</label>
          <input name="title" class="form-control" required></div>
        <div class="form-group"><label>${t('instructions')}</label>
          <textarea name="description" class="form-control" rows="4"></textarea></div>
        <div class="form-group"><label>${t('max_score')}</label>
          <input name="max_score" type="number" class="form-control" value="100" min="1"></div>
        <div class="form-group"><label>${t('due_date')}</label>
          ${dueDatePicker('asgn-due', '')}</div>
      </div>

      <!-- AI Generate tab -->
      <div id="asgn-pane-ai" class="hidden">
        <div class="form-group">
          <label>Topic *<span class="text-muted" style="font-weight:normal;margin-left:6px">e.g. "Adding Fractions", "The Water Cycle"</span></label>
          <input name="ai_topic" class="form-control" placeholder="Enter the topic to generate questions about">
        </div>
        <div class="form-group"><label>Number of questions</label>
          <input name="ai_num_q" type="number" class="form-control" value="4" min="1" max="10"></div>
        <div class="form-group"><label>${t('max_score')}</label>
          <input name="ai_max_score" type="number" class="form-control" value="100" min="1"></div>
        <div class="form-group"><label>${t('due_date')}</label>
          ${dueDatePicker('asgn-ai-due', '')}</div>
        <div id="asgn-ai-status" class="hidden" style="margin-bottom:8px">
          <span class="text-muted"> Generating…</span>
        </div>
      </div>

      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary" id="asgn-submit-btn">${t('create')}</button>
      </div>
    </form>`,
    async (fd) => {
      const mode = document.getElementById('asgn-tab-ai').classList.contains('active') ? 'ai' : 'manual';
      if (mode === 'ai') {
        const topic = (fd.get('ai_topic') || '').trim();
        if (!topic) { toast('Please enter a topic.', 'error'); return; }
        const btn = document.getElementById('asgn-submit-btn');
        const status = document.getElementById('asgn-ai-status');
        btn.disabled = true; btn.textContent = 'Generating…';
        status.classList.remove('hidden');
        try {
          await api('POST', `/assignments/course/${courseId}/generate`, {
            topic,
            num_questions: parseInt(fd.get('ai_num_q')) || 4,
            max_score: parseFloat(fd.get('ai_max_score')) || 100,
            due_date: fd.get('due_date') || null,
          });
          closeModal(); toast('Assignment generated!'); navigate('course', {id: courseId});
        } catch(err) { toast(err.message, 'error'); btn.disabled = false; btn.textContent = t('create'); status.classList.add('hidden'); }
      } else {
        try {
          await api('POST', `/assignments/course/${courseId}`,
            { title: fd.get('title'), description: fd.get('description') || null,
              due_date: fd.get('due_date') || null, max_score: parseFloat(fd.get('max_score')) || 100 });
          closeModal(); toast(t('create') + '!'); navigate('course', {id: courseId});
        } catch(err) { toast(err.message, 'error'); }
      }
    });
}

function asgnSwitchTab(tab) {
  document.getElementById('asgn-tab-manual').classList.toggle('active', tab === 'manual');
  document.getElementById('asgn-tab-ai').classList.toggle('active', tab === 'ai');
  document.getElementById('asgn-pane-manual').classList.toggle('hidden', tab !== 'manual');
  document.getElementById('asgn-pane-ai').classList.toggle('hidden', tab !== 'ai');
  const manualTitle = document.querySelector('#asgn-pane-manual input[name="title"]');
  if (manualTitle) manualTitle.required = (tab === 'manual');
}

async function openEditAssignmentModal(assignmentId, courseId) {
  let a;
  try { a = await api('GET', `/assignments/${assignmentId}`); } catch(err) { toast(err.message, 'error'); return; }
  openModal('Edit Assignment', `
    <form id="modal-form">
      <div class="form-group"><label>${t('title_label')} *</label>
        <input name="title" class="form-control" value="${htmlEsc(a.title)}" required></div>
      <div class="form-group"><label>${t('instructions')}</label>
        <textarea name="description" class="form-control" rows="6">${htmlEsc(a.description || '')}</textarea></div>
      <div class="form-group"><label>${t('max_score')}</label>
        <input name="max_score" type="number" class="form-control" value="${a.max_score}" min="1"></div>
      <div class="form-group"><label>${t('due_date')}</label>
        ${dueDatePicker('edit-asgn-due', a.due_date ? fmtDateTimeLocal(a.due_date) : '')}</div>
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="submit" class="btn btn-primary">${t('save')}</button>
      </div>
    </form>`,
    async (fd) => {
      try {
        await api('PUT', `/assignments/${assignmentId}`, {
          title: fd.get('title'),
          description: fd.get('description') || null,
          due_date: fd.get('due_date') || null,
          max_score: parseFloat(fd.get('max_score')) || 100,
          late_penalty_per_day: a.late_penalty_per_day || 0,
          max_late_days: a.max_late_days || null,
          allow_resubmission: a.allow_resubmission || false,
          max_submissions: a.max_submissions || 1,
        });
        closeModal();
        toast('Assignment updated!');
        navigate('assignment', { id: assignmentId });
      } catch(err) { toast(err.message, 'error'); }
    });
}

async function deleteAssignment(assignmentId, courseId) {
  if (!await showConfirm('Delete this assignment? This will also remove all student submissions and cannot be undone.')) return;
  try {
    await api('DELETE', `/assignments/${assignmentId}`);
    toast('Assignment deleted.');
    navigate('course', { id: courseId });
  } catch(err) { toast(err.message, 'error'); }
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
          <h2>${htmlEsc(a.title)}</h2>
        </div>
        <div style="text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:6px">
          ${a.due_date ? `<small class="text-muted">${t('due_date')}: ${fmtDateTime(a.due_date)}</small>` : ''}
          <small class="text-muted">${t('max_score')}: ${a.max_score} ${t('pts')}</small>
          ${canGrade ? `<div style="display:flex;gap:6px">
            <button class="btn btn-sm btn-secondary" onclick="openEditAssignmentModal(${a.id},${a.course_id})"> Edit Assignment</button>
            <button class="btn btn-sm btn-danger" onclick="deleteAssignment(${a.id},${a.course_id})"> Delete</button>
          </div>` : ''}
        </div>
      </div>
      ${a.description ? `<div class="card"><div class="card-header"><h3>${t('instructions')}</h3></div>
        <div class="card-body"><p style="white-space:pre-wrap">${htmlEsc(a.description)}</p></div></div>` : ''}
      ${!canGrade ? `
        <div class="card"><div class="card-header">
          <h3>${a.my_submission ? t('your_submission') : t('submit_assignment')}</h3></div>
          <div class="card-body">
            ${a.my_submission ? `
              <div style="margin-bottom:12px">
                ${a.my_submission.content ? `<div class="submission-content"><p>${htmlEsc(a.my_submission.content)}</p></div>` : ''}
                ${a.my_submission.file_name ? `
                  <div class="submission-file">
                    <span> ${htmlEsc(a.my_submission.file_name)}</span>
                    <a class="btn btn-sm" href="/api/assignments/submissions/${a.my_submission.id}/file?dl_token=${encodeURIComponent(state.token)}"
                       download="${htmlEsc(a.my_submission.file_name)}"> Download</a>
                  </div>` : ''}
                <small class="text-muted">${fmtDateTime(a.my_submission.submitted_at)}</small>
                ${a.my_submission.score!=null
                  ? `<div class="grade-result mt-8"><strong>${t('score')}: ${a.my_submission.score} / ${a.max_score}</strong>
                      ${a.my_submission.feedback?`<p>${a.my_submission.feedback}</p>`:''}</div>`
                  : `<p class="text-muted mt-8">${t('not_graded')}</p>`}
              </div>
              <button class="btn btn-sm" onclick="document.getElementById('sub-area').classList.toggle('hidden')">${t('edit_resubmit')}</button>
              <div id="sub-area" class="hidden" style="margin-top:14px">` : `<div id="sub-area">`}
            <div class="form-group" style="margin-top:${a.my_submission?'12px':'0'}">
              <label>Written response <span class="text-muted">(optional)</span></label>
              <textarea id="sub-content" class="form-control" rows="6">${htmlEsc(a.my_submission ? a.my_submission.content : '')}</textarea>
            </div>
            <div class="form-group">
              <label>Attach a file <span class="text-muted">(optional — any type, max 200 MB)</span></label>
              <input id="sub-file" type="file" class="form-control" accept="*/*">
            </div>
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
                  <strong>${htmlEsc(s.student_name)}</strong>
                  <small class="text-muted">${fmtDateTime(s.submitted_at)}</small>
                  ${s.score!=null ? `<span class="badge badge-success">${s.score}/${a.max_score}</span>`
                                  : `<span class="badge badge-warning">${t('not_graded')}</span>`}
                </div>
                ${s.content ? `<div class="submission-content"><p>${htmlEsc(s.content)}</p></div>` : ''}
                ${s.file_name ? `
                  <div class="submission-file">
                    <span> ${htmlEsc(s.file_name)}</span>
                    <a class="btn btn-sm" href="/api/assignments/submissions/${s.id}/file?dl_token=${encodeURIComponent(state.token)}"
                       download="${htmlEsc(s.file_name)}"> Download</a>
                  </div>` : ''}
                <div class="grade-form">
                  <div class="form-row">
                    <div class="form-group"><label>${t('score')} (max ${a.max_score})</label>
                      <input type="number" id="score-${s.id}" class="form-control" value="${s.score??''}" min="0" max="${a.max_score}" step="0.5"></div>
                    <div class="form-group" style="flex:2"><label>${t('feedback')}</label>
                      <input type="text" id="fb-${s.id}" class="form-control" value="${htmlEsc(s.feedback??'')}"></div>
                  </div>
                  <button class="btn btn-sm btn-primary" onclick="gradeSubmission(${s.id},${assignmentId})">${t('save_grade')}</button>
                </div>
              </div>`).join('') : `<p class="text-muted">${t('no_submissions')}</p>`}
          </div>
        </div>`}`;
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

async function submitAssignment(id) {
  const content = document.getElementById('sub-content')?.value.trim() || '';
  const fileInput = document.getElementById('sub-file');
  const file = fileInput?.files?.[0];
  if (!content && !file) { toast('Please add text or attach a file.', 'error'); return; }
  try {
    const fd = new FormData();
    fd.append('content', content);
    if (file) fd.append('file', file);
    const res = await fetch(`/api/assignments/${id}/submit`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${state.token}` },
      body: fd,
    });
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail || 'Error'); }
    toast(t('submit_assignment') + '!');
    navigate('assignment', {id});
    setTimeout(() => showPostSubmitModal(id), 400);
  } catch(err) { toast(err.message, 'error'); }
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
          <div class="post-submit-trophy"></div>
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
              ? `${t('due_date')}: <strong class="${isOverdue?'text-danger':''}">${fmtDate(a.due_date)}</strong>${isOverdue?' ':''}`
              : '';
            return `
              <div class="outstanding-item">
                <div class="outstanding-info">
                  <span class="outstanding-title">${htmlEsc(a.title)}</span>
                  <span class="outstanding-course"> ${htmlEsc(a.course_title)}</span>
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
          <option value="virtual"> ${t('virtual')}</option>
          <option value="physical"> ${t('physical')}</option>
        </select>
      </div>
      <div class="form-group"><label> Date &amp; Time *</label>
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
  if (!await showConfirm(t('delete')+'?')) return;
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
        <input name="title" class="form-control" required placeholder="e.g. Chapter 2 Assessment"></div>
      <div class="form-group"><label>${t('description')}</label>
        <textarea name="description" class="form-control" rows="3"></textarea></div>
      <div class="form-group"><label>${t('time_limit')} <small class="text-muted">(0 = none)</small></label>
        <input name="time_limit" type="number" class="form-control" value="0" min="0"></div>
      <div class="form-group"><label>${t('due_date')}</label>
        ${dueDatePicker('quiz-due', '')}</div>
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
        openAIGenerateModal(res.id, courseId, true);
      } catch(err) { toast(err.message,'error'); }
    });
}

async function deleteQuiz(quizId, courseId) {
  if (!await showConfirm(t('delete')+'?')) return;
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
      ? `<span class="badge badge-success"> ${t('quiz_published')}</span>`
      : `<span class="badge badge-warning"> ${t('quiz_draft')}</span>`;
    const examBadge = quiz.is_exam ? `<span class="exam-badge">EXAM</span>` : '';
    const unlockBadge = quiz.unlock_all_materials ? `<span class="badge badge-info" style="font-size:11px"> ${t('unlock_after_all_materials')}</span>` : '';
    el.innerHTML = `
      <div class="page-header">
        <div>
          <button class="btn btn-sm" onclick="navigate('course',{id:${quiz.course_id}})" style="margin-bottom:8px">${t('back')}</button>
          <h2>${t('quiz_builder')}: ${htmlEsc(quiz.title)}</h2>
          <div style="display:flex;gap:8px;margin-top:6px;align-items:center;flex-wrap:wrap">
            ${pubBadge}${examBadge}${unlockBadge}
            <small class="text-muted">${quiz.question_count} ${t('question_text')}(s) &bull; ${quiz.total_points} ${t('pts')}${quiz.time_limit ? ` &bull; ${quiz.time_limit} ${t('minutes')}` : ''}</small>
          </div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <button class="btn btn-sm" onclick="openEditQuizModal(${quizId})">${t('edit_quiz')}</button>
          <button class="btn btn-sm ${quiz.is_published ? 'btn-warning' : 'btn-success'}"
            onclick="togglePublishQuiz(${quizId},${quiz.is_published},${quiz.course_id})">
            ${quiz.is_published ? t('unpublish_quiz') : t('publish_quiz')}
          </button>
          <button class="btn btn-sm btn-info" onclick="openAIGenerateModal(${quizId},${quiz.course_id})">${t('ai_generate')}</button>
          <button class="btn btn-primary" onclick="openAddQuestionModal(${quizId})">${t('add_question')}</button>
        </div>
      </div>
      ${!quiz.is_published ? `
        <div class="alert alert-warning" style="margin-bottom:16px">
           ${t('quiz_draft')} — ${t('publish_quiz').toLowerCase()} when you\'re ready for students to see it.
        </div>` : ''}
      <div id="question-list">
        ${quiz.questions.length ? quiz.questions.map((q,i)=>questionBuilderCard(q,i,quizId)).join('')
                                : `<div class="card"><div class="card-body"><p class="text-muted">No questions yet — click "${t('add_question')}" to get started.</p></div></div>`}
      </div>
      <div id="attempts-section" style="margin-top:28px"></div>`;

    // Load attempts asynchronously
    const attemptsEl = el.querySelector('#attempts-section');
    try {
      const attempts = await api('GET', `/quizzes/${quizId}/attempts`);
      if (!attempts.length) { attemptsEl.innerHTML = ''; return; }
      const needsGrading = attempts.filter(a => a.needs_grading);
      attemptsEl.innerHTML = `
        <h3 style="margin-bottom:12px"> Student Submissions
          ${needsGrading.length ? `<span class="badge badge-warning" style="font-size:12px;margin-left:8px">${needsGrading.length} ${t('needs_grading')}</span>` : ''}
        </h3>
        <div style="overflow-x:auto">
        <table class="data-table">
          <thead><tr>
            <th>${t('name')}</th><th>Submitted</th><th>Score</th><th>Status</th><th></th>
          </tr></thead>
          <tbody>
          ${attempts.map(a => {
            const submitted = a.submitted_at ? fmtDate(a.submitted_at) : '—';
            const score = a.score != null ? `${a.score} / ${a.total_possible}` : '—';
            const status = !a.submitted_at
              ? `<span class="badge">In Progress</span>`
              : a.needs_grading
                ? `<span class="badge badge-warning"> ${t('needs_grading')}</span>`
                : `<span class="badge badge-success"> Graded</span>`;
            const gradeBtn = a.submitted_at
              ? `<button class="btn btn-sm btn-primary" onclick="openGradingPanel(${quizId},${a.id})">${t('grade_responses')}</button>`
              : '';
            return `<tr>
              <td>${htmlEsc(a.student_name)}</td>
              <td>${submitted}</td>
              <td>${score}</td>
              <td>${status}</td>
              <td>${gradeBtn}</td>
            </tr>`;
          }).join('')}
          </tbody>
        </table></div>`;
    } catch(_) {}
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
      <div class="form-group"><label>${t('time_limit')} <small class="text-muted">(0 = ${t('no')} limit)</small></label>
        <input name="time_limit" type="number" class="form-control" value="${quiz.time_limit||0}" min="0"></div>
      <div class="form-group"><label>${t('due_date')}</label>
        ${dueDatePicker('quiz-edit-due', dueFmt)}</div>
      <div class="form-group"><label>${t('max_attempts')} <small class="text-muted">(0 = ${t('unlimited')})</small></label>
        <input name="max_attempts" type="number" class="form-control" value="${quiz.max_attempts||0}" min="0"></div>
      <div class="form-group" style="display:flex;align-items:center;gap:10px;padding:10px 0">
        <input type="checkbox" name="is_exam" id="chk-is-exam" value="1"${quiz.is_exam?' checked':''} style="width:18px;height:18px;accent-color:var(--danger);flex-shrink:0">
        <label for="chk-is-exam" style="font-size:13px;font-weight:600;color:var(--text);cursor:pointer;margin:0">
           ${t('is_exam')}
        </label>
      </div>
      <div class="form-group" style="display:flex;align-items:center;gap:10px;padding:10px 0">
        <input type="checkbox" name="unlock_all_materials" id="chk-unlock-all" value="1"${quiz.unlock_all_materials?' checked':''} style="width:18px;height:18px;accent-color:var(--info);flex-shrink:0">
        <label for="chk-unlock-all" style="font-size:13px;font-weight:600;color:var(--text);cursor:pointer;margin:0">
           ${t('unlock_after_all_materials')}
        </label>
      </div>
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
          max_attempts: ma,
          is_exam: !!fd.get('is_exam'),
          unlock_all_materials: !!fd.get('unlock_all_materials'),
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
    toast(!isPublished ? ' ' + t('publish_quiz') : t('unpublish_quiz'));
    if (state.currentPage === 'quiz-builder') {
      navigate('quiz-builder', {id: quizId});
    } else {
      navigate('course', {id: courseId});
    }
  } catch(err) { toast(err.message, 'error'); }
}

function questionBuilderCard(q, idx, quizId) {
  const typeLabel = { multiple_choice: t('multiple_choice'), true_false: t('true_false'), short_answer: t('short_answer'), long_answer: t('long_answer') };
  return `
    <div class="question-card">
      <div class="question-card-header">
        <div>
          <span class="text-muted" style="font-size:11px;text-transform:uppercase">${t('q_num')} ${idx+1} &bull; ${typeLabel[q.question_type]||q.question_type} &bull; ${fmtPts(q.points)} ${t('pts')}</span>
          <strong style="display:block;margin-top:2px">${htmlEsc(q.question_text)}</strong>
        </div>
        <button class="btn btn-sm btn-danger" onclick="deleteQuestion(${q.id},${quizId})">${t('delete')}</button>
      </div>
      ${q.options.length ? `<div class="question-options">
        ${q.options.map(o=>`
          <div class="option-row${o.is_correct?' correct':''}">
            <span>${o.is_correct ? '' : ''}</span> ${htmlEsc(o.option_text)}
          </div>`).join('')}
      </div>` : `<p class="text-muted" style="font-size:12px;margin-top:4px">${q.question_type === 'long_answer' ? t('long_manual') : t('short_manual')}</p>`}
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
          <option value="long_answer">${t('long_answer')}</option>
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
  } else if (type === 'long_answer') {
    area.innerHTML = `<p class="text-muted" style="font-size:13px;padding:8px 0">${t('long_manual')}</p>`;
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
      <div class="form-group"><label>${t('options')} <small class="text-muted">(mark correct with )</small></label>
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
  if (!await showConfirm(t('delete')+'?')) return;
  try { await api('DELETE',`/quizzes/questions/${questionId}`); toast(t('delete')); navigate('quiz-builder',{id:quizId}); }
  catch(err) { toast(err.message,'error'); }
}

// ── AI Question Generator (with Manual tab) ──────────────────────────────────
async function openAIGenerateModal(quizId, courseId, autoOpen) {
  let materials = [];
  try { materials = await api('GET', `/courses/${courseId}/materials`); } catch(_) {}

  const closeAction = autoOpen
    ? `closeModal();navigate('quiz-builder',{id:${quizId}})`
    : `closeModal()`;

  openModal(t('ai_generate_title'), `
    <div>
      <!-- Tab bar -->
      <div style="display:flex;gap:0;margin-bottom:16px;border-bottom:2px solid var(--border)">
        <button type="button" id="tab-ai-btn"
          style="padding:8px 18px;border:none;background:none;cursor:pointer;font-weight:600;font-size:13px;color:var(--accent);border-bottom:2px solid var(--accent);margin-bottom:-2px"
          onclick="switchQTab('ai')">${t('tab_ai_gen')}</button>
        <button type="button" id="tab-manual-btn"
          style="padding:8px 18px;border:none;background:none;cursor:pointer;font-weight:600;font-size:13px;color:var(--muted);border-bottom:2px solid transparent;margin-bottom:-2px"
          onclick="switchQTab('manual')">${t('tab_manual')}</button>
      </div>

      <!-- AI tab -->
      <div id="tab-ai-panel">
        <div style="display:flex;gap:8px;margin-bottom:8px">
          <button type="button" class="btn btn-sm" onclick="aiSelectAll(true)">${t('select_all')}</button>
          <button type="button" class="btn btn-sm" onclick="aiSelectAll(false)">${t('deselect_all')}</button>
        </div>
        <div id="ai-mat-list" style="max-height:180px;overflow-y:auto;border:1px solid var(--border);border-radius:var(--radius);padding:8px;margin-bottom:14px">
          ${materials.length ? materials.map(m=>`
            <label style="display:flex;align-items:center;gap:8px;padding:5px 4px;cursor:pointer">
              <input type="checkbox" class="ai-mat-cb" value="${m.id}" ${autoOpen?'checked':''} style="width:15px;height:15px">
              <span style="font-size:13px">${htmlEsc(m.title)}</span>
              <span class="badge badge-info" style="font-size:10px">${m.material_type||'text'}</span>
            </label>`).join('') : `<p class="text-muted" style="font-size:13px">No materials in this course yet.</p>`}
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">
          <div class="form-group" style="margin:0">
            <label style="font-size:12px">${t('num_mc')}</label>
            <input id="ai-num-mc" type="number" class="form-control" value="5" min="0" max="20">
          </div>
          <div class="form-group" style="margin:0">
            <label style="font-size:12px">${t('num_tf')}</label>
            <input id="ai-num-tf" type="number" class="form-control" value="3" min="0" max="20">
          </div>
          <div class="form-group" style="margin:0">
            <label style="font-size:12px">${t('num_short')}</label>
            <input id="ai-num-short" type="number" class="form-control" value="2" min="0" max="10">
          </div>
          <div class="form-group" style="margin:0">
            <label style="font-size:12px">${t('num_long')}</label>
            <input id="ai-num-long" type="number" class="form-control" value="1" min="0" max="5">
          </div>
        </div>
        <p id="ai-gen-hint" style="display:none;color:var(--muted);font-size:12px;margin-bottom:8px">
           This may take a few minutes — please wait…
        </p>
        <div class="form-actions">
          <button type="button" class="btn" onclick="${closeAction}">${t('cancel')}</button>
          <button type="button" class="btn btn-primary" id="ai-gen-btn" onclick="runAIGenerate(${quizId})">${t('ai_generate')}</button>
        </div>
      </div>

      <!-- Manual tab -->
      <div id="tab-manual-panel" style="display:none">
        <div class="form-group">
          <label>${t('question_type')} *</label>
          <select id="mq-type" class="form-control" onchange="updateManualQUI()">
            <option value="multiple_choice">${t('multiple_choice')}</option>
            <option value="true_false">${t('true_false')}</option>
            <option value="short_answer">${t('short_answer')}</option>
            <option value="long_answer">${t('long_answer')}</option>
          </select>
        </div>
        <div class="form-group">
          <label>${t('question_text')} *</label>
          <textarea id="mq-text" class="form-control" rows="3"></textarea>
        </div>
        <div class="form-group">
          <label>${t('points')}</label>
          <input id="mq-pts" type="number" class="form-control" value="1" min="0.5" step="0.5">
        </div>
        <div id="mq-options-area"></div>
        <div class="form-actions">
          <button type="button" class="btn" onclick="${closeAction}">${t('cancel')}</button>
          <button type="button" class="btn btn-primary" onclick="submitManualQuestion(${quizId})">${t('add')}</button>
        </div>
      </div>
    </div>`);

  // Reset option counter and initialise manual options UI after DOM is ready
  window._mqOptCount = 4;
  setTimeout(updateManualQUI, 0);
}

function switchQTab(tab) {
  const isAI = tab === 'ai';
  document.getElementById('tab-ai-panel').style.display  = isAI ? '' : 'none';
  document.getElementById('tab-manual-panel').style.display = isAI ? 'none' : '';
  const aiBtn  = document.getElementById('tab-ai-btn');
  const manBtn = document.getElementById('tab-manual-btn');
  if (aiBtn)  { aiBtn.style.color  = isAI ? 'var(--accent)' : 'var(--muted)';  aiBtn.style.borderBottomColor  = isAI ? 'var(--accent)' : 'transparent'; }
  if (manBtn) { manBtn.style.color = isAI ? 'var(--muted)'  : 'var(--accent)'; manBtn.style.borderBottomColor = isAI ? 'transparent' : 'var(--accent)'; }
}

function updateManualQUI() {
  const type = document.getElementById('mq-type')?.value;
  const area = document.getElementById('mq-options-area');
  if (!area) return;
  if (type === 'short_answer') {
    area.innerHTML = `<p class="text-muted" style="font-size:13px;padding:6px 0">${t('short_manual')}</p>`;
  } else if (type === 'long_answer') {
    area.innerHTML = `<p class="text-muted" style="font-size:13px;padding:6px 0">${t('long_manual')}</p>`;
  } else if (type === 'true_false') {
    area.innerHTML = `
      <div class="form-group"><label>${t('correct_answer')}</label>
        <div class="tf-options">
          <label><input type="radio" name="mq-tf" value="0" checked> True</label>
          <label><input type="radio" name="mq-tf" value="1"> False</label>
        </div>
      </div>`;
  } else {
    // Multiple choice — start with 4 options, allow adding more
    area.innerHTML = `
      <div class="form-group">
        <label style="margin-bottom:6px">${t('options')} <small class="text-muted">(select correct)</small></label>
        <div id="mq-mc-opts">
          ${[0,1,2,3].map(i=>`
            <div class="mc-option" id="mq-opt-row-${i}">
              <input type="radio" name="mq-mc-correct" value="${i}">
              <input type="text" id="mq-mc-opt-${i}" class="form-control" placeholder="${t('options')} ${i+1}">
            </div>`).join('')}
        </div>
        <button type="button" class="btn btn-sm" style="margin-top:6px" onclick="addManualMCOption()">${t('add_option')}</button>
      </div>`;
  }
}

function addManualMCOption() {
  const container = document.getElementById('mq-mc-opts');
  if (!container) return;
  window._mqOptCount = (window._mqOptCount || 4);
  const i = window._mqOptCount++;
  const div = document.createElement('div');
  div.className = 'mc-option';
  div.id = `mq-opt-row-${i}`;
  div.innerHTML = `
    <input type="radio" name="mq-mc-correct" value="${i}">
    <input type="text" id="mq-mc-opt-${i}" class="form-control" placeholder="${t('options')} ${i+1}">`;
  container.appendChild(div);
}

async function submitManualQuestion(quizId) {
  const type = document.getElementById('mq-type').value;
  const text = (document.getElementById('mq-text')?.value || '').trim();
  const pts  = parseFloat(document.getElementById('mq-pts')?.value) || 1;
  if (!text) { toast(t('question_text') + ' required', 'error'); return; }

  let options = [];
  if (type === 'true_false') {
    const correct = document.querySelector('input[name="mq-tf"]:checked')?.value || '0';
    options = [
      { option_text: 'True',  is_correct: correct === '0' },
      { option_text: 'False', is_correct: correct === '1' },
    ];
  } else if (type === 'multiple_choice') {
    const correct = document.querySelector('input[name="mq-mc-correct"]:checked')?.value;
    // Collect all rendered option rows
    const rows = document.querySelectorAll('#mq-mc-opts .mc-option');
    rows.forEach((row, idx) => {
      const input = row.querySelector('input[type="text"]');
      const val   = input?.value.trim();
      if (val) options.push({ option_text: val, is_correct: String(idx) === correct });
    });
    if (options.length < 2) { toast('Add at least 2 options', 'error'); return; }
    if (correct === undefined || correct === null || !options.some(o => o.is_correct)) {
      toast('Select the correct option', 'error'); return;
    }
  }

  try {
    await api('POST', `/quizzes/${quizId}/questions`, { question_text: text, question_type: type, points: pts, options });
    closeModal();
    toast(t('add') + '!');
    navigate('quiz-builder', { id: quizId });
  } catch(err) { toast(err.message, 'error'); }
}

function aiSelectAll(checked) {
  document.querySelectorAll('.ai-mat-cb').forEach(cb => cb.checked = checked);
}

async function runAIGenerate(quizId) {
  const ids = [...document.querySelectorAll('.ai-mat-cb:checked')].map(cb => parseInt(cb.value));
  if (!ids.length) { toast(t('select_materials'), 'error'); return; }
  const btn = document.getElementById('ai-gen-btn');
  if (btn) { btn.disabled = true; btn.textContent = t('generating'); }
  const hint = document.getElementById('ai-gen-hint');
  if (hint) hint.style.display = 'block';
  try {
    const res = await api('POST', `/quizzes/${quizId}/ai-generate`, {
      material_ids: ids,
      num_mc: parseInt(document.getElementById('ai-num-mc').value) || 0,
      num_tf: parseInt(document.getElementById('ai-num-tf').value) || 0,
      num_short: parseInt(document.getElementById('ai-num-short').value) || 0,
      num_long: parseInt(document.getElementById('ai-num-long').value) || 0,
    });
    closeModal();
    toast(`${t('ai_generated_ok')} (${res.created} questions)`);
    navigate('quiz-builder', {id: quizId});
  } catch(err) {
    toast(err.message, 'error');
    if (btn) { btn.disabled = false; btn.textContent = t('ai_generate'); }
  }
}

// ── Teacher grading panel for long/short answers ─────────────────────────────
async function openGradingPanel(quizId, attemptId) {
  let data;
  try { data = await api('GET', `/quizzes/${quizId}/attempt/${attemptId}/long-answers`); }
  catch(err) { toast(err.message, 'error'); return; }

  if (!data.answers.length) { toast('No text answers to grade.'); return; }

  openModal(`${t('grading_panel')}: ${htmlEsc(data.student_name)}`, `
    <div>
      ${data.answers.map(a => `
        <div style="margin-bottom:18px;padding-bottom:18px;border-bottom:1px solid var(--border)">
          <div style="font-size:12px;color:var(--muted);text-transform:uppercase;margin-bottom:4px">
            ${a.question_type === 'long_answer' ? t('long_answer') : t('short_answer')} &bull; max ${a.max_points} pts
          </div>
          <p style="font-weight:600;margin-bottom:6px">${htmlEsc(a.question_text)}</p>
          <div style="background:rgba(148,163,184,.08);border-radius:var(--radius);padding:10px;margin-bottom:8px;font-size:13px">
            <small style="color:var(--muted)">${t('student_answer')}:</small><br>
            ${htmlEsc(a.student_answer || '(no answer)')}
          </div>
          <div style="display:flex;gap:8px;align-items:flex-end">
            <div class="form-group" style="margin:0;flex:0 0 90px">
              <label style="font-size:12px">${t('your_score')} / ${a.max_points}</label>
              <input type="number" class="form-control grade-score-input" data-aid="${a.answer_id}"
                value="${a.teacher_score ?? ''}" min="0" max="${a.max_points}" step="0.5">
            </div>
            <div class="form-group" style="margin:0;flex:1">
              <label style="font-size:12px">${t('feedback_optional')}</label>
              <input type="text" class="form-control grade-fb-input" data-aid="${a.answer_id}"
                value="${htmlEsc(a.teacher_feedback || '')}">
            </div>
          </div>
        </div>`).join('')}
      <div class="form-actions">
        <button type="button" class="btn" onclick="closeModal()">${t('cancel')}</button>
        <button type="button" class="btn btn-primary" onclick="submitGrades(${quizId},${attemptId})">${t('save_grades')}</button>
      </div>
    </div>`);
}

async function submitGrades(quizId, attemptId) {
  const grades = [];
  document.querySelectorAll('.grade-score-input').forEach(inp => {
    const aid = parseInt(inp.dataset.aid);
    const score = parseFloat(inp.value);
    if (!isNaN(score)) {
      const fb = document.querySelector(`.grade-fb-input[data-aid="${aid}"]`)?.value || null;
      grades.push({ answer_id: aid, score, feedback: fb });
    }
  });
  if (!grades.length) { toast('Enter at least one score', 'error'); return; }
  try {
    await api('POST', `/quizzes/${quizId}/grade-attempt/${attemptId}`, { grades });
    closeModal();
    toast(t('grades_saved'));
    navigate('quiz-builder', {id: quizId});
  } catch(err) { toast(err.message, 'error'); }
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
          <strong style="margin-left:12px">${htmlEsc(quiz.title)}</strong>
        </div>
        <div style="display:flex;align-items:center;gap:12px">
          <small class="text-muted">${quiz.question_count} ${t('question_text')}(s) &bull; ${quiz.total_points} ${t('pts')}</small>
          ${timerHtml}
        </div>
      </div>
      ${quiz.questions.map((q,i) => `
        <div class="quiz-question-block">
          <div class="quiz-q-num">${t('q_num')} ${i+1} ${t('of')} ${quiz.question_count} &bull; ${fmtPts(q.points)} ${t('pts')}</div>
          <div class="quiz-q-text">${htmlEsc(q.question_text)}</div>
          ${q.question_type === 'short_answer' ? `
            <textarea class="form-control" id="sa-${q.id}" rows="4" placeholder="…"></textarea>` :
          q.question_type === 'long_answer' ? `
            <div style="font-size:12px;color:var(--muted);margin-bottom:6px"> ${t('long_manual')}</div>
            <textarea class="form-control" id="sa-${q.id}" rows="7" placeholder="Write your response here…"></textarea>` : `
            <div class="quiz-options">
              ${q.options.map(o=>`
                <div class="quiz-option">
                  <input type="radio" name="q-${q.id}" id="opt-${o.id}" value="${o.id}">
                  <label for="opt-${o.id}">${htmlEsc(o.option_text)}</label>
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
    if (q.question_type === 'short_answer' || q.question_type === 'long_answer') {
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

// ═══════════════════════════════════════════════════════════
// EXAMS LIST PAGE
// ═══════════════════════════════════════════════════════════
async function renderExams(el) {
  loading(el);
  try {
    const courses = await api('GET', '/courses/');
    if (!courses) return;
    const relevant = state.user.role === 'student'
      ? courses.filter(c => c.enrolled)
      : courses.filter(c => c.teacher_id === state.user.id || state.user.role === 'admin');

    const perCourse = await Promise.all(
      relevant.map(c =>
        api('GET', `/quizzes/course/${c.id}`)
          .then(qs => ({ course: c, quizzes: (qs || []).filter(q => q.is_exam) }))
          .catch(() => ({ course: c, quizzes: [] }))
      )
    );

    const allExams = [];
    perCourse.forEach(({ course, quizzes }) => {
      quizzes.forEach(q => allExams.push({ ...q, course_title: course.title, course_id: course.id }));
    });

    const isTeacher = state.user.role !== 'student';

    let html = `<div class="page-header">
      <div><h2> ${t('exams')}</h2><p class="text-muted">${isTeacher ? 'Manage your course exams' : 'Your scheduled exams'}</p></div>
    </div>`;

    if (!allExams.length) {
      html += `<div class="card"><div class="card-body" style="text-align:center;color:var(--muted);padding:40px">${t('no_quizzes')}</div></div>`;
    } else {
      allExams.forEach(q => {
        const submitted = q.my_attempt && q.my_attempt.submitted_at;
        const started   = q.my_attempt && !q.my_attempt.submitted_at;
        const statusBadge = submitted
          ? `<span class="badge badge-success">Submitted</span>`
          : started
          ? `<span class="badge badge-warning">In Progress</span>`
          : `<span class="badge badge-secondary">${t('not_attempted')}</span>`;

        const publishBadge = q.is_published
          ? `<span class="badge badge-success">${t('quiz_published')}</span>`
          : `<span class="badge badge-secondary">${t('quiz_draft')}</span>`;

        let actionBtn = '';
        if (isTeacher) {
          actionBtn = `<button class="btn btn-sm btn-primary" onclick="navigate('quiz-builder',{id:${q.id}})">${t('edit_quiz')}</button>`;
        } else if (!submitted) {
          actionBtn = started
            ? `<button class="btn btn-sm btn-warning" onclick="startExam(${q.id})"> ${t('resume_quiz')}</button>`
            : `<button class="btn btn-sm btn-primary" onclick="startExam(${q.id})">${t('start_now')}</button>`;
        } else {
          actionBtn = `<button class="btn btn-sm" onclick="navigate('exam-take',{id:${q.id}})">${t('quiz_results')}</button>`;
        }

        html += `<div class="exam-card">
          <div class="exam-card-body">
            <div class="exam-title-row">
              <strong>${htmlEsc(q.title)}</strong>
              <span class="exam-badge">EXAM</span>
              ${isTeacher ? publishBadge : statusBadge}
            </div>
            <div style="font-size:12px;color:var(--muted);margin-top:3px">${htmlEsc(q.course_title)}</div>
            <div class="exam-meta">
              ${q.time_limit ? `<small> ${q.time_limit} ${t('minutes')}</small>` : ''}
              ${q.due_date   ? `<small> ${t('due_date')}: ${fmtDateTime(q.due_date)}</small>` : ''}
              ${q.question_count ? `<small>${q.question_count} questions · ${q.total_points} ${t('pts')}</small>` : ''}
            </div>
          </div>
          <div class="exam-card-actions">${actionBtn}</div>
        </div>`;
      });
    }

    el.innerHTML = html;
  } catch(err) {
    el.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
  }
}

async function startExam(examId) {
  try {
    await api('POST', `/quizzes/${examId}/start`);
    navigate('exam-take', { id: examId });
  } catch(err) { toast(err.message, 'error'); }
}

function enterExamLock() {
  state.examLocked = true;
  document.body.classList.add('exam-lock-active');
  // Block browser back/forward during exam
  history.pushState(null, '', location.href);
  window.onpopstate = () => {
    history.pushState(null, '', location.href);
    toast(t('exam_warning'), 'error');
  };
  window._examBeforeUnload = (e) => {
    e.preventDefault();
    e.returnValue = t('exam_warning');
    return t('exam_warning');
  };
  window.addEventListener('beforeunload', window._examBeforeUnload);
}

function exitExamLock() {
  state.examLocked = false;
  document.body.classList.remove('exam-lock-active');
  window.onpopstate = null;
  if (window._examBeforeUnload) {
    window.removeEventListener('beforeunload', window._examBeforeUnload);
    window._examBeforeUnload = null;
  }
}

async function renderExamTake(examId, el) {
  loading(el);
  try {
    const quiz = await api('GET', `/quizzes/${examId}`);
    const submitted = quiz.my_attempt && quiz.my_attempt.submitted_at;

    if (submitted) {
      exitExamLock();
      renderQuizResults(quiz, el);
      return;
    }

    // Enter lock mode
    enterExamLock();

    let timerHtml = '';
    if (quiz.time_limit && quiz.my_attempt) {
      timerHtml = `<div class="exam-topbar-timer" id="exam-timer">--:--</div>`;
    }

    el.innerHTML = `
      <div class="exam-topbar">
        <div class="exam-topbar-title">
          <span class="exam-topbar-badge">EXAM</span>
          ${htmlEsc(quiz.title)}
        </div>
        <div style="display:flex;align-items:center;gap:16px">
          <small style="color:var(--muted)">${quiz.question_count} questions · ${quiz.total_points} ${t('pts')}</small>
          ${timerHtml}
        </div>
      </div>
      <div class="exam-body">
        <div class="exam-warning-banner">
           ${t('exam_warning')}
        </div>
        ${quiz.questions.map((q, i) => `
          <div class="quiz-question-block">
            <div class="quiz-q-num">${t('q_num')} ${i+1} ${t('of')} ${quiz.question_count} &bull; ${fmtPts(q.points)} ${t('pts')}</div>
            <div class="quiz-q-text">${htmlEsc(q.question_text)}</div>
            ${q.question_type === 'short_answer' ? `
              <textarea class="form-control" id="sa-${q.id}" rows="4" placeholder="…"></textarea>` : `
              <div class="quiz-options">
                ${q.options.map(o => `
                  <div class="quiz-option">
                    <input type="radio" name="q-${q.id}" id="opt-${o.id}" value="${o.id}">
                    <label for="opt-${o.id}">${htmlEsc(o.option_text)}</label>
                  </div>`).join('')}
              </div>`}
          </div>`).join('')}
        <div class="exam-submit-bar">
          <small style="color:var(--muted)">${t('exam_warning').split('.')[0]}.</small>
          <button class="btn btn-primary" onclick="submitExam(${examId})">${t('submit_quiz')}</button>
        </div>
      </div>`;

    // Timer
    if (quiz.time_limit && quiz.my_attempt) {
      const elapsed = (Date.now() - new Date(quiz.my_attempt.started_at)) / 1000;
      const remaining = Math.max(0, quiz.time_limit * 60 - elapsed);
      startExamTimer(Math.floor(remaining), () => submitExamAuto(examId));
    }
  } catch(err) {
    exitExamLock();
    el.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
  }
}

function startExamTimer(seconds, onExpire) {
  let rem = seconds;
  const tick = () => {
    const el = document.getElementById('exam-timer');
    if (!el) { clearInterval(state.quizTimer); return; }
    const m = Math.floor(rem / 60), s = rem % 60;
    el.textContent = `${m}:${String(s).padStart(2, '0')}`;
    el.className = 'exam-topbar-timer' +
      (rem < 60 ? ' exam-timer-urgent' : rem < 300 ? ' exam-timer-warn' : '');
    if (rem <= 0) { clearInterval(state.quizTimer); onExpire(); }
    rem--;
  };
  tick();
  state.quizTimer = setInterval(tick, 1000);
}

async function submitExam(examId) {
  if (!await showConfirm(t('exam_submit_confirm'), { okLabel: t('submit') })) return;
  await _doSubmitExam(examId);
}

async function submitExamAuto(examId) {
  toast(t('exam_time_up'), 'error');
  await _doSubmitExam(examId);
}

async function _doSubmitExam(examId) {
  if (state.quizTimer) { clearInterval(state.quizTimer); state.quizTimer = null; }
  const quiz = await api('GET', `/quizzes/${examId}`).catch(() => null);
  if (!quiz) return;
  const answers = quiz.questions.map(q => {
    if (q.question_type === 'short_answer' || q.question_type === 'long_answer') {
      return { question_id: q.id, text_answer: document.getElementById(`sa-${q.id}`)?.value || '' };
    }
    const sel = document.querySelector(`input[name="q-${q.id}"]:checked`);
    return { question_id: q.id, selected_option_id: sel ? parseInt(sel.value) : null };
  });
  try {
    await api('POST', `/quizzes/${examId}/submit`, { answers });
    exitExamLock();
    toast(t('quiz_submitted'));
    navigate('exam-take', { id: examId });
  } catch(err) { toast(err.message, 'error'); }
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
           <span class="pq-pending-icon"></span>
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
           <div class="post-submit-trophy"></div>
           <p class="post-submit-congrats">${t('no_outstanding_quizzes')}</p>
         </div>`
      : `<p class="post-submit-subtitle">${t('outstanding_quizzes_msg')}</p>
         <div class="outstanding-list">
           ${pending.map(q => {
             const due = q.due_date ? new Date(q.due_date) : null;
             const overdue = due && due < now;
             const dueTxt = due
               ? `${t('due_date')}: <strong class="${overdue?'text-danger':''}">${fmtDate(q.due_date)}${overdue?' ':''}</strong>`
               : '';
             const resume = q.my_attempt && !q.my_attempt.submitted_at;
             return `
               <div class="outstanding-item">
                 <div class="outstanding-info">
                   <span class="outstanding-title"> ${htmlEsc(q.title)}</span>
                   <span class="outstanding-course"> ${htmlEsc(q.course_title)}</span>
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
          <h4 class="pq-section-title"> ${t('outstanding_quizzes')}</h4>
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
            <span class="urgent-quiz-title"> ${htmlEsc(q.title)}</span>
            <span class="urgent-quiz-course"> ${htmlEsc(q.course_title)}</span>
            ${due ? `<span class="urgent-quiz-due${overdue?' text-danger':''}">
              ${t('due_date')}: ${fmtDate(q.due_date)}${overdue?' ':''}
            </span>` : ''}
          </div>
          <button class="btn btn-sm btn-primary"
            onclick="${resume ? `navigate('quiz-take',{id:${q.id}})` : `startQuiz(${q.id})`}">
             ${resume ? t('resume_quiz') : t('start_now')}
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
        <h2>${htmlEsc(quiz.title)} — ${t('quiz_results')}</h2>
      </div>
      ${attempt?.score != null
        ? `<div class="stat-card" style="min-width:120px;text-align:center">
            <div class="stat-number">${attempt.score}</div>
            <div class="stat-label">${t('your_score')} / ${fmtPts(quiz.total_points)}</div>
           </div>`
        : `<span class="badge badge-warning"> ${t('pending_teacher_grade')}</span>`}
    </div>
    ${quiz.questions.map((q,i) => {
      const myAns = answerMap[q.id];
      const myOptId = myAns?.selected_option_id;
      const myText = myAns?.text_answer;
      return `
        <div class="quiz-question-block">
          <div class="quiz-q-num">${t('q_num')} ${i+1} &bull; ${fmtPts(q.points)} ${t('pts')}</div>
          <div class="quiz-q-text">${htmlEsc(q.question_text)}</div>
          ${(q.question_type === 'short_answer' || q.question_type === 'long_answer') ? `
            <div class="alert alert-success" style="margin-top:8px">
              <strong>${t('your_answer')}:</strong> ${htmlEsc(myText || '—')}
            </div>
            ${myAns?.teacher_score != null
              ? `<p style="font-size:13px;color:var(--success)"> ${fmtPts(myAns.teacher_score)} / ${fmtPts(q.points)} pts${myAns.teacher_feedback ? ` — ${htmlEsc(myAns.teacher_feedback)}` : ''}</p>`
              : `<p class="text-muted" style="font-size:12px"> ${t('pending_teacher_grade')}</p>`}` : `
            <div class="quiz-options" style="pointer-events:none">
              ${q.options.map(o => {
                let cls = '';
                if (o.is_correct && myOptId === o.id) cls = 'result-correct';
                else if (o.is_correct)               cls = 'result-correct';
                else if (myOptId === o.id)            cls = 'result-wrong';
                return `<div class="quiz-option ${cls}">
                  <input type="radio" ${myOptId===o.id?'checked':''} disabled>
                  <label>${htmlEsc(o.option_text)}
                    ${o.is_correct ? ' ' : ''}
                    ${myOptId===o.id && !o.is_correct ? ' ' : ''}
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
  if (!await showConfirm(t('delete')+'?')) return;
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
    const isTeacher = state.user.role === 'teacher';
    el.innerHTML = `
      <div class="page-header"><h2>${t('user_management')}</h2>
        <button class="btn btn-primary" onclick="openNewUserModal()">${t('add_user')}</button>
      </div>
      ${!isTeacher ? `<div class="tabs">
        <button class="tab active" onclick="filterUsers('all',this)">${t('all')} (${users.length})</button>
        <button class="tab" onclick="filterUsers('admin',this)">${t('admins')} (${users.filter(u=>u.role==='admin').length})</button>
        <button class="tab" onclick="filterUsers('teacher',this)">${t('teachers')} (${users.filter(u=>u.role==='teacher').length})</button>
        <button class="tab" onclick="filterUsers('student',this)">${t('students')} (${users.filter(u=>u.role==='student').length})</button>
      </div>` : ''}
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
  const isAdmin = state.user.role === 'admin';
  return list.map(u=>`
    <tr>
      <td>${htmlEsc(u.name)}</td><td>${htmlEsc(u.email)}</td>
      <td><span class="badge badge-${u.role}">${u.role}</span></td>
      <td>${u.id===state.user.id
        ? `<span class="text-muted">${t('you')}</span>`
        : (isAdmin ? `<button class="btn btn-sm btn-danger" onclick="deleteUser(${u.id})">${t('delete')}</button>` : '')}</td>
    </tr>`).join('');
}

function filterUsers(filter, btn) {
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('users-tbody').innerHTML = usersRows(window._users,filter);
}

function openNewUserModal() {
  const isTeacher = state.user.role === 'teacher';
  const roleField = isTeacher
    ? `<input type="hidden" name="role" value="teacher">`
    : `<div class="form-group"><label>${t('role')} *</label>
        <select name="role" class="form-control">
          <option value="student">${t('students')}</option>
          <option value="teacher">${t('teachers')}</option>
          <option value="admin">${t('admins')}</option>
        </select>
      </div>`;
  openModal(t('add_user'), `
    <form id="modal-form">
      <div class="form-group"><label>${t('full_name')} *</label>
        <input name="name" class="form-control" required placeholder="Jane Doe"></div>
      <div class="form-group"><label>${t('email')} *</label>
        <input name="email" type="email" class="form-control" required></div>
      <div class="form-group"><label>${t('password')} *</label>
        <input name="password" type="password" class="form-control" required minlength="6"></div>
      ${roleField}
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
  if (!await showConfirm(t('delete')+'?')) return;
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
      const hasGrades = data.courses && data.courses.length > 0;
      el.innerHTML = `
        <div class="page-header"><h2>${t('my_grades')}</h2>
          ${hasGrades ? `<div class="stat-card" style="min-width:120px;text-align:center">
            <div class="stat-number">${data.cumulative_gpa}</div>
            <div class="stat-label">${t('cumulative_gpa')}</div>
          </div>` : ''}
        </div>
        ${!hasGrades ? `
          <div class="gb-empty-state">
            <div class="gb-empty-icon"></div>
            <p class="gb-empty-title">No grades yet</p>
            <p class="gb-empty-sub">Your grades will appear here once your teacher has graded your submissions.</p>
          </div>` :
        data.courses.map(c => {
          const scores = Object.values(c.scores);
          return `
          <div class="card" style="margin-bottom:18px">
            <div class="card-header">
              <h3>${htmlEsc(c.course_title)}</h3>
              <div style="display:flex;gap:10px;align-items:center">
                <span class="grade-cell grade-${c.letter}">${c.letter} &nbsp;${c.weighted_pct}%</span>
                <small class="text-muted">GPA: ${c.gpa}</small>
              </div>
            </div>
            ${scores.length === 0 ? `
            <div class="card-body">
              <div class="gb-empty-state" style="padding:32px 24px">
                <div class="gb-empty-icon" style="font-size:32px"></div>
                <p class="gb-empty-title" style="font-size:14px">No graded work yet</p>
                <p class="gb-empty-sub" style="font-size:12.5px">Assignments will appear here once graded.</p>
              </div>
            </div>` : `
            <div class="card-body" style="padding:0">
              <div class="gradebook-table-wrapper">
                <table class="gradebook-table">
                  <thead><tr>
                    <th>${t('title_label')}</th>
                    <th>${t('score')}</th>
                    <th>${t('max_score')}</th>
                    <th>%</th>
                  </tr></thead>
                  <tbody>
                    ${scores.map(s => `
                      <tr>
                        <td><a class="table-link" onclick="navigate('assignment',{id:${s.id}})">${htmlEsc(s.title)}</a></td>
                        <td>${s.score !== null ? `<strong>${s.score}</strong>` : '<span class="text-muted">—</span>'}</td>
                        <td>${s.max_score}</td>
                        <td>${s.score !== null && s.max_score ? `<span class="grade-cell grade-${scoreToLetter(s.score, s.max_score)}" style="min-width:0;padding:2px 8px">${Math.round(s.score/s.max_score*100)}%</span>` : '<span class="text-muted">—</span>'}</td>
                      </tr>`).join('')}
                  </tbody>
                </table>
              </div>
            </div>`}
          </div>`;
        }).join('')}`;

    } else {
      // Teacher/Admin: course → student drill-down
      const courses = await api('GET', '/courses/');
      const mine = role === 'admin' ? courses : courses.filter(c => c.teacher_id === state.user.id);

      if (!mine.length) {
        el.innerHTML = `
          <div class="page-header"><h2>${t('gradebook')}</h2></div>
          <div class="gb-empty-state">
            <div class="gb-empty-icon"></div>
            <p class="gb-empty-title">No courses yet</p>
            <p class="gb-empty-sub">Create a course and add assignments to start tracking grades.</p>
          </div>`;
        return;
      }

      if (!state.currentParams.course_id) state.currentParams.course_id = mine[0].id;
      const cid = state.currentParams.course_id;
      const sid = state.currentParams.student_id || null;

      let gb = await api('GET', `/gradebook/course/${cid}`);

      el.innerHTML = `
        <div class="page-header"><h2>${t('gradebook')}</h2></div>
        <div class="card" style="margin-bottom:18px;padding:20px 24px">
          <div style="display:flex;gap:16px;align-items:flex-end;flex-wrap:wrap">
            <div style="flex:1;min-width:200px">
              <label class="form-label" style="margin-bottom:6px;display:block">Course</label>
              <select class="form-control" id="gb-course-sel">
                ${mine.map(c => `<option value="${c.id}" ${c.id==cid?'selected':''}>${htmlEsc(c.title)}</option>`).join('')}
              </select>
            </div>
            <div style="flex:1;min-width:200px">
              <label class="form-label" style="margin-bottom:6px;display:block">Student</label>
              <select class="form-control" id="gb-student-sel">
                <option value="">— All students (overview) —</option>
                ${(gb ? gb.students : []).map(s => `<option value="${s.student_id}" ${s.student_id==sid?'selected':''}>${htmlEsc(s.student_name)}</option>`).join('')}
              </select>
            </div>
          </div>
        </div>
        <div id="gb-body">
          ${gb ? (sid ? renderGradebookStudent(gb, parseInt(sid)) : renderGradebookTable(gb)) : ''}
        </div>`;

      el.querySelector('#gb-course-sel').addEventListener('change', function() {
        navigate('gradebook', {course_id: parseInt(this.value)});
      });
      el.querySelector('#gb-student-sel').addEventListener('change', function() {
        const v = this.value ? parseInt(this.value) : null;
        navigate('gradebook', {course_id: cid, ...(v ? {student_id: v} : {})});
      });
    }
  } catch(err) { el.innerHTML = `<div class="alert alert-error">${err.message}</div>`; }
}

function scoreToLetter(score, max) {
  if (!max) return 'N';
  const p = score / max * 100;
  if (p >= 90) return 'A';
  if (p >= 80) return 'B';
  if (p >= 70) return 'C';
  if (p >= 60) return 'D';
  return 'F';
}

function renderGradebookTable(gb) {
  if (!gb.students.length) return `
    <div class="gb-empty-state">
      <div class="gb-empty-icon"></div>
      <p class="gb-empty-title">No students enrolled</p>
      <p class="gb-empty-sub">Students who enroll in this course will appear here with their grades.</p>
    </div>`;
  const assignments = gb.assignments;
  if (!assignments.length) return `
    <div class="card">
      <div class="card-header"><h3>${htmlEsc(gb.course_title)}</h3>
        <small class="text-muted">${gb.students.length} student${gb.students.length!==1?'s':''} enrolled</small>
      </div>
      <div class="card-body">
        <div class="gb-empty-state" style="padding:36px 24px">
          <div class="gb-empty-icon" style="font-size:36px"></div>
          <p class="gb-empty-title" style="font-size:15px">No assignments yet</p>
          <p class="gb-empty-sub">Add assignments to this course to start tracking grades.</p>
        </div>
      </div>
    </div>`;
  return `
    <div class="card">
      <div class="card-header">
        <h3>${htmlEsc(gb.course_title)}</h3>
        <small class="text-muted">${gb.students.length} student${gb.students.length!==1?'s':''} · ${assignments.length} assignment${assignments.length!==1?'s':''}</small>
      </div>
      <div class="card-body" style="padding:0">
        <div class="gradebook-table-wrapper">
          <table class="gradebook-table">
            <thead>
              <tr>
                <th>Student</th>
                ${assignments.map(a => `<th><a class="table-link" onclick="navigate('assignment',{id:${a.id}})" title="${htmlEsc(a.title)}">${htmlEsc(a.title).substring(0,14)}${a.title.length>14?'…':''}${a.is_extra_credit?' ':''}</a></th>`).join('')}
                <th>Avg %</th><th>Grade</th>
              </tr>
            </thead>
            <tbody>
              ${gb.students.map(s => `
                <tr>
                  <td>${htmlEsc(s.student_name)}</td>
                  ${assignments.map(a => {
                    const sc = s.scores[a.id];
                    if (!sc || sc.score === null) return `<td class="text-muted">—</td>`;
                    const pct = a.max_score ? Math.round(sc.score/a.max_score*100) : null;
                    const letter = pct !== null ? scoreToLetter(sc.score, a.max_score) : 'N';
                    return `<td><span class="grade-cell grade-${letter}" style="min-width:0;padding:2px 8px;font-size:11.5px">${sc.score}</span></td>`;
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

function renderGradebookStudent(gb, studentId) {
  const student = gb.students.find(s => s.student_id === studentId);
  if (!student) return `<div class="alert alert-error">Student not found in this course.</div>`;
  const assignments = gb.assignments;

  const submitted = assignments.filter(a => student.scores[a.id]?.submitted).length;
  const graded    = assignments.filter(a => student.scores[a.id]?.graded).length;
  const missing   = assignments.filter(a => !student.scores[a.id]?.submitted).length;

  return `
    <div class="card" style="margin-bottom:18px;padding:20px 24px">
      <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
        <div style="width:44px;height:44px;border-radius:50%;background:var(--indigo);color:#fff;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;flex-shrink:0">
          ${htmlEsc(student.student_name.charAt(0).toUpperCase())}
        </div>
        <div>
          <div style="font-size:16px;font-weight:700;color:var(--text)">${htmlEsc(student.student_name)}</div>
          <div style="font-size:12px;color:var(--muted)">${htmlEsc(gb.course_title)}</div>
        </div>
        <div style="margin-left:auto;display:flex;gap:12px;flex-wrap:wrap">
          <div style="text-align:center">
            <div style="font-size:22px;font-weight:800;color:var(--text)">${student.weighted_pct}%</div>
            <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px">Average</div>
          </div>
          <div style="text-align:center">
            <span class="grade-cell grade-${student.letter}" style="font-size:20px;padding:4px 14px">${student.letter}</span>
            <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-top:4px">Grade</div>
          </div>
        </div>
      </div>
      <div style="display:flex;gap:20px;margin-top:16px;padding-top:14px;border-top:1px solid var(--border)">
        <div style="display:flex;align-items:center;gap:6px;font-size:13px">
          <span style="width:10px;height:10px;border-radius:50%;background:var(--success);display:inline-block"></span>
          <strong>${submitted}</strong> <span class="text-muted">submitted</span>
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:13px">
          <span style="width:10px;height:10px;border-radius:50%;background:var(--indigo);display:inline-block"></span>
          <strong>${graded}</strong> <span class="text-muted">graded</span>
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:13px">
          <span style="width:10px;height:10px;border-radius:50%;background:var(--danger);display:inline-block"></span>
          <strong>${missing}</strong> <span class="text-muted">missing</span>
        </div>
      </div>
    </div>

    <div class="card" style="padding:0">
      <div class="card-header" style="padding:14px 20px">
        <h3>Assignments</h3>
        <small class="text-muted">${assignments.length} total</small>
      </div>
      ${assignments.length === 0 ? `
        <div class="card-body">
          <div class="gb-empty-state" style="padding:36px">
            <div class="gb-empty-icon"></div>
            <p class="gb-empty-title">No assignments yet</p>
          </div>
        </div>` : `
      <div class="card-body" style="padding:0">
        <table class="gradebook-table" style="width:100%">
          <thead>
            <tr>
              <th style="padding:10px 18px">Assignment</th>
              <th style="padding:10px 12px;text-align:center">Status</th>
              <th style="padding:10px 12px;text-align:center">Score</th>
              <th style="padding:10px 12px;text-align:center">Max</th>
              <th style="padding:10px 12px;text-align:center">%</th>
              <th style="padding:10px 12px;text-align:center">Grade</th>
            </tr>
          </thead>
          <tbody>
            ${assignments.map(a => {
              const sc = student.scores[a.id] || {};
              const submitted = sc.submitted;
              const graded    = sc.graded;
              const score     = sc.score;
              const max       = a.max_score;
              const pct       = (graded && max) ? Math.round(score / max * 100) : null;
              const letter    = pct !== null ? scoreToLetter(score, max) : null;

              const statusBadge = !submitted
                ? `<span class="badge badge-danger">Missing</span>`
                : graded
                  ? `<span class="badge badge-success">Graded</span>`
                  : `<span class="badge badge-warning">Submitted</span>`;

              return `
                <tr>
                  <td style="padding:12px 18px;font-weight:500"><a class="table-link" onclick="navigate('assignment',{id:${a.id}})">${htmlEsc(a.title)}</a>${a.is_extra_credit ? ' <span style="font-size:11px;color:var(--gold)"> Extra credit</span>' : ''}</td>
                  <td style="padding:12px;text-align:center">${statusBadge}</td>
                  <td style="padding:12px;text-align:center">${graded ? `<strong>${score}</strong>` : '<span class="text-muted">—</span>'}</td>
                  <td style="padding:12px;text-align:center;color:var(--muted)">${max}</td>
                  <td style="padding:12px;text-align:center">${pct !== null ? `${pct}%` : '<span class="text-muted">—</span>'}</td>
                  <td style="padding:12px;text-align:center">${letter ? `<span class="grade-cell grade-${letter}" style="min-width:0;padding:2px 10px">${letter}</span>` : '<span class="text-muted">—</span>'}</td>
                </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>`}
    </div>

    ${gb.materials && gb.materials.length ? `
    <div class="card" style="padding:0;margin-top:18px">
      <div class="card-header" style="padding:14px 20px">
        <h3>Material Completions</h3>
        <small class="text-muted">${student.completed_material_ids ? student.completed_material_ids.length : 0} / ${gb.materials.length} completed</small>
      </div>
      <div class="card-body" style="padding:0">
        <table class="gradebook-table" style="width:100%">
          <thead>
            <tr>
              <th style="padding:10px 18px">Material</th>
              <th style="padding:10px 12px;text-align:center">Status</th>
              <th style="padding:10px 12px;text-align:center">Action</th>
            </tr>
          </thead>
          <tbody>
            ${gb.materials.map(m => {
              const done = student.completed_material_ids && student.completed_material_ids.includes(m.id);
              return `<tr>
                <td style="padding:12px 18px;font-weight:500">${htmlEsc(m.title)}</td>
                <td style="padding:12px;text-align:center">
                  ${done
                    ? '<span class="badge badge-success">Completed</span>'
                    : '<span class="badge" style="background:var(--border);color:var(--muted)">Not completed</span>'}
                </td>
                <td style="padding:12px;text-align:center">
                  ${done
                    ? `<button class="btn btn-sm btn-danger" onclick="unmarkMaterialComplete(${gb.course_id},${m.id},${student.student_id})">Unmark</button>`
                    : '<span class="text-muted">—</span>'}
                </td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
    </div>` : ''}`;
}

async function unmarkMaterialComplete(courseId, materialId, studentId) {
  if (!await showConfirm('Remove this completion record? The student will need to mark it complete again.')) return;
  try {
    await api('DELETE', `/courses/${courseId}/materials/${materialId}/complete/${studentId}`);
    toast('Completion removed.');
    navigate('gradebook', {course_id: courseId, student_id: studentId});
  } catch(err) { toast(err.message, 'error'); }
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

    const allEvents = [];
    const now = new Date();

    for (const c of enrolled) {
      const [asgns, sessions, quizzes] = await Promise.all([
        api('GET', `/assignments/course/${c.id}`),
        api('GET', `/sessions/course/${c.id}`),
        api('GET', `/quizzes/course/${c.id}`),
      ]);
      (asgns||[]).forEach(a => {
        if (a.due_date) allEvents.push({ date: new Date(a.due_date), title: a.title, course: c.title, type: 'assignment' });
      });
      (sessions||[]).forEach(s => {
        if (s.date) allEvents.push({ date: new Date(s.date), title: s.title, course: c.title, type: 'session' });
      });
      (quizzes||[]).forEach(q => {
        if (q.due_date) allEvents.push({ date: new Date(q.due_date), title: q.title, course: c.title, type: 'quiz' });
      });
    }

    allEvents.sort((a, b) => a.date - b.date);

    window._calState = { events: allEvents, year: now.getFullYear(), month: now.getMonth(), selected: null };

    const TYPE_ICON = { assignment: '', session: '', quiz: '' };
    const DAYS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

    function drawCal() {
      const { events, year, month, selected } = window._calState;
      const today = new Date();
      const firstDay = new Date(year, month, 1);
      const lastDay  = new Date(year, month + 1, 0);
      const monthLabel = firstDay.toLocaleString('en-GB', { month: 'long', year: 'numeric' });

      // Monday-anchored start offset
      const startOff = (firstDay.getDay() + 6) % 7;
      const totalCells = Math.ceil((startOff + lastDay.getDate()) / 7) * 7;

      let cells = '';
      for (let i = 0; i < totalCells; i++) {
        const d = i - startOff + 1;
        const valid = d >= 1 && d <= lastDay.getDate();
        if (!valid) { cells += `<div class="cal-cell cal-cell-empty"></div>`; continue; }
        const cellDate = new Date(year, month, d);
        const isToday    = cellDate.toDateString() === today.toDateString();
        const isSel      = selected && cellDate.toDateString() === new Date(selected).toDateString();
        const dayEvs     = events.filter(e => e.date.toDateString() === cellDate.toDateString());
        const dotTypes   = [...new Set(dayEvs.map(e => e.type))];
        cells += `<div class="cal-cell${isToday ? ' cal-today' : ''}${isSel ? ' cal-selected' : ''}"
          onclick="_calSelect('${cellDate.toISOString()}')">
          <span class="cal-cell-num">${d}</span>
          <div class="cal-dots">
            ${dotTypes.map(tp => `<span class="cal-dot cal-dot-${tp}"></span>`).join('')}
            ${dayEvs.length > 3 ? `<span class="cal-dot-more">+${dayEvs.length - 3}</span>` : ''}
          </div>
        </div>`;
      }

      // Right panel: selected day or upcoming
      let panelTitle, panelBody;
      if (selected) {
        const selDate = new Date(selected);
        const dayEvs  = events.filter(e => e.date.toDateString() === selDate.toDateString());
        panelTitle = selDate.toLocaleDateString('en-GB', { weekday:'long', day:'numeric', month:'long' });
        panelBody  = dayEvs.length
          ? dayEvs.map(ev => `
              <div class="cal-event-item">
                <span class="cal-event-icon">${TYPE_ICON[ev.type]||''}</span>
                <div class="cal-event-detail">
                  <div class="cal-event-title">${htmlEsc(ev.title)}</div>
                  <div class="cal-event-course">${htmlEsc(ev.course)}</div>
                </div>
                <span class="cal-event-badge cal-badge-${ev.type}">${ev.type}</span>
              </div>`).join('')
          : `<p class="text-muted" style="padding:16px 0">No events on this day.</p>`;
      } else {
        const upcoming = events.filter(e => e.date >= today).slice(0, 8);
        panelTitle = t('upcoming_events');
        panelBody  = upcoming.length
          ? upcoming.map(ev => {
              const daysLeft = Math.ceil((ev.date - today) / 86400000);
              const urgency  = daysLeft < 0 ? 'overdue' : daysLeft < 3 ? 'soon' : '';
              return `
              <div class="cal-event-item${urgency ? ' cal-event-' + urgency : ''}">
                <span class="cal-event-icon">${TYPE_ICON[ev.type]||''}</span>
                <div class="cal-event-detail">
                  <div class="cal-event-title">${htmlEsc(ev.title)}</div>
                  <div class="cal-event-course">${htmlEsc(ev.course)}</div>
                </div>
                <span class="cal-event-when">${daysLeft < 0 ? 'overdue' : daysLeft === 0 ? 'today' : daysLeft === 1 ? 'tomorrow' : `${daysLeft}d`}</span>
              </div>`;
            }).join('')
          : `<p class="text-muted" style="padding:16px 0">${t('no_events')}</p>`;
      }

      el.innerHTML = `
        <div class="page-header"><h2>${t('calendar')}</h2></div>
        <div class="cal-layout">
          <div class="cal-grid-card">
            <div class="cal-nav">
              <button class="btn btn-sm cal-nav-btn" onclick="_calNav(-1)">‹</button>
              <span class="cal-month-label">${monthLabel}</span>
              <button class="btn btn-sm cal-nav-btn" onclick="_calNav(1)">›</button>
            </div>
            <div class="cal-weekdays">${DAYS.map(d => `<div class="cal-wd">${d}</div>`).join('')}</div>
            <div class="cal-grid">${cells}</div>
          </div>
          <div class="cal-panel">
            <div class="cal-panel-header">
              <span class="cal-panel-title">${panelTitle}</span>
              ${selected ? `<button class="btn-link" onclick="_calSelect(null)">← All upcoming</button>` : ''}
            </div>
            <div class="cal-event-list">${panelBody}</div>
          </div>
        </div>`;
    }

    window._calNav = (dir) => {
      window._calState.month += dir;
      if (window._calState.month > 11) { window._calState.month = 0; window._calState.year++; }
      if (window._calState.month <  0) { window._calState.month = 11; window._calState.year--; }
      window._calState.selected = null;
      drawCal();
    };
    window._calSelect = (iso) => {
      window._calState.selected = (iso && window._calState.selected === iso) ? null : iso;
      drawCal();
    };

    drawCal();
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
                <div class="message-from">${htmlEsc(other||'?')}</div>
                <div class="message-subject">${htmlEsc(m.subject)}</div>
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
  if (!await showConfirm('Delete this message?')) return;
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
    let broadcastCourses = [];

    if (state.user.role === 'admin') {
      const [users, courses] = await Promise.all([
        api('GET', '/users/').catch(() => []),
        api('GET', '/courses/').catch(() => []),
      ]);
      persons = (users || []).filter(u => u.id !== state.user.id);
      broadcastCourses = courses || [];
    } else {
      const courses = await api('GET', '/courses/') || [];
      const relevant = state.user.role === 'teacher'
        ? courses.filter(c => c.teacher_id === state.user.id)
        : courses.filter(c => c.enrolled);
      broadcastCourses = relevant;
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

    // Build broadcast options
    let broadcastOptions = '';
    if (state.user.role === 'admin') {
      broadcastOptions += `<optgroup label="── Broadcast to Group ──">
        <option value="broadcast:students"> All Students</option>
        <option value="broadcast:teachers"> All Teachers</option>
        <option value="broadcast:everyone"> Everyone</option>
      </optgroup>`;
    } else if (state.user.role === 'teacher') {
      broadcastOptions += `<optgroup label="── Broadcast ──">
        <option value="broadcast:my_students"> All My Students</option>
      </optgroup>`;
    }

    if (broadcastCourses.length) {
      broadcastOptions += `<optgroup label="── Broadcast to Course ──">
        ${broadcastCourses.map(c => `<option value="broadcast:course:${c.id}"> ${htmlEsc(c.title)}</option>`).join('')}
      </optgroup>`;
    }

    if (persons.length || broadcastOptions) {
      recipientField = `
        <div class="form-group"><label>${t('recipient')} *</label>
          <select name="recipient_id" class="form-control" required>
            <option value="">— Select recipient —</option>
            ${broadcastOptions}
            ${persons.length ? `<optgroup label="── Individual ──">
              ${persons.map(p => `<option value="${p.id}">${htmlEsc(p.name)}${p.email ? ` (${htmlEsc(p.email)})` : ''} — ${p.role}</option>`).join('')}
            </optgroup>` : ''}
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
        if (String(recipId).startsWith('broadcast:')) {
          const target = recipId.slice('broadcast:'.length); // handles "students", "course:123", etc.
          const result = await api('POST', '/messages/broadcast', { target, subject: fd.get('subject'), body: fd.get('body') });
          closeModal(); toast(` Sent to ${result.sent} recipient${result.sent !== 1 ? 's' : ''}!`);
          navigate('messages', { tab: 'sent' });
        } else {
          await api('POST', '/messages/', { recipient_id: parseInt(recipId), subject: fd.get('subject'), body: fd.get('body') });
          closeModal(); toast(t('send') + '!'); navigate('messages', { tab: 'sent' });
        }
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
            ${mine.map(c => `<option value="${c.id}" ${c.id==cid?'selected':''}>${htmlEsc(c.title)}</option>`).join('')}
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
                    <div class="chart-bar-letter">${letter}</div>
                    <div class="chart-bar-track">
                      <div class="chart-bar-fill chart-bar-fill-${letter}" style="width:${pct}%"></div>
                    </div>
                    <div class="chart-bar-meta">${count} <span style="font-weight:400">(${pct}%)</span></div>
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
// ═══════════════════════════════════════════════════════════
// Question Banks Page
// ═══════════════════════════════════════════════════════════
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
            <h4>${htmlEsc(m.title)} ${!m.is_published?'<span class="badge badge-warning">Draft</span>':''}</h4>
            <small>${m.progress}% complete</small>
          </div>
          <div class="module-progress-bar"><div class="module-progress-fill" style="width:${m.progress}%"></div></div>
          <div class="module-item-list">
            ${m.items.map(item => `
              <div class="module-item-row">
                ${state.user.role === 'student' ? `
                  <div class="module-item-check${item.completed?' done':''}" onclick="completeModuleItem(${item.id},${courseId})">
                    ${item.completed ? '' : ''}
                  </div>` : '<div style="width:20px"></div>'}
                <div class="module-item-title">${htmlEsc(item.title)}</div>
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
  if (!await showConfirm(t('delete')+'?')) return;
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
            <h3>${b.is_pinned?' ':''}${htmlEsc(b.title)}</h3>
            <div style="display:flex;gap:6px;align-items:center">
              <small class="text-muted">${b.post_count} posts</small>
              <button class="btn btn-sm btn-primary" onclick="navigate('discussion-board',{id:${b.id}})">View Posts</button>
              ${canManage?`<button class="btn btn-sm btn-danger" onclick="deleteBoard(${b.id},${courseId})">${t('delete')}</button>`:''}
            </div>
          </div>
          ${b.description?`<div class="card-body"><p class="text-muted">${htmlEsc(b.description)}</p></div>`:''}
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
  if (!await showConfirm(t('delete')+'?')) return;
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
         <strong>Ollama is not running.</strong>
        Start it with: <code>ollama serve</code> and make sure
        <code>ollama pull ${statusData?.model || 'llama3.2'}</code> has been run.
      </div>` : '';

    el.innerHTML = `
      <div class="page-header">
        <h2> ${t('ai_tutor')}</h2>
        <button class="btn btn-primary" onclick="openNewTutorSessionModal()">${t('new_chat')}</button>
      </div>
      ${ollamaBanner}
      <div id="ai-tutor-sessions" style="margin-top:${ollamaOk ? '0' : '12px'}">
        ${(sessions||[]).length ? (sessions||[]).map(s => `
          <div class="card" style="margin-bottom:10px;cursor:pointer" onclick="navigate('ai-chat',{id:${s.id}})">
            <div class="card-body" style="display:flex;align-items:center;gap:14px;padding:14px 18px">
              <div style="font-size:1.6rem;flex-shrink:0">
                ${s.mode === 'assignment_help' ? '' : ''}
              </div>
              <div style="flex:1;min-width:0">
                <div style="font-weight:700;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
                  ${htmlEsc(s.title)}
                </div>
                <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
                  <span class="chat-mode-pill ${s.mode === 'assignment_help' ? 'chat-mode-assignment' : 'chat-mode-study'}">
                    ${s.mode === 'assignment_help' ? 'Assignment Help' : 'Study'}
                  </span>
                  ${s.course_title ? `<small class="text-muted"> ${htmlEsc(s.course_title)}</small>` : ''}
                  <small class="text-muted"> ${s.message_count} message${s.message_count !== 1 ? 's' : ''}</small>
                  <small class="text-muted">${fmtDate(s.created_at)}</small>
                </div>
              </div>
              <button class="btn btn-sm btn-danger" style="flex-shrink:0"
                onclick="event.stopPropagation();deleteTutorSession(${s.id})"></button>
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
                  ${session.mode === 'assignment_help' ? ' Hint-Only Mode' : ' Study Mode'}
                </span>
                ${session.course_title ? `<small class="text-muted"> ${htmlEsc(session.course_title)}</small>` : ''}
              </div>
            </div>
            ${ollamaOk
              ? `<span class="badge badge-success" style="flex-shrink:0"> Online</span>`
              : `<span class="badge badge-warning" style="flex-shrink:0"> Ollama offline</span>`}
          </div>

          ${!ollamaOk ? `<div class="chat-ollama-banner">
             Ollama is not running — messages will fail until you run <code>ollama serve</code>.
          </div>` : ''}

          <div class="chat-messages" id="chat-messages-area">
            ${(messages||[]).length
              ? (messages||[]).map(m => renderChatBubble(m)).join('')
              : `<div class="chat-empty">
                  <div class="chat-empty-icon"></div>
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
                
                <input type="file" id="chat-file-input" style="display:none"
                  accept=".txt,.py,.js,.ts,.jsx,.tsx,.java,.c,.cpp,.h,.cs,.go,.rb,.php,.html,.css,.md,.csv,.json,.xml,.yaml,.pdf,.docx,.jpg,.jpeg,.png,.gif,.webp"
                  onchange="handleChatFileSelect(${sessionId},this)">
              </label>
              <textarea id="chat-text-input" placeholder="${t('chat_placeholder')}"
                onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendChatMessage(${sessionId})}"
                oninput="this.style.height='auto';this.style.height=Math.min(this.scrollHeight,140)+'px'"></textarea>
              <button class="btn btn-primary" onclick="sendChatMessage(${sessionId})" id="chat-send-btn" style="flex-shrink:0">
                ${t('chat_send')} 
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
    toast(' Uploading…');
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
    toast(` ${data.filename} attached`);
  } catch(e) { toast(e.message, 'error'); }
}

function renderChatChips() {
  const el = document.getElementById('chat-file-chips');
  if (!el) return;
  el.innerHTML = (window._chatUploads || []).map((u, i) => `
    <span class="upload-chip">
      ${u.kind === 'image' ? '' : u.kind === 'pdf' ? '' : ''} ${htmlEsc(u.filename)}
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
    const isQuizLock = err.message.toLowerCase().includes('quiz') || err.message.toLowerCase().includes('locked');
    const errBubble = document.createElement('div');
    errBubble.className = 'chat-bubble-wrap assistant';
    errBubble.innerHTML = `
      <div class="chat-bubble assistant" style="color:var(--danger);border-color:var(--danger)">
        ${isQuizLock ? t('chat_locked') : ` ${htmlEsc(err.message)}`}
      </div>`;
    messagesArea?.appendChild(errBubble);
    if (messagesArea) messagesArea.scrollTop = messagesArea.scrollHeight;
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    document.getElementById('chat-text-input')?.focus();
  }
}

async function deleteTutorSession(id) {
  if (!await showConfirm('Delete this chat session and all its messages?')) return;
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

  openModal(' New AI Tutor Session', `
    <form id="modal-form">
      <div class="form-group"><label>Mode *</label>
        <select name="mode" class="form-control" id="tutor-mode-sel" onchange="onTutorModeChange()">
          <option value="study"> Study Session</option>
          <option value="assignment_help"> Assignment Help (hints only)</option>
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
        <button type="submit" class="btn btn-primary">Start Chat </button>
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
// Attendance Tracker
// ═══════════════════════════════════════════════════════════
async function renderAttendance(el) {
  loading(el);
  try {
    const courses = await api('GET', '/courses');
    const myCourses = state.user.role === 'teacher'
      ? courses.filter(c => c.teacher_id === state.user.id)
      : courses;

    const today = new Date().toISOString().slice(0, 10);

    el.innerHTML = `
      <div class="page-header"><h1>${t('attendance_title')}</h1></div>
      <div class="card" style="margin-bottom:20px;padding:20px 24px">
        <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end">
          <div class="form-group" style="margin:0;flex:1;min-width:200px">
            <label style="margin-bottom:6px;display:block">${t('att_pick_course')}</label>
            <select class="form-control" id="att-course-sel">
              <option value="">— ${t('att_pick_course')} —</option>
              ${myCourses.map(c => `<option value="${c.id}">${htmlEsc(c.title)}</option>`).join('')}
            </select>
          </div>
          <div class="form-group" style="margin:0">
            <label style="margin-bottom:6px;display:block">${t('att_pick_date')}</label>
            <input type="date" class="form-control" id="att-date-inp" value="${today}" style="min-width:160px">
          </div>
          <div style="padding-bottom:2px">
            <button class="btn btn-primary" id="att-load-btn" style="white-space:nowrap">${t('att_mark')}</button>
          </div>
        </div>
      </div>
      <div id="att-sheet"></div>
      <div class="card" style="margin-top:20px;padding:20px 24px">
        <h3 style="margin:0 0 16px">${t('att_history')}</h3>
        <div id="att-history-area"><p class="text-muted">${t('att_pick_course')}</p></div>
      </div>`;

    const sheetEl   = document.getElementById('att-sheet');
    const histEl    = document.getElementById('att-history-area');
    const courseSel = document.getElementById('att-course-sel');
    const dateInp   = document.getElementById('att-date-inp');

    async function loadSheet() {
      const cid  = courseSel.value;
      const date = dateInp.value;
      if (!cid || !date) return;

      loading(sheetEl);
      try {
        const [students, records] = await Promise.all([
          api('GET', `/courses/${cid}/students`),
          api('GET', `/courses/${cid}/attendance`),
        ]);

        const dayMap = {};
        records.filter(r => r.date === date).forEach(r => { dayMap[r.student_id] = r.status; });

        if (!students.length) {
          sheetEl.innerHTML = `<div class="card"><p class="text-muted">${t('att_no_students')}</p></div>`;
          return;
        }

        sheetEl.innerHTML = `
          <div class="card" style="padding:20px 24px">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px">
              <h3 style="margin:0">${t('att_mark')} — ${date}</h3>
              <button class="btn btn-primary" id="att-save-btn">${t('att_save')}</button>
            </div>
            <div style="overflow-x:auto">
              <table style="width:100%;border-collapse:collapse" id="att-table">
                <thead>
                  <tr style="border-bottom:2px solid var(--border)">
                    <th style="text-align:left;padding:10px 14px;color:var(--muted);font-weight:600;font-size:13px">#</th>
                    <th style="text-align:left;padding:10px 14px;color:var(--muted);font-weight:600;font-size:13px">Student</th>
                    <th style="text-align:center;padding:10px 14px;color:var(--success);font-weight:600;font-size:13px">${t('att_present')}</th>
                    <th style="text-align:center;padding:10px 14px;color:var(--gold);font-weight:600;font-size:13px">${t('att_late')}</th>
                    <th style="text-align:center;padding:10px 14px;color:var(--danger);font-weight:600;font-size:13px">${t('att_absent')}</th>
                  </tr>
                </thead>
                <tbody>
                  ${students.map((s, i) => {
                    const cur = dayMap[s.id] || 'present';
                    return `<tr style="border-bottom:1px solid var(--border)" data-sid="${s.id}">
                      <td style="padding:12px 14px;color:var(--muted);font-size:13px">${i + 1}</td>
                      <td style="padding:12px 14px;font-weight:600">${htmlEsc(s.name)}</td>
                      ${['present','late','absent'].map(st => `
                        <td style="text-align:center;padding:12px 14px">
                          <label style="cursor:pointer;display:flex;justify-content:center">
                            <input type="radio" name="att-${s.id}" value="${st}" ${cur === st ? 'checked' : ''}
                              style="accent-color:${st==='present'?'var(--success)':st==='late'?'var(--gold)':'var(--danger)'};width:20px;height:20px;cursor:pointer">
                          </label>
                        </td>`).join('')}
                    </tr>`;
                  }).join('')}
                </tbody>
              </table>
            </div>
          </div>`;

        document.getElementById('att-save-btn').onclick = async () => {
          const rows = document.querySelectorAll('#att-table tbody tr[data-sid]');
          const records = [];
          rows.forEach(row => {
            const sid = parseInt(row.dataset.sid);
            const sel = row.querySelector('input[type=radio]:checked');
            if (sel) records.push({ student_id: sid, status: sel.value });
          });
          try {
            await api('POST', `/courses/${cid}/attendance`, { date, records });
            toast(t('att_saved'), 'success');
            loadHistory(cid);
          } catch(e) { toast(e.message, 'error'); }
        };

        loadHistory(cid);
      } catch(e) {
        sheetEl.innerHTML = `<div class="alert alert-error">${e.message}</div>`;
      }
    }

    async function loadHistory(cid) {
      try {
        const [students, records] = await Promise.all([
          api('GET', `/courses/${cid}/students`),
          api('GET', `/courses/${cid}/attendance`),
        ]);

        if (!records.length) {
          histEl.innerHTML = `<p class="text-muted">${t('att_no_students')}</p>`;
          return;
        }

        // Build summary per student
        const stdMap = {};
        students.forEach(s => { stdMap[s.id] = s.name; });

        const summary = {};
        records.forEach(r => {
          if (!summary[r.student_id]) summary[r.student_id] = { present:0, late:0, absent:0 };
          summary[r.student_id][r.status]++;
        });

        // Unique sorted dates
        const dates = [...new Set(records.map(r => r.date))].sort();
        const dayRecords = {};
        records.forEach(r => {
          if (!dayRecords[r.date]) dayRecords[r.date] = {};
          dayRecords[r.date][r.student_id] = r.status;
        });

        histEl.innerHTML = `
          <h4 style="margin:0 0 14px">${t('att_summary')}</h4>
          <div style="overflow-x:auto">
            <table style="width:100%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="border-bottom:2px solid var(--border)">
                  <th style="text-align:left;padding:8px 12px;color:var(--muted);font-weight:600">Student</th>
                  <th style="text-align:center;padding:8px 12px;color:var(--success);font-weight:600">${t('att_present_count')}</th>
                  <th style="text-align:center;padding:8px 12px;color:var(--gold);font-weight:600">${t('att_late_count')}</th>
                  <th style="text-align:center;padding:8px 12px;color:var(--danger);font-weight:600">${t('att_absent_count')}</th>
                  <th style="text-align:center;padding:8px 12px;color:var(--muted);font-weight:600">${t('att_rate')}</th>
                </tr>
              </thead>
              <tbody>
                ${Object.entries(summary).map(([sid, s]) => {
                  const total = s.present + s.late + s.absent;
                  const rate  = total ? Math.round(s.present / total * 100) : 0;
                  const color = rate >= 80 ? 'var(--success)' : rate >= 60 ? 'var(--gold)' : 'var(--danger)';
                  return `<tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:10px 12px;font-weight:600">${htmlEsc(stdMap[sid] || sid)}</td>
                    <td style="text-align:center;padding:10px 12px">${s.present}</td>
                    <td style="text-align:center;padding:10px 12px">${s.late}</td>
                    <td style="text-align:center;padding:10px 12px">${s.absent}</td>
                    <td style="text-align:center;padding:10px 12px;font-weight:700;color:${color}">${rate}%</td>
                  </tr>`;
                }).join('')}
              </tbody>
            </table>
          </div>`;
      } catch(e) {
        histEl.innerHTML = `<div class="alert alert-error">${e.message}</div>`;
      }
    }

    document.getElementById('att-load-btn').onclick = loadSheet;

  } catch(err) {
    el.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
  }
}

// ═══════════════════════════════════════════════════════════
// Report Cards
// ═══════════════════════════════════════════════════════════
async function renderReportCards(el) {
  loading(el);
  try {
    if (state.user.role === 'student') {
      await renderStudentReportCards(el);
    } else {
      await renderTeacherReportCards(el);
    }
  } catch(err) {
    el.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
  }
}

async function renderStudentReportCards(el) {
  const cards = await api('GET', '/report-cards/my');
  el.innerHTML = `
    <div class="page-header"><h1>${t('report_cards_title')}</h1></div>
    ${!cards.length
      ? `<div class="card"><p class="text-muted">${t('rc_no_cards')}</p></div>`
      : cards.map(rc => `
        <div class="card" style="margin-bottom:16px;padding:20px 24px">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:14px">
            <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
              <strong style="font-size:16px">${htmlEsc(rc.course_title)}</strong>
              <span class="badge badge-success">${t('rc_published')}</span>
            </div>
            <span style="color:var(--muted);font-size:12px">${fmtDate(rc.updated_at)}</span>
          </div>
          <pre style="white-space:pre-wrap;font-family:inherit;line-height:1.75;color:var(--text);margin:0;background:var(--surface-2,var(--card));border:1px solid var(--border);padding:16px 18px;border-radius:8px;font-size:13px">${htmlEsc(rc.content)}</pre>
        </div>`).join('')}`;
}

async function renderTeacherReportCards(el) {
  const courses = await api('GET', '/courses');
  const myCourses = state.user.role === 'teacher'
    ? courses.filter(c => c.teacher_id === state.user.id)
    : courses;

  el.innerHTML = `
    <div class="page-header"><h1>${t('report_cards_title')}</h1></div>
    <div class="card" style="margin-bottom:20px;padding:20px 24px">
      <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end">
        <div class="form-group" style="margin:0;flex:1;min-width:200px">
          <label style="margin-bottom:6px;display:block">${t('rc_pick_course')}</label>
          <select class="form-control" id="rc-course-sel">
            <option value="">— ${t('rc_pick_course')} —</option>
            ${myCourses.map(c => `<option value="${c.id}">${htmlEsc(c.title)}</option>`).join('')}
          </select>
        </div>
        <div style="padding-bottom:2px">
          <button class="btn btn-primary" id="rc-load-btn" style="white-space:nowrap">Load</button>
        </div>
      </div>
    </div>
    <div id="rc-students-panel"></div>
    <div id="rc-cards-panel" style="margin-top:20px"></div>`;

  const studentsPanel = document.getElementById('rc-students-panel');
  const cardsPanel    = document.getElementById('rc-cards-panel');
  const courseSel     = document.getElementById('rc-course-sel');

  async function loadCourseCards() {
    const cid = courseSel.value;
    if (!cid) return;
    loading(studentsPanel);
    loading(cardsPanel);

    const [students, cards] = await Promise.all([
      api('GET', `/courses/${cid}/students`),
      api('GET', `/report-cards/course/${cid}`),
    ]);

    const cardMap = {};
    cards.forEach(c => { cardMap[c.student_id] = c; });

    studentsPanel.innerHTML = `
      <div class="card" style="padding:20px 24px">
        <h3 style="margin:0 0 16px">${t('rc_generate')}</h3>
        <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end">
          <div style="flex:1;min-width:200px">
            <select class="form-control" id="rc-student-sel">
              <option value="">— ${t('rc_pick_student')} —</option>
              ${students.map(s => `<option value="${s.id}">${htmlEsc(s.name)}</option>`).join('')}
            </select>
          </div>
          <div style="padding-bottom:2px">
            <button class="btn btn-primary" id="rc-gen-btn" style="white-space:nowrap">${t('rc_generate')}</button>
          </div>
        </div>
        <p id="rc-gen-status" style="margin:10px 0 0;color:var(--muted);font-size:13px"></p>
      </div>`;

    document.getElementById('rc-gen-btn').onclick = async () => {
      const sid = document.getElementById('rc-student-sel').value;
      if (!sid) return;
      const btn = document.getElementById('rc-gen-btn');
      const status = document.getElementById('rc-gen-status');
      btn.disabled = true; btn.textContent = t('rc_generating');
      status.textContent = t('rc_generating');
      try {
        await api('POST', '/report-cards/generate', { course_id: parseInt(cid), student_id: parseInt(sid) });
        toast(t('rc_generated'), 'success');
        loadCourseCards();
      } catch(e) {
        toast(e.message, 'error');
      } finally {
        btn.disabled = false; btn.textContent = t('rc_generate');
        status.textContent = '';
      }
    };

    if (!cards.length) {
      cardsPanel.innerHTML = `<div class="card"><p class="text-muted">${t('rc_no_cards')}</p></div>`;
      return;
    }

    cardsPanel.innerHTML = cards.map(rc => `
      <div class="card" style="margin-bottom:16px;padding:20px 24px" id="rc-card-${rc.id}">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:16px">
          <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
            <strong style="font-size:16px">${htmlEsc(rc.student_name)}</strong>
            <span class="badge ${rc.is_published ? 'badge-success' : 'badge-secondary'}">
              ${rc.is_published ? t('rc_published') : t('rc_draft')}
            </span>
            <span style="color:var(--muted);font-size:12px">${fmtDate(rc.updated_at)}</span>
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
            <button class="btn btn-sm" onclick="rcToggleEdit(${rc.id})" style="min-width:60px">${t('rc_edit')}</button>
            ${rc.is_published
              ? `<button class="btn btn-sm btn-gold" onclick="rcTogglePublish(${rc.id},false)" style="min-width:90px">${t('rc_unpublish')}</button>`
              : `<button class="btn btn-sm btn-success" onclick="rcTogglePublish(${rc.id},true)" style="min-width:80px">${t('rc_publish')}</button>`}
            <button class="btn btn-sm btn-danger" onclick="rcDelete(${rc.id})" style="min-width:64px">${t('rc_delete')}</button>
          </div>
        </div>
        <div id="rc-view-${rc.id}">
          <pre style="white-space:pre-wrap;font-family:inherit;line-height:1.75;color:var(--text);margin:0;background:var(--surface-2,var(--card));border:1px solid var(--border);padding:16px 18px;border-radius:8px;font-size:13px">${htmlEsc(rc.content)}</pre>
        </div>
        <div id="rc-edit-${rc.id}" style="display:none">
          <textarea class="form-control" id="rc-ta-${rc.id}" style="min-height:300px;font-family:inherit;font-size:13px;line-height:1.75">${htmlEsc(rc.content)}</textarea>
          <div style="margin-top:12px;display:flex;gap:8px">
            <button class="btn btn-primary btn-sm" onclick="rcSaveEdit(${rc.id})">${t('rc_save')}</button>
            <button class="btn btn-sm" onclick="rcToggleEdit(${rc.id})">${t('rc_cancel')}</button>
          </div>
        </div>
      </div>`).join('');
  }

  document.getElementById('rc-load-btn').onclick = loadCourseCards;

  // Expose helpers to inline onclick handlers
  window.rcToggleEdit = (id) => {
    const view = document.getElementById(`rc-view-${id}`);
    const edit = document.getElementById(`rc-edit-${id}`);
    if (edit.style.display === 'none') {
      view.style.display = 'none'; edit.style.display = 'block';
    } else {
      view.style.display = 'block'; edit.style.display = 'none';
    }
  };

  window.rcSaveEdit = async (id) => {
    const content = document.getElementById(`rc-ta-${id}`).value.trim();
    if (!content) return;
    try {
      await api('PUT', `/report-cards/${id}`, { content });
      toast(t('rc_save'), 'success');
      loadCourseCards();
    } catch(e) { toast(e.message, 'error'); }
  };

  window.rcTogglePublish = async (id, publish) => {
    try {
      await api('POST', `/report-cards/${id}/${publish ? 'publish' : 'unpublish'}`);
      toast(publish ? t('rc_published') : t('rc_draft'), 'success');
      loadCourseCards();
    } catch(e) { toast(e.message, 'error'); }
  };

  window.rcDelete = async (id) => {
    if (!await showConfirm(t('rc_delete') + '?')) return;
    try {
      await api('DELETE', `/report-cards/${id}`);
      toast(t('rc_deleted'), 'success');
      loadCourseCards();
    } catch(e) { toast(e.message, 'error'); }
  };
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
