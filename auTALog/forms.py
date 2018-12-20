#!/usr/bin/env python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms import IntegerField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, Email

class HoursForm(FlaskForm):
	student = StringField('student', validators=[DataRequired()])
	course = StringField('course', validators=[DataRequired()])
	comment = TextAreaField('comment')
	flag = BooleanField('flag')


class ActionForm(FlaskForm):
	action = StringField('action', validators=[DataRequired()])


class UserForm(FlaskForm):
	action = StringField('action', validators=[DataRequired()])
	email = StringField('email', validators=[Email()])
	name = StringField('name')
	active = BooleanField('active')
	password = PasswordField('password')
	roles = SelectMultipleField('roles')
	id = IntegerField('id')

class CourseForm(FlaskForm):
	id = IntegerField('id')
	action = StringField('action', validators=[DataRequired()])
	name = StringField('name')


class ClockOutForm(FlaskForm):
	summary = TextAreaField('summary')