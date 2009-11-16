                                                                     
                                                                     
                                                                     
                                             
# --------
# Admin.py
# --------

import cgi

from google.appengine.ext import db 
from google.appengine.ext import webapp

import ValidateAdmin
import ValidateFaculty

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

'''
We have a little javascript to take drop down lists in the Admin page
and stuff them into the text input fields for easy editing.
'''
javascript = """
<script type="text/javascript">
window.onload=setup;
function setup() {}
function changeField(a) {
   var x = document.getElementById(a + '_sel');
   document.getElementById(a).value = x.options[x.selectedIndex].text;
}
</script>
"""

class MainPage (webapp.RequestHandler) :

    '''
    The function printfield prints out the intput field and the select
    drop down box for each input field on the admin page.  The function takes
    in the field_title displayed next to the input field, used for display
    purposes only, and the field_name, which is important because it must
    match the field_name in the javascript, the post function, the name
    of the database class we get with the query, and the name of the
    column in the database class.
    '''

    def printfield (self, field_title, field_name) :
        self.response.out.write(field_title)
        self.response.out.write('<input type="text" name="' + field_name + '" id="' + field_name + '" style="position: absolute; left: 150px" />')
        self.response.out.write('<select id="' + field_name + '_sel" style="position: absolute; left: 315px" onchange="changeField(' + "'" + field_name + "'" + ')">')
        q = db.GqlQuery("SELECT * FROM " + field_name)
        i = list()
        for v in q :
            i.append(v.__dict__["_" + field_name])
        i.sort()
        for v in i :
            self.response.out.write("<option>" + v + "</option>")
        self.response.out.write("</select><br />")

    '''
    Fuction get prints out the web page.  First the javascript, then
    a page title and the big form that makes up the page.  Finally the 
    result of the Validation from post() is printed out at the bottom -
    it was stored in textstore.
    '''

    def course(self) :
        self.response.out.write("<br />Build Course: <select name='course_course_number'>")
        q = db.GqlQuery("SELECT * FROM course_number")
        i = list()
        for v in q :
            i.append(v.course_number)
        i.sort()
        for v in i :
            self.response.out.write("<option>" + v + "</option>")
        self.response.out.write("</select><select name='course_course_name'>")
        q = db.GqlQuery("SELECT * FROM course_name")
        i = list()
        for v in q :
            i.append(v.course_name)
        i.sort()
        for v in i :
            self.response.out.write("<option>" + v + "</option>")
        self.response.out.write("</select><select name='course_course_type'>")
        q = db.GqlQuery("SELECT * FROM course_type")
        i = list()
        for v in q :
            i.append(v.course_type)
        i.sort()
        for v in i :
            self.response.out.write("<option>" + v + "</option>")
        self.response.out.write("</select>")
        self.response.out.write("  Courses: <select name='course'>")
        q = db.GqlQuery("SELECT * FROM course")
        i = list()
        for v in q :
            blah = v.course_number.course_number + ", " + v.course_name.course_name + ", " + v.course_type.course_type
            i.append(blah)
        i.sort()
        for v in i :
            self.response.out.write("<option>" + v + "</option>")
        self.response.out.write("</select><br />")

    def get (self) :
        self.response.out.write(javascript)
        self.response.out.write('<font size="6">Admin Database Management</font>')
        self.response.out.write('<form action="/admin" method="post">')
        self.printfield('Faculty email', 'faculty_email')
        self.printfield('Student EID', 'student_eid')
        self.printfield('Faculty Type', 'faculty_type')
        self.printfield('Research Area', 'research_area')
        self.printfield('Building Abbreviation', 'building')
        self.printfield('Start Time', 'start_time')
        self.printfield('End Time', 'end_time')
        self.printfield('Degree Type', 'degree_type')
        self.printfield('Degree Name', 'degree_name')
        self.printfield('Institution', 'institution')
        self.printfield('Conference Name', 'conference_name')
        self.printfield('Conference Location', 'location')
        self.printfield('Journal Name', 'journal_name')
        self.printfield('Publisher', 'publisher')
        self.printfield('Student Type', 'student_type')
        self.printfield('Course Number', 'course_number')
        self.printfield('Course Name', 'course_name')
        self.printfield('Course Type', 'course_type')
        self.printfield('Semester', 'semester')
        self.printfield('Award Name', 'award_name')
        self.printfield('Award Type', 'award_type')
        self.response.out.write("""
            <br />Remove item:<input type="checkbox" name="Remove"/><br />
            """)
        self.course()
        self.response.out.write("""
            Add Course<input type="checkbox" name="AddCourse"/>
            Remove Course<input type="checkbox" name="RemoveCourse"/><br /><br />
            <input type="submit" value="Submit"/>
            </form>""")
        self.response.out.write("<a href=''>Login Page</a><br />")
        self.response.out.write("<a href='importer'>Import Faculty Data</a><br />")
        self.response.out.write("<a href='exporter'>Export Faculty Data</a><br />")
        self.response.out.write(textstore)

    '''
    Fuction "go" processes each field on the Admin page.
    It runs when the "Submit" button is pressed.  If the "Remove" checkbox
    was checked, the user wants to remove any text inputs in the text fields
    from the database so we attempt to do so and save a result string
    in textstore for printing by "get".  If Remove was not checked, we 
    check to see if the input string was valid for that field (determined
    by the second input to "go", validator, which is a function).  The
    input field is either added to the database or an error message is 
    put into textstore.
    To add a new field to the database we create a new object and use 
    put().  The constructor is passed into "go" as constr, it is 
    different for each field and is just to the database class.
    '''

    def go (self, field, validator, constr) :
        global textstore
        s = cgi.escape(self.request.get(field))
        if (s != "") :
            if (cgi.escape(self.request.get("Remove")) == "on") :
                i = db.GqlQuery("SELECT * FROM " + field)
                found = ""
                for v in i :
                    if (v.__dict__["_" + field] == s) :
                        found = v
                if (found != "") :
                    found.delete()
                    textstore = textstore + 'Removed ' + field + ' ' + s + '.<br />'
                else :
                    textstore = textstore + '<font color="color:red">' + field + ' ' + s + ' not in database.</font><br />'
            else :
                if validator(s) :
                    i = db.GqlQuery("SELECT * FROM " + field)
                    found = False
                    for v in i :
                        if (v.__dict__["_" + field] == s) :
                            found = True
                    if (not found) :
                        f = constr(**{field : s})
                        f.put()
                        textstore = textstore + 'Added new ' + field + ' ' + s + '.<br />'
                        if (field == "faculty_email") :
                            textstore = textstore + 'Created new faculty member account: ' + s + '<br />'
                            f2 = Faculty(email = s)
                            f2.put()
                    else :
                        textstore = textstore + '<font color="color:red">' + field + ' ' + s + ' already in database.</font><br />'
                else :
                    textstore = textstore + '<font color="color:red">Invalid new ' + field + ' ' + s + '.</font><br />'

    def addcourse(self) :
        global textstore
        if (cgi.escape(self.request.get("AddCourse")) == "on") :
            ccno = cgi.escape(self.request.get("course_course_number"))
            ccnm = cgi.escape(self.request.get("course_course_name"))
            ccty = cgi.escape(self.request.get("course_course_type"))
            if ((ccno == "") or (ccnm == "") or (ccty == "")) :
                textstore = textstore + '<font color="color:red">Error adding course:  All fields must be filled in.'
            else :
                q = db.GqlQuery("SELECT * FROM course_number WHERE course_number = :1", ccno)
                ccnoobj = q.get()
                q = db.GqlQuery("SELECT * FROM course_name WHERE course_name = :1", ccnm)
                ccnmobj = q.get()
                q = db.GqlQuery("SELECT * FROM course_type WHERE course_type = :1", ccty)
                cctyobj = q.get()
                q = db.GqlQuery("SELECT * FROM course")
                found = False
                for v in q :
                    if ((v.course_number.key() == ccnoobj.key()) and (v.course_name.key() == ccnmobj.key()) and (v.course_type.key() == cctyobj.key())) :
                        found = True
                if (found) :
                    textstore = textstore + '<font color="color:red">Cannot add course, already in database'
                else :
                    textstore = textstore + 'Added new course: ' + ccnoobj.course_number + ", " + ccnmobj.course_name + ", " + cctyobj.course_type + "<br />"
                    c = course(course_number=ccnoobj.key(), course_name=ccnmobj.key(), course_type=cctyobj.key())
                    c.put()


    def removecourse(self) :
        global textstore
        if (cgi.escape(self.request.get("RemoveCourse")) == "on") :
            crs = cgi.escape(self.request.get("course"))
            if (crs == "") :
                textstore = textstore + '<font color="color:red">Error removing course:  None selected.'
            else:
                textstore = textstore + '<font color="color:red">Sorry, course removal not implemented yet.'


    '''
    Function "post" checks each input field and then runs "get".
    Each field is checked with the "go" function, which takes in the
    name of the input field to be checked (must match "field_name" for
    the fields that are set up in the "get" function), the 
    Validator function to be used to check the input, and the constructor
    class for the database which will be used to create a new entry
    in the database if all the tests pass.
    '''

    def post (self) :
        global textstore
        textstore = ""
        self.go('faculty_email', ValidateFaculty.email, faculty_email)
        self.go('student_eid', ValidateAdmin.student_eid, student_eid)
        self.go('faculty_type', ValidateAdmin.faculty_type, faculty_type)
        self.go('research_area', ValidateAdmin.research_area, research_area)
        self.go('building', ValidateAdmin.building, building)
        self.go('start_time', ValidateAdmin.start_time, start_time)
        self.go('end_time', ValidateAdmin.end_time, end_time)
        self.go('degree_type', ValidateAdmin.degree_type, degree_type)
        self.go('degree_name', ValidateAdmin.degree_name, degree_name)
        self.go('institution', ValidateAdmin.institution, institution)
        self.go('conference_name', ValidateAdmin.conference_name, conference_name)
        self.go('location', ValidateAdmin.location, location)
        self.go('journal_name', ValidateAdmin.journal_name, journal_name)
        self.go('publisher', ValidateAdmin.publisher, publisher)
        self.go('student_type', ValidateAdmin.student_type, student_type)
        self.go('course_number', ValidateAdmin.course_number, course_number)
        self.go('course_name', ValidateAdmin.course_name, course_name)
        self.go('course_type', ValidateAdmin.course_type, course_type)
        self.go('semester', ValidateAdmin.semester, semester)
        self.go('award_name', ValidateAdmin.award_name, award_name)
        self.go('award_type', ValidateAdmin.award_type, award_type)
        self.addcourse()
        self.removecourse()
        self.get()

if __name__ == "__main__":
    main()