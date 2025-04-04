from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "05112003"  
app.config["MYSQL_DB"] = "career_tracker"   

mysql = MySQL(app)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# User Dashboard
@app.route("/dashboard")
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template("dashboard.html", users=users)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")   

# Add User Form Submission
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

@app.route("/users", methods=["GET"])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email FROM users")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)

@app.route("/update_user/<int:user_id>", methods=["PUT"])
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

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#CRUD for courses
@app.route("/add_course", methods=["POST"])
def add_course():
    if request.method == "POST":
        course_code = request.form["course_code"]
        course_name = request.form["course_name"]
        credits = request.form["credits"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO courses (course_code, course_name, credits) VALUES (%s, %s, %s)", 
                    (course_code, course_name, credits))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for("courses"))

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route("/courses", methods=["GET"])
def get_courses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()
    cur.close()
    return render_template("courses.html", courses=courses)

@app.route("/update_course/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    try:
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE courses SET course_code = %s, course_name = %s, credits = %s WHERE id = %s",
            (data["course_code"], data["course_name"], data["credits"], course_id),
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Course updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_course/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Course deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#CRUD for grades
@app.route("/grades")
def grades():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT users.name, courses.course_name, grades.grade
        FROM grades
        JOIN users ON grades.user_id = users.user_id
        JOIN courses ON grades.course_id = courses.course_id
    """)
    grades = cur.fetchall()
    cur.close()
    return render_template("grades.html", grades=grades)


@app.route("/add_grade", methods=["POST"])
def add_grade():
    if request.method == "POST":
        user_id = request.form["user_id"]
        course_id = request.form["course_id"]
        grade = request.form["grade"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO grades (user_id, course_id, grade) VALUES (%s, %s, %s)", 
                    (user_id, course_id, grade))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for("grades"))

@app.route("/update_grade/<int:grade_id>", methods=["PUT"])
def update_grade(grade_id):
    try:
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE grades SET grade = %s WHERE id = %s",
            (data["grade"], grade_id),
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Grade updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_grade/<int:grade_id>", methods=["DELETE"])
def delete_grade(grade_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Grade deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#CRUD for CareerRec
@app.route("/careers")
def careers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM careerrecommendations")
    careers = cur.fetchall()
    cur.close()
    return render_template("careers.html", careers=careers)

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

@app.route("/update_career/<int:career_id>", methods=["PUT"])
def update_career(career_id):
    try:
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE careerrecommendations SET career_name = %s, description = %s, min_gpa = %s WHERE id = %s",
            (data["career_name"], data["description"], data["min_gpa"], career_id),
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Career recommendation updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_career/<int:career_id>", methods=["DELETE"])
def delete_career(career_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM careerrecommendations WHERE id = %s", (career_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Career recommendation deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
