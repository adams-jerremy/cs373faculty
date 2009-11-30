                                                                     
                                                                     
                                                                     
                                             
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
import Datastore


'''
These classes create the database model.  For now, the class
name must match the column name in the database because the
functions below which access the information in queries, 
create new rows, etc all depend on this.
'''

class rawxml(db.Model):
    xml = db.TextProperty()


'''
textstore is a global variable for passing messages between get and post.
'''
textstore = ""

get = lambda k: '' if db.get(k.key()) is None else db.get(k.key())

class Faculty() :
    faculty_firstname = ""
    faculty_lastname = ""
    office = ()
    phone_number = ""
    email = ""
    website = ""
    faculty_type = ""
    research_areas = []
    office_hours = []
    degrees = []
    conferences = []
    journals = []
    graduate_students = []
    classes = []
    awards = []
    books = []
    
def export(f) :
    if f.name is not None :
        name = str(f.name)
        name = name.partition(' ')
        faculty_firstname =  name[0]
        faculty_lastname = name[2]
    if f.building is None :
        office = ("","")
    else :
        building = f.building
        office = (building.building,f.room)
    if f.phone is not None :
        phone_number = f.phone
    email = f.email
    if f.website is not None :
        website = f.website
    if f.type is not None :
        type = f.type
        faculty_type = type.faculty_type
    # xml = '<?xml version="1.0" encoding="UTF-8" standalone = "yes"?>'
    xml = ""
    xml += "<faculty_member><faculty_firstname>" + faculty_firstname + "</faculty_firstname><faculty_lastname>"
    xml += faculty_lastname + "</faculty_lastname><office><building>" + office[0] + "</building><room>" + office[1]
    xml += "</room></office><phone_number>" + phone_number + "</phone_number><email>" + email + "</email><website>"
    xml += website + "</website><faculty_type>" + faculty_type + "</faculty_type><research_areas>"
    
    areas = Datastore.AreaJoin.gql("WHERE faculty=:1",f)
    for ra in areas :
        area = ra.area
        xml += "<research_area>" + area.research_area + "</research_area>"
        
    xml += "</research_areas><office_hours>"
    
    ohs = Datastore.OfficeHourJoin.gql("WHERE faculty=:1",f)
    for oh in ohs :
        xml += "<office_hour><day>" + oh.day + "</day><start>" + oh.start + "</start><end>" + oh.end + "</end></office_hour>"
    
    xml += "</office_hours><degrees>"
    
    degs = Datastore.DegreeJoin.gql("WHERE faculty=:1",f)
    for deg in degs : 
        type = deg.type
        major = deg.major
        institute = deg.institute
        year = deg.year
        xml += "<degree><degree_type>" + type.degree_type + "</degree_type><degree_name>" + major.degree_name + "</degree_name><institution>" + institute.institution\
        + "</institution><degree_date>" + str(year) + "</degree_date></degree>"
    
    xml += "</degrees><conferences>"
    
    confs = Datastore.ConferenceJoin.gql("WHERE faculty=:1",f)
    for conf in confs :
        conference = conf.conference
        title = conf.title
        location = conf.location
        year = conf.year
        xml += "<conference><conference_name>" + conference.conference_name + "</conference_name><conference_date>" + year + "</conference_date><location>"\
        + location.location + "</location><title>" + title + "</title></conference>"
    
    xml += "</conferences><journals>"
    
    jours = Datastore.ArticleJoin.gql("WHERE faculty=:1",f)
    for jour in jours :
        journal = jour.journal
        title = jour.title
        date = jour.date
        xml += "<journal><journal_name>" + journal.journal_name + "</journal_name><article_title>" + title + "</article_title><journal_date>"\
        + date + "</journal_date></journal>"
    
    xml += "</journals><graduate_students>"
    
    gss = Datastore.StudentJoin.gql("WHERE faculty=:1",f)
    for gs in gss :
        student = gs.student
        studenttype = student.student_type
        xml += "<graduate_student><student_firstname>" + student.first_name + "</student_firstname><student_lastname>" + student.last_name\
        + "</student_lastname><student_type>" + studenttype.student_type + "</student_type><dissertation>" + student.dissertation + "</dissertation><student_date>"\
        + student.date + "</student_date></graduate_student>"
    
    xml += "</graduate_students><classes>"
    
    cs = Datastore.CourseJoin.gql("WHERE faculty=:1",f)
    for c in cs :
        course = c.course
        semester = c.semester
        xml += "<class><class_name>" + course.course_name + "</class_name><course_number>" + course.course_number + "</course_number><class_type>" + course.course_type\
        + "</class_type><semester>" + semester.semester + "</semester><unique>" + course.unique + "</unique></class>"
    
    xml += "</classes><awards>"
    
    awds = Datastore.AwardJoin.gql("WHERE faculty=:1",f)
    for awd in awds :
	type = awd.type
        xml += "<award><award_name>" + awd.title + "</award_name><award_type>" + type.award_type + "</award_type><award_date>" + awd.year\
        + "</award_date></award>"
    
    xml += "</awards><books>"
    
    bs = Datastore.BookJoin.gql("WHERE faculty=:1",f)
    for b in bs :
        title = b.title
        publisher = b.publisher
        coauthors = Datastore.BookJoin.gql("WHERE title=:1",title)
        c = ""
        for ca in coauthors :   # ca is each tuple of the coauthor's first and last names
            if ca.name != f.name :
                name = str(ca.name)
                name = name.partition(' ')
                cafn = name[0]
                caln = name[2]
                cafn
                c += "<coauthor><coauthor_firstname>" + cafn + "</coauthor_firstname><coauthor_lastname>" + caln\
                + "</coauthor_lastname></coauthor>"
        xml += "<book><book_name>" + title + "</book_name><coauthors>" + c + "</coauthors><publisher>" + publisher.publisher + "</publisher></book>" 
        
    xml += "</books></faculty_member>"
    return xml
  
getEntry = lambda x : db.get(x.key())
getBuilding = lambda k : '' if k.building == None else getEntry(k.building).building
getType = lambda k : '' if k.type == None else getEntry(k.type).type
def doExport(f) :
    return export(f)

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
    

    def post (self) :
        global textstore
#        for v in rawxml.all():
#            self.response.out.write(v.xml+'<br>')
	self.response.out.write('<?xml version="1.0" encoding="UTF-8" standalone = "yes"?>')
	self.response.out.write("<faculty_members>")
        for f in Datastore.Faculty.all():
            self.response.out.write(doExport(f))
	self.response.out.write("</faculty_members>")
        textstore = ""
        #self.get()

if __name__ == "__main__":
    main()