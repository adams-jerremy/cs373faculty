#!/usr/bin/env python
# --------
# Faculty.py
# --------


import cgi
import types
import re

from google.appengine.ext        import db
from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms
import os

import Datastore
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
    return '<input type="text" title="'+title+'" name="'+id+'" value = "' +(value if value is not None else '')+ '" />'
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
    aws = getOnFac(Datastore.AwardJoin,facKey)
    s = ""
    for a in aws:
        s+=tab(4)+a.title+", "+db.get(a.type.key()).award_type+", "+str(a.year)
        s+=removeCheckBox(a)
    return s

def conferenceList(facKey):
    cs = getOnFac(Datastore.ConferenceJoin,facKey)
    s = ""
    for c in cs:
        s+=tab(4)+c.title+" for "+db.get(c.conference.key()).conference_name+" in "+db.get(c.conference.key()).conference_name+", "+str(c.year)
        s+=removeCheckBox(c)
    return s

def articleList(facKey):
    arts = getOnFac(Datastore.ArticleJoin,facKey)
    s = ""
    for a in arts:
        s+=tab(4)+a.title+" in "+db.get(a.journal.key()).journal_name+", "+a.date
        s+=removeCheckBox(a)
    return s 

def officeHourList(facKey):
    os = getOnFac(Datastore.OfficeHourJoin,facKey)
    s =""
    for o in os:
        s+=tab(4)+o.day+" from "+o.start+" to "+o.end
        s+=removeCheckBox(o)
    return s

def studentList(facKey):
    sts = getOnFac(Datastore.StudentJoin,facKey)
    s = ""
    for st in sts:
        s+=tab(4)+db.get(st.student.key()).student_eid
        s+=removeCheckBox(st)
    return s
def degreeList(facKey):
    ds = getOnFac(Datastore.DegreeJoin,facKey)
    s = ""
    for d in ds:
        s+=tab(4)+db.get(d.type.key()).degree_type+" in "+db.get(d.major.key()).degree_name+" from "+db.get(d.institute.key()).institution
        s+=removeCheckBox(d)
    return s    

def courseList(facKey):
    cs = getOnFac(Datastore.CourseJoin,facKey)
    s = ""
    for c in cs:
        s+=tab(4)+str(c.unique)+": "+db.get(c.course.key()).course_number.course_number+", "+db.get(c.course.key()).course_name.course_name
        s+=removeCheckBox(c)
    return s
def researchAreaList(facKey):
    ras = getOnFac(Datastore.AreaJoin,facKey)
    s = ""
    for ra in ras:
        s+= tab(4)+ db.get(ra.area.key()).research_area
        s+=removeCheckBox(ra)
    return s
def bookList(facKey):
    bs = getOnFac(Datastore.BookJoin,facKey)
    s = ""
    for b in bs:
        s+= tab(4)+b.title+" from "+  db.get(b.publisher.key()).publisher
        s+=removeCheckBox(b)
    return s

def dropDown(table,name,column,title='',selected=None):
    entries = table.all()
    s = '<select title="'+title+'" name="'
    s+= name
    s+='"><option value = ""></option>'
    for e in entries:
        s+='<option '
        s+='selected="selected"' if selected == e else ''
        s+='value="'
        s+=str(e.key())
        s+='">'
        s+=e.__dict__["_"+column]
        s+='</option>'
    s+='</select>' 
    return s

def courseDropDown():
    entries = Datastore.course.all()
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

style ="""
<style type="text/css"> m{color: #ADADAD;} 
</style type="text/css"><m>%s: </m>
        """

class MainPage (webapp.RequestHandler) :
    """
    Takes care of main page
    """
    def get (self) :
        facid = self.request.get("facid")
        facs = Datastore.Faculty.gql("WHERE email = :1",facid)
        if facs.count() < 1 or facid is None or facid == "":
            self.redirect("/")
        fac = facs.get()
        key = fac.key()
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
#        form = FacultyForm()
#        template_values = {'form': form}
#        path = os.path.join(os.path.dirname(__file__), 'fac.html')
#        self.response.out.write(template.render(path, template_values))
        self.response.out.write('<form action="/faculty?facid='+facid+'" method="post">')
        self.response.out.write("Name: "+textInputField("name",fac.name))
        self.response.out.write("<br>Type: "+dropDown(Datastore.faculty_type,"faculty_type","faculty_type",selected=fac.type))
        self.response.out.write("<br>Phone: "+textInputField("phone",fac.phone))
        self.response.out.write("<br>Office: "+dropDown(Datastore.building,"building","building",title=tooltip["build"],selected=fac.building)+textInputField("room",fac.room,title=tooltip["room"]))
        self.response.out.write("<br>Email: "+textInputField("email",fac.email))
        self.response.out.write("<br>Website: "+textInputField("website",fac.website))
        self.response.out.write('<br><br>Degrees</p1><br>')
        self.response.out.write(degreeList(key))
        self.response.out.write(dropDown(Datastore.degree_type,"degree_type","degree_type",title=tooltip["dType"]))
        self.response.out.write(dropDown(Datastore.degree_name,"degree_name","degree_name",title=tooltip["dName"]))
        self.response.out.write(dropDown(Datastore.institution,"institution","institution",title=tooltip["inst"]))
        self.response.out.write(textInputField("degreeYear",title=tooltip["year"]))
        self.response.out.write('<br><br>Research Areas</p1><br>')
        self.response.out.write(researchAreaList(key))
        self.response.out.write(dropDown(Datastore.research_area,"researchArea","research_area",title=tooltip["ra"]))
        self.response.out.write('<br><br>Books<br>')
        self.response.out.write(bookList(key))
        self.response.out.write(textInputField("bookTitle",title=tooltip["title"]))
        self.response.out.write(dropDown(Datastore.publisher,"publisher","publisher",title = tooltip["publisher"]))
        self.response.out.write('<br><br>Courses<br>')
        self.response.out.write(courseList(key))
        self.response.out.write(textInputField("unique",title=tooltip["unique"]))
        self.response.out.write(courseDropDown())
        self.response.out.write(dropDown(Datastore.semester,"semester","semester",title=tooltip["semester"]))
        self.response.out.write('<br><br>Graduate Students<br>')
        self.response.out.write(studentList(key))
        self.response.out.write(dropDown(Datastore.student_eid,"student_eid","student_eid",title=tooltip["student"]))
        self.response.out.write('<br><br>Office Hours<br>')
        self.response.out.write(officeHourList(key))
        self.response.out.write(dropDownList("Day",["","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],title=tooltip["day"]))
        self.response.out.write(dropDownList("StartTime",["","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"],title=tooltip["start"]))
        self.response.out.write(dropDownList("EndTime",["","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"],title=tooltip["end"]))
        self.response.out.write('<br><br>Articles<br>')
        self.response.out.write(articleList(key))
        self.response.out.write(textInputField("articleTitle",title=tooltip["title"]))
        self.response.out.write(textInputField("articleDate",title=tooltip["year"]))
        self.response.out.write(dropDown(Datastore.journal_name,"journal_name","journal_name",title=tooltip["journal"]))
        self.response.out.write('<br><br>Conferences<br>')
        self.response.out.write(conferenceList(key))
        self.response.out.write(textInputField("confTitle",title=tooltip["title"]))
        self.response.out.write(textInputField("confYear",title=tooltip["year"]))
        self.response.out.write(dropDown(Datastore.conference_name,"conference_name","conference_name",title=tooltip["conf"]))
        self.response.out.write(dropDown(Datastore.location,"location","location",title=tooltip["loc"]))
        self.response.out.write('<br><br>Award<br>')
        self.response.out.write(awardList(key))
        self.response.out.write(textInputField("awardTitle",title=tooltip["title"]))
        self.response.out.write(dropDown(Datastore.award_type,"award_type","award_type",title=tooltip["type"]))
        self.response.out.write(textInputField("awardYear",title=tooltip["year"]))
        
        
        self.response.out.write('<br><input type="submit" value="Submit" /> </form><br />')
        
        
    def doDeletes(self, table, facKey):
        map(lambda x: x.delete(),filter(lambda x:cgi.escape(self.request.get('R'+str(x.key()))) == 'on', table.gql("WHERE faculty=:1",facKey)))
            
    """
    takes care of submissions
    """
    def post (self) :
        fac = Datastore.Faculty.gql("WHERE email = :1",self.request.get("facid"))[0]
        facKey = fac.key()
        facAttrs = ("name","phone","room","email","website")
        def validate(s):
            a = cgi.escape(self.request.get(s))
            if(a=="" or ValidateFaculty.__dict__[s](a)): fac.__dict__['_'+s] = a;
        map(validate,facAttrs)
        
        s = self.request.get("faculty_type")
        if s != "": fac.type = db.Key(encoded=s);
        s = self.request.get("building")
        if s != "": fac.building = db.Key(encoded=s);
        fac.put()
        
        def fun(table,dict,keyDict):
            if filled(*dict.values()) and filled(*keyDict.values()) :
                for k in keyDict:
                   keyDict[k] = db.Key(keyDict[k])
                dict.update(keyDict)
                table(faculty = facKey,**dict).put()
        get = lambda x:cgi.escape(self.request.get(x))
        yearToInt = lambda x: -1 if re.search('^\d+$',x) is None else int(x)
        uniqueToInt = lambda x: -1 if re.search('^\d+$',x) is None else int(x)
        
        fun(Datastore.DegreeJoin,{"year":yearToInt(get('degreeYear'))},{"type":get('degree_type'),"major":get('degree_name'),"institute":get('institution')})
        fun(Datastore.AreaJoin,{},{"area":get('researchArea')})
        fun(Datastore.BookJoin,{"title":get('bookTitle')},{"publisher":get("publisher")})
        fun(Datastore.CourseJoin,{"unique":uniqueToInt(get('unique'))},{"course":get('course'),"semester":get('semester')})
        fun(Datastore.StudentJoin,{},{"student":get('student_eid')})
        fun(Datastore.OfficeHourJoin,{"day":get('Day'),"start":get('StartTime'),"end":get('EndTime')},{})
        fun(Datastore.ArticleJoin,{"title":get('articleTitle'),"date":get('articleDate')},{'journal':get('journal_name')})
        fun(Datastore.ConferenceJoin,{"title":get('confTitle'),"year":yearToInt(get('confYear'))},{"conference":get("conference_name"),"location":get("location")})
        fun(Datastore.AwardJoin,{"title":get('awardTitle'),"year":yearToInt(get('awardYear'))},{"type":get('award_type')})
        
        joins = (Datastore.AreaJoin,Datastore.BookJoin,Datastore.CourseJoin,Datastore.StudentJoin,Datastore.OfficeHourJoin,Datastore.ArticleJoin,Datastore.ConferenceJoin,Datastore.AwardJoin,Datastore.DegreeJoin)
        map(lambda x:self.doDeletes(x,facKey),joins)
        self.get()


if __name__ == "__main__":
    main()
