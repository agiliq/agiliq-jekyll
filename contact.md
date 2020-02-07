---
layout: default
title: Contact Us
permalink: /contact/
redirect_from: "/contactus/"
---

<script src='https://www.google.com/recaptcha/api.js?render=6Ld3LooUAAAAAOMMKL8bO5ap1f-0LcM_gL8Wr8YB'></script>
<div class="row">
	<form class="container" action="https://asia-northeast1-agiliqdotcom-211208.cloudfunctions.net/contact-send-email" method="POST">
		<p>
			Are you building Python web applications or APIs? We would love to help you.
			You can email us at <a href="mailto:hello@agiliq.com">hello@agiliq.com</a> or fill the form below to get in touch with us</p>
		<div class="form-group">
			<label for="id_name">Full Name</label>
			<input type="text" name="name" class="form-control" id="id_name" placeholder="Enter your name and surname" required="required">
		</div>
		<div class="form-group">
			<label for="id_email" required="required">Email address</label>
			<input type="email" name="email" class="form-control" id="id_email" aria-describedby="emailHelp" placeholder="Enter your email">
		</div>
		<div class="form-group">
			<label for="id_messge">Write your message</label>
			<textarea class="form-control" id="id_messge" rows="3" name="body"></textarea>
		</div>
		<input type="submit" name="Submit"
			value="Send Message"
			class="btn btn--dark btn--rounded" />
		<input type="hidden" id="g-recaptcha-response" name="g-recaptcha-response" />
		<hr/>
		<p>You can also call us at <a href="tel:+919949997612">+91 9949997612</a></p>
		<hr/>
	</form>
</div>
<script>
grecaptcha.ready(function() {
	grecaptcha.execute('6Ld3LooUAAAAAOMMKL8bO5ap1f-0LcM_gL8Wr8YB', {action: 'contact_form'})
	.then(function(token) {
		document.getElementById('g-recaptcha-response').value=token;
	});
});
</script>
