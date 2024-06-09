from flask import Flask, render_template, render_template, request, redirect, url_for, make_response, session, flash
import platform
from datetime import datetime
import os
from app import app
from app.forms import LoginForm, ChangePasswordForm, TodoForm, FeedbackForm,RegistrationForm, UpdateAccountForm
from app.models import Todo, Feedback, User
import json
from app import db
from flask_login import login_user, current_user, logout_user, login_required
from app.util import save_picture
JSON_FILE = os.path.join(app.static_folder, 'data/login.json')


my_skills = ["Python", "Flask", "HTML", "CSS", "JavaScript"]

@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response

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
    
@app.route('/register', methods=['GET', 'POST'])    
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin_page'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        new_user = User(name=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {new_user.username}!", "success")
            return redirect(url_for("login"))
        except:
            db.session.rollback()
            flash("Something went wrong!", category="danger")
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_page'))
    
    form = LoginForm()

    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.verify_password(form.password.data): 
            login_user(user, remember=form.remember.data)
            flash("Logged in successfully!!", category="success")    
            return redirect(url_for("admin_page"))

        flash("Wrong data! Try again!", category="danger")
        return redirect(url_for("login"))
    
    return render_template('login.html', form=form)

@app.route('/admin')
@login_required
def admin_page():
    return render_template('admin.html', cookies=request.cookies)


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!!", category="success")
    return redirect(url_for("login"))

@app.route('/account')
@login_required
def account():
    password_form = ChangePasswordForm()
    info_form = UpdateAccountForm()
    return render_template('account.html', password_form=password_form, info_form=info_form)

@app.route('/users')
def users():
    return render_template('users.html', users=User.query.all())

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

@app.route('/update-user', methods=["POST"])
@login_required
def update_user():
    form = UpdateAccountForm(current_user=current_user)

    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        try:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash("Info updated!", category="success")
        except:
            db.session.rollback()
            flash("Failed!", category="danger")
        return redirect(url_for("account"))

    flash("Validation error!", category="danger")
    return render_template('account.html', password_form=ChangePasswordForm(), info_form=form)

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

@app.route('/todos')
def todos():
    todo_list = Todo.query.all()
    return render_template("todo.html", todo_list=todo_list, form=TodoForm())
 
@app.route("/todos/add", methods=["POST"])
def add_todo():
    form=TodoForm()
    new_todo = Todo(title=form.title.data, due_date=form.due_date.data, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todos"))
 
@app.route("/todos/update/<int:id>")
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.complete = not todo.complete   
    db.session.commit()
    return redirect(url_for("todos"))
 
@app.route("/todos/delete/<int:id>")
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todos"))

@app.route('/feedbacks', methods=["GET", "POST"])
def feedbacks():
    form=FeedbackForm()

    if form.validate_on_submit():
        new_feedback = Feedback(
            topic= form.topic.data,
            text=form.text.data,
            mark=form.mark.data,
            user_email=form.email.data,  
            date=datetime.now())
        
        try:
            db.session.add(new_feedback)
            db.session.commit()
            flash("Feedback added!", category="success")
        except:
            db.session.rollback()
            flash("Something went wrong!", category="danger")
        return redirect(url_for("feedbacks"))

    feedbacks = Feedback.query.all()
    return render_template("feedbacks.html", feedbacks=feedbacks, form=form)
 
@app.route("/feedbacks/delete/<int:id>")
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    try:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", category="success")
    except:
        db.session.rollback()
        flash("Something went wrong!", category="danger")
    
    return redirect(url_for("feedbacks"))

