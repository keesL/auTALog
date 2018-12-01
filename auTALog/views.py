from auTALog import app, db
from auTALog.models import Course, Log, User, TutoringSession
from auTALog.forms import HoursForm, ActionForm

from datetime import datetime
from markupsafe import Markup
import flask
from flask_security import login_required


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
	else:
		ts = TutoringSession.query.filter_by(id=tsid).first()

	# process buttons being pushed
	if flask.request.method == 'POST':		
		if tsid is None:
			ts = TutoringSession(ta=flask.session['user_id'], 
				started=datetime.now())
			db.session.add(ts)
			db.session.commit()
			flask.session['tsid'] = ts.id
			flask.flash("Started new tutoring session", 'success')
		else:
			ts.ended = datetime.now()
			duration = ts.ended - ts.started
			
			db.session.commit()
			flask.session.pop('tsid', None)
			ts = None
			flask.flash(Markup('Tutoring session ended after {} minutes.'+
				' Please <a href="'+flask.url_for('security.logout')+
				'">log out</a>').format(int(duration.seconds / 60)), 
				'danger')

	duration = datetime.now() - ts.started
	return flask.render_template("index.html", user=user, 
		clock=ts, duration=int(duration.seconds / 60))



@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
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
			print("Form did not validate")

	# show recent encounters
	logs = db.session.query(Log, TutoringSession, User, Course).filter(
		Log.subject == Course.id).filter(
		TutoringSession.id == Log.session).filter(
		TutoringSession.ta == User.id).order_by(
		Log.timestamp.desc()).limit(5)

	user = User.query.filter_by(id=flask.session['user_id']).first()
	return flask.render_template("post.html", logs=logs, 
		courses=Course.query.all(), form=form, user=user)