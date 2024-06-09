from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, EmailField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, Regexp
from app.models import User

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired("Email is required"), Email()])
    password = PasswordField(label='Password', validators=[DataRequired("Password is required")])
    remember = BooleanField(label="Remember me")
    submit = SubmitField(label="Sign in")

class RegistrationForm(FlaskForm):
    username = StringField(label='User name', validators=[
            DataRequired("Name is required"),
            Length(min=4, max=14, message="Min length - 4, max - 14 symbols"),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0, 'Username must have only lettters, numbers, dots or underscores')
        ])
    email = StringField(label='Email', validators=[DataRequired("Email is required"), Email()])
    password = PasswordField(label='Password', validators=[
            DataRequired("Password is required"), 
            Length(min=7, message="Min length - 7 symbols")
        ])
    confirm_password = PasswordField(label='Confirm password', validators=[DataRequired("Confirm password is required"),EqualTo('password')])
    submit = SubmitField(label="Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(label='Old password', validators=[
            DataRequired("Old password is required"), 
            Length(min=4, max=10, message="Min length - 4, max - 10 symbols")
        ])
    new_password = PasswordField(label='New password', validators=[
            DataRequired("New password is required"), 
            Length(min=4, max=10, message="Min length - 4, max - 10 symbols")
        ])
    submit = SubmitField(label="Save changes")

class TodoForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired("Title is required")])
    due_date = DateField(label='Due date')
    submit = SubmitField(label="Save")

class FeedbackForm(FlaskForm):
    text = TextAreaField(label='Text', validators=[DataRequired("Text is required")])
    topic = StringField(label='Topic', validators=[DataRequired("Topic is required")])
    mark =  RadioField(choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],
                       validators=[DataRequired("Mark is required")])
    email = EmailField(label='User email', validators=[DataRequired("Email is required")])
    submit = SubmitField(label="Save")
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField(label='User name', validators=[
            DataRequired("Name is required"),
            Length(min=4, max=14, message="Min length - 4, max - 14 symbols"),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0, 'Username must have only lettters, numbers, dots or underscores')
        ])
    email = StringField(label='Email', validators=[DataRequired("Email is required"), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])
    about_me = TextAreaField('About me')
    submit = SubmitField(label="Update")

    def __init__(self, current_user = None):
        super().__init__()
        self.current_user = current_user

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and self.current_user.email != field.data:
            raise ValidationError("Email already registered")
        
    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user and self.current_user.username != field.data:
            raise ValidationError("Username already in use")