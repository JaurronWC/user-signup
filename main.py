#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
	<title>Signup</title>
	<style type="text/css">
		.error {
			color: red;
		}
	</style>
</head>
<body>
	<h1>
		<a href="/">Signup</a>
	</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
	"""Acts as the root of our site (/)
	"""
	def get(self):
	
		unerror = self.request.get('uerror')
		passerror = self.request.get('perror')
		emailerror = self.request.get('emerror')
		username = self.request.get('username')
		email = self.request.get('email')

		#form for adding information into the page
		add_form = """
		<form action="/welcome" method="post">
			<label>Username: </label>
				<input type="text" name="username" value="{uname}" /> <font style="color:red:">{uerror}</font>
			<br>
			<label>Password</label>
				<input type="password" name="password" />
			<br>
			<label>Verify Password</label>
				<input type="password" name="vpassword" /> <font style="color:red">{perror}</font>
			<br>
			<label>Email (optional)</label>
				<input type="email" name="email" value="{uemail}" /><font style="color:red">{eerror}</font>
			<br>
			<input type="submit" value="Submit" />
		</form>
		""".format(uname=username, uerror=unerror, perror=passerror, uemail=email, eerror=emailerror)
		
		response = page_header + add_form + page_footer
		self.response.write(response)

class Welcome(webapp2.RequestHandler):
	"""User is redirected to this page upon a successful sign up and greeted by name
	"""

	def post(self):
	
		uerror = ""
		perror = ""
		emerror = ""
		username = self.request.get('username')
		password = self.request.get('password')
		vpassword = self.request.get('vpassword')
		email = self.request.get('email') 
		
		#validate input
		if not password == vpassword:
			perror = "Passwords don't match!"
			self.redirect('/?perror={}&username={}&email={}'.format(cgi.escape(perror, quote=True),username,email))
			
		if valid_username(username) == None:
			uerror = "Please enter a valid username!"
			self.redirect('/?uerror={}&email={}'.format(cgi.escape(uerror, quote=True),email))
			
		if valid_password(password) == None:
			perror = "Please enter a valid password!"
			self.redirect('/?perror={}&username={}&emai={}'.format(cgi.escape(perror, quote=True),username,email))
			
		if valid_email(email) == None:
			emerror = "Please enter a valid email!"
			self.redirect('/?username={}&emerror={}'.format(cgi.escape(emerror, quote=True), email))
		
		welcome_user = "<strong>Welcome {0}! </strong>".format(username)
		
		response = page_header + welcome_user + page_footer
		self.response.write(response)

app = webapp2.WSGIApplication([
	('/', Index),
	('/welcome', Welcome)
], debug=True)
