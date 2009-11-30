                                                                     
                                                                     
                                                                     
                                             
# --------
# Importer.py
# --------
import types
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

class GraduateStudent(db.Model) :
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    student_type = db.ReferenceProperty(reference_class=student_type)
    dissertation = db.StringProperty()
    date = db.IntegerProperty()


class Faculty(db.Model):
    name = db.StringProperty()
    phone = db.StringProperty()
    building = db.ReferenceProperty(reference_class=building)
    room = db.StringProperty()
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

class AreaJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    area = db.ReferenceProperty(reference_class=research_area)

class StudentJoin(db.Model):
    faculty = db.ReferenceProperty(reference_class=Faculty)
    student = db.ReferenceProperty(reference_class=GraduateStudent)

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
                if (field not in textstore) :
                    textstore[field] = ""
                textstore[field] += 'Created new faculty member account: ' + s + '<br />'
                f2 = Faculty(email = s)
                f2.put()
                return True
            else :
                if (field not in textstore) :
                    textstore[field] = ""
                textstore[field] += '<font color="color:red"> wtf ' + field + ' ' + s + ' already in database.</font><br />'
                return True
        else :
            i = db.GqlQuery("SELECT * FROM " + field)
            found = False
            for v in i :
                if (v.__dict__["_" + field] == s) :
                    found = True
            if (not found) :
                f = constr(**{field : s})
                f.put()
                if (field not in textstore) :
                    textstore[field] = ""
                textstore[field] += 'Added new ' + field + ' ' + s + '.<br />'
                return True
            else :
                if (field not in textstore) :
                    textstore[field] = ""
                textstore[field] += '<font color="color:red">' + field + ' ' + s + ' already in database.</font><br />'
                return True
    else :
        if (field not in textstore) :
            textstore[field] = ""
        textstore[field] += '<font color="color:red">Invalid new ' + field + ' ' + s + '.</font><br />'
        return False


def addcourse(ccno, ccnm, ccty) :
    global textstore
    if ((ccno == "") or (ccnm == "") or (ccty == "")) :
        if ('course' not in textstore) :
            textstore['course'] = ""
        textstore['course'] += '<font color="color:red">Error adding course:  All fields must be filled in.</font><br />'
        return False
    else :
        q = db.GqlQuery("SELECT * FROM course_number WHERE course_number = :1", ccno)
        ccnoobj = q.get()
        q = db.GqlQuery("SELECT * FROM course_name WHERE course_name = :1", ccnm)
        ccnmobj = q.get()
        q = db.GqlQuery("SELECT * FROM course_type WHERE course_type = :1", ccty)
        cctyobj = q.get()
        if ((type(ccnoobj) is types.NoneType) or (type(ccnmobj) is types.NoneType) or (type(cctyobj) is types.NoneType)) :
            if ('course' not in textstore) :
                textstore['course'] = ""
            textstore['course'] += "<font color='color:red'>Error adding course: " + ccno + " " + ccnm + " " + ccty + ".  At least one field is invalid.</font><br />"
            return False
        q = db.GqlQuery("SELECT * FROM course")
        found = False
        for v in q :
            if ((v.course_number.key() == ccnoobj.key()) and (v.course_name.key() == ccnmobj.key()) and (v.course_type.key() == cctyobj.key())) :
                found = v
        if (found != False) :
            if ('course' not in textstore) :
                textstore['course'] = ""
            textstore['course'] += '<font color="color:red">Cannot add course, already in database</font><br />'
            return v
        else :
            if ('course' not in textstore) :
                textstore['course'] = ""
            textstore['course'] += 'Added new course: ' + ccnoobj.course_number + ", " + ccnmobj.course_name + ", " + cctyobj.course_type + "<br />"
            c = course(course_number=ccnoobj.key(), course_name=ccnmobj.key(), course_type=cctyobj.key())
            c.put()
            return c

def strtoint(x) :
    s = re.split("\D",x)
    x = ''
    for v in s :
        if len(v) > 0 :
            x = v
    if (x == '') :
        return 0
    else :
        return int(x)



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
            office_hours.append((self.chop2(str(oh.day.string)), self.chop2(str(oh.start.string)), self.chop2(str(oh.end.string))))
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

        grad_stud = []
        for v in graduate_students :
            q = db.GqlQuery("SELECT * FROM GraduateStudent WHERE first_name = :1 AND last_name = :2", v[0], v[1])
            c = q.get()
            if (type(c) is types.NoneType) :
                validateImport('student_type', ValidateAdmin.student_type, student_type, v[2])
                q = db.GqlQuery("SELECT * FROM student_type WHERE student_type = :1", v[2])
                student_type_key = q.get().key()
                grad_date = strtoint(v[4])
                c = GraduateStudent(first_name=v[0],last_name=v[1],student_type=student_type_key,dissertation=v[3],date=grad_date)
                c.put()
                grad_stud.append(c)
                if ('graduate_students' not in textstore) :
                    textstore['graduate_students'] = ""
                textstore['graduate_students'] += "Added new graduate student " + v[0] + " " + v[1] + " " + v[2] + " " + v[3] + " " + str(grad_date) + "<br />"
            else :
                if ('graduate_students' not in textstore) :
                    textstore['graduate_students'] = ""
                textstore['graduate_students'] += "<font color='color:red'>Cannot add new graduate student " + v[0] + " " + v[1] + ", already in database.</font><br />"
                grad_stud.append(c)
                

        classes2 = []
        for v in classes :
            numvalid = validateImport('course_number', ValidateAdmin.course_number, course_number, v[1])
            namevalid = validateImport('course_name', ValidateAdmin.course_name, course_name, v[0])
            typevalid = validateImport('course_type', ValidateAdmin.course_type, course_type, v[2])
            if (numvalid and namevalid and typevalid) :
                l = addcourse(v[1], v[0], v[2])
                if (l != False) :
                    classes2.append((l,v[3],v[4]))
            else :
                if ('course' not in textstore) :
                    textstore['course'] = ""
                textstore['course'] += "<font color='color:red'>Error adding course: " + v[1] + " " + v[0] + " " + v[2] + ".  At least one field is invalid.</font><br />"                
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
            v.name = faculty_firstname + " " + faculty_lastname
            v.phone = phone_number
            q = db.GqlQuery("SELECT * FROM building WHERE building = :1", office[0])
            bldgobj = q.get()
            v.building = bldgobj.key()
            v.room = office[1]
            v.website = website
            q = db.GqlQuery("SELECT * FROM faculty_type WHERE faculty_type = :1", fac_type)
            typeobj = q.get()
            v.type = typeobj.key()
            v.put()
            if ('faculty_email' not in textstore) :
                textstore['faculty_email'] = ""
            textstore["faculty_email"] += "Creating new faculty member: " + email + "<br />Name: " + faculty_firstname + " " + faculty_lastname + "<br />"
            textstore["faculty_email"] += "Phone: " + phone_number + "<br />Website: " + website + "<br />"
            textstore["faculty_email"] += "Building: " + office[0] + "  Room: " + office[1] + "<br />"
            textstore["faculty_email"] += "Faculty Type: " + fac_type + "<br />"

            fackey = v.key()            

            for i in degrees :
                q = db.GqlQuery("SELECT * FROM degree_type WHERE degree_type = :1", i[0])
                degree_type_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM degree_name WHERE degree_name = :1", i[1])
                degree_name_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM institution WHERE institution = :1", i[2])
                institution_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM DegreeJoin WHERE faculty = :1", fackey)
                degree_year = strtoint(i[3])
                found2 = False
                for j in q :
                    if (j.type.key() == degree_type_key) and (j.major.key() == degree_name_key) and (j.institute.key() == institution_key) and (j.year == degree_year) :
                        found2 = True
                        if ('degrees' not in textstore) :
                            textstore['degrees'] = ""
                        textstore['degrees'] += "<font color='color:red'>Degree " + i[0] + " " + i[1] + " " + i[2] + " " + str(degree_year)
                        textstore['degrees'] += " not added to " + email + ", already in database.</font><br />"
                if (not found2) :
                    k = DegreeJoin(faculty=fackey,type=degree_type_key,major=degree_name_key,institute=institution_key,year=degree_year)
                    k.put()
                    if ('degrees' not in textstore) :
                        textstore['degrees'] = ""
                    textstore['degrees'] += "Added new degree to " + email + ": " + i[0] + " " + i[1] + " " + i[2] + " " + str(degree_year) + "<br />"

            for i in research_areas :
                q = db.GqlQuery("SELECT * FROM research_area WHERE research_area = :1", i)
                k = q.get().key()
                q = db.GqlQuery("SELECT * FROM AreaJoin WHERE faculty = :1", fackey)
                found2 = False
                for j in q :
                    if (j.area.key() == k) :
                        found2 = True
                        if ('research_areas' not in textstore) :
                            textstore['research_areas'] = ""
                        textstore['research_areas'] += "<font color='color:red'>Research Area " + i
                        textstore['research_areas'] += " not added to " + email + ", already in database.</font><br />"
                if (not found2) :
                    k = AreaJoin(faculty=fackey,area=k)
                    k.put()
                    if ('research_areas' not in textstore) :
                        textstore['research_areas'] = ""
                    textstore['research_areas'] += "Added new research area to " + email + ": " + i + "<br />"

            for i in office_hours :
                q = db.GqlQuery("SELECT * FROM OfficeHourJoin WHERE faculty = :1", fackey)
                found2 = False
                for j in q :
                    if (j.day == i[0]) and (j.start == i[1]) and (j.end == i[2]) :
                        found2 = True
                        if ('office_hours' not in textstore) :
                            textstore['office_hours'] = ""
                        textstore['office_hours'] += "<font color='color:red'>Office Hours " + i[0] + " " + i[1] + " " + i[2]
                        textstore['office_hours'] += " not added to " + email + ", already in database.</font><br />"
                if (not found2) :
                    k = OfficeHourJoin(faculty=fackey,day=i[0],start=i[1],end=i[2])
                    k.put()
                    if ('office_hours' not in textstore) :
                        textstore['office_hours'] = ""
                    textstore['office_hours'] += "Added new office hours to " + email + ": " + i[0] + " " + i[1] + " " + i[2] + "<br />"

            for i in grad_stud :
                q = db.GqlQuery("SELECT * FROM StudentJoin WHERE faculty = :1 AND student = :2", fackey, i.key())
                c = q.get()
                if (type(c) is types.NoneType) :
                    sj = StudentJoin(faculty=fackey,student=i)
                    sj.put()
                    if ('grad_stud' not in textstore) :
                        textstore['grad_stud'] = ""
                    textstore['grad_stud'] += "Added graduate student " + str(i) + " to " + email + ".<br />"
                else :
                    if ('grad_stud' not in textstore) :
                        textstore['grad_stud'] = ""
                    textstore['grad_stud'] += "<font color='color:red'>Cannot add graduate student " + str(i) + " to " + email + ", association already exists.</font><br />"


            for i in classes2 :
                q = db.GqlQuery("SELECT * FROM semester WHERE semester = :1", i[1])
                semester_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM CourseJoin WHERE faculty = :1", fackey)
                class_unique = strtoint(i[2])
                found2 = False
                for j in q :
                    if (j.unique == class_unique) and (j.semester.key() == semester_key) and (j.course.key() == i[0].key()) :
                        found2 = True
                        if ('classes' not in textstore) :
                            textstore['classes'] = ""
                        textstore['classes'] += "<font color='color:red'>Class " + str(i[0].key()) + " " + i[1] + " " + str(class_unique)
                        textstore['classes'] += " not added to " + email + ", already in database.</font><br />"
                if (not found2) :
                    k = CourseJoin(faculty=fackey,unique=class_unique,course=i[0].key(),semester=semester_key)
                    k.put()
                    if ('classes' not in textstore) :
                        textstore['classes'] = ""
                    textstore['classes'] += "Added new class to " + email + ": " + str(i[0].key()) + " " + i[1] + " " + str(class_unique) + "<br />"

            for i in journals :
                q = db.GqlQuery("SELECT * FROM journal_name WHERE journal_name = :1", i[0])
                journal_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM ArticleJoin WHERE faculty = :1", fackey)
                found2 = False
                for j in q :
                    if (j.title == i[1]) and (j.date == i[2]) and (j.journal.key() == journal_key) :
                        found2 = True
                        if ('journals' not in textstore) :
                            textstore['journals'] = ""
                        textstore['journals'] += "<font color='color:red'>Journal article " + i[0] + " " + i[1] + " " + i[2]
                        textstore['journals'] += " not added to " + email + ", already in database.</font><br />"
                if (not found2) :
                    k = ArticleJoin(faculty=fackey,journal=journal_key,title=i[1],date=i[2])
                    k.put()
                    if ('journals' not in textstore) :
                        textstore['journals'] = ""
                    textstore['journals'] += "Added new journal article to " + email + ": " + i[0] + " " + i[1] + " " + i[2] + "<br />"

            for i in conferences :
                q = db.GqlQuery("SELECT * FROM conference_name WHERE conference_name = :1", i[0])
                conf_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM location WHERE location = :1", i[2])
                loc_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM ConferenceJoin WHERE faculty = :1", fackey)
                conf_year = strtoint(i[1])
                found2 = False
                for j in q :
                    if (j.title == i[3]) and (j.year == conf_year) and (j.conference.key() == conf_key) and (j.location.key() == loc_key) :
                        found2 = True
                        if ('conferences' not in textstore) :
                            textstore['conferences'] = ""
                        textstore['conferences'] += "<font color='color:red'>Conference presentation " + i[0] + " " + str(conf_year) + " " + i[2] + " " + i[3]
                        textstore['conferences'] += " not added to " + email + ", already in database.</font><br />"
                if (not found2) :
                    k = ConferenceJoin(faculty=fackey,conference=conf_key,title=i[3],location=loc_key,year=conf_year)
                    k.put()
                    if ('conferences' not in textstore) :
                        textstore['conferences'] = ""
                    textstore['conferences'] += "Added new conference presentation to " + email + ": " + i[0] + " " + str(conf_year) + " " + i[2] + " " + i[3] + "<br />"

            for i in books :
                q = db.GqlQuery("SELECT * FROM publisher WHERE publisher = :1", i[2])
                pub_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM BookJoin WHERE faculty = :1", fackey)
                found2 = False
                for j in q :
                    if (j.title == i[0]) :
                        found2 = True
                        if ('books' not in textstore) :
                            textstore['books'] = ""
                        textstore['books'] += "<font color='color:red'>Book " + i[0] + " " + i[2]
                        textstore['books'] += " not added to " + email + ", already in database.</font><br />"
                if (not found2) :
                    k = BookJoin(faculty=fackey,title=i[0],publisher=pub_key)
                    k.put()
                    if ('books' not in textstore) :
                        textstore['books'] = ""
                    textstore['books'] += "Added new book to " + email + ": " + i[0] + " " + i[2] + "<br />"

            for i in awards :
                q = db.GqlQuery("SELECT * FROM award_type WHERE award_type = :1", i[1])
                at_key = q.get().key()
                q = db.GqlQuery("SELECT * FROM AwardJoin WHERE faculty = :1", fackey)
                found2 = False
                awd_year = strtoint(i[2])
                for j in q :
                    if (j.title == i[0]) and (j.type.key() == at_key) and (j.year == awd_year) :
                        found2 = True
                        if ('awards' not in textstore) :
                            textstore['awards'] = ""
                        textstore['awards'] += "<font color='color:red'>Award " + i[0] + " " + i[1] + " " + str(awd_year)
                        textstore['awards'] += " not added to " + email + ", already in database.</font><br />"
                if (not found2) :
                    k = AwardJoin(faculty=fackey,title=i[0],type=at_key,year=awd_year)
                    k.put()
                    if ('awards' not in textstore) :
                        textstore['awards'] = ""
                    textstore['awards'] += "Added new award to " + email + ": " + i[0] + " " + i[1] + " " + str(awd_year) + "<br />"



    def post (self) :
        global textstore
        textstore = {}
        s = self.request.get("xmlinput")
        self.process(s)
        self.get()

if __name__ == "__main__":
    main()