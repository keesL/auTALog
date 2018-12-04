from auTALog import app, db
from auTALog.models import Course, Log, User, TutoringSession, roles_users, Role
from auTALog.forms import HoursForm, ActionForm, UserForm, CourseForm

from datetime import datetime
from markupsafe import Markup
import flask
from flask_security import login_required, roles_accepted
from flask_security.utils import hash_password


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
	form = ActionForm(flask.request.form)
	user = User.query.filter_by(id=
		flask.session['user_id']).first()

	# determine if we are in session
	tsid = flask.session.get('tsid')
	if tsid is None:
		ts = None
		duration = 0
	else:
		ts = TutoringSession.query.filter_by(id=tsid).first()
		duration = (datetime.now() - ts.started).seconds

	# process buttons being pushed
	if flask.request.method == 'POST':		
		if tsid is None:
			ts = TutoringSession(ta=flask.session['user_id'], 
				started=datetime.now())
			db.session.add(ts)
			db.session.commit()
			flask.session['tsid'] = ts.id
			flask.flash("Started new session", 'success')
		else:
			ts.ended = datetime.now()
			
			db.session.commit()
			flask.session.pop('tsid', None)
			ts = None
			flask.flash(Markup('Session ended after {} minutes.'+
				' Please <a href="'+flask.url_for('security.logout')+
				'">log out</a>').format(int(duration / 60)), 
				'danger')
	
	return flask.render_template("index.html", form=form,  
		clock=ts, duration=int(duration / 60), user=user)



@app.route('/post', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'tutor')
def post():
	tsid = flask.session.get('tsid')
	if tsid is None:
		flask.flash('Clock in before recording encounters', 'warning')
		return flask.redirect(flask.url_for('index'))

	form = HoursForm(flask.request.form)
	if flask.request.method == 'POST':
		# record new encounter if form is filled out correctly
		if  form.validate_on_submit():
			log = Log(student=form.student.data, 
				session=flask.session['tsid'], 
				subject=form.course.data, 
				comment=form.comment.data)
			db.session.add(log)
			db.session.commit()
			flask.flash("Encounter recorded successfully", "success")
		else:
			flask.flash("Form did not validate", "warning")

	# show recent encounters
	logs = db.session.query(Log, TutoringSession, User, Course).filter(
		Log.subject == Course.id).filter(
		TutoringSession.id == Log.session).filter(
		TutoringSession.ta == User.id).order_by(
		Log.timestamp.desc()).limit(5)

	return flask.render_template("post.html", logs=logs, 
		courses=Course.query.order_by(Course.id).all(), form=form)



@app.route('/admin', methods=['GET'])
@roles_accepted('admin')
@login_required
def admin():
	user = User.query.filter_by(id=flask.session['user_id']).first()
	return flask.render_template('admin.html')



@app.route('/admin/user', methods=['POST', 'GET'])
@app.route('/admin/user/<id>/<action>', methods=['GET'])
@roles_accepted('admin')
@login_required
def users(id=None, action=None):
	userform = UserForm(flask.request.form)
	user = User.query.filter_by(id=flask.session['user_id']).first()
	subj = None
	subj_roles = None
	all_roles = Role.query.order_by(Role.id).all()

	if flask.request.method=='POST':
		action = userform.action.data
		id = userform.id.data

	if action == "edit":
		subj = User.query.filter_by(id=id).first()
		subj_roles = Role.query.join(roles_users).filter(
			roles_users.c.user_id == id).all()

	elif action == "save" and flask.request.method=='POST':
		update = User.query.filter_by(id=userform.id.data).first()

		if update is None:
			update = User(active=True)

		subj_roles = db.session.query(roles_users).filter(
			roles_users.c.user_id == update.id).all()

		update.name = userform.name.data
		update.email = userform.email.data
		update.active = userform.active.data

		# add missing roles
		for role in userform.roles.data:
			role = int(role)
			if not (update.id, role) in subj_roles:
				r = Role.query.filter_by(id = role).first()
				flask.flash("Added role {}".format(r.name), "info")
				ins = roles_users.insert().values(user_id=update.id, role_id=role)
				db.session.execute(ins)
				subj_roles.append((update.id, role))

		# delete removed roles
		for (userid, roleid) in subj_roles:
			roleid = str(roleid)
			if not roleid in userform.roles.data:
				r = Role.query.filter_by(id = roleid).first()
				flask.flash("Removed role {}".format(r.name), "info")
				rm = roles_users.delete().where(
					roles_users.c.user_id == userid).where(
					roles_users.c.role_id == roleid)				
				db.session.execute(rm)

		# update password (if needed)
		if  userform.password.data != "":
			flask.flash("Password has been updated", "info")
			update.password = hash_password(userform.password.data)

		db.session.add(update)
		db.session.commit()
		flask.flash("Saved.", "info")

	elif action == "delete":
		rm = roles_users.delete().where(roles_users.c.user_id == id)
		db.session.execute(rm)
		
		subject = User.query.filter_by(id=id).first()
		db.session.delete(subject)
		db.session.commit()



	return flask.render_template('users.html', 
		users=User.query.all(), form=userform, 
		action=action, subject=subj, subject_roles=subj_roles, 
		all_roles=all_roles)




@app.route('/admin/course', methods=['POST', 'GET'])
@app.route('/admin/course/<id>/<action>', methods=['GET'])
@roles_accepted('admin')
@login_required
def courses(id=None, action=None):
	courseform = CourseForm(flask.request.form)
	user = User.query.filter_by(id=flask.session['user_id']).first()
	subj = None

	if flask.request.method=='POST':
		action = courseform.action.data
		id = courseform.id.data

	if action == "edit":
		subj = Course.query.filter_by(id=id).first()
		
	elif action == "save" and flask.request.method=='POST':
		update = Course.query.filter_by(id=courseform.id.data).first()

		if update is None:
			update = Course()

		update.label = courseform.name.data
		
		db.session.add(update)
		db.session.commit()
		flask.flash("Saved.", "info")
		subj=None

	elif action == "delete":
		subject = Course.query.filter_by(id=id).first()
		db.session.delete(subject)
		db.session.commit()
		flask.flash("Removed course", "info")


	return flask.render_template('courses.html', 
		courses=Course.query.all(), form=courseform, 
		action=action, subject=subj)