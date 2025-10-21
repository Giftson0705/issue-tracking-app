from flask import Flask, jsonify, request, render_template,redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import config

# app = Flask(__name__)
# app.config["MONGO_URI"] = config.MONGO_URI
# mongo = PyMongo(app)
# db = mongo.db[config.DB_NAME]

app = Flask(__name__)
app.config["MONGO_URI"] = config.MONGO_URI  # Must be exactly like this

mongo = PyMongo(app)  # Now PyMongo knows the URI

db = mongo.db  # This is your DB object

@app.route('/')
def index():
    issues = db.issues.find()
    return render_template('index.html', issues = issues)

#login and signup

@app.route('/signup', methods = ['GET', 'POST'] )
def signup():
    if request.method == 'POST':
        username =request.form['username']
        password = request.form['password']
        role = request.form.get('role','user')

        if db.users.find_one({'username': username}):
            flash("Username already exists", "warning")
            return redirect(url_for('signup'))
        
    hashed_pw = generate_password_hash(password)
    db.users.insert_one({
        'username': username,
        'password': hashed_pw,
        'role': role
    })
    flash("account created :) login", "success")
    return redirect(url_for('login'))
    return render_template('login.html', signup=True)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        session['username'] = username
        session['role'] = user['role']
        flash(f"welcome {username}", "success ")

        if user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('index'))   
    else:
        flash("invalid credentials", "danger")
        return render_template('login.html') 
    
@app.route('/logout')
def logout():
    session.clear()
    flash("logged out successfully", "info")
    return redirect(url_for('login'))


#issues
@app.route('/add', methods=['GET','POST'])
def add_issue():

    if "username" not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        db.issues.insert_one({
            "title" : request.form.get['title'],
            "description" : request.form['description'],
            "priority" : request.form['priority'],
            "status" : "open",
            "created_by" : session['username']
        })
        return redirect(url_for('index'))
    return render_template('add_issues.html')


@app.route('/issue/<id>', methods = ['GET', 'POST'])
def issue_detail(id):

    if "username" not in session:
        return redirect(url_for('login'))

    issue = db.issues.find_one({'_id': ObjectId(id)})
    if request.method == 'post':
        db.issues.update_one(
            {'_id': ObjectId(id)}, 
            {'$set' : {'status' : request.form['status']}}
            )
        return redirect(url_for('index'))
    return render_template('issue_detail.html', issue = issue)

#for admin
@app.route('/admin')
def admin_dashboard():
    if "username" not in session or session.get('role') != 'admin':
        flash("admin access only", "danger")
        return redirect(url_for('login'))
    
    users = db.users.find()
    issues = db.issues.find()
    return render_template('admin_dashboard.html', users=all, issues=all)



if __name__ == '__main__':
    app.run(debug=True)
    

    
# AI code


# from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash  # ✅ missing import
# import config

# app = Flask(__name__)
# app.secret_key = "supersecretkey" 
# app.config["MONGO_URI"] = config.MONGO_URI  
# print("Mongo URI:", app.config["MONGO_URI"])  # Debugging line to check the URI

# mongo = PyMongo(app)
# db = mongo.db



# # HOME PAGE
# @app.route('/')
# def index():
#     return render_template('index.html')



# # SIGNUP
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         role = request.form.get('role', 'user')

#         if db.users.find_one({'username': username}):
#             flash("Username already exists", "warning")
#             return redirect(url_for('signup'))
        

#         hashed_pw = generate_password_hash(password)
#         db.users.insert_one({
#             'username': username,
#             'password': hashed_pw,
#             'role': role
#         })
#         flash("Account created successfully :) Please login.", "success")
#         return redirect(url_for('login'))

#     return render_template('login.html', signup=True)  # Optional: you can later split this into separate signup.html
    
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = db.users.find_one({'username': username})  

#         if user and check_password_hash(user['password'], password):
#             session['username'] = username
#             session['role'] = user['role']
#             flash(f"Welcome {username}!", "success")

#             if user['role'] == 'admin':
#                 return redirect(url_for('admin_dashboard'))
#             else:
#                 return redirect(url_for('index'))
#         else:
#             flash("Invalid credentials", "danger")
#             return render_template('login.html')
    
#     return render_template('login.html') 


# #logout
# @app.route('/logout')
# def logout():
#     session.clear()
#     flash("Logged out successfully", "info")
#     return redirect(url_for('login'))


# #add issue
# @app.route('/add', methods=['GET', 'POST'])
# def add_issue():
#     if "username" not in session:
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         db.issues.insert_one({
#             "title": request.form['title'],
#             "description": request.form['description'],
#             "priority": request.form['priority'],
#             "status": "open",
#             "created_by": session['username']
#         })
#         flash("Issue added successfully!", "success")
#         return redirect(url_for('index'))
    
#     return render_template('add_issue.html')


# @app.route('/issue/<id>', methods=['GET', 'POST'])
# def issue_detail(id):
#     if "username" not in session:
#         return redirect(url_for('login'))

#     issue = db.issues.find_one({'_id': ObjectId(id)})

#     if request.method == 'POST':
#         db.issues.update_one(
#             {'_id': ObjectId(id)},
#             {'$set': {'status': request.form['status']}}
#         )
#         flash("Issue updated successfully", "info")
#         return redirect(url_for('index'))
    
#     return render_template('issue_detail.html', issue=issue)



# # ADMIN DASHBOARD

# @app.route('/admin')
# def admin_dashboard():
#     if "username" not in session or session.get('role') != 'admin':
#         flash("Admin access only", "danger")
#         return redirect(url_for('login'))
#     users = list(db.users.find())
#     issues = list(db.issues.find())
#     return render_template('admin_dashboard.html', users=users, issues=issues)



# if __name__ == '__main__':
#     app.run(debug=True)
