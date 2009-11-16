#!/usr/bin/env python
# --------
# Faculty.py
# --------


import cgi
import types

from google.appengine.ext        import db
from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template 
from google.appengine.ext.db     import djangoforms

import ValidateFaculty
import main

#options = {"facTypes":("","Professor","Lecturer","Researcher"),
#           "buildings":("","TAY","PAI","ACES","ENS"),
#           "researchAreas":("","AI","Compilers","OS","Robotics","Algorithms"),
#           "gradStudents":("","Student1(st0001)","Student2(st0002)"),
#           "courses":("","55555","55556"),
#           "books":("","AwesomeBook","Anotherbook","LessAwesomeBook"),
#           "awards":("","Awards","SuperAwesomeAward")
#   }

class student_eid(db.Model) :
    student_eid = db.StringProperty(required=True)
class faculty_type(db.Model) :
    faculty_type = db.StringProperty(required=True)
    def __str__(self):
        return self._faculty_type
class research_area(db.Model) :
    research_area = db.StringProperty(required=True)
class building(db.Model) :
    building = db.StringProperty(required=True)
    def __str__(self):
        return self._building
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
class course(db.Model):
    course_number = db.ReferenceProperty(reference_class=course_number)
    course_name = db.ReferenceProperty(reference_class=course_name)
    course_type = db.ReferenceProperty(reference_class=course_type)
    
class semester(db.Model) :
    semester = db.StringProperty(required=True)
class award_name(db.Model) :
    award_name = db.StringProperty(required=True)
class award_type(db.Model) :
    award_type = db.StringProperty(required=True)

"""
Database Faculty Model
"""

class Faculty(db.Model):
    name = db.StringProperty()
    phone = db.StringProperty(validator=ValidateFaculty.phone_number)
    building = db.ReferenceProperty(reference_class=building)
    room = db.StringProperty(validator=ValidateFaculty.room)
    email = db.EmailProperty(required=True)
    website = db.LinkProperty()
    type = db.ReferenceProperty(reference_class=faculty_type)

"""
Faculty Form
"""



class FacultyForm (djangoforms.ModelForm) :
    class Meta :
        model = Faculty
    
    
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

#class Faculty:
#
#    def __init__(self):
#        self.phone = ""
#        self.name = ""
#        self.building = ""
#        self.room = ""
#        self.email = ""
#        self.website = "http://"
#        self.officeHours = []
#        self.type = ""
#        self.degrees = []
#        self.researchAreas = []
#        self.gradStudents = []
#        self.courses = []
#        self.articles = []
#        self.conferences = []
#        self.books= []
#        self.awards = []
#"""
#Simple class for holding onto conference data
#"""        
#class Conference:
#    conferences = ("","Conference","AnotherConference","aThird")
#    locations = ("","Location","Burbank","Singapore","Fiji","Stalingrad")
#    def __init__(self,name,location,title,date):
#        self.name = name
#        self.location = location
#        self.title = title
#        self.date = date
#    def __len__(self):
#        return len(self.title)+len(self.name)+len(self.date)+len(self.location)+len("at  in , ")
#    
#"""
#Simple class for holding onto article data
#"""        
#class Article:
#    journals = ("","Scientific American","Applied Computing", "Robotic Murder Monthly")
#    def __init__(self,t,j,d):
#        self.title = t
#        self.journal = j
#        self.date = d
#    def __len__(self):
#        return len(self.title)+len(self.journal)+len(self.date)+len(" in , ")
#    
#"""
#Simple class for holding onto degree data
#"""        
#class Degree:
#    types = ("","B.S.","B.A.","M.S.","M.A.","Ph.D.")
#    institutions = ("","UT","Less Important")
#    def __init__(self,t,i,d):
#        self.type = t
#        self.institution = i
#        self.date = d
#    def __len__(self):
#        return len(self.type)+len(self.institution)+len(self.date)+len(" from in ")    
#
#"""
#Simple class for holding onto officeHour data
#"""        
#class OfficeHour:
#    days = ("","M","T","W","R","F")
#    times = ("","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30")
#    def __init__(self,day,b,e):
#        self.day = day
#        self.beginTime = b
#        self.endTime = e
#    def __len__(self):
#        return len(self.day)+len(self.beginTime)+len(self.endTime)+len(" from in ")
#"""
#function to check if any of the values passed in are filled
#"""
#def anyFilled(*t):
#    for e in t:
#        if e!="": return True;
#        
#"""
#Function for making 'generic' text boxes
#"""
#
#def textBox(t):
#    s = '<textarea rows ="'
#    s+= str(len(t)+1)
#    s+= '" cols="'
#    s+= str(max(map(len,t)) if len(t)>0 else 25)
#    s+='" readonly="readonly">'
#    for o in t:
#        s+=o
#        s+='\n'
#    s+='</textarea>'
#    return s
#
#"""
#function for making conference text boxes- a little more involved than regular textboxes
#"""
#
#def conferenceTextBox(f):
#    s = '<textarea rows ="'
#    s+= str(len(f.conferences)+1)
#    s+= '" cols="'
#    s+= str(max(map(len,f.conferences)) if len(f.conferences)>0 else 25)
#    s+='" readonly="readonly">'
#    for conf in f.conferences: #name location title date
#        s+=conf.title
#        s+= ' at '
#        s+=conf.name
#        s+= ' in '
#        s+=conf.location
#        s+=', '
#        s+=conf.date
#        s+='\n'
#    s+='</textarea>'
#    return s    
#
#"""
#function for making article text boxes- a little more involved than regular textboxes
#"""
#def articleTextBox(f):
#    s = '<textarea rows ="'
#    s+= str(len(f.articles)+1)
#    s+= '" cols="'
#    s+= str(max(map(len,f.articles)) if len(f.articles)>0 else 25)
#    s+='" readonly="readonly">'
#    for article in f.articles:
#        s+=article.title
#        s+= ' in '
#        s+=article.journal
#        s+= ', '
#        s+=article.date
#        s+='\n'
#    s+='</textarea>'
#    return s
#    
#"""
#function for making office hour text boxes- a little more involved than regular textboxes
#"""
#def officeHoursTextBox(f):
#    s = '<textarea rows ="'
#    s+= str(len(f.articles)+1)
#    s+= '" cols="'
#    s+= str(max(map(len,f.officeHours)) if len(f.officeHours)>0 else 25)
#    s+='" readonly="readonly">'
#    for officeHour in f.officeHours:
#        s+=officeHour.day
#        s+= ' from '
#        s+=officeHour.beginTime
#        s+= ' to '
#        s+=officeHour.endTime
#        s+='\n'
#    s+='</textarea>'
#    return s
#
#"""
#function for making degree text boxes- a little more involved than regular textboxes
#"""
#def degreesTextBox(f):
#    s = '<textarea rows ="'
#    s+= str(len(f.degrees)+1)
#    s+= '" cols="'
#    s+= str(max(map(len,f.degrees)) if len(f.degrees)>0 else 25)
#    s+='" readonly="readonly">'
#    for degree in f.degrees:
#        s+=degree.type
#        s+= ' degree from '
#        s+=degree.institution
#        s+= ' in '
#        s+=degree.date
#        s+='\n'
#    s+='</textarea>'
#    return s
#
#    
#
#"""
#Function for making generic drop down lists
#"""
def dropDownList(name,options):
    s = '<select name="'
    s+=name
    s+='">'
    for o in options:
        s+='<option value="'
        s+=o
        s+='">'
        s+=o
        s+='</option>'
    s+='</select>' 
    return s

#"""
#Generically create a textinput
#"""
#
def textInputField(id,value=''):
    return '<input type="text" name="'+id+'" value = "' +value+ '" />'
#
#'''
#handler for faculty page
#'''

def removeCheckBox(entry):
    return ' Remove:<input type="checkbox" name="R'+str(entry.key())+'"/>\n<br>'

def getOnFac(table,facKey):
    return table.gql("WHERE faculty=:1",facKey)

def tab(i):
    return '&nbsp;'*i

def awardList(facKey):
    aws = getOnFac(AwardJoin,facKey)
    s = ""
    for a in aws:
        s+=tab(4)+a.title+", "+db.get(a.type.key()).award_type+", "+str(a.year)
        s+=removeCheckBox(a)
    return s

def conferenceList(facKey):
    cs = getOnFac(ConferenceJoin,facKey)
    s = ""
    for c in cs:
        s+=tab(4)+c.title+" for "+db.get(c.conference.key()).conference_name+" in "+db.get(c.conference.key()).conference_name+", "+str(c.year)
        s+=removeCheckBox(c)
    return s

def articleList(facKey):
    arts = getOnFac(ArticleJoin,facKey)
    s = ""
    for a in arts:
        s+=tab(4)+a.title+" in "+db.get(a.journal.key()).journal_name+", "+a.date
        s+=removeCheckBox(a)
    return s 

def officeHourList(facKey):
    os = getOnFac(OfficeHourJoin,facKey)
    s =""
    for o in os:
        s+=tab(4)+o.day+" from "+o.start+" to "+o.end
        s+=removeCheckBox(o)
    return s

def studentList(facKey):
    sts = getOnFac(StudentJoin,facKey)
    s = ""
    for st in sts:
        s+=tab(4)+db.get(st.student.key()).student_eid
        s+=removeCheckBox(st)
    return s
    

def courseList(facKey):
    cs = getOnFac(CourseJoin,facKey)
    s = ""
    for c in cs:
        s+=tab(4)+str(c.unique)+": "+db.get(c.course.key()).course_number.course_number+", "+db.get(c.course.key()).course_name.course_name
        s+=removeCheckBox(c)
    return s
def researchAreaList(facKey):
    ras = getOnFac(AreaJoin,facKey)
    s = ""
    for ra in ras:
        s+= tab(4)+ db.get(ra.area.key()).research_area
        s+=removeCheckBox(ra)
    return s
def bookList(facKey):
    bs = getOnFac(BookJoin,facKey)
    s = ""
    for b in bs:
        s+= tab(4)+b.title+" from "+  db.get(b.publisher.key()).publisher
        s+=removeCheckBox(b)
    return s

def dropDown(table,name,column):
    entries = table.all()
    s = '<select name="'
    s+= name
    s+='"><option value = ""></option>'
    for e in entries:
        s+='<option value="'
        s+=str(e.key())
        s+='">'
        s+=e.__dict__["_"+column]
        s+='</option>'
    s+='</select>' 
    return s

def courseDropDown():
    entries = course.all()
    s = '<select name="'
    s+= "course"
    s+='"><option value = ""></option>'
    for e in entries:
        s+='<option value="'
        s+=str(e.key())
        s+='">'
        s+=e.course_number.course_number + ", " + e.course_name.course_name + ", " + e.course_type.course_type
        s+='</option>'
    s+='</select>' 
    return s

class MainPage (webapp.RequestHandler) :
    """
    Takes care of main page
    """
    def get (self) :
        fac = Faculty.gql("WHERE email = :1","blah@blah.com")[0]
        key = fac.key()
        data = {"website":fac.website,"type":""if fac.type is None else fac.type.key(),"email":fac.email,"name":fac.name,"phone":fac.phone,"building":""if fac.building is None else fac.building.key(),"room":fac.room}
        form = FacultyForm(data = data)
        self.response.out.write('<form action="/faculty" method="post">')
        self.response.out.write(form)
        self.response.out.write('<br><br>Research Areas<br>')
        self.response.out.write(researchAreaList(key))
        #self.response.out.write(researchAreaDropDown())
        self.response.out.write(dropDown(research_area,"researchArea","research_area"))
        self.response.out.write('<br><br>Books<br>')
        self.response.out.write(bookList(key))
        self.response.out.write(textInputField("bookTitle"))
        self.response.out.write(dropDown(publisher,"publisher","publisher"))
        self.response.out.write('<br><br>Courses<br>')
        self.response.out.write(courseList(key))
        self.response.out.write(textInputField("unique"))
        self.response.out.write(courseDropDown())
        self.response.out.write(dropDown(semester,"semester","semester"))
        self.response.out.write('<br><br>Graduate Students<br>')
        self.response.out.write(studentList(key))
        self.response.out.write(dropDown(student_eid,"student_eid","student_eid"))
        self.response.out.write('<br><br>Office Hours<br>')
        self.response.out.write(officeHourList(key))
        self.response.out.write(dropDownList("Day",["","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
        self.response.out.write(dropDownList("StartTime",["","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"]))
        self.response.out.write(dropDownList("EndTime",["","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"]))
        self.response.out.write('<br><br>Articles<br>')
        self.response.out.write(articleList(key))
        self.response.out.write(textInputField("articleTitle"))
        self.response.out.write(textInputField("articleDate"))
        self.response.out.write(dropDown(journal_name,"journal_name","journal_name"))
        self.response.out.write('<br><br>Conferences<br>')
        self.response.out.write(conferenceList(key))
        self.response.out.write(textInputField("confTitle"))
        self.response.out.write(textInputField("confYear"))
        self.response.out.write(dropDown(conference_name,"conference_name","conference_name"))
        self.response.out.write(dropDown(location,"location","location"))
        self.response.out.write('<br><br>Award<br>')
        self.response.out.write(awardList(key))
        self.response.out.write(textInputField("awardTitle"))
        self.response.out.write(dropDown(award_type,"award_type","award_type"))
        self.response.out.write(textInputField("awardYear"))
        
        
        self.response.out.write('<br><input type="submit" value="Submit" /> </form><br />')
        
        
    def doDeletes(self, table, facKey):
        map(lambda x: x.delete(),filter(lambda x:cgi.escape(self.request.get('R'+str(x.key()))) == 'on', table.gql("WHERE faculty=:1",facKey)))
            
    """
    takes care of submissions
    """
    def post (self) :
        fac = Faculty.gql("WHERE email = :1","blah@blah.com")[0]
        facKey = fac.key()
        form = FacultyForm(data=self.request.POST)
        if form.is_valid():    
            fac.name = self.request.POST["name"]
            fac.phone = self.request.POST["phone"]
            s = self.request.POST["type"]
            if s != "": fac.type = db.Key(encoded=s);
            s = self.request.POST["building"]
            if s != "": fac.building = db.Key(encoded=s);
            fac.room = self.request.POST["room"]
            fac.email = self.request.POST["email"]
            fac.website = self.request.POST["website"]
            fac.put()
        else:
            self.response.out.write("Bad Data")
            
        ra = cgi.escape(self.request.get('researchArea'))
        if ra != "":
            AreaJoin(faculty = facKey,area = db.Key(ra)).put()
        self.doDeletes(AreaJoin,facKey)
        
        bookTitle = cgi.escape(self.request.get('bookTitle'))
        publisher = cgi.escape(self.request.get('publisher'))
        if bookTitle!="" and publisher != "":
            BookJoin(faculty=facKey,title=bookTitle,publisher=db.Key(publisher)).put()
        self.doDeletes(BookJoin,facKey)
            
        course = cgi.escape(self.request.get('course'))
        unique = cgi.escape(self.request.get('unique'))
        semester = cgi.escape(self.request.get('semester'))
        if course!="" and unique != "" and semester != "":
            CourseJoin(faculty=facKey,unique=int(unique),course=db.Key(course),semester=db.Key(semester)).put()
        self.doDeletes(CourseJoin,facKey)    
        
        student = cgi.escape(self.request.get('student_eid'))
        if student!="":
            StudentJoin(faculty=facKey,student=db.Key(student)).put()
        self.doDeletes(StudentJoin,facKey)    
        
        day = cgi.escape(self.request.get('Day'))
        start = cgi.escape(self.request.get('StartTime'))
        end = cgi.escape(self.request.get('EndTime'))
        if day != "" and start != "" and end != "":
            OfficeHourJoin(faculty=facKey,day=day,start=start,end=end).put()
        self.doDeletes(OfficeHourJoin,facKey)    
            
        articleTitle = cgi.escape(self.request.get('articleTitle'))
        journalName = cgi.escape(self.request.get('journal_name'))
        articleDate =cgi.escape(self.request.get('articleDate'))
        if articleTitle != "" and journalName != "" and articleDate != "":
            ArticleJoin(faculty=facKey, title=articleTitle,journal=db.Key(journalName),date=articleDate).put()
        self.doDeletes(ArticleJoin,facKey)
        
        confTitle = cgi.escape(self.request.get('confTitle'))
        conf = cgi.escape(self.request.get('conference_name'))
        confYear = cgi.escape(self.request.get('confYear'))
        confLoc = cgi.escape(self.request.get('location'))
        if conf != "" and confTitle != "" and confYear != "" and confLoc != "":
            ConferenceJoin(faculty=facKey,title=confTitle,year=int(confYear),conference=db.Key(conf),location=db.Key(confLoc)).put()
        self.doDeletes(ConferenceJoin,facKey)
        
        awardTitle = cgi.escape(self.request.get('awardTitle'))
        awardYear = cgi.escape(self.request.get('awardYear'))
        awardType = cgi.escape(self.request.get('award_type'))
        
        if awardTitle!=None and awardYear!=None and awardType != None:
            AwardJoin(faculty=facKey,title=awardTitle,type=db.Key(awardType),year=int(awardYear)).put()
        self.doDeletes(AwardJoin,facKey)
        

        #map(lambda x: x.delete(),filter(lambda x:cgi.escape(self.request.get('R'+str(x.area.key()))) == 'on', ras))
#        name = cgi.escape(self.request.get('name'))
#        building = cgi.escape(self.request.get('building'))
#        room = cgi.escape(self.request.get('room'))
#        phone = cgi.escape(self.request.get('phone'))
#        email = cgi.escape(self.request.get('email'))
#        website = cgi.escape(self.request.get('website'))
#        officeHourDay = cgi.escape(self.request.get('officeHourDay'))
#        officeHourBegin = cgi.escape(self.request.get('beginTime'))
#        officeHourEnd = cgi.escape(self.request.get('endTime'))
#        facType = cgi.escape(self.request.get('facType'))
#        degreeType = cgi.escape(self.request.get('degreeType'))
#        degreeInst = cgi.escape(self.request.get('degreeInst'))
#        degreeYear = cgi.escape(self.request.get('degreeYear'))
#        researchArea = cgi.escape(self.request.get('researchArea'))
#        gradStudent = cgi.escape(self.request.get('gradStudent'))
#        course = cgi.escape(self.request.get('course'))
#        articleTitle = cgi.escape(self.request.get('articleTitle'))
#        journal = cgi.escape(self.request.get('journal'))
#        articleYear = cgi.escape(self.request.get('articleYear'))
#        confName = cgi.escape(self.request.get('conference'))
#        confLoc = cgi.escape(self.request.get('conferenceLocation'))
#        confTitle = cgi.escape(self.request.get('conferenceTitle'))
#        confDate = cgi.escape(self.request.get('conferenceDate'))
#        book = cgi.escape(self.request.get('book'))
#        award = cgi.escape(self.request.get('award'))
#        logout = cgi.escape(self.request.get('logout')) == 'on'
#        
#        if ValidateFaculty.name(name):
#            fac.name = name
#        else:
#            self.response.out.write('Invalid name<br />')
#        
#        if ValidateFaculty.office(building, room) :
#            fac.building = building
#            fac.room = room
#        else :
#            self.response.out.write('Invalid Office.<br />')
#            
#        if ValidateFaculty.phone_number(phone) :
#            fac.phone = phone
#        else :
#            self.response.out.write('Invalid number.<br />')
#        if ValidateFaculty.email(email) :
#            fac.email = email
#        else :
#            self.response.out.write('Invalid email.<br />')
#        if ValidateFaculty.website(website) :
#            fac.website = website
#        else :
#            self.response.out.write('Invalid Website.<br />')
#        if officeHourDay!="" or officeHourBegin!="" or officeHourEnd !="":
#            if ValidateFaculty.officeHour(officeHourDay,officeHourBegin,officeHourEnd) :
#                fac.officeHours.append(OfficeHour(officeHourDay,officeHourBegin,officeHourEnd))
#            else:
#                self.response.out.write('Invalid Office Hour.<br />')
#        fac.type = facType
#        if degreeType!="" or degreeInst!="" or degreeYear !="":
#            if ValidateFaculty.degree(fac.degrees,degreeType,degreeInst,degreeYear) :
#                fac.degrees.append(Degree(degreeType,degreeInst,degreeYear))
#            else:
#                self.response.out.write('Invalid Degree.<br />')
#        if researchArea!="":
#            if ValidateFaculty.researchArea(fac.researchAreas,researchArea) :
#                fac.researchAreas.append(researchArea)
#            else:
#                self.response.out.write('Invalid Research Area.<br />')
#        if gradStudent != "":
#            if ValidateFaculty.graduateStudent(fac.gradStudents,gradStudent) :
#                fac.gradStudents.append(gradStudent)
#            else:
#                self.response.out.write('Invalid Grad Student.<br />')
#        if course != "":
#            if ValidateFaculty.course(fac.courses,course) :
#                fac.courses.append(course)
#            else:
#                self.response.out.write('Invalid Course.<br />')
#
#        if articleTitle!="" or articleYear!="" or journal !="":
#            if ValidateFaculty.article(fac.articles,articleTitle,journal,articleYear) :
#                fac.articles.append(Article(articleTitle,journal,articleYear))
#            else:
#                self.response.out.write('Invalid Article.<br />') 
#        if anyFilled(confName,confLoc,confTitle,confDate):
#            if ValidateFaculty.conference(fac.conferences,confName,confLoc,confTitle,confDate) :
#                fac.conferences.append(Conference(confName,confLoc,confTitle,confDate))
#            else:
#                self.response.out.write('Invalid Conference.<br />')        
#        if book != "":
#            if ValidateFaculty.book(fac.books,book) :
#                fac.books.append(book)
#            else:
#                self.response.out.write('Invalid book.<br />')
#        if award != "":
#            if ValidateFaculty.award(fac.awards,award) :
#                fac.awards.append(award)
#            else:
#                self.response.out.write('Invalid Award.<br />')
        self.get()


if __name__ == "__main__":
    main()
