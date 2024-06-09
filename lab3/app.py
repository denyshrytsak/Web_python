from flask import Flask, render_template, request
import platform
from datetime import datetime

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)