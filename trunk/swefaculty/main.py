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
import SearchPage
import Public
current_user = ""
keywords = ""

class current_user(db.Model) :
    current_user = db.StringProperty(required=True)
    session_id = db.IntegerProperty(required=True)

class MainPage (webapp.RequestHandler) :
    def get (self) :
        self.response.out.write("""
            <head>
            <title> University of Texas Austin Faculty Database </title>
            <style type="text/css">
            .olink:link {color: #F07000; }
            h1{
            font-family:"Georgia", sans serif;
            font-size:60px;
            margin: 4px 0px;
            color: #ADADAD;
            margin-top:180px;
            }
            p1{
            font-size:5px;
            }
            body{
            text-align:center;
            background-color: #000052;
            }
            a{
            text-decoration:none;
            font-family:"Georgia", sans serif;
            color:#9999FF;
            }
            input.blue {
            background-color: #9999FF; 
            font-size: 15px;
            }
            div.login {
            position:absolute;
            right:20px;
            top:20px;
            height:50px;
            width:300px;
            border:1px solid #9999FF;
            }
            div.button{
            position:absolute;
            right:5px;
            top:15px;
            }
            div.input1{
            position:absolute;
            right:75px;
            top: 10px
            }
            div.link1{
            margin-right:175px;
            margin-top:-13px;
            font-size:.8em;
            }

            </style>
            </head>
            <form action="/" method="post">
            <div class="login"><div class="input1"><input type="text" class="blue" name="id" style="width:200px" /></div>
            <div class="button"><input type="submit" value ="Login" /></div></div>
            <h1> Faculty Database </h1>
            <br>
            <br>
            <input type="text" class="blue" name="Search"/>
            <input type="submit" value ="Search" />
            </form>
            <div class="link1"><a href="/search">Advanced Search</a></div>
            </body>
            """)
        


    def post (self) :
        global current_user
        s = cgi.escape(self.request.get("id"))
        if s == "admin" :
            self.redirect("/admin")
        else :
            q = db.GqlQuery("SELECT * from Faculty")
            for v in q :
                if (s == v.email) :
                    current_user = s
                    self.redirect("/faculty?facid="+s)
        self.get()
        self.response.out.write("""
        <style type="text/css">
        m{color: #D90000;}
        </style type="text/css">
        <br><br><br>
        <m>Invalid ID.</m>
        """)

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
         ("/search", SearchPage.MainPage),
         ("/tester",Tester.MainPage),
         ("/public",Public.MainPage)],
        debug=True)
    run_wsgi_app(x)

if __name__ == "__main__":
    main()
