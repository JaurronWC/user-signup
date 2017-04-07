#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
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


class Index(webapp2.RequestHandler):
    """Acts as the root of our site (/)
    """
    def get(self):

        #form for adding information into the page
        add_form = '''
        <form action="/welcome" method="post">
            <table>
                <tr><label>
                <td>Name</td>
                <td><input type="text" name="user-name" /></td>
                </label></tr>
                <tr><label>
                <td>Password</td>
                <td><input type="password" name="user-password" /></td>
                </label></tr>
                <tr><label>
                <td>Verify Password</td>
                <td><input type="password" name="user-verify" /></td>
                </label></tr>
                <tr><label>
                <td>Email (Optional)</td>
                <td><input type="text" name="user-email" /></td>
                </label></tr>
            </table>
            <input type="submit" value="Submit" />
        </form>
        '''

        #if there's an error display it next to the location,otherwise display nothing
        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = "<p class='error'>" + error_esc + "</p>"
        else:
            error_element = ""

        #construct and display the page
        main_form = add_form + error_element
        content = page_header + main_form + page_footer
        self.response.write(content)

class Welcome(webapp2.RequestHandler):
    """User is redirected to this page upon a successful sign up and greeted by name
    """

    def post(self):

        #look inside the request for each piece of information
        user_name = self.request.get("user-name")
        user_password = self.request.get("user-password")
        user_verify = self.request.get("user-verify")
        user_email = self.request.get("user-email")

        # return an error if the user didn't enter a name, password, or verified password
        if (not user_name) or (user_name.strip() == ""):
            error = "Please enter your name."
            self.redirect("/?error=" +cgi.escape(error, quote=True))

        if (not user_password) or  (user_password.strip() == ""):
            error = "Please enter a password."
            self.redirect("/?error=" +cgi.escape(error, quote=True))

        if user_password != "":
            if (not user_verify) or  (user_verify.strip() == ""):
                error = "Please verify your password."
                self.redirect("/?error=" +cgi.escape(error, quote=True))

        #escape HTML in user name and Email
        user_name_escaped = cgi.escape(user_name, quote=True)
        email_escaped = cgi.escape(user_email, quote=True)

        if user_email != "":
            sent_email = "A verification email has been sent to " + user_email
        else:
            sent_email = ""

        welcome_user = "<strong>Welcome " + user_name_escaped + "! </strong>" + "<br> <br>" + sent_email
        content = page_header + welcome_user + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
