                                                                     
                                                                     
                                                                     
                                             
#
#  TestFaculty3.py
#  Faculty3
#
#  Created by Samira Irani on 11/1/09.
#  Copyright (c) 2009 UT Austin. All rights reserved.
#

import importer
import exporter
import unittest
import string
import Admin
from google.appengine.ext import db
from google.appengine.ext import webapp

class TestFaculty3 (unittest.TestCase) :
    def test_db (self) :
        cn = course_number(course_number="CS101")
        cn.put()
        q = db.GqlQuery("SELECT * FROM course_number")
	get = q.get()
        self.assert_(get.course_number.course_number == "CS101")
	cn.delete()
	q = db.GqlQuery("SELECT * FROM course_number")
	get = q.get()
	self.assert_(get is None)

        
    def test_import (self) :
        f = importer.Faculty()
        f.process("IETest.txt")
        self.assert_(f.faculty_firstname == "Joe")
        self.assert_(f.faculty_lastname == "James")
        self.assert_(f.office == ("TAY", "3.112"))
        self.assert_(f.phone_number == "5124448888")
        self.assert_(f.email == "joesm...@cs.utexas.edu")
        self.assert_(f.website == "http://cs.utexas.edu/~joesmith")
        self.assert_(f.faculty_type == "Researcher")
        self.assert_(f.research_areas == ["Autonomous Vehicles", "Artificial Intelligence"])
        self.assert_(f.office_hours == [{"Monday":("11:00 AM", "1:00 PM")}])
        self.assert_(f.degrees == [("PhD", "Computer Science", "University of Texas at Austin", "1987")])
        self.assert_(f.conferences == [("Vehicle Talk Day", "2008-08", "Austin, Texas", "How Cars Drive Themselves")])
        self.assert_(f.journals == [("Journal of Academic Stuff(s)", "How I Made Vehicles Drive Themselves", "1999-06")])
        self.assert_(f.graduate_students == [("Bob", "White", "Masters", "How Stuff Works", "2009-07")])
        self.assert_(f.classes == [("Intro to Operating Systems", "CS373H", "Undergraduate", "Spring 2010", "55075")])
        self.assert_(f.awards == [("Award for Being Great", "Award", "2007")])
        self.assert_(f.books == [("Book of Stuff", [("John", "Smithington")])])
        
    def test_export(self) :
        f = importer.Faculty()
        f.faculty_firstname = "Joe"
        f.faculty_lastname = "James"
        f.office = ("TAY", "3.112")
        f.phone_number = "5124448888"
        f.email = "joesm...@cs.utexas.edu"
        f.website = "http://cs.utexas.edu/~joesmith"
        f.faculty_type = "Researcher"
        f.research_areas = ["Autonomous Vehicles", "Artificial Intelligence"]
        f.office_hours = [{"Monday":("11:00 AM", "1:00 PM")}]
        f.degrees = [("PhD", "Computer Science", "University of Texas at Austin", "1987")]
        f.conferences = [("Vehicle Talk Day", "2008-08", "Austin, Texas", "How Cars Drive Themselves")]
        f.journals = [("Journal of Academic Stuff(s)", "How I Made Vehicles Drive Themselves", "1999-06")]
        f.graduate_students = [("Bob", "White", "Masters", "How Stuff Works", "2009-07")]
        f.classes = [("Intro to Operating Systems", "CS373H", "Undergraduate", "Spring 2010", "55075")]
        f.awards = [("Award for Being Great", "Award", "2007")]
        f.books = [("Book of Stuff", [("John", "Smithington")])]
        exporter.export(f)
        file = open(string.strip(f.faculty_firstname) + ".xml")
        
        self.assert_(file.readline() == "<?xml version='1.0' encoding='utf-8'?>\n")
        #print file.readline()
        self.assert_(file.readline() == "<faculty_member>\n")
        self.assert_(file.readline() == " <faculty_firstname>\n")
        self.assert_(file.readline() == "  Joe\n")
        self.assert_(file.readline() == " </faculty_firstname>\n")
        self.assert_(file.readline() == " <faculty_lastname>\n")
        self.assert_(file.readline() == "  James\n")
        self.assert_(file.readline() == " </faculty_lastname>\n")
        self.assert_(file.readline() == " <office>\n")
        self.assert_(file.readline() == "  <building>\n")
        self.assert_(file.readline() == "   TAY\n")
        self.assert_(file.readline() == "  </building>\n")
        self.assert_(file.readline() == "  <room>\n")
        self.assert_(file.readline() == "   3.112\n")
        self.assert_(file.readline() == "  </room>\n")
        self.assert_(file.readline() == " </office>\n")
        self.assert_(file.readline() == " <phone_number>\n")
        self.assert_(file.readline() == "  5124448888\n")
        self.assert_(file.readline() == " </phone_number>\n")
        self.assert_(file.readline() == " <email>\n")
        self.assert_(file.readline() == "  joesm...@cs.utexas.edu\n")
        self.assert_(file.readline() == " </email>\n")
        self.assert_(file.readline() == " <website>")
        self.assert_(file.readline() == "  http://cs.utexas.edu/~joesmith\n")
        self.assert_(file.readline() == " </website>\n")
        self.assert_(file.readline() == " <faculty_type>\n")
        self.assert_(file.readline() == "  Researcher\n")
        self.assert_(file.readline() == " </faculty_type>\n")
        self.assert_(file.readline() == " <research_areas>\n")
        self.assert_(file.readline() == "  <research_area>\n")
        self.assert_(file.readline() == "   Autonomous Vehicles\n")
        self.assert_(file.readline() == "  </research_area>\n")
        self.assert_(file.readline() == "  <research_area>\n")
        self.assert_(file.readline() == "   Artificial Intelligence\n")
        self.assert_(file.readline() == "  </research_area>\n")
        self.assert_(file.readline() == " </research_areas>\n")
        self.assert_(file.readline() == " <office_hours>\n")
        self.assert_(file.readline() == "  <office_hour>\n")
        self.assert_(file.readline() == "   <day>\n")
        self.assert_(file.readline() == "    Monday\n")
        self.assert_(file.readline() == "   </day>\n")
        self.assert_(file.readline() == "   <start>\n")
        self.assert_(file.readline() == "    11:00 AM\n")
        self.assert_(file.readline() == "   </start>\n")
        self.assert_(file.readline() == "   <end>\n")
        self.assert_(file.readline() == "    1:00 PM\n")
        self.assert_(file.readline() == "   </end>\n")
        self.assert_(file.readline() == "  </office_hour>\n")
        self.assert_(file.readline() == " </office_hours>\n")
        self.assert_(file.readline() == " <degrees>\n")
        self.assert_(file.readline() == "  <degree>\n")
        self.assert_(file.readline() == "   <degree_type>\n")
        self.assert_(file.readline() == "    PhD\n")
        self.assert_(file.readline() == "   </degree_type>\n")
        self.assert_(file.readline() == "   <degree_name>\n")
        self.assert_(file.readline() == "    Computer Science\n")
        self.assert_(file.readline() == "   </degree_name>\n")
        self.assert_(file.readline() == "   <institution>\n")
        self.assert_(file.readline() == "    University of Texas at Austin\n")
        self.assert_(file.readline() == "   </institution>\n")
        self.assert_(file.readline() == "   <degree_date>\n")
        self.assert_(file.readline() == "    1987\n")
        self.assert_(file.readline() == "   </degree_date>\n")
        self.assert_(file.readline() == "  </degree>\n")
        self.assert_(file.readline() == " </degrees>\n")
        self.assert_(file.readline() == " <conferences>\n")
        self.assert_(file.readline() == "  <conference>\n")
        self.assert_(file.readline() == "   <conference_name>\n")
        self.assert_(file.readline() == "    Vehicle Talk Day\n")
        self.assert_(file.readline() == "   </conference_name>\n")
        self.assert_(file.readline() == "   <conference_date>\n")
        self.assert_(file.readline() == "    2008-08\n")
        self.assert_(file.readline() == "   </conference_date>\n")
        self.assert_(file.readline() == "   <location>\n")
        self.assert_(file.readline() == "    Austin, Texas\n")
        self.assert_(file.readline() == "   </location>\n")
        self.assert_(file.readline() == "   <title>\n")
        self.assert_(file.readline() == "    How Cars Drive Themselves\n")
        self.assert_(file.readline() == "   </title>\n")
        self.assert_(file.readline() == "  </conference>\n")
        self.assert_(file.readline() == " </conferences>\n")
        self.assert_(file.readline() == " <journals>\n")
        self.assert_(file.readline() == "  <journal>\n")
        self.assert_(file.readline() == "   <journal_name>\n")
        self.assert_(file.readline() == "    Journal of Academic Stuff(s)\n")
        self.assert_(file.readline() == "   </journal_name>\n")
        self.assert_(file.readline() == "   <article_title>\n")
        self.assert_(file.readline() == "    How I Made Vehicles Drive Themselves\n")
        self.assert_(file.readline() == "   </article_title>\n")
        self.assert_(file.readline() == "   <journal_date>\n")
        self.assert_(file.readline() == "    1999-06\n")
        self.assert_(file.readline() == "   </journal_date>\n")
        self.assert_(file.readline() == "  </journal>\n")
        self.assert_(file.readline() == " </journals>\n")
        self.assert_(file.readline() == " <graduate_students>\n")
        self.assert_(file.readline() == "  <graduate_student>\n")
        self.assert_(file.readline() == "   <student_firstname>\n")
        self.assert_(file.readline() == "    Bob\n")
        self.assert_(file.readline() == "   </student_firstname>\n")
        self.assert_(file.readline() == "   <student_lastname>\n")
        self.assert_(file.readline() == "    White\n")
        self.assert_(file.readline() == "   </student_lastname>\n")
        self.assert_(file.readline() == "   <student_type>\n")
        self.assert_(file.readline() == "    Masters\n")
        self.assert_(file.readline() == "   </student_type>\n")
        self.assert_(file.readline() == "   <dissertation>\n")
        self.assert_(file.readline() == "    How Stuff Works\n")
        self.assert_(file.readline() == "   </dissertation>\n")
        self.assert_(file.readline() == "   <student_date>\n")
        self.assert_(file.readline() == "    2009-07\n")
        self.assert_(file.readline() == "   </student_date>\n")
        self.assert_(file.readline() == "  </graduate_student>\n")
        self.assert_(file.readline() == " </graduate_students>\n")
        self.assert_(file.readline() == " <classes>\n")
        self.assert_(file.readline() == "  <class>\n")
        self.assert_(file.readline() == "   <class_name>\n")
        self.assert_(file.readline() == "    Intro to Operating Systems\n")
        self.assert_(file.readline() == "   </class_name>\n")
        self.assert_(file.readline() == "   <course_number>\n")
        self.assert_(file.readline() == "    CS373H\n")
        self.assert_(file.readline() == "   </course_number>\n")
        self.assert_(file.readline() == "   <class_type>\n")
        self.assert_(file.readline() == "    Undergraduate\n")
        self.assert_(file.readline() == "   </class_type>\n")
        self.assert_(file.readline() == "   <semester>\n")
        self.assert_(file.readline() == "    Spring 2010\n")
        self.assert_(file.readline() == "   </semester>\n")
        self.assert_(file.readline() == "   <unique>\n")
        self.assert_(file.readline() == "    55075\n")
        self.assert_(file.readline() == "   </unique>\n")
        self.assert_(file.readline() == "  </class>\n")
        self.assert_(file.readline() == " </classes>\n")
        self.assert_(file.readline() == " <awards>\n")
        self.assert_(file.readline() == "  <award>\n")
        self.assert_(file.readline() == "   <award_name>\n")
        self.assert_(file.readline() == "    Award for Being Great\n")
        self.assert_(file.readline() == "   </award_name>\n")
        self.assert_(file.readline() == "   <award_type>\n")
        self.assert_(file.readline() == "    Award\n")
        self.assert_(file.readline() == "   </award_type>\n")
        self.assert_(file.readline() == "   <award_date>\n")
        self.assert_(file.readline() == "    2007\n")
        self.assert_(file.readline() == "   </award_date>\n")
        self.assert_(file.readline() == "  </award>\n")
        self.assert_(file.readline() == " </awards>\n")
        self.assert_(file.readline() == " <books>\n")
        self.assert_(file.readline() == "  <book>")
        self.assert_(file.readline() == "   <book_name>")
        self.assert_(file.readline() == "    Book of Stuff")
        self.assert_(file.readline() == "   </book_name>")
        self.assert_(file.readline() == "   <coauthors>")
        self.assert_(file.readline() == "    <coauthor>")
        self.assert_(file.readline() == "     <coauthor_firstname>")
        self.assert_(file.readline() == "      John")
        self.assert_(file.readline() == "     </coauthor_firstname>")
        self.assert_(file.readline() == "     <coauthor_lastname>")
        self.assert_(file.readline() == "      Smithington")
        self.assert_(file.readline() == "     </coauthor_lastname>")
        self.assert_(file.readline() == "    </coauthor>")
        self.assert_(file.readline() == "   </coauthors>")
        self.assert_(file.readline() == "  </book>")
        self.assert_(file.readline() == " </books>")
        self.assert_(file.readline() == "</faculty_member>")       
        
class MainPage (webapp.RequestHandler) :
    def get (self) :
        self.response.out.write('<html><body><b>Tester</b><br />')
        self.response.out.write('All Passed!')
        self.response.out.write('</body></html>')

if __name__ == "__main__" :
    unittest.main()
        
