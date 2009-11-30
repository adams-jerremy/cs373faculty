                                                                     
                                                                     
                                                                     
                                             
# --------
# Exporter.py
# --------

import cgi

from google.appengine.ext import db 
from google.appengine.ext import webapp

import ValidateAdmin
import ValidateFaculty
import ImporterPage
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
    xml = '<?xml version="1.0" encoding="UTF-8" standalone = "yes"?>'
    
    xml += "<faculty_member><faculty_firstname>" + f.faculty_firstname + "</faculty_firstname><faculty_lastname>"\
    + f.faculty_lastname + "</faculty_lastname><office><building>" + f.office[0] + "</building><room>" + f.office[1]\
    + "</room></office><phone_number>" + f.phone_number + "</phone_number><email>" + f.email + "</email><website>"\
    + f.website + "</website><faculty_type>" + f.faculty_type + "</faculty_type><research_areas>"
    
    for ra in f.research_areas :
        xml += "<research_area>" + ra + "</research_area>"
        
    xml += "</research_areas><office_hours>"
    
    for oh in f.office_hours :
        for day in oh.keys() :
            xml += "<office_hour><day>" + day + "</day><start>" + oh[day][0] + "</start><end>" + oh[day][1] + "</end></office_hour>"
    
    xml += "</office_hours><degrees>"
    
    for deg in f.degrees : 
        xml += "<degree><degree_type>" + deg[0] + "</degree_type><degree_name>" + deg[1] + "</degree_name><institution>" + deg[2]\
        + "</institution><degree_date>" + deg[3] + "</degree_date></degree>"
    
    xml += "</degrees><conferences>"
    
    for conf in f.conferences :
        xml += "<conference><conference_name>" + conf[0] + "</conference_name><conference_date>" + conf[1] + "</conference_date><location>"\
        + conf[2] + "</location><title>" + conf[3] + "</title></conference>"
    
    xml += "</conferences><journals>"
    
    for jour in f.journals :
        xml += "<journal><journal_name>" + jour[0] + "</journal_name><article_title>" + jour[1] + "</article_title><journal_date>"\
        + jour[2] + "</journal_date></journal>"
    
    xml += "</journals><graduate_students>"
    
    for gs in f.graduate_students : 
        xml += "<graduate_student><student_firstname>" + gs[0] + "</student_firstname><student_lastname>" + gs[1]\
        + "</student_lastname><student_type>" + gs[2] + "</student_type><dissertation>" + gs[3] + "</dissertation><student_date>"\
        + gs[4] + "</student_date></graduate_student>"
    
    xml += "</graduate_students><classes>"
    
    for c in f.classes :
        xml += "<class><class_name>" + c[0] + "</class_name><course_number>" + c[1] + "</course_number><class_type>" + c[2]\
        + "</class_type><semester>" + c[3] + "</semester><unique>" + c[4] + "</unique></class>"
    
    xml += "</classes><awards>"
    
    for awd in f.awards :
        xml += "<award><award_name>" + awd[0] + "</award_name><award_type>" + awd[1] + "</award_type><award_date>" + awd[2]\
        + "</award_date></award>"
    
    xml += "</awards><books>"
    
    for b in f.books : 
        coauthors = b[1] #b[1] is the list of tuples of coauthors
        c = ""
        for ca in coauthors :   # ca is each tuple of the coauthor's first and last names
            c += "<coauthor><coauthor_firstname>" + ca[0] + "</coauthor_firstname><coauthor_lastname>" + ca[1]\
            + "</coauthor_lastname></coauthor>"
        xml += "<book><book_name>" + b[0] + "</book_name><coauthors>" + c + "</coauthors><publisher>" + b[2] + "</publisher></book>" 
        
    xml += "</books></faculty_member>"
    return xml
  
getEntry = lambda x : db.get(x.key())
getBuilding = lambda k : '' if k.building == None else getEntry(k.building).building
getType = lambda k : '' if k.type == None else getEntry(k.type).type
def doExport(f) :
    temp = Faculty()
    temp.faculty_firstname = f.name
    temp.office = (getBuilding(f),f.room)
    temp.phone_number = f.phone
    temp.email = f.email
    temp.website = '' if f.website is None else f.website
    temp.faculty_type = ' ' if f.type is None or db.get(f.type.key()).faculty_type is None  else db.get(f.type.key()).faculty_type
    
    return export(temp)

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
        for f in Datastore.Faculty.all():
            self.response.out.write(doExport(f))
        textstore = ""
        self.get()

if __name__ == "__main__":
    main()
