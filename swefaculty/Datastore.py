import cgi
import types
import re

from google.appengine.ext        import db
from google.appengine.ext        import search 
from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template 
import ValidateFaculty

class institution(db.Model) :
    institution = db.StringProperty(required=True)
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
    phone = db.StringProperty(validator=ValidateFaculty.phone)
    building = db.ReferenceProperty(reference_class=building)
    room = db.StringProperty(validator=ValidateFaculty.room)
    email = db.EmailProperty(required=True)
    website = db.StringProperty()
    type = db.ReferenceProperty(reference_class=faculty_type)
    
    
class OfficeHourJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    day = db.StringProperty(choices = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    start = db.StringProperty()
    end = db.StringProperty()

    
class DegreeJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    type = db.ReferenceProperty(reference_class=degree_type)
    major = db.ReferenceProperty(reference_class=degree_name)
    institute = db.ReferenceProperty(reference_class=institution)
    year = db.IntegerProperty(validator=ValidateFaculty.year)
    print
    
class AreaJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    area = db.ReferenceProperty(reference_class=research_area)
    
class StudentJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    student = db.ReferenceProperty(reference_class=student_eid)

class CourseJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    unique = db.IntegerProperty(validator=ValidateFaculty.unique)
    course = db.ReferenceProperty(reference_class=course)
    semester = db.ReferenceProperty(reference_class=semester)

class ArticleJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    journal = db.ReferenceProperty(reference_class=journal_name)
    title = db.TextProperty()
    date = db.StringProperty()#db.DateProperty()

class ConferenceJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    conference = db.ReferenceProperty(reference_class=conference_name)
    title = db.TextProperty()
    location =db.ReferenceProperty(reference_class=location)
    year = db.IntegerProperty(validator=ValidateFaculty.year)
    
class BookJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    title = db.TextProperty()
    publisher = db.ReferenceProperty(reference_class=publisher)

class AwardJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    title = db.TextProperty()
    type = db.ReferenceProperty(reference_class=award_type)
    year = db.IntegerProperty(validator=ValidateFaculty.year)
