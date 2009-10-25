import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Faculty(db.Model):
    author = db.UserProperty()
    name = db.StringProperty(multiline=False)
    phone = db.StringProperty(multiline=False)
    email = db.StringProperty(multiline=False)
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        link = '<a href="%s">%s</a>'
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            linktext = 'Login'
        link = link % (url,linktext)    

        self.response.out.write('<html><body>')

        facs = db.GqlQuery("SELECT * FROM Faculty ORDER BY date DESC LIMIT 10")

        for fac in facs:
            if fac.author:
                self.response.out.write('<b>%s</b> wrote:' % fac.author.nickname())
            else:
                self.response.out.write('An anonymous person wrote:')
            self.response.out.write('<blockquote>%s %s %s</blockquote>'% (cgi.escape(fac.name), cgi.escape(fac.phone), cgi.escape(fac.email)))

        # Write the submission form and the footer of the page
        self.response.out.write("""
                    <form action="/display" method="post">
                        <div><textarea name="name" rows="1" cols="60"></textarea></div>
                        <div><textarea name="phone" rows="1" cols="60"></textarea></div>
                        <div><textarea name="email" rows="1" cols="60"></textarea></div>
                        <div><input type="submit" value="Submit"></div>
                    </form>"""+link+"""
                </body>
            </html>""")
        
        
class DB(webapp.RequestHandler):
    def post(self):
        fac = Faculty()
        if users.get_current_user():
            fac.author = users.get_current_user()

        fac.name = self.request.get('name')
        fac.phone = self.request.get('phone')
        fac.email = self.request.get('email')
        fac.put()
        self.redirect('/')

application = webapp.WSGIApplication([('/', MainPage),('/display', DB)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()