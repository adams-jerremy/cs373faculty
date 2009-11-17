# -------
# main.py
# -------

import cgi

from google.appengine.ext import db 
from google.appengine.ext             import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import Admin
import Faculty
import ImporterPage
import ExporterPage
import Tester

current_user = ""

class current_user(db.Model) :
    current_user = db.StringProperty(required=True)
    session_id = db.IntegerProperty(required=True)

class MainPage (webapp.RequestHandler) :
    def get (self) :
        self.response.out.write("""
            <head>
            <title> FacBook </title>
            <style type="text/css">
            .olink:link {color: #F07000; }
            h1{
            font-family:"Georgia", sans serif;
            font-size:50px;
            margin: 4px 0px;
            color: #2C7EC9;
            margin-top:180px;
            }
            h2{
            font-family:"Georgia", sans serif;
            text-align:right;
            font-size:15px;
            color: #F0AE35;
            }
            p1{
            font-size:5px;
            }
            body
            {
            text-align:center;
            }

            </style>
            </head>
            <h2> <a href="admin" class="olink">Admin Login</a>  </h2>
            <h1> FacBook </h1>
            <p1> &#169 David Martin </p1>
            <br>
            <br>
            <form action="/" method="post">
            <input type="text" name="id" />
            <input type="submit" value ="Login" />
            </body>
            </form>""")

    def post (self) :
        global current_user
        s = cgi.escape(self.request.get("id"))
        if s == "admin" :
            self.redirect("/admin")
        else :
            q = db.GqlQuery("SELECT * from faculty_email")
            for v in q :
                if (s == v.faculty_email) :
                    current_user = s
                    self.redirect("/faculty")
        self.response.out.write("Invalid ID.<br />")
        self.get()

def get_current_user () :
    global current_user
    return current_user

def main () :
    x = webapp.WSGIApplication(
        [("/",        MainPage),
         ("/admin",   Admin.MainPage),
         ("/faculty", Faculty.MainPage),
         ("/importer", ImporterPage.MainPage),
         ("/exporter", ExporterPage.MainPage),
         ("/tester",Tester.MainPage)],
        debug=True)
    run_wsgi_app(x)

if __name__ == "__main__":
    main()
