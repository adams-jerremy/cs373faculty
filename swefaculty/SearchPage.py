#
#  SearchPage.py
#  
#
#  Created by Samira Irani on 11/22/09.
#  Copyright (c) 2009 UT Austin. All rights reserved.
#
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template 

import Faculty
import Datastore
import cgi

def concat(x,y): return x+y;
def xmap(uf,i): return (uf(v) for v in i);
def mapReduce(bf,uf,i,d=''): return reduce(bf,xmap(uf,i),d);

def select(name,table,col):
    return '<select style="margin: 0.2em" multiple="multiple" size="10" name="'+name+'"><optgroup label="'+name+'">'+mapReduce(concat,lambda e:'<option value='+str(e.key())+'>'+(''if e.__dict__['_'+col] is None else str(e.__dict__['_'+col]))+'</option>',table.all())+'</optgroup></select>'
    
searches =[("Names",Datastore.Faculty,'name'),
        ("Rooms",Datastore.Faculty,'room'),
        ("Buildings",Datastore.building,'building'),
        ("Days",Datastore.OfficeHourJoin,'day'),
        ("Faculty Type",Datastore.faculty_type, 'faculty_type'),
        ("Degree Type",Datastore.degree_type, 'degree_type'),
        ("Degree Names",Datastore.degree_name, 'degree_name'),
        ("Institutions",Datastore.institution, 'institution'),
        ("Reasearch Areas", Datastore.research_area, 'research_area'),
        ("Conference Names",Datastore.conference_name, 'conference_name'),
        ("Conference Titles",Datastore.ConferenceJoin, 'title'),
        ("Conference Locations",Datastore.location, 'location'),
        ("Conference Years",Datastore.ConferenceJoin, 'year'),
        ("Journals",Datastore.journal_name, 'journal_name'),
        ("Books",Datastore.BookJoin, 'title'),
        ("Publishers",Datastore.publisher, 'publisher'),
        ("Graduate Student Types",Datastore.student_type, 'student_type'),
        ("Course Numbers",Datastore.course_number, 'course_number'),
        ("Course Types",Datastore.course_type, 'course_type'),
        ("Semesters",Datastore.semester, 'semester'),
        ("Award Types",Datastore.award_type, 'award_type'),
        ("Award Titles",Datastore.AwardJoin, 'title'),
        ("Award Years",Datastore.AwardJoin, 'year')]
        
class MainPage (webapp.RequestHandler) :
    def get(self) :
        self.response.out.write('<form id="SearchForm" method="post" action="/search">')
        for s in searches:
            self.response.out.write(select(*s))
        
     #  self.response.out.write(select("Graduate Students' EIDs",Datastore.student_type, 'student'))
        
        self.response.out.write('<input type="submit" name="searchaction" value="Search" />')
        
    def post (self) :
        self.response.out.write('<html><body>You wrote:<pre>')
        for s in searches:
            self.response.out.write(str(self.request.get(s[0],allow_multiple = True))+'<br>')
        self.response.out.write('</pre></body></html>')

