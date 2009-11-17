                                                                     
                                                                     
                                                                     
                                             
# --------
# Importer.py
# --------

import cgi

from google.appengine.ext import db 
from google.appengine.ext import webapp

import ValidateAdmin
import ValidateFaculty
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulSOAP
import re

'''
These classes create the database model.  For now, the class
name must match the column name in the database because the
functions below which access the information in queries, 
create new rows, etc all depend on this.
'''

class faculty_email(db.Model) :
    faculty_email = db.StringProperty(required=True)
class student_eid(db.Model) :
    student_eid = db.StringProperty(required=True)
class faculty_type(db.Model) :
    faculty_type = db.StringProperty(required=True)
class research_area(db.Model) :
    research_area = db.StringProperty(required=True)
class building(db.Model) :
    building = db.StringProperty(required=True)
class start_time(db.Model) :
    start_time = db.StringProperty(required=True)
class end_time(db.Model) :
    end_time = db.StringProperty(required=True)
class degree_type(db.Model) :
    degree_type = db.StringProperty(required=True)
class degree_name(db.Model) :
    degree_name = db.StringProperty(required=True)
class institution(db.Model) :
    institution = db.StringProperty(required=True)
class conference_name(db.Model) :
    conference_name = db.StringProperty(required=True)
class location(db.Model) :
    location = db.StringProperty(required=True)
class journal_name(db.Model) :
    journal_name = db.StringProperty(required=True)
class publisher(db.Model) :
    publisher = db.StringProperty(required=True)
class student_type(db.Model) :
    student_type = db.StringProperty(required=True)
class course_number(db.Model) :
    course_number = db.StringProperty(required=True)
class course_name(db.Model) :
    course_name = db.StringProperty(required=True)
class course_type(db.Model) :
    course_type = db.StringProperty(required=True)
class semester(db.Model) :
    semester = db.StringProperty(required=True)
class award_name(db.Model) :
    award_name = db.StringProperty(required=True)
class award_type(db.Model) :
    award_type = db.StringProperty(required=True)

class course(db.Model) :
    course_number = db.ReferenceProperty(reference_class=course_number)
    course_name = db.ReferenceProperty(reference_class=course_name)
    course_type = db.ReferenceProperty(reference_class=course_type)

class Faculty(db.Model):
    name = db.StringProperty()
    phone = db.PhoneNumberProperty()
    building = db.ReferenceProperty(building)
    room = db.StringProperty(validator=ValidateFaculty.room)
    email = db.EmailProperty(required=True)
    website = db.LinkProperty()
    type = db.ReferenceProperty(reference_class=faculty_type)



'''
textstore is a global variable for passing messages between get and post.
'''
textstore = ""


class MainPage (webapp.RequestHandler) :

    '''
    '''

    def get (self) :
        self.response.out.write('<font size="6">XML Importer</font>')
        self.response.out.write('<form action="/importer" method="post">')
        self.response.out.write("""
            <textarea name="xmlinput" cols="80" rows="20">
            </textarea>
            <input type="submit" value="Submit"/>
            </form>""")
        self.response.out.write("<a href=''>Login Page</a><br />")
        self.response.out.write("<a href='admin'>Admin Page</a><br />")
        self.response.out.write("<a href='exporter'>Export Faculty Data</a><br />")
        self.response.out.write(textstore)

    '''
    '''

    def chop (self, s) :
        s = s.replace("\n","")
        s = s.replace("\r","")
        s = s.replace(" ","")
        return s

    def chop2 (self, s) :
        s = s.replace("\n","")
        s = s.replace("\r","")
        return s


    def process (self, xml) :
        global textstore
        facxml = BeautifulStoneSoup(str(xml))
        
        faculty_firstname = facxml.faculty_firstname.string
        faculty_lastname = facxml.faculty_lastname.string
        office = (self.chop(str(facxml.office.building.string)), self.chop(str(facxml.office.room.string)))
        #phone_number = self.chop(str(facxml.phone_number.string))
        email = self.chop(str(facxml.email.string))
        #website = self.chop(str(facxml.website.string))
        #faculty_type = self.chop2(str(facxml.faculty_type.string))

        research_areas = []
        for ra in facxml.research_areas.findAll("research_area"):
            #research_areas.append(self.chop2(str(ra.string)))
            research_areas.append(ra.string)
        office_hours = []
        for oh in facxml.office_hours.findAll("office_hour") :
            office_hours.append({oh.day.string : (oh.start.string, oh.end.string)})
        degrees = []
        for deg in facxml.degrees.findAll("degree") :
            #degrees.append((self.chop2(str(deg.degree_type.string)),self.chop2(str(deg.degree_name.string)), self.chop2(str(deg.institution.string)), self.chop2(str(deg.degree_date.string))))
            degrees.append((deg.degree_type.string,deg.degree_name.string, deg.institution.string, deg.degree_date.string))
        conferences = []
        for con in facxml.conferences.findAll("conference") :
            conferences.append((con.conference_name.string, con.conference_date.string, con.location.string, con.title.string))
        journals = []
        for jour in facxml.journals.findAll("journal") :
            journals.append((jour.journal_name.string, jour.article_title.string, jour.journal_date.string))
        graduate_students = []
        for gs in facxml.graduate_students.findAll("graduate_student") :
            graduate_students.append((gs.student_firstname.string, gs.student_lastname.string, gs.student_type.string, gs.dissertation.string, gs.student_date.string))
        classes = []
        for cls in facxml.classes.findAll("class") :
            classes.append((cls.class_name.string,cls.course_number.string, cls.class_type.string, cls.semester.string, cls.unique.string))
        awards = []
        for awd in facxml.awards.findAll("award") :
            awards.append((awd.award_name.string, awd.award_type.string, awd.award_date.string))
        books = []
        for bk in facxml.books.findAll("book") :
            coauthors = []
            for ca in bk.coauthors.findAll("coauthor"):
                coauthors.append((ca.coauthor_firstname.string, ca.coauthor_lastname.string))
                books.append((bk.book_name.string, coauthors, bk.publisher.string))

        g = db.GqlQuery("SELECT * from faculty_email")
        found = False
        for v in g :
            if (v.faculty_email == email) :
                found = True
        if (found) :
            textstore += '<br /><font color="color:red">Error: faculty_email ' + email + ' already in database.</font>'
            return
        if (not ValidateFaculty.email(email)) :
            textstore += '<br /><font color="color:red">Error Invalid email address: ' + email + '</font>'
            return
        f1 = faculty_email(faculty_email = email)
        f1.put()
        f2 = Faculty(email = email)
        f2.put()
        textstore += "<br />Added faculty_email " + email + " to database."
        textstore += "<br />Added new faculty member " + email + " to database."

        bldg = office[0]
        g = db.GqlQuery("SELECT * from building")
        found = False
        for v in g :
            if (v.building == bldg) :
                bldg = v
                found = True
        if (not found) :
            if (not ValidateAdmin.building(bldg)) :
                textstore += '<br /><font color="color:red"Error, Invalid building abbreviation: ' + bldg + '</font>'
            else :
                f1 = building(building = bldg)
                f1.put()        
                textstore += '<br />Added new building to database: ' + bldg

    def post (self) :
        global textstore
        textstore = ""
        s = self.request.get("xmlinput")
        self.process(s)
        self.get()

if __name__ == "__main__":
    main()