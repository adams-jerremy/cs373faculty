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
import Datastore



awardList = lambda f: Faculty.makeList(f,Datastore.AwardJoin,Faculty.awardLine,False)
conferenceList = lambda f: Faculty.makeList(f,Datastore.ConferenceJoin,Faculty.conferenceLine,False)
articleList = lambda f: Faculty.makeList(f,Datastore.ArticleJoin,Faculty.articleLine,False)
officeHourList = lambda f: Faculty.makeList(f,Datastore.OfficeHourJoin,Faculty.officeHourLine,False)
studentList = lambda f: Faculty.makeList(f,Datastore.StudentJoin,Faculty.studentLine,False)
degreeList = lambda f: Faculty.makeList(f,Datastore.DegreeJoin,Faculty.degreeLine,False)
courseList = lambda f: Faculty.makeList(f,Datastore.CourseJoin,Faculty.courseLine,False)
researchAreaList = lambda f: Faculty.makeList(f,Datastore.AreaJoin,Faculty.researchAreaLine,False)
bookList = lambda f: Faculty.makeList(f,Datastore.BookJoin,Faculty.bookLine,False)


class MainPage (webapp.RequestHandler) :
    """
    Takes care of main page
    """
    def get (self) :
        facid = self.request.get("facid")
        fac = Datastore.Faculty.gql("WHERE email = :1",facid).get()
        if fac is None: self.redirect("/"); return;
        
        key = fac.key()
        self.response.out.write("""
            <head>
            <title>"""+(fac.name if fac.name is not None else fac.email)+""" </title>
             <style type="text/css">
            h1{
            font-family:"Georgia", sans serif;
            font-size:50px;
            margin: 4px 0px;
            color: #2C7EC9;
            margin-top:15px
            }
            </style>
            </head>
            <h1> Faculty Information </h1>
            <br>
            """)
        self.response.out.write("Name: "+fac.name)
        self.response.out.write("<br>Type: "+'' if fac.type is None else db.get(fac.type.key()).faculty_type)
        self.response.out.write("<br>Phone: "+fac.phone)
        self.response.out.write("<br>Office: "+('' if fac.building is None else db.get(fac.building.key()).building)+" "+fac.room)
        self.response.out.write("<br>Email: "+fac.email)
        self.response.out.write("<br>Website: "+fac.website)
        self.response.out.write('<br><br>Degrees</p1><br>')
        self.response.out.write(degreeList(key))
        self.response.out.write('<br><br>Research Areas</p1><br>')
        self.response.out.write(researchAreaList(key))
        self.response.out.write('<br><br>Books<br>')
        self.response.out.write(bookList(key))
        self.response.out.write('<br><br>Courses<br>')
        self.response.out.write(courseList(key))
        self.response.out.write('<br><br>Graduate Students<br>')
        self.response.out.write(studentList(key))
        self.response.out.write('<br><br>Office Hours<br>')
        self.response.out.write(officeHourList(key))
        self.response.out.write('<br><br>Articles<br>')
        self.response.out.write(articleList(key))
        self.response.out.write('<br><br>Conferences<br>')
        self.response.out.write(conferenceList(key))
        self.response.out.write('<br><br>Award<br>')
        self.response.out.write(awardList(key))
            
    """
    takes care of submissions
    """
    def post (self) :
        self.get()