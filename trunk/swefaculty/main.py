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
        self.response.out.write('Login')
        self.response.out.write("""
            <form action="/" method="post">
            <input type="text" name="id" />
            <input type="submit" />
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
