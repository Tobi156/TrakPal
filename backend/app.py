from flask import Flask
from flask import request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "05112003"  
app.config["MYSQL_DB"] = "career_tracker"   

mysql = MySQL(app)

@app.route("/")
def home():
    return "Flask is connected to MariaDB!"

@app.route("/test_db")
def test_db():
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES;")
    tables = cur.fetchall()
    cur.close()
    return f"Tables: {tables}"

#CRUD for users
@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        data = request.json  # Get JSON data from request
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (data["name"], data["email"], data["password"]),
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "User added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        return jsonify({"message": "User updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "User deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
