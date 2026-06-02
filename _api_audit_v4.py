"""
_api_audit_v4.py — Full audit of all NEW endpoints added in the feature batch.
Covers: prerequisites, waitlist, calendar, departments, cohorts, conferences,
        user_sessions, audit, plagiarism, ratings, streaks, xp, library,
        payments, clubs, code_sandbox, ai_tutor, timetable, analytics (new),
        sessions (meeting), assignments (late policy), announcements (scheduled),
        notifications (email prefs), recommendations.

Usage:
    python _api_audit_v4.py http://127.0.0.1:8000
"""

import json, sys, time, urllib.request, urllib.error, urllib.parse
from datetime import datetime, date

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000") + "/api"
PASS, FAIL = [], []

TS = str(int(time.time()))[-6:]   # unique suffix for this run


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _req(method, path, body=None, token=None):
    url = BASE + path
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body is not None else None
    try:
        rq = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(rq, timeout=15) as r:
            raw = r.read().decode(errors="replace")
            try:    return r.status, json.loads(raw) if raw else {}
            except: return r.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:    return e.code, json.loads(raw)
        except: return e.code, raw
    except Exception as e:
        return 0, str(e)


def _form(path, fields, token=None):
    """POST application/x-www-form-urlencoded."""
    url = BASE + path
    data = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in fields.items()).encode()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        rq = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(rq, timeout=15) as r:
            raw = r.read().decode(errors="replace")
            try:    return r.status, json.loads(raw) if raw else {}
            except: return r.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:    return e.code, json.loads(raw)
        except: return e.code, raw
    except Exception as e:
        return 0, str(e)


def chk(name, status, body, expected):
    ok = status in (expected if isinstance(expected, (list, tuple)) else [expected])
    tag = "OK " if ok else "FAIL"
    print(f"  {tag} [{status}] {name}")
    if not ok:
        FAIL.append(f"[{status}] {name} — expected {expected} — body: {str(body)[:200]}")
    else:
        PASS.append(name)
    return ok, status, body


# ── Setup: login users ─────────────────────────────────────────────────────────
print("\n=== SETUP ===")

def login(email, pw):
    s, b = _form("/auth/login", {"username": email, "password": pw})
    if s == 200 and isinstance(b, dict):
        return b.get("access_token")
    return None

admin_tok = login("admin@school.edu", "Admin123")
assert admin_tok, "Admin login failed — is the server running?"

# Create teacher
s, b = _req("POST", "/users/", {"name": f"T4_{TS}", "email": f"t4_{TS}@test.com",
    "password": "Teacher123", "role": "teacher"}, admin_tok)
teacher_id = b.get("id") if s in (200, 201) else None
teacher_tok = login(f"t4_{TS}@test.com", "Teacher123")

# Create student 1
s, b = _req("POST", "/users/", {"name": f"S4a_{TS}", "email": f"s4a_{TS}@test.com",
    "password": "Student123", "role": "student"}, admin_tok)
student1_id = b.get("id") if s in (200, 201) else None
student1_tok = login(f"s4a_{TS}@test.com", "Student123")

# Create student 2
s, b = _req("POST", "/users/", {"name": f"S4b_{TS}", "email": f"s4b_{TS}@test.com",
    "password": "Student123", "role": "student"}, admin_tok)
student2_id = b.get("id") if s in (200, 201) else None
student2_tok = login(f"s4b_{TS}@test.com", "Student123")

# Create parent
s, b = _req("POST", "/users/", {"name": f"P4_{TS}", "email": f"p4_{TS}@test.com",
    "password": "Parent1234", "role": "parent"}, admin_tok)
parent_id = b.get("id") if s in (200, 201) else None
parent_tok = login(f"p4_{TS}@test.com", "Parent1234")

# Create courses
s, b = _req("POST", "/courses/", {"title": f"Course4A_{TS}", "subject": "Math"}, teacher_tok)
course1_id = b.get("id") if s in (200, 201) else None

s, b = _req("POST", "/courses/", {"title": f"Course4B_{TS}", "subject": "Science"}, teacher_tok)
course2_id = b.get("id") if s in (200, 201) else None

# Enroll student 1 in course1
_req("POST", f"/courses/{course1_id}/enroll", {}, student1_tok)

# Create assignment in course1  (path: /assignments/course/{id})
s, b = _req("POST", f"/assignments/course/{course1_id}", {
    "title": f"Assign4_{TS}", "max_score": 100.0,
    "late_penalty_per_day": 5.0, "max_late_days": 3
}, teacher_tok)
assign_id = b.get("id") if s in (200, 201) else None

# Student 1 submits the assignment
s, b = _req("POST", f"/assignments/{assign_id}/submit", {"content": "My answer to this test assignment"}, student1_tok)
sub1_id = b.get("submission_id") if s in (200, 201) else None

# Link parent to student1
_req("POST", "/parents/link", {"student_id": student1_id}, parent_tok)

print(f"  teacher_id={teacher_id}, student1_id={student1_id}, student2_id={student2_id}")
print(f"  parent_id={parent_id}, course1_id={course1_id}, course2_id={course2_id}")
print(f"  assign_id={assign_id}, sub1_id={sub1_id}")


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== PREREQUISITES ===")

# Add prerequisite: course2 requires course1
s, b = _req("POST", "/prerequisites/", {"course_id": course2_id, "prerequisite_course_id": course1_id}, teacher_tok)
prereq_id = b.get("id") if s == 200 else None
chk("Add prerequisite (teacher)", s, b, 200)

# Duplicate
s, b = _req("POST", "/prerequisites/", {"course_id": course2_id, "prerequisite_course_id": course1_id}, teacher_tok)
chk("Add duplicate prereq => 400", s, b, 400)

# Self-reference
s, b = _req("POST", "/prerequisites/", {"course_id": course1_id, "prerequisite_course_id": course1_id}, teacher_tok)
chk("Self-prerequisite => 400", s, b, 400)

# List
s, b = _req("GET", f"/prerequisites/course/{course2_id}", token=student1_tok)
chk("List prerequisites (student)", s, b, 200)

# Student2 tries to enroll in course2 without passing course1
s, b = _req("POST", f"/courses/{course2_id}/enroll", {}, student2_tok)
chk("Enroll blocked by prereq => 400", s, b, 400)

# Grade student1 in assign (so they pass), then enroll in course2 should work
s, b = _req("PUT", f"/assignments/{assign_id}/submissions/{sub1_id}/grade",
            {"score": 80.0, "feedback": "Good"}, teacher_tok)
# Student2 still can't because they have no submission - that's expected

# Delete prerequisite
if prereq_id:
    s, b = _req("DELETE", f"/prerequisites/{prereq_id}", token=teacher_tok)
    chk("Delete prerequisite", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== ENROLLMENT CAPS & WAITLIST ===")

# Set enrollment cap to 1 on course2 (update via admin)
s, b = _req("PUT", f"/courses/{course2_id}", {
    "title": f"Course4B_{TS}", "subject": "Science",
    "enrollment_cap": 1
}, teacher_tok)
chk("Set enrollment cap", s, b, 200)

# Enroll student1 into course2 (fills the cap)
s, b = _req("POST", f"/courses/{course2_id}/enroll", {}, student1_tok)
chk("Enroll student1 (fills cap)", s, b, 200)

# Student2 tries to enroll - should be redirected to waitlist
s, b = _req("POST", f"/courses/{course2_id}/enroll", {}, student2_tok)
chk("Enroll when full => redirected to waitlist (400)", s, b, 400)

# Student2 was auto-added to waitlist when enrollment was blocked — verify
# (Explicit join should now return 400 "already on waitlist")
s, b = _req("POST", f"/waitlist/{course2_id}", token=student2_tok)
chk("Join waitlist again => 400 (already auto-added)", s, b, 400)

# Can't join if already enrolled
s, b = _req("POST", f"/waitlist/{course1_id}", token=student1_tok)
chk("Join waitlist when enrolled => 400", s, b, 400)

# Teacher views waitlist
s, b = _req("GET", f"/waitlist/{course2_id}", token=teacher_tok)
chk("Get waitlist (teacher)", s, b, 200)
waitlist_has_s2 = isinstance(b, list) and len(b) > 0  # student2 auto-added on failed enroll
chk("Waitlist is non-empty (student2 auto-added)", 200 if waitlist_has_s2 else 400, {}, 200)

# Student1 unenrolls from course2 => student2 should be auto-promoted
s, b = _req("DELETE", f"/courses/{course2_id}/enroll", token=student1_tok)
chk("Unenroll triggers waitlist promotion", s, b, 200)

# Verify student2 is now enrolled
s, b = _req("GET", f"/courses/{course2_id}", token=admin_tok)
if s == 200 and isinstance(b, dict):
    enrolled_ids = [st["id"] for st in b.get("students", [])]
    chk("Student2 auto-promoted from waitlist", 200 if student2_id in enrolled_ids else 400, {}, 200)
else:
    chk("Student2 auto-promoted from waitlist", 400, "could not check", 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== ACADEMIC CALENDAR ===")

s, b = _req("POST", "/calendar/", {
    "title": "Summer Break", "event_type": "holiday",
    "start_date": "2026-07-01", "end_date": "2026-07-31"
}, admin_tok)
cal_id = b.get("id") if s == 200 else None
chk("Create calendar event (admin)", s, b, 200)

# Invalid type
s, b = _req("POST", "/calendar/", {
    "title": "Bad", "event_type": "invalid",
    "start_date": "2026-07-01", "end_date": "2026-07-31"
}, admin_tok)
chk("Invalid event_type => 400", s, b, 400)

# End before start
s, b = _req("POST", "/calendar/", {
    "title": "Bad dates", "event_type": "holiday",
    "start_date": "2026-07-31", "end_date": "2026-07-01"
}, admin_tok)
chk("end_date before start_date => 400", s, b, 400)

# Teacher cannot create
s, b = _req("POST", "/calendar/", {
    "title": "T Event", "event_type": "other",
    "start_date": "2026-08-01", "end_date": "2026-08-01"
}, teacher_tok)
chk("Teacher create calendar => 403", s, b, 403)

# List
s, b = _req("GET", "/calendar/", token=student1_tok)
chk("List calendar events (student)", s, b, 200)

# Filter by year/month
s, b = _req("GET", "/calendar/?year=2026&month=7", token=admin_tok)
chk("Filter calendar by year/month", s, b, 200)

if cal_id:
    s, b = _req("PUT", f"/calendar/{cal_id}", {"title": "Summer Holiday"}, admin_tok)
    chk("Update calendar event", s, b, 200)

    s, b = _req("DELETE", f"/calendar/{cal_id}", token=admin_tok)
    chk("Delete calendar event", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== DEPARTMENTS ===")

s, b = _req("POST", "/departments/", {"name": f"Dept4_{TS}", "description": "Math Dept"}, admin_tok)
dept_id = b.get("id") if s == 200 else None
chk("Create department (admin)", s, b, 200)

# Duplicate name
s, b = _req("POST", "/departments/", {"name": f"Dept4_{TS}"}, admin_tok)
chk("Duplicate department name => 400", s, b, 400)

# Teacher can't create
s, b = _req("POST", "/departments/", {"name": f"DeptT_{TS}"}, teacher_tok)
chk("Teacher create dept => 403", s, b, 403)

s, b = _req("GET", "/departments/", token=student1_tok)
chk("List departments (student)", s, b, 200)

if dept_id:
    s, b = _req("GET", f"/departments/{dept_id}", token=student1_tok)
    chk("Get department detail", s, b, 200)

    s, b = _req("POST", f"/departments/{dept_id}/members",
                {"teacher_id": teacher_id, "role": "member"}, admin_tok)
    chk("Add teacher to department", s, b, 200)

    # Add student as teacher — should fail
    s, b = _req("POST", f"/departments/{dept_id}/members",
                {"teacher_id": student1_id, "role": "member"}, admin_tok)
    chk("Add student to dept => 400", s, b, 400)

    # Duplicate
    s, b = _req("POST", f"/departments/{dept_id}/members",
                {"teacher_id": teacher_id, "role": "member"}, admin_tok)
    chk("Add teacher twice => 400", s, b, 400)

    s, b = _req("PUT", f"/departments/{dept_id}", {"description": "Updated"}, admin_tok)
    chk("Update department", s, b, 200)

    s, b = _req("DELETE", f"/departments/{dept_id}/members/{teacher_id}", token=admin_tok)
    chk("Remove dept member", s, b, 200)

    s, b = _req("DELETE", f"/departments/{dept_id}", token=admin_tok)
    chk("Delete department", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== COHORTS ===")

s, b = _req("POST", "/cohorts/", {"name": f"Cohort4_{TS}", "year": 2026}, admin_tok)
cohort_id = b.get("id") if s == 200 else None
chk("Create cohort (admin)", s, b, 200)

# Teacher can list
s, b = _req("GET", "/cohorts/", token=teacher_tok)
chk("List cohorts (teacher)", s, b, 200)

# Student cannot list
s, b = _req("GET", "/cohorts/", token=student1_tok)
chk("Student list cohorts => 403", s, b, 403)

if cohort_id:
    s, b = _req("POST", f"/cohorts/{cohort_id}/members", {"student_id": student1_id}, admin_tok)
    chk("Add student to cohort", s, b, 200)

    # Non-student
    s, b = _req("POST", f"/cohorts/{cohort_id}/members", {"student_id": teacher_id}, admin_tok)
    chk("Add teacher to cohort => 400", s, b, 400)

    # Duplicate
    s, b = _req("POST", f"/cohorts/{cohort_id}/members", {"student_id": student1_id}, admin_tok)
    chk("Add student twice => 400", s, b, 400)

    s, b = _req("GET", f"/cohorts/{cohort_id}", token=teacher_tok)
    chk("Get cohort detail (teacher)", s, b, 200)

    # Bulk enroll cohort into course1
    s, b = _req("POST", f"/cohorts/{cohort_id}/enroll-all/{course1_id}", token=admin_tok)
    chk("Bulk enroll cohort", s, b, 200)

    s, b = _req("PUT", f"/cohorts/{cohort_id}", {"description": "Updated"}, admin_tok)
    chk("Update cohort", s, b, 200)

    s, b = _req("DELETE", f"/cohorts/{cohort_id}/members/{student1_id}", token=admin_tok)
    chk("Remove cohort member", s, b, 200)

    s, b = _req("DELETE", f"/cohorts/{cohort_id}", token=admin_tok)
    chk("Delete cohort", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== CONFERENCES ===")

s, b = _req("POST", "/conferences/slots", {
    "date": "2026-07-15", "start_time": "09:00", "end_time": "09:30"
}, teacher_tok)
slot_id = b.get("id") if s == 200 else None
chk("Create conference slot (teacher)", s, b, 200)

# Student can't create
s, b = _req("POST", "/conferences/slots", {
    "date": "2026-07-15", "start_time": "10:00", "end_time": "10:30"
}, student1_tok)
chk("Student create slot => 403", s, b, 403)

# Parent sees unbooked slots
s, b = _req("GET", "/conferences/slots", token=parent_tok)
chk("Parent list slots", s, b, 200)

# Teacher sees own slots
s, b = _req("GET", "/conferences/slots", token=teacher_tok)
chk("Teacher list own slots", s, b, 200)

if slot_id:
    # Parent books slot
    s, b = _req("POST", f"/conferences/book/{slot_id}",
                {"student_id": student1_id, "notes": "About Math grade"}, parent_tok)
    booking_id = b.get("id") if s == 200 else None
    chk("Parent book slot", s, b, 200)

    # Double-book
    s2b, b2b = _req("POST", f"/conferences/book/{slot_id}",
                    {"student_id": student1_id}, parent_tok)
    chk("Double-book slot => 400", s2b, b2b, 400)

    s, b = _req("GET", "/conferences/my-bookings", token=parent_tok)
    chk("Parent get own bookings", s, b, 200)

    s, b = _req("GET", "/conferences/teacher-bookings", token=teacher_tok)
    chk("Teacher get bookings", s, b, 200)

    # Parent tries to book without linked student
    s, b = _req("POST", f"/conferences/book/{slot_id}",
                {"student_id": student2_id}, parent_tok)
    chk("Book unlinked student => 403", s, b, [403, 400])

    # Can't delete a booked slot
    s, b = _req("DELETE", f"/conferences/slots/{slot_id}", token=teacher_tok)
    chk("Delete booked slot => 400", s, b, 400)

    if booking_id:
        s, b = _req("DELETE", f"/conferences/bookings/{booking_id}", token=parent_tok)
        chk("Cancel booking (parent)", s, b, 200)

    # Now can delete
    s, b = _req("DELETE", f"/conferences/slots/{slot_id}", token=teacher_tok)
    chk("Delete unbooked slot (teacher)", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== USER SESSIONS ===")

s, b = _req("GET", "/user-sessions/", token=admin_tok)
chk("List own sessions (admin)", s, b, 200)

s, b = _req("GET", "/user-sessions/", token=student1_tok)
chk("List own sessions (student)", s, b, 200)

s, b = _req("DELETE", "/user-sessions/all", token=admin_tok)
chk("Revoke all other sessions", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== AUDIT LOG ===")

s, b = _req("GET", "/audit/", token=admin_tok)
chk("Get audit log (admin)", s, b, 200)

s, b = _req("GET", "/audit/?limit=5&offset=0", token=admin_tok)
chk("Audit log with pagination", s, b, 200)

s, b = _req("GET", "/audit/", token=teacher_tok)
chk("Teacher get audit log => 403", s, b, 403)

s, b = _req("GET", "/audit/my", token=student1_tok)
chk("My activity log (student)", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== PLAGIARISM ===")

# Need a second submission for plagiarism to work
s, b = _req("POST", f"/courses/{course1_id}/enroll", {}, student2_tok)
_req("POST", f"/assignments/{assign_id}/submit",
     {"content": "My answer to this test assignment"}, student2_tok)

s, b = _req("POST", f"/plagiarism/check/{assign_id}", token=teacher_tok)
chk("Run plagiarism check (teacher)", s, b, 200)

s, b = _req("GET", f"/plagiarism/{assign_id}", token=teacher_tok)
chk("Get plagiarism reports (teacher)", s, b, 200)

s, b = _req("POST", f"/plagiarism/check/{assign_id}", token=student1_tok)
chk("Student run plagiarism => 403", s, b, 403)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== RATINGS ===")

# Student must be enrolled to rate
s, b = _req("POST", f"/ratings/course/{course1_id}",
            {"rating": 5, "review": "Great course!"}, student1_tok)
rating_id = b.get("id") if s == 200 else None
chk("Student rate enrolled course", s, b, 200)

# Update rating (same endpoint)
s, b = _req("POST", f"/ratings/course/{course1_id}",
            {"rating": 4, "review": "Updated review"}, student1_tok)
chk("Update rating (idempotent)", s, b, 200)

# Invalid rating range
s, b = _req("POST", f"/ratings/course/{course1_id}",
            {"rating": 6}, student1_tok)
chk("Rating out of range => 422", s, b, 422)

# Not enrolled student
s, b = _req("POST", f"/ratings/course/{course2_id}",
            {"rating": 3}, student1_tok)
chk("Rate unenrolled course => 400", s, b, 400)

# List ratings (anyone)
s, b = _req("GET", f"/ratings/course/{course1_id}", token=admin_tok)
chk("List course ratings", s, b, 200)

if rating_id:
    s, b = _req("DELETE", f"/ratings/{rating_id}", token=student1_tok)
    chk("Delete own rating (student)", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== STREAKS ===")

s, b = _req("GET", "/streaks/my", token=student1_tok)
chk("Get own streak (student)", s, b, 200)

s, b = _req("GET", "/streaks/my", token=teacher_tok)
chk("Teacher get streak => 403", s, b, 403)

s, b = _req("GET", "/streaks/leaderboard", token=admin_tok)
chk("Streak leaderboard (admin)", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== XP SYSTEM ===")

s, b = _req("GET", "/xp/my", token=student1_tok)
chk("Get own XP (student)", s, b, 200)

s, b = _req("GET", "/xp/leaderboard", token=student1_tok)
chk("XP leaderboard (any auth)", s, b, 200)

s, b = _req("GET", f"/xp/{student1_id}", token=teacher_tok)
chk("Teacher get student XP", s, b, 200)

s, b = _req("GET", f"/xp/{student1_id}", token=student1_tok)
chk("Student get own XP via user_id => 403", s, b, 403)

s, b = _req("GET", "/xp/999999", token=teacher_tok)
chk("XP for nonexistent user => 404", s, b, 404)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== LIBRARY ===")

s, b = _req("POST", "/library/", {
    "title": f"Book4_{TS}", "author": "Author A",
    "isbn": f"978-{TS}", "category": "Science", "total_copies": 2
}, admin_tok)
book_id = b.get("id") if s == 200 else None
chk("Add book (admin)", s, b, 200)

# Teacher can't add
s, b = _req("POST", "/library/", {
    "title": "T Book", "author": "T Author", "category": "Math"
}, teacher_tok)
chk("Teacher add book => 403", s, b, 403)

# List books (any auth)
s, b = _req("GET", "/library/", token=student1_tok)
chk("List books (student)", s, b, 200)

# Search
s, b = _req("GET", f"/library/?q=Book4_{TS}", token=admin_tok)
chk("Search books", s, b, 200)

if book_id:
    s, b = _req("GET", f"/library/{book_id}", token=student1_tok)
    chk("Get book detail", s, b, 200)

    s, b = _req("POST", f"/library/{book_id}/borrow", token=student1_tok)
    borrow_id = b.get("id") if s == 200 else None
    chk("Borrow book (student)", s, b, 200)

    # Double-borrow
    s, b = _req("POST", f"/library/{book_id}/borrow", token=student1_tok)
    chk("Double-borrow => 400", s, b, 400)

    # My borrows
    s, b = _req("GET", "/library/my-borrows", token=student1_tok)
    chk("Get my borrows (student)", s, b, 200)

    # Admin all borrows
    s, b = _req("GET", "/library/borrows", token=admin_tok)
    chk("Admin all borrows", s, b, 200)

    if borrow_id:
        # Renew
        s, b = _req("POST", f"/library/borrows/{borrow_id}/renew", token=student1_tok)
        chk("Renew borrow", s, b, 200)

        # Return
        s, b = _req("POST", f"/library/borrows/{borrow_id}/return", token=student1_tok)
        chk("Return book", s, b, 200)

        # Double-return
        s, b = _req("POST", f"/library/borrows/{borrow_id}/return", token=student1_tok)
        chk("Double-return => 400", s, b, 400)

    # Update book
    s, b = _req("PUT", f"/library/{book_id}", {"total_copies": 3}, admin_tok)
    chk("Update book", s, b, 200)

    # Delete book
    s, b = _req("DELETE", f"/library/{book_id}", token=admin_tok)
    chk("Delete book (admin)", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== PAYMENTS ===")

s, b = _req("POST", "/payments/invoices", {
    "student_id": student1_id, "title": f"Tuition_{TS}", "amount": 500.0
}, admin_tok)
invoice_id = b.get("id") if s == 200 else None
chk("Create invoice (admin)", s, b, 200)

# Invalid student
s, b = _req("POST", "/payments/invoices", {
    "student_id": teacher_id, "title": "Bad", "amount": 100.0
}, admin_tok)
chk("Invoice for teacher => 400", s, b, 400)

# Teacher list
s, b = _req("GET", "/payments/invoices", token=teacher_tok)
chk("Teacher list invoices", s, b, 200)

# Student list own
s, b = _req("GET", "/payments/invoices", token=student1_tok)
chk("Student list own invoices", s, b, 200)

# Student get own invoice
if invoice_id:
    s, b = _req("GET", f"/payments/invoices/{invoice_id}", token=student1_tok)
    chk("Student get own invoice", s, b, 200)

    # Student2 can't get student1's invoice
    s, b = _req("GET", f"/payments/invoices/{invoice_id}", token=student2_tok)
    chk("Student2 get student1 invoice => 403", s, b, 403)

    # Record payment
    s, b = _req("POST", f"/payments/invoices/{invoice_id}/pay", {
        "amount_paid": 500.0, "payment_method": "card"
    }, admin_tok)
    chk("Record payment", s, b, 200)
    chk("Invoice status is paid", 200 if isinstance(b, dict) and b.get("invoice_status") == "paid" else 400, {}, 200)

    # Update paid invoice
    s, b = _req("PUT", f"/payments/invoices/{invoice_id}", {"title": "Updated"}, admin_tok)
    chk("Update invoice", s, b, 200)

    # Can't delete paid invoice
    s, b = _req("DELETE", f"/payments/invoices/{invoice_id}", token=admin_tok)
    chk("Delete paid invoice => 400", s, b, 400)

s, b = _req("GET", "/payments/my", token=student1_tok)
chk("Student my invoices", s, b, 200)

s, b = _req("GET", "/payments/summary", token=admin_tok)
chk("Payment summary (admin)", s, b, 200)

s, b = _req("GET", "/payments/summary", token=teacher_tok)
chk("Teacher payment summary => 403", s, b, 403)

# Create unpaid invoice and delete it
s, b = _req("POST", "/payments/invoices", {
    "student_id": student1_id, "title": f"Delete_{TS}", "amount": 10.0
}, admin_tok)
if s == 200:
    del_inv_id = b.get("id")
    s2, b2 = _req("DELETE", f"/payments/invoices/{del_inv_id}", token=admin_tok)
    chk("Delete unpaid invoice", s2, b2, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== CLUBS ===")

s, b = _req("POST", "/clubs/", {
    "name": f"Club4_{TS}", "description": "A test club", "is_open": True
}, teacher_tok)
club_id = b.get("id") if s == 200 else None
chk("Create club (teacher)", s, b, 200)

s, b = _req("GET", "/clubs/", token=student1_tok)
chk("List clubs (student)", s, b, 200)

if club_id:
    s, b = _req("GET", f"/clubs/{club_id}", token=student1_tok)
    chk("Get club detail", s, b, 200)

    # Student joins
    s, b = _req("POST", f"/clubs/{club_id}/join", token=student1_tok)
    chk("Student join club", s, b, 200)

    # Double-join
    s, b = _req("POST", f"/clubs/{club_id}/join", token=student1_tok)
    chk("Double-join => 400", s, b, 400)

    # Create post as member
    s, b = _req("POST", f"/clubs/{club_id}/posts",
                {"title": "Test post", "content": "Hello club!"}, student1_tok)
    post_id = b.get("id") if s == 200 else None
    chk("Club member creates post", s, b, 200)

    # Non-member can't post
    s, b = _req("POST", f"/clubs/{club_id}/posts",
                {"title": "Outsider", "content": "Hi"}, student2_tok)
    chk("Non-member post => 403", s, b, 403)

    # List posts
    s, b = _req("GET", f"/clubs/{club_id}/posts", token=admin_tok)
    chk("List club posts", s, b, 200)

    if post_id:
        s, b = _req("DELETE", f"/clubs/{club_id}/posts/{post_id}", token=student1_tok)
        chk("Delete own post", s, b, 200)

    # Student leaves
    s, b = _req("DELETE", f"/clubs/{club_id}/leave", token=student1_tok)
    chk("Student leave club", s, b, 200)

    # Update club
    s, b = _req("PUT", f"/clubs/{club_id}", {"is_open": False}, teacher_tok)
    chk("Update club (teacher)", s, b, 200)

    # Student can't join closed club
    s, b = _req("POST", f"/clubs/{club_id}/join", token=student1_tok)
    chk("Join closed club => 400", s, b, 400)

    # Delete
    s, b = _req("DELETE", f"/clubs/{club_id}", token=admin_tok)
    chk("Delete club (admin)", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== CODE SANDBOX ===")

s, b = _req("POST", "/sandbox/run", {
    "language": "python",
    "code": "print('hello world')\nx = 2 + 2\nprint(x)"
}, student1_tok)
chk("Run valid Python code", s, b, 200)
if s == 200 and isinstance(b, dict):
    chk("stdout contains 'hello world'", 200 if "hello" in b.get("stdout", "") else 400, {}, 200)
    chk("exit_code is 0", 200 if b.get("exit_code") == 0 else 400, {}, 200)

# With stdin
s, b = _req("POST", "/sandbox/run", {
    "language": "python",
    "code": "name = input()\nprint('Hello,', name)",
    "stdin": "World"
}, student1_tok)
chk("Python with stdin", s, b, 200)

# Syntax error
s, b = _req("POST", "/sandbox/run", {
    "language": "python",
    "code": "this is not valid python!!!"
}, student1_tok)
chk("Syntax error => exit_code != 0", 200 if s == 200 and isinstance(b, dict) and b.get("exit_code") != 0 else 400, {}, 200)

# Dangerous import blocked
s, b = _req("POST", "/sandbox/run", {
    "language": "python", "code": "import os\nprint(os.getcwd())"
}, student1_tok)
chk("Dangerous import blocked => 400", s, b, 400)

# Unsupported language
s, b = _req("POST", "/sandbox/run", {
    "language": "javascript", "code": "console.log('hi')"
}, student1_tok)
chk("Unsupported language => 400", s, b, 400)

# Teacher can't run code
s, b = _req("POST", "/sandbox/run", {
    "language": "python", "code": "print('hi')"
}, teacher_tok)
chk("Teacher run sandbox => 403", s, b, 403)

# History
s, b = _req("GET", "/sandbox/history", token=student1_tok)
chk("Student code history", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== AI TUTOR (Ollama status only — won't test chat without Ollama) ===")

s, b = _req("GET", "/ai-tutor/status", token=student1_tok)
chk("AI tutor status endpoint", s, b, 200)

# Create session (Ollama doesn't need to be running for this)
s, b = _req("POST", "/ai-tutor/sessions", {
    "course_id": course1_id, "title": "Test Session"
}, student1_tok)
tutor_session_id = b.get("id") if s == 200 else None
chk("Create tutor session", s, b, 200)

# List sessions
s, b = _req("GET", "/ai-tutor/sessions", token=student1_tok)
chk("List tutor sessions", s, b, 200)

# Teacher can't create tutor session
s, b = _req("POST", "/ai-tutor/sessions", {"title": "T session"}, teacher_tok)
chk("Teacher create tutor session => 403", s, b, 403)

if tutor_session_id:
    # Get messages
    s, b = _req("GET", f"/ai-tutor/sessions/{tutor_session_id}/messages", token=student1_tok)
    chk("Get tutor session messages", s, b, 200)

    # Send message — expect 200 (Ollama running), 503 (not configured),
    # or 0 (timeout = first inference is loading model, which takes >15s)
    s, b = _req("POST", f"/ai-tutor/sessions/{tutor_session_id}/messages",
                {"content": "What is 2+2?"}, student1_tok)
    chk("Send tutor message (200/503/timeout ok)", s, b, [200, 503, 0])

    # Delete session
    s, b = _req("DELETE", f"/ai-tutor/sessions/{tutor_session_id}", token=student1_tok)
    chk("Delete tutor session", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== TIMETABLE ===")

s, b = _req("POST", "/timetable/", {
    "course_id": course1_id, "day_of_week": 0,
    "start_time": "09:00", "end_time": "10:00", "room": "101"
}, teacher_tok)
slot_id2 = b.get("id") if s == 200 else None
chk("Add timetable slot (teacher)", s, b, 200)

# Invalid day
s, b = _req("POST", "/timetable/", {
    "course_id": course1_id, "day_of_week": 9,
    "start_time": "09:00", "end_time": "10:00"
}, teacher_tok)
chk("Invalid day_of_week => 400", s, b, 400)

# List for course
s, b = _req("GET", f"/timetable/course/{course1_id}", token=student1_tok)
chk("Course timetable (student)", s, b, 200)

# Personal timetable
s, b = _req("GET", "/timetable/my", token=student1_tok)
chk("My timetable (student)", s, b, 200)

s, b = _req("GET", "/timetable/my", token=teacher_tok)
chk("My timetable (teacher)", s, b, 200)

if slot_id2:
    s, b = _req("PUT", f"/timetable/{slot_id2}", {"room": "202"}, teacher_tok)
    chk("Update timetable slot", s, b, 200)

    s, b = _req("DELETE", f"/timetable/{slot_id2}", token=teacher_tok)
    chk("Delete timetable slot", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== ENHANCED ANALYTICS ===")

s, b = _req("GET", "/analytics/at-risk", token=admin_tok)
chk("At-risk students (admin)", s, b, 200)

s, b = _req("GET", f"/analytics/at-risk?course_id={course1_id}", token=teacher_tok)
chk("At-risk by course (teacher)", s, b, 200)

s, b = _req("GET", "/analytics/at-risk", token=student1_tok)
chk("Student at-risk => 403", s, b, 403)

s, b = _req("GET", "/analytics/teacher-performance", token=admin_tok)
chk("Teacher performance (admin)", s, b, 200)

s, b = _req("GET", "/analytics/teacher-performance", token=teacher_tok)
chk("Teacher performance by teacher => 403", s, b, 403)

s, b = _req("GET", f"/analytics/course-effectiveness/{course1_id}", token=teacher_tok)
chk("Course effectiveness (teacher)", s, b, 200)

# CSV export: gradebook
s, b = _req("GET", f"/analytics/export/gradebook/{course1_id}", token=teacher_tok)
chk("Export gradebook CSV", s, b, 200)

# CSV export: attendance
s, b = _req("GET", f"/analytics/export/attendance/{course1_id}", token=teacher_tok)
chk("Export attendance CSV", s, b, 200)

# PDF transcript
s, b = _req("GET", f"/analytics/export/transcript/{student1_id}", token=admin_tok)
chk("Export transcript PDF (admin)", s, b, 200)

s, b = _req("GET", f"/analytics/export/transcript/{student1_id}", token=teacher_tok)
chk("Teacher export transcript => 403", s, b, 403)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== SESSION MEETING LINKS ===")

# Create a class session first
s, b = _req("POST", f"/sessions/course/{course1_id}", {
    "title": f"Session4_{TS}",
    "session_type": "virtual", "date": "2026-07-15T09:00:00"
}, teacher_tok)
class_session_id = b.get("id") if s in (200, 201) else None
chk("Create class session", s, b, [200, 201])

if class_session_id:
    s, b = _req("POST", f"/sessions/{class_session_id}/meeting",
                {"meeting_url": "https://zoom.us/j/123456", "provider": "zoom"}, teacher_tok)
    chk("Set meeting URL (teacher)", s, b, 200)

    s, b = _req("GET", f"/sessions/{class_session_id}/meeting", token=student1_tok)
    chk("Get meeting URL (student)", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== ANNOUNCEMENT SCHEDULING ===")

# Published immediately
s, b = _req("POST", "/announcements/", {
    "title": "Live Now", "content": "This is live",
    "course_id": course1_id
}, teacher_tok)
chk("Create immediate announcement", s, b, [200, 201])

# Scheduled in future (draft)
s, b = _req("POST", "/announcements/", {
    "title": "Future Ann", "content": "Coming soon",
    "course_id": course1_id,
    "publish_at": "2030-01-01T00:00:00"
}, teacher_tok)
future_ann_id = b.get("id") if s in (200, 201) else None
chk("Create scheduled announcement (draft)", s, b, [200, 201])

if future_ann_id:
    # Student should not see it in the list
    s, b = _req("GET", f"/announcements/?course_id={course1_id}", token=student1_tok)
    if s == 200 and isinstance(b, list):
        ids = [a.get("id") for a in b]
        chk("Draft announcement hidden from student", 200 if future_ann_id not in ids else 400, {}, 200)
    else:
        chk("Draft announcement hidden from student", s, b, 200)

    # Teacher sees it
    s, b = _req("GET", f"/announcements/?course_id={course1_id}", token=teacher_tok)
    if s == 200 and isinstance(b, list):
        ids = [a.get("id") for a in b]
        chk("Draft announcement visible to teacher", 200 if future_ann_id in ids else 400, {}, 200)
    else:
        chk("Draft announcement visible to teacher", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== NOTIFICATION EMAIL PREFERENCES ===")

s, b = _req("PATCH", "/notifications/email-preferences", {"email_notifications": False}, student1_tok)
chk("Toggle email off (student)", s, b, 200)

s, b = _req("PATCH", "/notifications/email-preferences", {"email_notifications": True}, student1_tok)
chk("Toggle email on (student)", s, b, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== RECOMMENDATIONS ===")

s, b = _req("GET", "/recommendations/my", token=student1_tok)
chk("Get my recommendations (student)", s, b, 200)

s, b = _req("POST", f"/recommendations/generate/{course1_id}", token=teacher_tok)
chk("Generate recommendations (teacher)", s, b, 200)

# Admin only endpoint check
s, b = _req("GET", "/recommendations/my", token=teacher_tok)
chk("Teacher my recommendations => 403", s, b, 403)

# Dismiss (if any recs exist)
s, b = _req("GET", "/recommendations/my", token=student1_tok)
if s == 200 and isinstance(b, list) and len(b) > 0:
    rec_id = b[0].get("id")
    if rec_id:
        s2, b2 = _req("POST", f"/recommendations/{rec_id}/dismiss", token=student1_tok)
        chk("Dismiss recommendation", s2, b2, 200)
else:
    print("  -- (no recommendations to dismiss)")


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== LATE SUBMISSION POLICY ===")

# Create assignment with late penalty
s, b = _req("POST", f"/assignments/course/{course1_id}", {
    "title": f"LateAssign_{TS}",
    "max_score": 100.0,
    "due_date": "2026-05-01T00:00:00",  # ~1 month ago — late but within 60-day max
    "late_penalty_per_day": 10.0,
    "max_late_days": 60,               # allow up to 60 days late
    "allow_resubmission": True,
    "max_submissions": 3
}, teacher_tok)
late_assign_id = b.get("id") if s in (200, 201) else None
chk("Create assignment with late policy", s, b, [200, 201])

if late_assign_id:
    # Student submits (late)
    s, b = _req("POST", f"/assignments/{late_assign_id}/submit",
                {"content": "Late submission"}, student1_tok)
    late_sub_id = b.get("submission_id") if s in (200, 201) else None
    chk("Submit late assignment", s, b, [200, 201])

    # Resubmit (allowed)
    s, b = _req("POST", f"/assignments/{late_assign_id}/submit",
                {"content": "Resubmission"}, student1_tok)
    chk("Resubmit when allowed", s, b, [200, 201])

    if late_sub_id:
        # Grade — should apply late penalty
        s, b = _req("PUT", f"/assignments/{late_assign_id}/submissions/{late_sub_id}/grade",
                    {"score": 90.0}, teacher_tok)
        chk("Grade applies late penalty", s, b, 200)
        if s == 200 and isinstance(b, dict):
            # Score should be < 90 due to late penalty
            final = b.get("score", 90)
            chk("Late penalty reduces score", 200 if final < 90 else 400, {}, 200)


# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== CLEANUP ===")

# Delete test users (cascades everything)
for uid in [teacher_id, student1_id, student2_id, parent_id]:
    if uid:
        s, b = _req("DELETE", f"/users/{uid}", token=admin_tok)

# Delete test courses
for cid in [course1_id, course2_id]:
    if cid:
        s, b = _req("DELETE", f"/courses/{cid}", token=admin_tok)

print("  Cleanup done")


# ═══════════════════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
total = len(PASS) + len(FAIL)
print(f"RESULTS: {len(PASS)}/{total} passed   {len(FAIL)} FAILED")
if FAIL:
    print("\nFAILED:")
    for f in FAIL:
        print(f"  FAIL: {f}")
else:
    print("All tests passed!")
