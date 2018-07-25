---
layout: default
title: Contact Us
permalink: /contact/
redirect_from: "/contactus/"
---
<div class="row">

	<p>
		Are you building Python web applications or APIs? We would love to help you.
	</p>

	<p>
		You can email us at <a href="mailto:hello@agiliq.com">hello@agiliq.com</a>
	</p>
	<p> Or, fill the form below</p>

	<form action="https://asia-northeast1-agiliqdotcom-211208.cloudfunctions.net/contact-send-email" method="POST">
		<p>
			<table border="1|0">
			<tr>
				<td>Name</td>
				<td>
				<input type="text" id="name" name="name" placeholder="Name">
				</td>
			</tr>
			<tr>
				<td>Email</td>
				<td>
				<input type="email" id="email" name="email" placeholder="Email">
				</td>
			</tr>
			<tr>
				<td>Message</td>
				<td>
				<textarea rows="6" cols="30" id="body" name="body" placeholder="Message"></textarea>
				</td>
			</tr>
			<tr>
				<td colspan="2" align="center">
					<input type="submit" name="Submit" 
						class="btn btn--dark btn--rounded">
						Send Message
					</input>
				</td>
			</tr>
			</table>
		</p>
	</form>
	<p>
		Or, call us at <a href="tel:+919949997612">+91 9949997612</a>
	</p>
</div>
