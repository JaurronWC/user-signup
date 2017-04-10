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

        #forms for adding information into the page
        add_form = '''
        <form action="/welcome" method="post">
            <table>
                <tr><label>
                <td>Username</td>
                <td><input type="text" name="user-name" /></td>
                 '''
        password_form = '''
                <tr><label>
                <td>Password</td>
                <td><input type="password" name="user-password" /></td>
                '''
        verify_form = '''
                <tr><label>
                <td>Verify Password</td>
                <td><input type="password" name="user-verify" /></td>
                 '''
        email_form = '''
                <tr><label>
                <td>Email (Optional)</td>
                <td><input type="text" name="user-email" /></td>
                '''
        form_end ='''
            </table>
            <input type="submit" value="Submit" />
        </form>
        '''

        #if there's an error display it next to the location,otherwise display nothing
        u_error = self.request.get("u_error")
        if u_error:
            unerror_esc = cgi.escape(u_error, quote=True)
            unerror_element = '''<td> <font color="red">''' + unerror_esc + '''</font></td></label></tr>'''
        else:
            unerror_element = ""

        p_error = self.request.get("p_error")
        if p_error:
            p_error_esc = cgi.escape(p_error, quote=True)
            pass_error_element = '''<td> <font color="red">''' + p_error_esc + '''</font></td></label></tr>'''
        else:
            pass_error_element = ""

        v_error = self.request.get("v_error")
        if v_error:
            v_error_esc = cgi.escape(v_error, quote=True)
            v_error_element = '''<td> <font color="red">''' + v_error_esc + '''</font></td></label></tr>'''
        else:
            v_error_element = ""

        e_error = self.request.get("e_error")
        if e_error:
            e_error_esc = cgi.escape(e_error, quote=True)
            e_error_element = '''<td> <font color="red">''' + e_error_esc + '''</font></td></label></tr>'''
        else:
            e_error_element = ""

        #construct and display the page
        main_form = add_form + unerror_element + password_form + pass_error_element + verify_form + v_error_element + email_form + e_error_element + form_end
        content = page_header + main_form + page_footer
        self.response.write(content)

class Welcome(webapp2.RequestHandler):
    """User is redirected to this page upon a successful sign up and greeted by name
    """

    def post(self):

        #look inside the request for each piece of information and escape the html in any of them
        user_name = self.request.get("user-name")
        user_name_escaped = cgi.escape(user_name, quote=True)
        user_password = self.request.get("user-password")
        user_password_escaped = cgi.escape(user_password, quote=True)
        user_verify = self.request.get("user-verify")
        user_verify_escaped = cgi.escape(user_verify, quote=True)
        user_email = self.request.get("user-email")
        email_escaped = cgi.escape(user_email, quote=True)



        # return an error if the user didn't enter a name, password, or verified password
        if (not user_name_escaped) or (user_name_escaped.strip() == ""):
            u_error = "Please enter a username."
            self.redirect("/")
        elif not valid_username(user_name_escaped):
            u_error = "Please a valid username."
            self.redirect("/")


        if (not user_password_escaped) or  (user_password_escaped.strip() == ""):
            p_error = "Please enter a password."
            self.redirect("/")
        elif not valid_password(user_password_escaped):
            p_error = "Please enter a valid password"
            self.redirect("/")
        else:
            p_error = ""

        if user_password != "":
            if (not user_verify_escaped) or  (user_verify_escaped.strip() == ""):
                v_error = "Please verify your password."
                self.redirect("/")
            elif user_verify_escaped != user_password_escaped:
                v_error = "Your passwords do not match."
                self.redirect("/")
            else:
                v_error = ""

        if user_email != "":
            if not valid_email:
                e_error = "Please enter a valid email."
                self.redirect("/")
            else:
                sent_email = "A verification email has been sent to " + email_escaped
        else:
            sent_email = ""

        welcome_user = "<strong>Welcome " + user_name_escaped + "! </strong>" + "<br> <br>" + sent_email
        content = page_header + welcome_user + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
