                                                                     
                                                                     
                                                                     
                                             
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

class student_eid(db.Model) :
    student_eid = db.StringProperty(required=True)
class faculty_type(db.Model) :
    faculty_type = db.StringProperty(required=True)
class research_area(db.Model) :
    research_area = db.StringProperty(required=True)
class building(db.Model) :
    building = db.StringProperty(required=True)
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
textstore = {}


def validateImport (field, validator, constr, s) :
    global textstore
    if validator(s) :
        if (field == "faculty_email") :
            i = db.GqlQuery("SELECT * FROM Faculty")
            found = False
            for v in i :
                if (v.email == s) :
                    found = True
            if (not found) :
                textstore[field] = 'Created new faculty member account: ' + s + '<br />'
                f2 = Faculty(email = s)
                f2.put()
            else :
                textstore[field] = '<font color="color:red">' + field + ' ' + s + ' already in database.</font><br />'
        else :
            i = db.GqlQuery("SELECT * FROM " + field)
            found = False
            for v in i :
                if (v.__dict__["_" + field] == s) :
                    found = True
            if (not found) :
                f = constr(**{field : s})
                f.put()
                textstore[field] = 'Added new ' + field + ' ' + s + '.<br />'
            else :
                textstore[field] = '<font color="color:red">' + field + ' ' + s + ' already in database.</font><br />'
    else :
        textstore[field] = '<font color="color:red">Invalid new ' + field + ' ' + s + '.</font><br />'



class MainPage (webapp.RequestHandler) :

    '''
    '''

    def get (self) :
        self.response.out.write('<font size="6">XML Importer</font>')
        self.response.out.write('<form action="/importer" method="post">')
        self.response.out.write("""
            <textarea name="xmlinput" cols="80" rows="20"></textarea>
            <input type="submit" value="Submit"/>
            </form>""")
        self.response.out.write("<a href=''>Login Page</a><br />")
        self.response.out.write("<a href='admin'>Admin Page</a><br />")
        self.response.out.write("<a href='exporter'>Export Faculty Data</a><br />")
        self.response.out.write("<br />Import result:<br />")
        for v in textstore.values() :
            self.response.out.write(v)

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

        faculty_firstname = self.chop(str(facxml.faculty_firstname.string))
        faculty_lastname = self.chop(str(facxml.faculty_lastname.string))
        phone_number = self.chop(str(facxml.phone_number.string))
        website = self.chop(str(facxml.website.string))
        email = self.chop(str(facxml.email.string))
        office = (self.chop(str(facxml.office.building.string)), self.chop(str(facxml.office.room.string)))
        research_areas = []
        for ra in facxml.research_areas.findAll("research_area"):
            research_areas.append(self.chop2(str(ra.string)))
        fac_type = self.chop2(str(facxml.faculty_type.string))
        degrees = []
        for deg in facxml.degrees.findAll("degree") :
            degrees.append((self.chop2(str(deg.degree_type.string)),self.chop2(str(deg.degree_name.string)), self.chop2(str(deg.institution.string)), self.chop2(str(deg.degree_date.string))))
        conferences = []
        for con in facxml.conferences.findAll("conference") :
            conferences.append((self.chop2(str(con.conference_name.string)), self.chop2(str(con.conference_date.string)), self.chop2(str(con.location.string)), self.chop2(str(con.title.string))))
        journals = []
        for jour in facxml.journals.findAll("journal") :
            journals.append((self.chop2(str(jour.journal_name.string)), self.chop2(str(jour.article_title.string)), self.chop2(str(jour.journal_date.string))))
        graduate_students = []
        for gs in facxml.graduate_students.findAll("graduate_student") :
            graduate_students.append((self.chop2(str(gs.student_firstname.string)), self.chop2(str(gs.student_lastname.string)), self.chop2(str(gs.student_type.string)), self.chop2(str(gs.dissertation.string)), self.chop2(str(gs.student_date.string))))
        office_hours = []
        for oh in facxml.office_hours.findAll("office_hour") :
            office_hours.append({oh.day.string : (oh.start.string, oh.end.string)})
        classes = []
        for cls in facxml.classes.findAll("class") :
            classes.append((self.chop2(str(cls.class_name.string)),self.chop2(str(cls.course_number.string)), self.chop2(str(cls.class_type.string)), self.chop2(str(cls.semester.string)), self.chop2(str(cls.unique.string))))
        awards = []
        for awd in facxml.awards.findAll("award") :
            awards.append((self.chop2(str(awd.award_name.string)), self.chop2(str(awd.award_type.string)), self.chop2(str(awd.award_date.string))))
        books = []
        for bk in facxml.books.findAll("book") :
            coauthors = []
            for ca in bk.coauthors.findAll("coauthor"):
                coauthors.append((self.chop2(str(ca.coauthor_firstname.string)), self.chop2(str(ca.coauthor_lastname.string))))
                books.append((self.chop2(str(bk.book_name.string)), coauthors, self.chop2(str(bk.publisher.string))))

        # Admin page imports:
        validateImport('faculty_email', ValidateFaculty.email, Faculty, email)
        bldg = office[0]
        validateImport('building', ValidateAdmin.building, building, bldg)
        for v in research_areas :
            validateImport('research_area', ValidateAdmin.research_area, research_area, v)
        validateImport('faculty_type', ValidateAdmin.faculty_type, faculty_type, fac_type)
        for dt in degrees:
            validateImport('degree_type', ValidateAdmin.degree_type, degree_type, dt[0])
            validateImport('degree_name', ValidateAdmin.degree_name, degree_name, dt[1])
            validateImport('institution', ValidateAdmin.institution, institution, dt[2])
        for con in conferences :
            validateImport('conference_name', ValidateAdmin.conference_name, conference_name, con[0])
            validateImport('location', ValidateAdmin.location, location, con[2])
        for jour in journals :
            validateImport('journal_name', ValidateAdmin.journal_name, journal_name, jour[0])
        for v in books :
            validateImport('publisher', ValidateAdmin.publisher, publisher, v[2])
        for v in graduate_students :
            validateImport('student_type', ValidateAdmin.student_type, student_type, v[2])
        for v in classes :
            validateImport('course_number', ValidateAdmin.course_number, course_number, v[1])
            validateImport('course_name', ValidateAdmin.course_name, course_name, v[0])
            validateImport('course_type', ValidateAdmin.course_type, course_type, v[2])
            validateImport('semester', ValidateAdmin.semester, semester, v[3])
        for v in awards :
            validateImport('award_type', ValidateAdmin.award_type, award_type, v[1])

        # Faculty page imports:
        i = db.GqlQuery("SELECT * from Faculty")
        found = False
        for v in i :
            if v.email == email :
                found = v
        if (found != False) :
            textstore["faculty_email"] = faculty_firstname + faculty_lastname + phone_number + website
            v.name = faculty_firstname + " " + faculty_lastname
            v.phone = phone_number
            v.room = office[1]
            v.website = website
            # v.building = set reference to buildling table
            # v.type = reference '' ''
            v.put()


    def post (self) :
        global textstore
        textstore = {}
        s = self.request.get("xmlinput")
        self.process(s)
        self.get()

if __name__ == "__main__":
    main()