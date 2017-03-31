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
        #header = "<h2>Signup</h2>"

        add_form = '''
        <form method="post">
            <table>
                <tr><label>
                <td>Name</td>
                <td><input type="text" value="" /></td>
                </label></tr>
                <tr><label>
                <td>Password</td>
                <td><input type="password" value="" /></td>
                </label></tr>
                <tr><label>
                <td>Verify Password</td>
                <td><input type="password" value="" /></td>
                </label></tr>
                <tr><label>
                <td>Email (Optional)</td>
                <td><input type="text" value="" /></td>
                </label></tr>
            </table>
            <input type="submit" value="Submit" />
        </form>
        '''

        main_form = add_form
        content = page_header + main_form + page_footer
        self.response.write(content)

class AddInfo(webapp2.RequestHandler):
    """"Class for taking entered info and determining if it's valid or not
    """"
    def post(self):


class Welcome(webapp2.RequestHandler):
    """User is redirected to this page upon a successful sign up and greeted by name
    """

    def get(self):
        header = "<h2>Welcome [UserName]"



        main_form = header
        content = page_header + header + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
