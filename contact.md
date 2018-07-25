---
layout: default
title: Contact
permalink: /contact/
redirect_from: "/contactus/"
---
<div class="row">
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
				<input type="email" id="email" name="email" placeholder="email">
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
					<input type="submit" name="Submit"/>
				</td>
			</tr>
			</table>
		</p>
	</form>
	<p>
		Or, call us at <a href="tel:+919949997612"><h3>+91 9949997612</h3></a>
	</p>
</div>
