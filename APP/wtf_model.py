
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, FileField , SelectField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PredictionForm(FlaskForm):
    model = SelectField('Model', choices=['Model 1', 'Model 2'], validators=[DataRequired()])
    file = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Predict')
