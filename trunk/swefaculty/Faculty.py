# --------
# Faculty.py
# --------


import cgi

from google.appengine.ext import webapp

import ValidateFaculty

options = {"facTypes":("","Professor","Lecturer","Researcher"),
           "buildings":("","TAY","PAI","ACES","ENS"),
           "researchAreas":("","AI","Compilers","OS","Robotics","Algorithms"),
           "gradStudents":("","Student1(st0001)","Student2(st0002)"),
           "courses":("","55555","55556"),
           "books":("","AwesomeBook","Anotherbook","LessAwesomeBook"),
           "awards":("","Awards","SuperAwesomeAward")
           }
'''
Simple class for holding onto faculty data
'''
class Faculty:

    def __init__(self):
        self.phone = ""
        self.name = ""
        self.building = ""
        self.room = ""
        self.email = ""
        self.website = "http://"
        self.officeHours = []
        self.type = ""
        self.degrees = []
        self.researchAreas = []
        self.gradStudents = []
        self.courses = []
        self.articles = []
        self.conferences = []
        self.books= []
        self.awards = []
'''
Simple class for holding onto conference data
'''        
class Conference:
    conferences = ("","Conference","AnotherConference","aThird")
    locations = ("","Location","Burbank","Singapore","Fiji","Stalingrad")
    def __init__(self,name,location,title,date):
        self.name = name
        self.location = location
        self.title = title
        self.date = date
    def __len__(self):
        return len(self.title)+len(self.name)+len(self.date)+len(self.location)+len("at  in , ")
    
'''
Simple class for holding onto article data
'''        
class Article:
    journals = ("","Scientific American","Applied Computing", "Robotic Murder Monthly")
    def __init__(self,t,j,d):
        self.title = t
        self.journal = j
        self.date = d
    def __len__(self):
        return len(self.title)+len(self.journal)+len(self.date)+len(" in , ")
    
'''
Simple class for holding onto degree data
'''        
class Degree:
    types = ("","B.S.","B.A.","M.S.","M.A.","Ph.D.")
    institutions = ("","UT","Less Important")
    def __init__(self,t,i,d):
        self.type = t
        self.institution = i
        self.date = d
    def __len__(self):
        return len(self.type)+len(self.institution)+len(self.date)+len(" from in ")    

'''
Simple class for holding onto officeHour data
'''        
class OfficeHour:
    days = ("","M","T","W","R","F")
    times = ("","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30")
    def __init__(self,day,b,e):
        self.day = day
        self.beginTime = b
        self.endTime = e
    def __len__(self):
        return len(self.day)+len(self.beginTime)+len(self.endTime)+len(" from in ")
'''
function to check if any of the values passed in are filled
'''
def anyFilled(*t):
    for e in t:
        if e!="": return True;
        
'''
Function for making 'generic' text boxes
'''

def textBox(t):
    s = '<textarea rows ="'
    s+= str(len(t)+1)
    s+= '" cols="'
    s+= str(max(map(len,t)) if len(t)>0 else 25)
    s+='" readonly="readonly">'
    for o in t:
        s+=o
        s+='\n'
    s+='</textarea>'
    return s

'''
function for making conference text boxes- a little more involved than regular textboxes
'''

def conferenceTextBox(f):
    s = '<textarea rows ="'
    s+= str(len(f.conferences)+1)
    s+= '" cols="'
    s+= str(max(map(len,f.conferences)) if len(f.conferences)>0 else 25)
    s+='" readonly="readonly">'
    for conf in f.conferences: #name location title date
        s+=conf.title
        s+= ' at '
        s+=conf.name
        s+= ' in '
        s+=conf.location
        s+=', '
        s+=conf.date
        s+='\n'
    s+='</textarea>'
    return s    

'''
function for making article text boxes- a little more involved than regular textboxes
'''
def articleTextBox(f):
    s = '<textarea rows ="'
    s+= str(len(f.articles)+1)
    s+= '" cols="'
    s+= str(max(map(len,f.articles)) if len(f.articles)>0 else 25)
    s+='" readonly="readonly">'
    for article in f.articles:
        s+=article.title
        s+= ' in '
        s+=article.journal
        s+= ', '
        s+=article.date
        s+='\n'
    s+='</textarea>'
    return s
    
'''
function for making office hour text boxes- a little more involved than regular textboxes
'''
def officeHoursTextBox(f):
    s = '<textarea rows ="'
    s+= str(len(f.articles)+1)
    s+= '" cols="'
    s+= str(max(map(len,f.officeHours)) if len(f.officeHours)>0 else 25)
    s+='" readonly="readonly">'
    for officeHour in f.officeHours:
        s+=officeHour.day
        s+= ' from '
        s+=officeHour.beginTime
        s+= ' to '
        s+=officeHour.endTime
        s+='\n'
    s+='</textarea>'
    return s

'''
function for making degree text boxes- a little more involved than regular textboxes
'''
def degreesTextBox(f):
    s = '<textarea rows ="'
    s+= str(len(f.degrees)+1)
    s+= '" cols="'
    s+= str(max(map(len,f.degrees)) if len(f.degrees)>0 else 25)
    s+='" readonly="readonly">'
    for degree in f.degrees:
        s+=degree.type
        s+= ' degree from '
        s+=degree.institution
        s+= ' in '
        s+=degree.date
        s+='\n'
    s+='</textarea>'
    return s

    

'''
Function for making generic drop down lists
'''
def dropDown(name,options,preselect,selected=""):
    s = '<select name="'
    s+=name
    s+='">'
    for o in options:
        s+='<option value="'
        s+=o
        s+=('" selected>' if preselect and o==selected else '">')
        s+=o
        s+='</option>'
    s+='</select>' 
    return s

'''
Genericly create a textinput
'''

def textInputField(id,value=''):
    return '<input type="text" name="'+id+'" value = "' +value+ '" />'

'''
Handler for faculty page
'''

class MainPage (webapp.RequestHandler) :
    id = ""
    facs = {}
    type = ""
    '''
    Takes care of main page
    '''
    def get (self) :
        self.response.out.write('<form action="/faculty" method="post">')
        if MainPage.facs.has_key(MainPage.id):
            MainPage.type = "submit"
            self.response.out.write('ID:')
            self.response.out.write(MainPage.id);
            fac = MainPage.facs[MainPage.id]
            self.response.out.write('<br />Faculty Name<br />')
            self.response.out.write(textInputField('name',fac.name))
            self.response.out.write('<br/>Faculty Office Building<br/>')
            self.response.out.write(dropDown('building',options["buildings"],True,fac.building))
            self.response.out.write('<br/>Faculty Room Number<br/>')
            self.response.out.write(textInputField('room',fac.room))
            self.response.out.write('<br/>Faculty Phone<br/>')
            self.response.out.write(textInputField('phone',fac.phone))
            self.response.out.write('<br/>Faculty email<br/>')
            self.response.out.write(textInputField('email',fac.email))
            self.response.out.write('<br/>Faculty website<br/>')
            self.response.out.write(textInputField('website',fac.website))
            self.response.out.write('<br/>Faculty Office Hours<br/>')
            self.response.out.write(officeHoursTextBox(fac))
            self.response.out.write(dropDown('officeHourDay',OfficeHour.days,False))
            self.response.out.write(dropDown('beginTime',OfficeHour.times,False))
            self.response.out.write(dropDown('endTime',OfficeHour.times,False))
            self.response.out.write('<br/>Faculty Type<br/>')
            self.response.out.write(dropDown('facType',options["facTypes"],True,fac.type))
            self.response.out.write('<br/>Degrees<br/>')
            self.response.out.write(degreesTextBox(fac))
            self.response.out.write(dropDown('degreeType',Degree.types,False))
            self.response.out.write(dropDown('degreeInst',Degree.institutions,False))
            self.response.out.write(textInputField('degreeYear'))
            self.response.out.write('<br/>Research Areas<br/>')
            self.response.out.write(textBox(fac.researchAreas))
            self.response.out.write(dropDown('researchArea',options['researchAreas'],False))
            self.response.out.write('<br/>Graduate Students<br/>')
            self.response.out.write(textBox(fac.gradStudents))
            self.response.out.write(dropDown('gradStudent',options['gradStudents'],False))
            self.response.out.write('<br/>Courses<br/>')
            self.response.out.write(textBox(fac.courses))
            self.response.out.write(dropDown('course',options['courses'],False))
            self.response.out.write('<br/>Articles<br/>')
            self.response.out.write(articleTextBox(fac))
            self.response.out.write(dropDown('journal',Article.journals,False))
            self.response.out.write(textInputField('articleTitle'))
            self.response.out.write(textInputField('articleYear'))
            self.response.out.write('<br/>Conferences<br/>')
            self.response.out.write(conferenceTextBox(fac))
            self.response.out.write(dropDown('conference',Conference.conferences,False))
            self.response.out.write(dropDown('conferenceLocation',Conference.locations,False))
            self.response.out.write(textInputField('conferenceTitle'))
            self.response.out.write(textInputField('conferenceDate'))
            self.response.out.write('<br/>Books<br/>')
            self.response.out.write(textBox(fac.books))
            self.response.out.write(dropDown('book',options['books'],False))
            self.response.out.write('<br/>Awards<br/>')
            self.response.out.write(textBox(fac.awards))
            self.response.out.write(dropDown('award',options['awards'],False))
            self.response.out.write('<br/>')
        else:
            MainPage.type = "Login"
            self.response.out.write('ID:')
            self.response.out.write(textInputField('FacID'))
        self.response.out.write('<input type="submit" value="Submit" /> </form><br />')
        self.response.out.write('<form action="/" method="get"><input type="submit" value="Logout!"></form>')
        
        
        
    '''
    takes care of submissions
    '''
    def post (self) :
        if MainPage.type == "Login":
            MainPage.id = cgi.escape(self.request.get('FacID'))
            if not MainPage.facs.has_key(MainPage.id):
                MainPage.facs[MainPage.id] = Faculty()
        else :
            fac = MainPage.facs[MainPage.id]
            name = cgi.escape(self.request.get('name'))
            building = cgi.escape(self.request.get('building'))
            room = cgi.escape(self.request.get('room'))
            phone = cgi.escape(self.request.get('phone'))
            email = cgi.escape(self.request.get('email'))
            website = cgi.escape(self.request.get('website'))
            officeHourDay = cgi.escape(self.request.get('officeHourDay'))
            officeHourBegin = cgi.escape(self.request.get('beginTime'))
            officeHourEnd = cgi.escape(self.request.get('endTime'))
            facType = cgi.escape(self.request.get('facType'))
            degreeType = cgi.escape(self.request.get('degreeType'))
            degreeInst = cgi.escape(self.request.get('degreeInst'))
            degreeYear = cgi.escape(self.request.get('degreeYear'))
            researchArea = cgi.escape(self.request.get('researchArea'))
            gradStudent = cgi.escape(self.request.get('gradStudent'))
            course = cgi.escape(self.request.get('course'))
            articleTitle = cgi.escape(self.request.get('articleTitle'))
            journal = cgi.escape(self.request.get('journal'))
            articleYear = cgi.escape(self.request.get('articleYear'))
            confName = cgi.escape(self.request.get('conference'))
            confLoc = cgi.escape(self.request.get('conferenceLocation'))
            confTitle = cgi.escape(self.request.get('conferenceTitle'))
            confDate = cgi.escape(self.request.get('conferenceDate'))
            book = cgi.escape(self.request.get('book'))
            award = cgi.escape(self.request.get('award'))
            
            if ValidateFaculty.name(name):
                fac.name = name
            else:
                self.response.out.write('Invalid name<br />')
            
            if ValidateFaculty.office(building, room) :
                fac.building = building
                fac.room = room
            else :
                self.response.out.write('Invalid Office.<br />')
                
            if ValidateFaculty.phone_number(phone) :
                fac.phone = phone
            else :
                self.response.out.write('Invalid number.<br />')
            if ValidateFaculty.email(email) :
                fac.email = email
            else :
                self.response.out.write('Invalid email.<br />')
            if ValidateFaculty.website(website) :
                fac.website = website
            else :
                self.response.out.write('Invalid Website.<br />')
            if officeHourDay!="" or officeHourBegin!="" or officeHourEnd !="":
                if ValidateFaculty.officeHour(officeHourDay,officeHourBegin,officeHourEnd) :
                    fac.officeHours.append(OfficeHour(officeHourDay,officeHourBegin,officeHourEnd))
                else:
                    self.response.out.write('Invalid Office Hour.<br />')
            fac.type = facType
            if degreeType!="" or degreeInst!="" or degreeYear !="":
                if ValidateFaculty.degree(fac.degrees,degreeType,degreeInst,degreeYear) :
                    fac.degrees.append(Degree(degreeType,degreeInst,degreeYear))
                else:
                    self.response.out.write('Invalid Degree.<br />')
            if researchArea!="":
                if ValidateFaculty.researchArea(fac.researchAreas,researchArea) :
                    fac.researchAreas.append(researchArea)
                else:
                    self.response.out.write('Invalid Research Area.<br />')
            if gradStudent != "":
                if ValidateFaculty.graduateStudent(fac.gradStudents,gradStudent) :
                    fac.gradStudents.append(gradStudent)
                else:
                    self.response.out.write('Invalid Grad Student.<br />')
            if course != "":
                if ValidateFaculty.course(fac.courses,course) :
                    fac.courses.append(course)
                else:
                    self.response.out.write('Invalid Course.<br />')

            if articleTitle!="" or articleYear!="" or journal !="":
                if ValidateFaculty.article(fac.articles,articleTitle,journal,articleYear) :
                    fac.articles.append(Article(articleTitle,journal,articleYear))
                else:
                    self.response.out.write('Invalid Article.<br />') 
            if anyFilled(confName,confLoc,confTitle,confDate):
                if ValidateFaculty.conference(fac.conferences,confName,confLoc,confTitle,confDate) :
                    fac.conferences.append(Conference(confName,confLoc,confTitle,confDate))
                else:
                    self.response.out.write('Invalid Conference.<br />')        
            if book != "":
                if ValidateFaculty.book(fac.books,book) :
                    fac.books.append(book)
                else:
                    self.response.out.write('Invalid book.<br />')
            if award != "":
                if ValidateFaculty.award(fac.awards,award) :
                    fac.awards.append(award)
                else:
                    self.response.out.write('Invalid Award.<br />')
        self.get()


if __name__ == "__main__":
    main()
