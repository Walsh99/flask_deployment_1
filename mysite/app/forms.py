from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class AssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    module_code = StringField('Module Code', validators=[DataRequired(), Length(max=20)])
    deadline = DateField('Deadline', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    is_completed = BooleanField('Completed')
