from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Date, Boolean, JSON
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    role = Column(SAEnum("admin", "teacher", "student", "parent"), nullable=False, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)

    courses_teaching = relationship("Course", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")
    submissions = relationship("Submission", back_populates="student")
    announcements = relationship("Announcement", back_populates="author")
    quiz_attempts = relationship("QuizAttempt", back_populates="student")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete")
    user_badges = relationship("UserBadge", back_populates="user", cascade="all, delete",
                               foreign_keys="UserBadge.user_id")
    portfolio = relationship("Portfolio", back_populates="student", uselist=False, cascade="all, delete")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    subject = Column(String(100))
    grade_level = Column(String(50))
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("User", back_populates="courses_teaching")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete")
    materials = relationship("Material", back_populates="course", cascade="all, delete")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete")
    announcements = relationship("Announcement", back_populates="course")
    attendance_records = relationship("Attendance", back_populates="course", cascade="all, delete")
    sessions = relationship("ClassSession", back_populates="course", cascade="all, delete")
    quizzes = relationship("Quiz", back_populates="course", cascade="all, delete")
    grade_categories = relationship("GradeCategory", back_populates="course", cascade="all, delete")
    discussion_boards = relationship("DiscussionBoard", back_populates="course", cascade="all, delete")
    modules = relationship("CourseModule", back_populates="course", cascade="all, delete")
    surveys = relationship("Survey", back_populates="course", cascade="all, delete")


class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="materials")


class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    max_score = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    grade_category_id = Column(Integer, ForeignKey("grade_categories.id"), nullable=True)
    is_extra_credit = Column(Boolean, default=False)
    rubric_id = Column(Integer, ForeignKey("rubrics.id"), nullable=True)

    course = relationship("Course", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete")
    grade_category = relationship("GradeCategory", back_populates="assignments")
    rubric = relationship("Rubric", back_populates="assignments")


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text)
    score = Column(Float)
    feedback = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    graded_at = Column(DateTime)

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", back_populates="submissions")
    rubric_grades = relationship("RubricGrade", back_populates="submission", cascade="all, delete")
    grade_changes = relationship("GradeChange", back_populates="submission", cascade="all, delete")


class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="announcements")
    course = relationship("Course", back_populates="announcements")


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(SAEnum("present", "absent", "late"), nullable=False, default="present")

    course = relationship("Course", back_populates="attendance_records")


# ── Virtual / Physical Sessions ──────────────────────────────────────────────

class ClassSession(Base):
    __tablename__ = "class_sessions"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    session_type = Column(SAEnum("virtual", "physical"), nullable=False, default="virtual")
    date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    location = Column(String(500))   # meeting URL for virtual, room/address for physical
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="sessions")


# ── Quiz System ──────────────────────────────────────────────────────────────

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    time_limit = Column(Integer)        # minutes; None = unlimited
    due_date = Column(DateTime)
    shuffle = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="quizzes")
    questions = relationship(
        "QuizQuestion", back_populates="quiz",
        cascade="all, delete", order_by="QuizQuestion.order_num"
    )
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(
        SAEnum("multiple_choice", "true_false", "short_answer"), nullable=False
    )
    points = Column(Float, default=1.0)
    order_num = Column(Integer, default=0)

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuizOption", back_populates="question", cascade="all, delete")
    answers = relationship("QuizAnswer", back_populates="question", cascade="all, delete")


class QuizOption(Base):
    __tablename__ = "quiz_options"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    option_text = Column(String(500), nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("QuizQuestion", back_populates="options")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime)
    score = Column(Float)

    quiz = relationship("Quiz", back_populates="attempts")
    student = relationship("User", back_populates="quiz_attempts")
    answers = relationship("QuizAnswer", back_populates="attempt", cascade="all, delete")


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("quiz_options.id"), nullable=True)
    text_answer = Column(Text, nullable=True)

    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("QuizQuestion", back_populates="answers")
    selected_option = relationship("QuizOption")


# ── Password Reset ───────────────────────────────────────────────────────────

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    token      = Column(String(100), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    used       = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


# ── NEW MODELS ────────────────────────────────────────────────────────────────

class GradeCategory(Base):
    __tablename__ = "grade_categories"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    name = Column(String(100), nullable=False)
    weight = Column(Float, default=100.0)  # percentage weight
    drop_lowest = Column(Integer, default=0)

    course = relationship("Course", back_populates="grade_categories")
    assignments = relationship("Assignment", back_populates="grade_category")


class Rubric(Base):
    __tablename__ = "rubrics"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    criteria = relationship("RubricCriterion", back_populates="rubric", cascade="all, delete",
                            order_by="RubricCriterion.order_num")
    assignments = relationship("Assignment", back_populates="rubric")


class RubricCriterion(Base):
    __tablename__ = "rubric_criteria"
    id = Column(Integer, primary_key=True)
    rubric_id = Column(Integer, ForeignKey("rubrics.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    max_points = Column(Float, default=10.0)
    order_num = Column(Integer, default=0)

    rubric = relationship("Rubric", back_populates="criteria")
    levels = relationship("RubricLevel", back_populates="criterion", cascade="all, delete")
    rubric_grades = relationship("RubricGrade", back_populates="criterion", cascade="all, delete")


class RubricLevel(Base):
    __tablename__ = "rubric_levels"
    id = Column(Integer, primary_key=True)
    criterion_id = Column(Integer, ForeignKey("rubric_criteria.id"), nullable=False)
    label = Column(String(100), nullable=False)
    description = Column(Text)
    points = Column(Float, default=0.0)

    criterion = relationship("RubricCriterion", back_populates="levels")


class RubricGrade(Base):
    __tablename__ = "rubric_grades"
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    criterion_id = Column(Integer, ForeignKey("rubric_criteria.id"), nullable=False)
    points_awarded = Column(Float, default=0.0)
    comment = Column(Text)

    submission = relationship("Submission", back_populates="rubric_grades")
    criterion = relationship("RubricCriterion", back_populates="rubric_grades")


class QuestionBank(Base):
    __tablename__ = "question_banks"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("BankQuestion", back_populates="bank", cascade="all, delete")


class BankQuestion(Base):
    __tablename__ = "bank_questions"
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey("question_banks.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(SAEnum("multiple_choice", "true_false", "short_answer"), nullable=False)
    points = Column(Float, default=1.0)
    options = Column(JSON)  # list of {text, is_correct}
    tags = Column(String(500))

    bank = relationship("QuestionBank", back_populates="questions")


class CourseModule(Base):
    __tablename__ = "course_modules"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    order_num = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)

    course = relationship("Course", back_populates="modules")
    items = relationship("ModuleItem", back_populates="module", cascade="all, delete",
                         order_by="ModuleItem.order_num")


class ModuleItem(Base):
    __tablename__ = "module_items"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("course_modules.id"), nullable=False)
    item_type = Column(SAEnum("assignment", "quiz", "material", "session", "page"), nullable=False)
    item_id = Column(Integer)
    title = Column(String(200), nullable=False)
    order_num = Column(Integer, default=0)
    is_required = Column(Boolean, default=True)

    module = relationship("CourseModule", back_populates="items")
    completions = relationship("ModuleCompletion", back_populates="module_item", cascade="all, delete")


class ModuleCompletion(Base):
    __tablename__ = "module_completions"
    id = Column(Integer, primary_key=True)
    module_item_id = Column(Integer, ForeignKey("module_items.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)

    module_item = relationship("ModuleItem", back_populates="completions")


class DiscussionBoard(Base):
    __tablename__ = "discussion_boards"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    is_pinned = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="discussion_boards")
    posts = relationship("DiscussionPost", back_populates="board", cascade="all, delete")


class DiscussionPost(Base):
    __tablename__ = "discussion_posts"
    id = Column(Integer, primary_key=True)
    board_id = Column(Integer, ForeignKey("discussion_boards.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("discussion_posts.id"), nullable=True)
    content = Column(Text, nullable=False)
    is_endorsed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    board = relationship("DiscussionBoard", back_populates="posts")
    author = relationship("User")
    replies = relationship(
        "DiscussionPost",
        foreign_keys=[parent_id],
        back_populates="parent_post",
    )
    parent_post = relationship(
        "DiscussionPost",
        foreign_keys=[parent_id],
        back_populates="replies",
        remote_side="DiscussionPost.id",
    )


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(300), nullable=False)
    body = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    deleted_by_sender = Column(Boolean, default=False)
    deleted_by_recipient = Column(Boolean, default=False)

    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text)
    link = Column(String(500))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(10), default="🏅")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_badges = relationship("UserBadge", back_populates="badge", cascade="all, delete")


class UserBadge(Base):
    __tablename__ = "user_badges"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    awarded_at = Column(DateTime, default=datetime.utcnow)
    awarded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    note = Column(Text)

    user = relationship("User", back_populates="user_badges", foreign_keys=[user_id])
    badge = relationship("Badge", back_populates="user_badges")
    awarder = relationship("User", foreign_keys=[awarded_by])


class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    title = Column(String(200), default="My Portfolio")
    bio = Column(Text)
    is_public = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", back_populates="portfolio")
    items = relationship("PortfolioItem", back_populates="portfolio", cascade="all, delete")


class PortfolioItem(Base):
    __tablename__ = "portfolio_items"
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    content = Column(Text)
    url = Column(String(500))
    tags = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="items")


class ParentLink(Base):
    __tablename__ = "parent_links"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    relation = Column(String(50), default="parent")

    parent = relationship("User", foreign_keys=[parent_id])
    student = relationship("User", foreign_keys=[student_id])


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    action_type = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    is_anonymous = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="surveys")
    questions = relationship("SurveyQuestion", back_populates="survey", cascade="all, delete",
                             order_by="SurveyQuestion.order_num")
    responses = relationship("SurveyResponse", back_populates="survey", cascade="all, delete")


class SurveyQuestion(Base):
    __tablename__ = "survey_questions"
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(SAEnum("text", "multiple_choice", "rating"), nullable=False)
    options = Column(JSON)
    order_num = Column(Integer, default=0)

    survey = relationship("Survey", back_populates="questions")
    answers = relationship("SurveyAnswer", back_populates="question", cascade="all, delete")


class SurveyResponse(Base):
    __tablename__ = "survey_responses"
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # null if anonymous
    submitted_at = Column(DateTime, default=datetime.utcnow)

    survey = relationship("Survey", back_populates="responses")
    answers = relationship("SurveyAnswer", back_populates="response", cascade="all, delete")


class SurveyAnswer(Base):
    __tablename__ = "survey_answers"
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey("survey_responses.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("survey_questions.id"), nullable=False)
    answer_text = Column(Text)

    response = relationship("SurveyResponse", back_populates="answers")
    question = relationship("SurveyQuestion", back_populates="answers")


class PeerReview(Base):
    __tablename__ = "peer_reviews"
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewee_submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    feedback = Column(Text)
    score = Column(Float, nullable=True)
    submitted_at = Column(DateTime, nullable=True)

    assignment = relationship("Assignment")
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    reviewee_submission = relationship("Submission")


class GradeChange(Base):
    __tablename__ = "grade_changes"
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    old_score = Column(Float, nullable=True)
    new_score = Column(Float, nullable=True)
    reason = Column(Text)
    changed_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="grade_changes")
    changer = relationship("User", foreign_keys=[changed_by])


# ═══════════════════════════════════════════════════════════════════════════════
# LEARNING INTELLIGENCE & SOCIAL FEATURES
# ═══════════════════════════════════════════════════════════════════════════════

# ── 1. Spaced Repetition (SM-2 algorithm) ────────────────────────────────────

class SRCard(Base):
    """One flash-card per (student, quiz_question) pair, managed by the SM-2 algorithm."""
    __tablename__ = "sr_cards"
    id            = Column(Integer, primary_key=True)
    student_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id   = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    interval      = Column(Integer, default=1)    # days until next review
    ease_factor   = Column(Float,   default=2.5)  # SM-2 difficulty multiplier
    repetitions   = Column(Integer, default=0)    # consecutive correct recalls
    due_date      = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime)
    last_quality  = Column(Integer)               # 0-5 quality of most recent answer

    student  = relationship("User")
    question = relationship("QuizQuestion")


# ── 2. Teach-it-back ──────────────────────────────────────────────────────────

class TeachBackPrompt(Base):
    """A 'explain this concept in your own words' challenge set by a teacher."""
    __tablename__ = "teach_back_prompts"
    id         = Column(Integer, primary_key=True)
    course_id  = Column(Integer, ForeignKey("courses.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"),  nullable=False)
    concept    = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    course       = relationship("Course")
    teacher      = relationship("User")
    submissions  = relationship("TeachBackSubmission", back_populates="prompt",
                                cascade="all, delete")


class TeachBackSubmission(Base):
    __tablename__ = "teach_back_submissions"
    id           = Column(Integer, primary_key=True)
    prompt_id    = Column(Integer, ForeignKey("teach_back_prompts.id"), nullable=False)
    student_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    explanation  = Column(Text, nullable=False)
    score        = Column(Float)   # teacher-assigned score (0-100)
    feedback     = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    prompt  = relationship("TeachBackPrompt", back_populates="submissions")
    student = relationship("User")
    votes   = relationship("TeachBackVote", back_populates="submission",
                           cascade="all, delete")


class TeachBackVote(Base):
    """Peer upvote on a teach-back submission (one per student per submission)."""
    __tablename__ = "teach_back_votes"
    id            = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey("teach_back_submissions.id"), nullable=False)
    voter_id      = Column(Integer, ForeignKey("users.id"), nullable=False)

    submission = relationship("TeachBackSubmission", back_populates="votes")


# ── 3. Confusion heatmap ──────────────────────────────────────────────────────

class ConfusionSignal(Base):
    """Student presses 'confused' or 'clear' during a live session."""
    __tablename__ = "confusion_signals"
    id         = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    signal     = Column(SAEnum("confused", "clear"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ClassSession")
    student = relationship("User")


# ── 4. Anonymous peer help board ──────────────────────────────────────────────

class HelpPost(Base):
    """A question posted by a student (optionally anonymously) per course."""
    __tablename__ = "help_posts"
    id           = Column(Integer, primary_key=True)
    course_id    = Column(Integer, ForeignKey("courses.id"), nullable=False)
    author_id    = Column(Integer, ForeignKey("users.id"),   nullable=False)
    is_anonymous = Column(Boolean, default=True)
    title        = Column(String(200), nullable=False)
    body         = Column(Text, nullable=False)
    is_resolved  = Column(Boolean, default=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

    course   = relationship("Course")
    author   = relationship("User")
    answers  = relationship("HelpAnswer", back_populates="post", cascade="all, delete")
    votes    = relationship("HelpVote",   back_populates="post", cascade="all, delete")


class HelpAnswer(Base):
    __tablename__ = "help_answers"
    id           = Column(Integer, primary_key=True)
    post_id      = Column(Integer, ForeignKey("help_posts.id"), nullable=False)
    author_id    = Column(Integer, ForeignKey("users.id"),      nullable=False)
    is_anonymous = Column(Boolean, default=False)
    body         = Column(Text, nullable=False)
    is_endorsed  = Column(Boolean, default=False)  # teacher-marked as correct
    created_at   = Column(DateTime, default=datetime.utcnow)

    post   = relationship("HelpPost", back_populates="answers")
    author = relationship("User")
    votes  = relationship("HelpAnswerVote", back_populates="answer", cascade="all, delete")


class HelpVote(Base):
    """Upvote on a question (one per user per post)."""
    __tablename__ = "help_votes"
    id       = Column(Integer, primary_key=True)
    post_id  = Column(Integer, ForeignKey("help_posts.id"), nullable=False)
    voter_id = Column(Integer, ForeignKey("users.id"),      nullable=False)

    post = relationship("HelpPost", back_populates="votes")


class HelpAnswerVote(Base):
    """Upvote on an answer (one per user per answer)."""
    __tablename__ = "help_answer_votes"
    id        = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey("help_answers.id"), nullable=False)
    voter_id  = Column(Integer, ForeignKey("users.id"),        nullable=False)

    answer = relationship("HelpAnswer", back_populates="votes")


# ── 5. Knowledge graph ────────────────────────────────────────────────────────

class Concept(Base):
    """A named concept (e.g. 'Quadratic Equations') that can span multiple courses."""
    __tablename__ = "concepts"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    color       = Column(String(7), default="#2563eb")  # hex for graph node colour

    links_out   = relationship("ConceptLink", foreign_keys="ConceptLink.from_id",
                               back_populates="from_concept", cascade="all, delete")
    links_in    = relationship("ConceptLink", foreign_keys="ConceptLink.to_id",
                               back_populates="to_concept",   cascade="all, delete")
    course_tags = relationship("ConceptCourseTag", back_populates="concept",
                               cascade="all, delete")


class ConceptLink(Base):
    """Directed edge between two concepts (e.g. 'Algebra → Calculus')."""
    __tablename__ = "concept_links"
    id      = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    to_id   = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    label   = Column(String(100), default="relates to")

    from_concept = relationship("Concept", foreign_keys=[from_id], back_populates="links_out")
    to_concept   = relationship("Concept", foreign_keys=[to_id],   back_populates="links_in")


class ConceptCourseTag(Base):
    """Tags a concept as appearing in a specific course."""
    __tablename__ = "concept_course_tags"
    id         = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    course_id  = Column(Integer, ForeignKey("courses.id"),  nullable=False)

    concept = relationship("Concept", back_populates="course_tags")
    course  = relationship("Course")


# ── 6. Study group auto-matcher ───────────────────────────────────────────────

class StudyGroup(Base):
    __tablename__ = "study_groups"
    id              = Column(Integer, primary_key=True)
    course_id       = Column(Integer, ForeignKey("courses.id"), nullable=False)
    name            = Column(String(100), nullable=False)
    is_auto_matched = Column(Boolean, default=False)
    created_at      = Column(DateTime, default=datetime.utcnow)

    course   = relationship("Course")
    members  = relationship("StudyGroupMember", back_populates="group",
                            cascade="all, delete")


class StudyGroupMember(Base):
    __tablename__ = "study_group_members"
    id         = Column(Integer, primary_key=True)
    group_id   = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"),         nullable=False)

    group   = relationship("StudyGroup", back_populates="members")
    student = relationship("User")
