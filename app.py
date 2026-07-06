from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key="local-secret-key" 

# MongoDB connection
client=MongoClient("mongodb://localhost:27017/")
db=client["user_db"]
users=db["users"]

# Home (Login Page)
@app.route("/")
def home():
    return render_template("login.html")

# Register Page 
@app.route("/register")
def register():
    return render_template("register.html")

# Register Logic
@app.route("/register_user", methods=["POST"])
def register_user():
    username = request.form["Username"]
    email=request.form["Email"]
    password = request.form["Password"]
    
    # Check if user exists
    if users.find_one({"Username": username}):
        return "User already exists!"

    users.insert_one({"Username": username, "Email":email,"Password": password})
    return redirect("/")

# Login Logic
@app.route("/login", methods=["POST"])
def login():
    username = request.form["Username"]
    password = request.form["Password"]

    user = users.find_one({"Username": username, "Password": password})

    if user:
        session["username"] = username
        return redirect("/dashboard")
    else:
        return "Invalid Login!"

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session["username"])
    return redirect("/")

# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True, use_reloader=False)