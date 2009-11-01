#
#  import.py
#  Faculty2
#
#  Created by Samira Irani on 10/31/09.
#  Copyright (c) 2009 UT Austin. All rights reserved.
#

from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup
import sys
import exporter

"""
Simple Faculty class that holds onto faculty data frmom an xml file.
"""
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
    
    """
    This method takes in the file name from the command line and calls process().
    """
    def input(self) :
        filename = sys.argv[1]
        self.process(filename)
    
    """
    This method parses the given xml file and stores the data into the appropriate containers.
    """
    def process (self, filename) :
        f = open(filename)
        xml = ""
        while True :
            s = f.readline()
            if len(s) == 0 :
                break
            xml += s

        facxml = BeautifulStoneSoup(xml)
        self.faculty_firstname = facxml.faculty_firstname.string
        self.faculty_lastname = facxml.faculty_lastname.string
        self.office = (facxml.office.building.string, facxml.office.room.string)
        self.phone_number = facxml.phone_number.string
        self.email = facxml.email.string
        self.website = facxml.website.string
        self.faculty_type = facxml.faculty_type.string
        
        for ra in facxml.research_areas.findAll("research_area"):
            self.research_areas.append(ra.string)
        
        for oh in facxml.office_hours.findAll("office_hour") :
            self.office_hours.append({oh.day.string : (oh.start.string, oh.end.string)})
            
        for deg in facxml.degrees.findAll("degree") :
            self.degrees.append((deg.degree_type.string, deg.degree_name.string, deg.institution.string, deg.degree_date.string))
            
        for con in facxml.conferences.findAll("conference") :
            self.conferences.append((con.conference_name.string, con.conference_date.string, con.location.string, con.title.string))
            
        for jour in facxml.journals.findAll("journal") :
            self.journals.append((jour.journal_name.string, jour.article_title.string, jour.journal_date.string))
        
        for gs in facxml.graduate_students.findAll("graduate_student") :
            self.graduate_students.append((gs.student_firstname.string, gs.student_lastname.string, gs.student_type.string, gs.dissertation.string, gs.student_date.string))
            
        for cls in facxml.classes.findAll("class") :
            self.classes.append((cls.class_name.string,cls.course_number.string, cls.class_type.string, cls.semester.string, cls.unique.string))
            
        for awd in facxml.awards.findAll("award") :
            self.awards.append((awd.award_name.string, awd.award_type.string, awd.award_date.string))
            
        for bk in facxml.books.findAll("book") :
            coauthors = []
            for ca in bk.coauthors.findAll("coauthor"):
                coauthors.append((ca.coauthor_firstname.string, ca.coauthor_lastname.string))
            self.books.append((bk.book_name.string, coauthors))
        
if __name__ == "__main__" : 
    f = Faculty()
    f.input()
    exporter.export(f)
    
    
    