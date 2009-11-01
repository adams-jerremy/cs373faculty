# --------
# Admin.py
# --------

import cgi

from google.appengine.ext import webapp

import ValidateAdmin

'''
The Admin dictionary is a temporary store for the "database" information
read in by the Admin page.  When the database is running with the web
interface this data will be stored in the real database.
'''

Admin = {}
Admin["faculty_eid"] = set()
Admin["student_eid"] = set()
Admin["faculty_type"] = set()
Admin["research_area"] = set()
Admin["building"] = set()
Admin["day"] = set()
Admin["start_time"] = set()
Admin["end_time"] = set()
Admin["degree_type"] = set()
Admin["degree_name"] = set()
Admin["institution"] = set()
Admin["conference_name"] = set()
Admin["journal_name"] = set()
Admin["student_type"] = set()
Admin["course_number"] = set()
Admin["course_name"] = set()
Admin["class_type"] = set()
Admin["semester"] = set()
Admin["award_name"] = set()
Admin["award_type"] = set()

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
    match the field_name in the javascript, the post function, and every
    where else.
    '''

    def printfield (self, field_title, field_name) :
        self.response.out.write(field_title)
        self.response.out.write('<input type="text" name="' + field_name + '" id="' + field_name + '" style="position: absolute; left: 150px" />')
        self.response.out.write('<select id="' + field_name + '_sel" style="position: absolute; left: 315px" onchange="changeField(' + "'" + field_name + "'" + ')">')
        i = list(Admin[field_name])
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

    def get (self) :
        self.response.out.write(javascript)
        self.response.out.write('<font size="6">Admin Database Management</font>')
        self.response.out.write('<form action="/admin" method="post">')
        self.printfield('Faculty EID', 'faculty_eid')
        self.printfield('Student EID', 'student_eid')
        self.printfield('Faculty Type', 'faculty_type')
        self.printfield('Research Area', 'research_area')
        self.printfield('Building Abbreviation', 'building')
        self.printfield('Day', 'day')
        self.printfield('Start Time', 'start_time')
        self.printfield('End Time', 'end_time')
        self.printfield('Degree Type', 'degree_type')
        self.printfield('Degree Name', 'degree_name')
        self.printfield('Institution', 'institution')
        self.printfield('Conference Name', 'conference_name')
        self.printfield('Journal Name', 'journal_name')
        self.printfield('Student Type', 'student_type')
        self.printfield('Course Number', 'course_number')
        self.printfield('Course Name', 'course_name')
        self.printfield('Class Type', 'class_type')
        self.printfield('Semester', 'semester')
        self.printfield('Award Name', 'award_name')
        self.printfield('Award Type', 'award_type')
        self.response.out.write("""
            <br />Remove item:<input type="checkbox" name="Remove"/><br />
            <input type="submit" value="Submit"/>
            </form>""")
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
    '''

    def go (self, field, validator) :
        global textstore
        s = cgi.escape(self.request.get(field))
        if (s != "") :
            if (cgi.escape(self.request.get("Remove")) == "on") :
                if (s in Admin[field]) :
                    Admin[field].remove(s)
                    textstore = textstore + 'Removed ' + field + ' ' + s + '.<br />'
                else :
                    textstore = textstore + '<font color="color:red">' + field + ' ' + s + ' not in database.</font><br />'
            else :
                if validator(s) :
                    if (s not in Admin[field]) :
                        Admin[field].add(s)
                        textstore = textstore + 'Added new ' + field + ' ' + s + '.<br />'
                    else :
                        textstore = textstore + '<font color="color:red">' + field + ' ' + s + ' already in database.</font><br />'
                else :
                    textstore = textstore + '<font color="color:red">Invalid new ' + field + ' ' + s + '.</font><br />'


    '''
    Function "post" checks each input field and then runs "get".
    Each field is checked with the "go" function, which takes in the
    name of the input field to be checked (must match "field_name" for
    the fields that are set up in the "get" function) and the 
    Validator function to be used to check the input.
    '''

    def post (self) :
        global textstore
        textstore = ""
        self.go('faculty_eid', ValidateAdmin.faculty_eid)
        self.go('student_eid', ValidateAdmin.student_eid)
        self.go('faculty_type', ValidateAdmin.faculty_type)
        self.go('research_area', ValidateAdmin.research_area)
        self.go('building', ValidateAdmin.building)
        self.go('day', ValidateAdmin.day)
        self.go('start_time', ValidateAdmin.start_time)
        self.go('end_time', ValidateAdmin.end_time)
        self.go('degree_type', ValidateAdmin.degree_type)
        self.go('degree_name', ValidateAdmin.degree_name)
        self.go('institution', ValidateAdmin.institution)
        self.go('conference_name', ValidateAdmin.conference_name)
        self.go('journal_name', ValidateAdmin.journal_name)
        self.go('student_type', ValidateAdmin.student_type)
        self.go('course_number', ValidateAdmin.course_number)
        self.go('course_name', ValidateAdmin.course_name)
        self.go('class_type', ValidateAdmin.class_type)
        self.go('semester', ValidateAdmin.semester)
        self.go('award_name', ValidateAdmin.award_name)
        self.go('award_type', ValidateAdmin.award_type)
        self.get()

if __name__ == "__main__":
    main()