# from flask import Flask, jsonify, request, render_template,redirect, url_for, session, flash
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# import config

# # app = Flask(__name__)
# # app.config["MONGO_URI"] = config.MONGO_URI
# # mongo = PyMongo(app)
# # db = mongo.db[config.DB_NAME]

# app = Flask(__name__)
# app.config["MONGO_URI"] = config.MONGO_URI  # Must be exactly like this

# mongo = PyMongo(app)  # Now PyMongo knows the URI

# db = mongo.db  # This is your DB object

# @app.route('/')
# def index():
#     issues = db.issues.find()
#     return render_template('index.html', issues = issues)

# #login and signup

# @app.route('/signup', methods = ['GET', 'POST'] )
# def signup():
#     if request.method == 'POST':
#         username =request.form['username']
#         password = request.form['password']
#         role = request.form.get('role','user')

#         if db.users.find_one({'username': username}):
#             flash("Username already exists", "warning")
#             return redirect(url_for('signup'))
        
#     hashed_pw = generate_password_hash(password)
#     db.users.insert_one({
#         'username': username,
#         'password': hashed_pw,
#         'role': role
#     })
#     flash("account created :) login", "success")
#     return redirect(url_for('login'))
#     return render_template('login.html', signup=True)


# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = db.users.find_one({'username': username})

#     if user and check_password_hash(user['password'], password):
#         session['username'] = username
#         session['role'] = user['role']
#         flash(f"welcome {username}", "success ")

#         if user['role'] == 'admin':
#             return redirect(url_for('admin_dashboard'))
#         else:
#             return redirect(url_for('index'))   
#     else:
#         flash("invalid credentials", "danger")
#         return render_template('login.html') 
    
# @app.route('/logout')
# def logout():
#     session.clear()
#     flash("logged out successfully", "info")
#     return redirect(url_for('login'))


# #issues
# @app.route('/add', methods=['GET','POST'])
# def add_issue():

#     if "username" not in session:
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         db.issues.insert_one({
#             "title" : request.form.get['title'],
#             "description" : request.form['description'],
#             "priority" : request.form['priority'],
#             "status" : "open",
#             "created_by" : session['username']
#         })
#         return redirect(url_for('index'))
#     return render_template('add_issues.html')


# @app.route('/issue/<id>', methods = ['GET', 'POST'])
# def issue_detail(id):

#     if "username" not in session:
#         return redirect(url_for('login'))

#     issue = db.issues.find_one({'_id': ObjectId(id)})
#     if request.method == 'post':
#         db.issues.update_one(
#             {'_id': ObjectId(id)}, 
#             {'$set' : {'status' : request.form['status']}}
#             )
#         return redirect(url_for('index'))
#     return render_template('issue_detail.html', issue = issue)

# #for admin
# @app.route('/admin')
# def admin_dashboard():
#     if "username" not in session or session.get('role') != 'admin':
#         flash("admin access only", "danger")
#         return redirect(url_for('login'))
    
#     users = db.users.find()
#     issues = db.issues.find()
#     return render_template('admin_dashboard.html', users=all, issues=all)



# if __name__ == '__main__':
#     app.run(debug=True)

# # AI code
# from flask import Flask, jsonify, request

# from flask_pymongo import PyMongo
# import config

# app = Flask(__name__)

# # MongoDB Config
# app.config["MONGO_URI"] = config.MONGO_URI
# mongo = PyMongo(app)
# db = mongo.db

# @app.route('/')
# def home():
#     return jsonify({"message": "Issue Tracker API is live!"})

# @app.route('/health')
# def health_check():
#     try:
#         mongo.cx.server_info()  # Check if MongoDB is reachable
#         return jsonify({"status": "OK", "db": "Connected"}), 200
#     except Exception as e:
#         return jsonify({"status": "Error", "details": str(e)}), 500
    
# # 🧱 Step 2: Signup Route
# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()

#     if not data or not data.get('username') or not data.get('password'):
#         return jsonify({"error": "Username and password are required"}), 400

#     username = data['username']
#     password = data['password']
#     role = data.get('role', 'user')  # default role = user

#     if db.users.find_one({"username": username}):
#         return jsonify({"error": "Username already exists"}), 409

#     hashed_pw = generate_password_hash(password)

#     db.users.insert_one({
#         "username": username,
#         "password": hashed_pw,
#         "role": role
#     })

#     return jsonify({"message": f"User '{username}' created successfully", "role": role}), 201



# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# 🧠 Temporary in-memory "database"
users = []      # Each user: {"username": str, "password": hashed_pw, "role": "user"/"admin"}
issues = []     # Each issue: {"id": int, "title": str, "description": str, "priority": str, "status": str, "created_by": str}


# 🧩 Route 1: Home (testing)
@app.route('/')
def home():
    return jsonify({"message": "Issue Tracker API running 🚀"})


# 🧩 Route 2: Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    # Check if user already exists
    for user in users:
        if user["username"] == username:
            return jsonify({"error": "Username already exists"}), 400

    hashed_pw = generate_password_hash(password)
    users.append({
        "username": username,
        "password": hashed_pw,
        "role": role
    })

    return jsonify({"message": "User registered successfully!"}), 201


# 🧩 Route 3: Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and check_password_hash(user["password"], password):
            session["username"] = username
            session["role"] = user["role"]
            return jsonify({"message": f"Welcome {username}", "role": user["role"]}), 200

    return jsonify({"error": "Invalid credentials"}), 401


# 🧩 Route 4: Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


# 🧩 Route 5: Add Issue (for logged-in users)
@app.route('/issues', methods=['POST'])
def add_issue():
    if "username" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()
    issue = {
        "id": len(issues) + 1,
        "title": data.get("title"),
        "description": data.get("description"),
        "priority": data.get("priority"),
        "status": "open",
        "created_by": session["username"]
    }
    issues.append(issue)
    return jsonify({"message": "Issue added successfully!", "issue": issue}), 201


# 🧩 Route 6: View All Issues
@app.route('/issues', methods=['GET'])
def get_issues():
    return jsonify(issues)


# 🧩 Route 7: Update Issue Status (only admin)
@app.route('/issues/<int:issue_id>', methods=['PATCH'])
def update_issue(issue_id):
    if "username" not in session:
        return jsonify({"error": "Login required"}), 401

    if session["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    new_status = data.get("status")

    for issue in issues:
        if issue["id"] == issue_id:
            issue["status"] = new_status
            return jsonify({"message": "Issue status updated", "issue": issue}), 200

    return jsonify({"error": "Issue not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)