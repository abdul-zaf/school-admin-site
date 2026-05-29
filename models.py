from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Date, Boolean
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
    role = Column(SAEnum("admin", "teacher", "student"), nullable=False, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)

    courses_teaching = relationship("Course", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")
    submissions = relationship("Submission", back_populates="student")
    announcements = relationship("Announcement", back_populates="author")
    quiz_attempts = relationship("QuizAttempt", back_populates="student")


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

    course = relationship("Course", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete")


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
