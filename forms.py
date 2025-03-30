from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from flask_wtf.file import FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    author = StringField('Author', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Optional()])
    cover = FileField('Cover Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    book_file = FileField('Book File (PDF, EPUB, MOBI)', validators=[
        Optional(),
        FileAllowed(['pdf', 'epub', 'mobi'], 'Book files only!')
    ])
    book_url = StringField('Book URL (External Link)', validators=[Optional(), Length(max=500)])
    publisher = StringField('Publisher', validators=[Optional(), Length(max=255)])
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1000, max=3000)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=20)])
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('business', 'Business'),
        ('self-help', 'Self-Help'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('other', 'Other')
    ])
    submit = SubmitField('Save Book')
