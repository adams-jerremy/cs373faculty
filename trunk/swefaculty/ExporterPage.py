                                                                     
                                                                     
                                                                     
                                             
# --------
# Exporter.py
# --------

import cgi

from google.appengine.ext import db 
from google.appengine.ext import webapp

import ValidateAdmin
import ValidateFaculty
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup



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
    phone = db.StringProperty()
    building = db.ReferenceProperty(building)
    room = db.StringProperty(validator=ValidateFaculty.room)
    email = db.EmailProperty(required=True)
    website = db.StringProperty()
    type = db.ReferenceProperty(reference_class=faculty_type)
class rawxml(db.Model):
    xml = db.TextProperty()


'''
textstore is a global variable for passing messages between get and post.
'''
textstore = ""


class MainPage (webapp.RequestHandler) :

    '''
    '''

    def get (self) :
        self.response.out.write('<font size="6">XML Exporter</font>')
        self.response.out.write('<form action="/exporter" method="post">')
        self.response.out.write("""
            <input type="submit" value="Get It!"/>
            </form>""")
        self.response.out.write("<a href=''>Login Page</a><br />")
        self.response.out.write("<a href='admin'>Admin Page</a><br />")
        self.response.out.write("<a href='importer'>Import Faculty Data</a><br />")
        self.response.out.write(textstore)

    '''
    '''


    def process (self, xml) :
        global textstore
        textstore = textstore + xml
        facxml = BeautifulStoneSoup(xml)
        textstore = textstore + "<br /><br />"
        for v in facxml :
            textstore += "blah: " + str(v) + "<br />"
        '''
        faculty_firstname = facxml.faculty_firstname.string
        self.faculty_lastname = facxml.faculty_lastname.string
        self.office = (facxml.office.building.string, facxml.office.room.string)
        self.phone_number = facxml.phone_number.string
        self.email = facxml.email.string
        self.website = facxml.website.string
        self.faculty_type = facxml.faculty_type.string

        for ra in facxml.research_areas.findAll("research_area"):
            self.research_areas.append(ra.string)

        for oh in facxml.office_hours.findAll("office_hour") :
            self.office_hours.append({oh.day.string : (oh.start.string, oh.end.string)})

        for deg in facxml.degrees.findAll("degree") :
            self.degrees.append((deg.degree_type.string, deg.degree_name.string, deg.institution.string, deg.degree_date.string))

        for con in facxml.conferences.findAll("conference") :
            self.conferences.append((con.conference_name.string, con.conference_date.string, con.location.string, con.title.string))

        for jour in facxml.journals.findAll("journal") :
            self.journals.append((jour.journal_name.string, jour.article_title.string, jour.journal_date.string))

        for gs in facxml.graduate_students.findAll("graduate_student") :
            self.graduate_students.append((gs.student_firstname.string, gs.student_lastname.string, gs.student_type.string, gs.dissertation.string, gs.student_date.string))

        for cls in facxml.classes.findAll("class") :
            self.classes.append((cls.class_name.string,cls.course_number.string, cls.class_type.string, cls.semester.string, cls.unique.string))

        for awd in facxml.awards.findAll("award") :
            self.awards.append((awd.award_name.string, awd.award_type.string, awd.award_date.string))

        for bk in facxml.books.findAll("book") :
            coauthors = []
        for ca in bk.coauthors.findAll("coauthor"):
            coauthors.append((ca.coauthor_firstname.string, ca.coauthor_lastname.string))
            self.books.append((bk.book_name.string, coauthors, bk.publisher.string))
        '''


    def post (self) :
        global textstore
        for v in rawxml.all():
            self.response.out.write(v.xml+'<br>')
        textstore = ""
        #s = cgi.escape(self.request.get("xmlinput"))
        #self.process(s)
        self.get()

if __name__ == "__main__":
    main()
