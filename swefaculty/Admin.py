import cgi

from google.appengine.ext import webapp

import ValidateAdmin

class MainPage (webapp.RequestHandler) :
    def get (self) :
        self.response.out.write('Admin Phone')
        self.response.out.write("""
            <form action="/admin" method="post">
            <input type="text" name="phone" />
            <input type="submit" />
            </form>""")

    def post (self) :
        s = cgi.escape(self.request.get('phone'))
        if ValidateAdmin.phone_number(s) :
            self.response.out.write('Valid number.<br />')
        else :
            self.response.out.write('Invalid number.<br />')
        self.get()

if __name__ == "__main__":
    main()
