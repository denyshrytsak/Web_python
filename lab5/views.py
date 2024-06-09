from flask import Flask, render_template, render_template, request, redirect, url_for, make_response, session, flash
import platform
from datetime import datetime
import os
from app import app
from app.forms import LoginForm, ChangePasswordForm
import json

JSON_FILE = os.path.join(app.static_folder, 'data/login.json')


my_skills = ["Python", "Flask", "HTML", "CSS", "JavaScript"]

@app.route('/')
def home():
    return render_template('home.html', title="Home")

@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title="Portfolio")

@app.route('/skills')
@app.route('/skills/<int:id>')
def display_skills(id=None):
    if id is not None and id < len(my_skills):
        skill = my_skills[id]
        return render_template('skill.html', title="Skill Details", skill=skill)
    return render_template('skills.html', title="Skills", skills=my_skills, total=len(my_skills))

@app.context_processor
def inject_now():
    return {
        'now': datetime.utcnow(),
        'os_info': platform.system() + " " + platform.release(),
        'user_agent': request.headers.get('User-Agent')
    }

@app.route('/login', methods=['GET', 'POST'])
def login():

    if"username" in session:
        return redirect(url_for("admin_page"))   
    
    form = LoginForm()

    if  form.validate_on_submit(): 
        username = form.name.data
        password = form.password.data
        remember = form.remember.data

        with open(JSON_FILE) as f:
            users = json.load(f).get("users")
            if any(user.get("name") == username and user.get("password") == password for user in users): 
                if remember:
                    session["username"] = username
                    flash("Logged in successfully!!", category="success")
                    return redirect(url_for("admin_page"))
                
                flash("Logged in successfully to about!!", category="success")
                return redirect(url_for("about_page"))

            flash("Wrong data! Try again!", category="danger")
            return redirect(url_for("login"))
    
    return render_template('login.html', form=form)

@app.route('/admin')
def admin_page():
    form = ChangePasswordForm()

    if "username" not in session:
        flash("You need to login first!", category="danger")
        return redirect(url_for("login"))

    return render_template('admin.html', username=session.get("username"), cookies=request.cookies, form=form)

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    flash("Logged out successfully!!", category="success")
    return redirect(url_for("login"))

@app.route('/info')
def info_page():
    if not session.get("username"):
        return redirect(url_for("login"))

    return render_template('info.html', username=session.get("username"),message=session.pop("message", None),cookies=request.cookies, os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())


@app.route('/cookies', methods=["POST"])
def add_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    exp_date = request.form.get("date")

    if key and value and exp_date:
        response = make_response(redirect(url_for("info_page")))
        response.set_cookie(key, value, expires=datetime.strptime(exp_date, "%Y-%m-%dT%H:%M"))
        session["message"] = {"successfully": True, "text": f"Success! {key} : {value} was added."}
        return response

    session["message"] = {"successfully": False, "text": "Failed!"}
    return redirect(url_for("info_page"))

@app.route('/cookies/delete', methods=["POST"])
@app.route('/cookies/delete/<key>', methods=["POST"])
def delete_cookie(key = None):
    response = make_response(redirect(url_for("info_page")))

    if key:
        response.delete_cookie(key)
        session["message"] = {"successfully": True, "text": f"Success! cookie: {key} was deleted."}
    else:
        for key in request.cookies.keys():
            response.delete_cookie(key)
    
    return response

@app.route('/change-password', methods=["POST"])
def change_password():
    old = request.form.get("old")
    new = request.form.get("new")
    username = session.get("username")

    file =  open(JSON_FILE, "r")
    data = json.load(file)
    file.close()    
    users = data.get("users")

    index = next((i for i, user in enumerate(users) if user["name"] == username), -1)

    if index >= 0 and users[index]["password"] == old:
        users[index]["password"] = new
        file = open(JSON_FILE, "w+")
        file.write(json.dumps(data))
        file.close() 
        session["message"] = {"successfully": True, "text": "Password changed!"}
    else:
        session["message"] = {"successfully": False, "text": "Failed!"}

    return redirect(url_for("info_page"))

