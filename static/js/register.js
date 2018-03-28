function password_matching() {
	var password = document.getElementById("password").value;
	var repeat_password = document.getElementById("repeat_password").value;
	if (password == repeat_password) {
		return true;
	}
	else {
		return false;
	}
}

function form_submit() {
	if (password_matching()) {
		document.getElementById("register_form").submit();
	}
}