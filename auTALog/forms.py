#!/usr/bin/env python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class HoursForm(FlaskForm):
	student = StringField('student', validators=[DataRequired()])
	course = StringField('course', validators=[DataRequired()])
	comment = TextAreaField('comment')
	flag = BooleanField('flag')


class ActionForm(FlaskForm):
	action = StringField('action', validators=[DataRequired()])