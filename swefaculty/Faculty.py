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

tooltip = { "":"",
           "remove":"Select To Remove Entry",
           "title":"Title",
           "publisher":"Publisher",
           "unique":"Course Unique",
           "semester":"Semester",
           "day":"day",
           "start":"Start Time",
           "end":"End Time",
           "journal":"Journal",
           "year":"Year",
           "type":"Type",
           "loc":"Location",
           "conf":"Conference",
           "ra":"Research Area",
           "student":"Graduate Student",
           "inst":"Institution",
           "dName":"Degree Name",
           "dType":"Degree Type",
           "room":"Office Number",
           "build":"Office Building"
           }

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

def filled(*t):
    return "" not in t

#"""
#Function for making generic drop down lists
#"""
def dropDownList(name,options,title=''):
    s = '<select title="'+title+'" name="'
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
def textInputField(id,value='',title=''):
    return '<input type="text" title="'+title+'" name="'+id+'" value = "' +value+ '" />'
#
#'''
#handler for faculty page
#'''

def removeCheckBox(entry):
    return ' Remove:<input type="checkbox" title="'+tooltip["remove"]+'" name="R'+str(entry.key())+'"/>\n<br>'

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
def degreeList(facKey):
    ds = getOnFac(DegreeJoin,facKey)
    s = ""
    for d in ds:
        s+=tab(4)+db.get(d.type.key()).degree_type+" in "+db.get(d.major.key()).degree_name+" from "+db.get(d.institute.key()).institution
        s+=removeCheckBox(d)
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

def dropDown(table,name,column,title=''):
    entries = table.all()
    s = '<select title="'+title+'" name="'
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
        fac = Faculty.gql("WHERE email = :1",main.get_current_user())[0]
        key = fac.key()
        data = {"website":fac.website,"type":""if fac.type is None else fac.type.key(),"email":fac.email,"name":fac.name,"phone":fac.phone,"building":""if fac.building is None else fac.building.key(),"room":fac.room}
        form = FacultyForm(data = data)
        self.response.out.write("""
            <head>
            <title>"""+(fac.name if fac.name is not None else fac.email)+""" </title>
             <style type="text/css">
            h1{
            font-family:"Georgia", sans serif;
            font-size:50px;
            margin: 4px 0px;
            color: #2C7EC9;
            margin-top:15px
            }
            </style>
            </head>
            <h1> Faculty Database </h1>
            <br>
            """)
            
        self.response.out.write('<form action="/faculty" method="post">')
        self.response.out.write("Name: "+textInputField("name"))
        self.response.out.write("<br>Type: "+dropDown(faculty_type,"faculty_type","faculty_type"))
        self.response.out.write("<br>Phone: "+textInputField("phone"))
        self.response.out.write("<br>Office: "+dropDown(building,"building","building",title=tooltip["build"])+textInputField("room",title=tooltip["room"]))
        self.response.out.write("<br>Email: "+textInputField("email"))
        self.response.out.write("<br>Website: "+textInputField("website"))
        self.response.out.write('<br><br>Degrees</p1><br>')
        self.response.out.write(degreeList(key))
        self.response.out.write(dropDown(degree_type,"degree_type","degree_type",title=tooltip["dType"]))
        self.response.out.write(dropDown(degree_name,"degree_name","degree_name",title=tooltip["dName"]))
        self.response.out.write(dropDown(institution,"institution","institution",title=tooltip["inst"]))
        self.response.out.write(textInputField("degreeYear",title=tooltip["year"]))
        self.response.out.write('<br><br>Research Areas</p1><br>')
        self.response.out.write(researchAreaList(key))
        self.response.out.write(dropDown(research_area,"researchArea","research_area",title=tooltip["ra"]))
        self.response.out.write('<br><br>Books<br>')
        self.response.out.write(bookList(key))
        self.response.out.write(textInputField("bookTitle",title=tooltip["title"]))
        self.response.out.write(dropDown(publisher,"publisher","publisher",title = tooltip["publisher"]))
        self.response.out.write('<br><br>Courses<br>')
        self.response.out.write(courseList(key))
        self.response.out.write(textInputField("unique",title=tooltip["unique"]))
        self.response.out.write(courseDropDown())
        self.response.out.write(dropDown(semester,"semester","semester",title=tooltip["semester"]))
        self.response.out.write('<br><br>Graduate Students<br>')
        self.response.out.write(studentList(key))
        self.response.out.write(dropDown(student_eid,"student_eid","student_eid",title=tooltip["student"]))
        self.response.out.write('<br><br>Office Hours<br>')
        self.response.out.write(officeHourList(key))
        self.response.out.write(dropDownList("Day",["","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],title=tooltip["day"]))
        self.response.out.write(dropDownList("StartTime",["","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"],title=tooltip["start"]))
        self.response.out.write(dropDownList("EndTime",["","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"],title=tooltip["end"]))
        self.response.out.write('<br><br>Articles<br>')
        self.response.out.write(articleList(key))
        self.response.out.write(textInputField("articleTitle",title=tooltip["title"]))
        self.response.out.write(textInputField("articleDate",title=tooltip["year"]))
        self.response.out.write(dropDown(journal_name,"journal_name","journal_name",title=tooltip["journal"]))
        self.response.out.write('<br><br>Conferences<br>')
        self.response.out.write(conferenceList(key))
        self.response.out.write(textInputField("confTitle",title=tooltip["title"]))
        self.response.out.write(textInputField("confYear",title=tooltip["year"]))
        self.response.out.write(dropDown(conference_name,"conference_name","conference_name",title=tooltip["conf"]))
        self.response.out.write(dropDown(location,"location","location",title=tooltip["loc"]))
        self.response.out.write('<br><br>Award<br>')
        self.response.out.write(awardList(key))
        self.response.out.write(textInputField("awardTitle",title=tooltip["title"]))
        self.response.out.write(dropDown(award_type,"award_type","award_type",title=tooltip["type"]))
        self.response.out.write(textInputField("awardYear",title=tooltip["year"]))
        
        
        self.response.out.write('<br><input type="submit" value="Submit" /> </form><br />')
        
        
    def doDeletes(self, table, facKey):
        map(lambda x: x.delete(),filter(lambda x:cgi.escape(self.request.get('R'+str(x.key()))) == 'on', table.gql("WHERE faculty=:1",facKey)))
            
    """
    takes care of submissions
    """
    def post (self) :
        fac = Faculty.gql("WHERE email = :1",main.get_current_user())[0]
        facKey = fac.key()
        
        fac.name = self.request.get("name")
        fac.phone = self.request.get("phone")
        s = self.request.get("faculty_type")
        if s != "": fac.type = db.Key(encoded=s);
        s = self.request.get("building")
        if s != "": fac.building = db.Key(encoded=s);
        fac.room = self.request.get("room")
        fac.email = self.request.get("email")
        fac.website = self.request.get("website")
        fac.put()
        
        dType = cgi.escape(self.request.get('degree_type'))
        dName = cgi.escape(self.request.get('degree_name'))
        dInst = cgi.escape(self.request.get('institution'))
        dYear = cgi.escape(self.request.get('degreeYear'))
        if filled(dType,dName,dInst,dYear):
            DegreeJoin(faculty = facKey, type = db.Key(dType),major = db.Key(dName),institute=db.Key(dInst),year=int(dYear)).put()
        
        ra = cgi.escape(self.request.get('researchArea'))
        if filled(ra):
            AreaJoin(faculty = facKey,area = db.Key(ra)).put()
#        self.doDeletes(AreaJoin,facKey)
        
        bookTitle = cgi.escape(self.request.get('bookTitle'))
        publisher = cgi.escape(self.request.get('publisher'))
        if filled(bookTitle,publisher):
            BookJoin(faculty=facKey,title=bookTitle,publisher=db.Key(publisher)).put()
#        self.doDeletes(BookJoin,facKey)
            
        course = cgi.escape(self.request.get('course'))
        unique = cgi.escape(self.request.get('unique'))
        semester = cgi.escape(self.request.get('semester'))
        if filled(course,unique,semester):
            CourseJoin(faculty=facKey,unique=int(unique),course=db.Key(course),semester=db.Key(semester)).put()
#        self.doDeletes(CourseJoin,facKey)    
        
        student = cgi.escape(self.request.get('student_eid'))
        if filled(student):
            StudentJoin(faculty=facKey,student=db.Key(student)).put()
#        self.doDeletes(StudentJoin,facKey)    
        
        day = cgi.escape(self.request.get('Day'))
        start = cgi.escape(self.request.get('StartTime'))
        end = cgi.escape(self.request.get('EndTime'))
        if filled(day,start,end):
            OfficeHourJoin(faculty=facKey,day=day,start=start,end=end).put()
#        self.doDeletes(OfficeHourJoin,facKey)    
            
        articleTitle = cgi.escape(self.request.get('articleTitle'))
        journalName = cgi.escape(self.request.get('journal_name'))
        articleDate =cgi.escape(self.request.get('articleDate'))
        if filled(articleTitle, journalName, articleDate):
            ArticleJoin(faculty=facKey, title=articleTitle,journal=db.Key(journalName),date=articleDate).put()
#        self.doDeletes(ArticleJoin,facKey)
        
        confTitle = cgi.escape(self.request.get('confTitle'))
        conf = cgi.escape(self.request.get('conference_name'))
        confYear = cgi.escape(self.request.get('confYear'))
        confLoc = cgi.escape(self.request.get('location'))
        if filled(conf, confTitle, confYear, confLoc):
            ConferenceJoin(faculty=facKey,title=confTitle,year=int(confYear),conference=db.Key(conf),location=db.Key(confLoc)).put()
#        self.doDeletes(ConferenceJoin,facKey)
        
        awardTitle = cgi.escape(self.request.get('awardTitle'))
        awardYear = cgi.escape(self.request.get('awardYear'))
        awardType = cgi.escape(self.request.get('award_type'))
        
        if filled(awardTitle, awardYear, awardType):
            AwardJoin(faculty=facKey,title=awardTitle,type=db.Key(awardType),year=int(awardYear)).put()
#        self.doDeletes(AwardJoin,facKey)
        
        joins = (AreaJoin,BookJoin,CourseJoin,StudentJoin,OfficeHourJoin,ArticleJoin,ConferenceJoin,AwardJoin,DegreeJoin)
        map(lambda x:self.doDeletes(x,facKey),joins)
        self.get()


if __name__ == "__main__":
    main()
