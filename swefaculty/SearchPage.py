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
def mapReduce(bf,uf,i): return reduce(bf,xmap(uf,i));

def select(name,table,col):
    return '<select style="margin: 0.2em" multiple="multiple" size="10" name="'+name+'"><optgroup label="'+name+'">'+mapReduce(concat,lambda e:'<option value='+str(e.key())+'>'+e.__dict__['_'+col]+'</option>',table.all())+'</optgroup></select>'
    

class MainPage (webapp.RequestHandler) :
    def get(self) :
        self.response.out.write('<form id="SearchForm" method="post" action="/search">')
        self.response.out.write(select("Names",Datastore.Faculty,'name'))
        self.response.out.write(select("Rooms",Datastore.Faculty,'room'))
        self.response.out.write(select("Buildings",Datastore.building,'building'))
        self.response.out.write(select("Days",Datastore.OfficeHourJoin,'day'))
        types = Datastore.Faculty.all()
        """
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="name">')
        
        self.response.out.write('<optgroup label="Names">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(fac.key()) + '>')
            self.response.out.write(fac.name)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        """
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="building">')
        build = Datastore.building.all()
        self.response.out.write('<optgroup label="Buildings">')
        i = 1
        for abr in build :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(abr.building)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="room">')
        self.response.out.write('<optgroup label="Rooms">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.room)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="days">')
        types = Datastore.OfficeHourJoin.all()
        self.response.out.write('<optgroup label="Days">')
        i = 1
        for oh in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(oh.day)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="faculty_type">')
        types = Datastore.faculty_type.all()
        self.response.out.write('<optgroup label="Faculty Type">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.faculty_type)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="degreetype">')
        types = Datastore.degree_type.all()
        self.response.out.write('<optgroup label="Degree Type">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.degree_type)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="degreename">')
        types = Datastore.degree_name.all()
        self.response.out.write('<optgroup label="Degree Name">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.degree_name)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="institution">')
        types = Datastore.institution.all()
        self.response.out.write('<optgroup label="Degree Type">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.institution)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="conference">')
        types = Datastore.conference_name.all()
        self.response.out.write('<optgroup label="Conferences">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.conference_name)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="conferencetitle">')
        types = Datastore.ConferenceJoin.all()
        self.response.out.write('<optgroup label="Conferences">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.title)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="conferencelocation">')
        types = Datastore.location.all()
        self.response.out.write('<optgroup label="Conference Locations">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.location)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="conferenceyear">')
        types = Datastore.ConferenceJoin.all()
        self.response.out.write('<optgroup label="Conference Years">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.year)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="journalname">')
        types = Datastore.journal_name.all()
        self.response.out.write('<optgroup label="Journals">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.journal_name)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="books">')
        types = Datastore.BookJoin.all()
        self.response.out.write('<optgroup label="Books">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.title)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="publisher">')
        types = Datastore.publisher.all()
        self.response.out.write('<optgroup label="Book Publishers">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.publisher)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="gradstudents">')
        types = Datastore.student_eid.all()
        self.response.out.write('<optgroup label="Graduate Student EID">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.student_eid)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="studenttype">')
        types = Datastore.student_type.all()
        self.response.out.write('<optgroup label="Graduate Student Types">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.student_type)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="coursenumber">')
        types = Datastore.course_number.all()
        self.response.out.write('<optgroup label="Course Numbers">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.course_number)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
                
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="coursetype">')
        types = Datastore.course_type.all()
        self.response.out.write('<optgroup label="Course Types">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.course_type)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')        
                
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="semeester">')
        types = Datastore.semester.all()
        self.response.out.write('<optgroup label="Course Semesters">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.semester)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
                
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="awardtype">')
        types = Datastore.award_type.all()
        self.response.out.write('<optgroup label="Award Types">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.award_type)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="institution">')
        types = Datastore.AwardJoin.all()
        self.response.out.write('<optgroup label="Award Titles">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.title)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')
        
        self.response.out.write('<select style="margin: 0.2em" multiple="multiple" size="10" name="institution">')
        types = Datastore.AwardJoin.all()
        self.response.out.write('<optgroup label="Award Year">')
        i = 1
        for fac in types :
            self.response.out.write('<option value=' + str(i) + '>')
            self.response.out.write(fac.year)
            self.response.out.write('</option>')
            i+=1
        self.response.out.write('</optgroup></select>')

        self.response.out.write('<input type="submit" name="searchaction" value="Search" />')
        
    def post (self) :
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('name')))
        self.response.out.write('</pre></body></html>')

