from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from MySQLdb.cursors import DictCursor
from functools import wraps

# Decorator to ensure user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to view this page.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to ensure user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to view this page.")
            return redirect(url_for("login"))
        if not session.get("is_admin"):
            flash("Access denied: Admins only.")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'trakpal'

# Database Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "05112003"
app.config["MYSQL_DB"] = "career_tracker"

# Initialize MySQL
mysql = MySQL(app)

# Home Page - Requires login
@app.route("/")
@login_required
def home():
    user_id = session["user_id"]
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch user information
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    major = user['major'] if user else None

    # Fetch grades for GPA calculation
    cur.execute("""
        SELECT grade
        FROM grades
        WHERE user_id = %s
    """, (user_id,))
    grades = cur.fetchall()

    # Grade points mapping
    GRADE_POINTS = {
        'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0,
        'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'F': 0.0
    }
    total_points = 0
    total_courses = 0
    for row in grades:
        grade = row['grade']
        if grade in GRADE_POINTS:
            total_points += GRADE_POINTS[grade]
            total_courses += 1

    # Calculate average grade
    avg_grade = round(total_points / total_courses, 2) if total_courses > 0 else None

    # Fetch career recommendations based on GPA
    if avg_grade is not None:
        cur.execute("""
            SELECT cr.*
            FROM careerrecommendations cr
            JOIN careermatches cm ON cr.career_id = cm.career_id
            WHERE cm.major = %s AND cr.min_gpa <= %s
        """, (major, avg_grade))
        careers = cur.fetchall()
    else:
        careers = []

    cur.close()
    stats = {
        "total_courses": total_courses,
        "avg_grade": avg_grade
    }
    return render_template("index.html", user=user, stats=stats, careers=careers)

# Dashboard - Requires login and admin privileges
@app.route("/dashboard")
@login_required
@admin_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template("dashboard.html", users=users)

# Signup page - Handles both GET and POST requests
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        major = request.form.get("major", "")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password_hash, major) VALUES (%s, %s, %s, %s)",
                    (name, email, password, major))
        mysql.connection.commit()
        cur.close()
        flash("Account created! You can now log in.")
        return redirect(url_for("login"))
    return render_template("signup.html")

# Login page - Handles both GET and POST requests
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["name"] = user[1]
            session["is_admin"] = user[6]
            flash("Logged in successfully!")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials.")
    return render_template("login.html")

# Logout route 
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("login"))

# Add User (Admin only)
@app.route("/add_user", methods=["POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("dashboard"))

# Get Users (Admin only) - Returns JSON of users
@app.route("/users", methods=["GET"])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email FROM users")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)

# Update User (Admin only) 
@app.route("/update_user/<int:user_id>", methods=["POST"])
def update_user(user_id):
    try:
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE users SET name = %s, email = %s WHERE id = %s",
            (data["name"], data["email"], user_id),
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete User (Admin only)
@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Courses page - Requires login
@app.route("/courses")
@login_required
def courses():
    user_id = session["user_id"]
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Get the user's major
    cur.execute("SELECT major FROM users WHERE user_id = %s", (user_id,))
    user_major_result = cur.fetchone()
    user_major = user_major_result["major"] if user_major_result else None

    # Get user's entered courses
    cur.execute("""
        SELECT course_id, course_code, course_name, credits, difficulty_level
        FROM courses
        WHERE user_id = %s
    """, (user_id,))
    courses = cur.fetchall()

    # Get required courses for the user's major
    missing_courses = []
    if user_major:
        cur.execute("""
            SELECT course_code, course_name
            FROM requiredcourses
            WHERE major = %s
            AND course_code NOT IN (
                SELECT course_code FROM courses WHERE user_id = %s
            )
        """, (user_major, user_id))
        missing_courses = cur.fetchall()

    cur.close()
    return render_template(
        "courses.html",
        courses=courses,
        missing_courses=missing_courses,
        user_major=user_major
    )

# Add Course 
@app.route("/add_course", methods=["POST"])
@login_required
def add_course():
    course_code = request.form["course_code"]
    course_name = request.form["course_name"]
    credits = request.form["credits"]
    difficulty_level = request.form["difficulty_level"]
    user_id = session["user_id"]
    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO courses (course_code, course_name, credits, difficulty_level, user_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (course_code, course_name, credits, difficulty_level, user_id),
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('courses'))

# Update Course 
@app.route('/update_course/<int:course_id>', methods=['POST'])
@login_required
def update_course(course_id):
    name = request.form['course_name']
    code = request.form['course_code']
    credits = request.form['credits']
    difficulty = request.form['difficulty_level']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Courses
        SET course_name = %s, course_code = %s, credits = %s, difficulty_level = %s
        WHERE course_id = %s AND user_id = %s
    """, (name, code, credits, difficulty, course_id, session['user_id']))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('courses'))

# Delete Course
@app.route("/delete_course/<int:course_id>", methods=["POST"])
@login_required
def delete_course(course_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('courses'))

# Grades page 
@app.route('/grades')
@login_required
def grades():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Include g.grade_id in SELECT
    cur.execute("""
        SELECT g.grade_id, u.name, c.course_name, g.grade, c.course_code
        FROM Grades g
        JOIN Users u ON g.user_id = u.user_id
        JOIN Courses c ON g.course_id = c.course_id
        WHERE g.user_id = %s
    """, (session['user_id'],))
    grades = cur.fetchall()

    cur.execute("""
        SELECT course_id, course_name, course_code
        FROM Courses
        WHERE user_id = %s
    """, (session['user_id'],))
    courses = cur.fetchall()

    cur.close()
    return render_template("grades.html", grades=grades, user_courses=courses)

# Add Grade 
@app.route('/add_grade', methods=['POST'])
@login_required
def add_grade():
    course_id = request.form['course_id']
    grade = request.form['grade']
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Grades (user_id, course_id, grade)
        VALUES (%s, %s, %s)
    """, (session['user_id'], course_id, grade))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('grades'))

# Update Grade 
@app.route('/update_grade/<int:grade_id>', methods=['POST'])
@login_required
def update_grade(grade_id):
    grade = request.form['grade']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Grades SET grade = %s WHERE grade_id = %s AND user_id = %s", (grade, grade_id, session['user_id']))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('grades'))

# Delete Grade
@app.route("/delete_grade/<int:grade_id>", methods=["POST"])
@login_required
def delete_grade(grade_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM grades WHERE grade_id = %s", (grade_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('grades'))

# Careers page 
@app.route("/careers")
@login_required
def careers():
    user_id = session["user_id"]
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch user major
    cur.execute("SELECT major FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    major = user['major'] if user else None

    # Fetch all grades for user
    cur.execute("""
        SELECT grade
        FROM grades
        WHERE user_id = %s
    """, (user_id,))
    grades = cur.fetchall()

    # Mapping letter grades to grade points
    GRADE_POINTS = {
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'F': 0.0
    }
    total_points = 0
    total_courses = 0
    for grade_row in grades:
        grade_letter = grade_row['grade']
        if grade_letter in GRADE_POINTS:
            total_points += GRADE_POINTS[grade_letter]
            total_courses += 1

    # Calculate GPA
    gpa = round(total_points / total_courses, 2) if total_courses > 0 else 0.0

    # Fetch careers matching GPA and Major
    careers = []
    if major:
        cur.execute("""
            SELECT cr.*
            FROM careerrecommendations cr
            JOIN careermatches cm ON cr.career_id = cm.career_id
            WHERE LOWER(cm.major) = LOWER(%s) AND cr.min_gpa <= %s
        """, (major, gpa))
        careers = cur.fetchall()
    else:
        cur.execute("""
            SELECT cr.*
            FROM careerrecommendations cr
            WHERE cr.min_gpa <= %s
        """, (gpa,))
        careers = cur.fetchall()
    cur.close()
    return render_template("careers.html", careers=careers, gpa=gpa)

# Add Career (Admin only) 
@app.route("/add_career", methods=["POST"])
def add_career():
    if request.method == "POST":
        career_name = request.form["career_name"]
        description = request.form["description"]
        min_gpa = request.form["min_gpa"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO careerrecommendations (career_name, description, min_gpa) VALUES (%s, %s, %s)",
                    (career_name, description, min_gpa))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("careers"))

# Browse all careers
@app.route('/careers/all')
@login_required
def browse_all_careers():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM CareerRecommendations")
    all_careers = cur.fetchall()
    cur.close()
    return render_template('browse_careers.html', careers=all_careers)

# Career detail page
@app.route('/career/<int:career_id>')
@login_required
def career_detail(career_id):
    from_page = request.args.get('from_page', 'all')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM careerrecommendations WHERE career_id = %s", (career_id,))
    career = cur.fetchone()
    cur.execute("SELECT major FROM careermatches WHERE career_id = %s", (career_id,))
    majors = [row['major'] for row in cur.fetchall()]
    cur.close()
    if career:
        return render_template('career_detail.html', career=career, majors=majors, from_page=from_page)
    else:
        return "Career not found", 404

if __name__ == "__main__":
    app.run(debug=True)
