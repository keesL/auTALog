
function cleanField() {
	// assume adelphi swipe card if starts with % and ends with ?
	if (student.value.startsWith("%") &&
	    student.value.endsWith("?")) {
		student.value = student.value.substring(1,8);
	}
}

function nosubmit(evt) {
	if (evt && evt.which==13) {
		evt.preventDefault();

		var course=document.getElementById('course');
		if (course) {
			course.focus();
		}
		return false;
	}
	return true;
}

student = document.getElementById('student');
if (student) {
	student.addEventListener("focusout", cleanField);
	student.addEventListener("keypress", nosubmit);
	student.focus()
}
