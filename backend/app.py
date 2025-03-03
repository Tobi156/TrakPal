from flask import Flask
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


if __name__ == "__main__":
    app.run(debug=True)
