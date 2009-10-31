import cgi

from google.appengine.ext             import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import Admin
import Faculty

class MainPage (webapp.RequestHandler) :
    def get (self) :
        self.response.out.write('Login')
        self.response.out.write("""
            <form action="/" method="post">
            <input type="text" name="id" />
            <input type="submit" />
            </form>""")

    def post (self) :
        s = cgi.escape(self.request.get("id"))
        if s == "admin" :
            self.redirect("/admin")
        elif s == "faculty" :
            self.redirect("/faculty")
        self.response.out.write("Invalid ID.<br />")
        self.get()

def main () :
    x = webapp.WSGIApplication(
        [("/",        MainPage),
         ("/admin",   Admin.MainPage),
         ("/faculty", Faculty.MainPage)],
        debug=True)
    run_wsgi_app(x)

if __name__ == "__main__":
    main()

