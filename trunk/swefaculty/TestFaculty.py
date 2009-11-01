#!/usr/bin/env python

# ------------------------------------
# projects/python/matlab/TestFaculty.py
# Copyright (C) 2009
# Glenn P. Downing
# ------------------------------------

# To run the tests
#     TestFaculty.py

# To document the tests
#     pydoc -w TestFaculty

import ValidateFaculty
import unittest

# ----------
# TestAdmin
# ----------

class Degree (object) :
    def __init__ (self, a, b, c) :
        self.type = a
        self.institution = b
        self.date = c

class TestFaculty (unittest.TestCase) :

    # --------
    #  course
    # --------

    def test_course1 (self) :
        m = ["CS373","CS357","CS347"]
        self.assert_(ValidateFaculty.course(m,"CS313K") == True)

    def test_course2 (self) :
        m = ["CS373","CS357","CS347"]
        self.assert_(ValidateFaculty.course(m,"CS373") == False)

    # --------
    #  degree
    # --------

    def test_degree1 (self) :
        degree1 = Degree("BSCS","UT",2009)
        degree2 = Degree("BSEE","GaTech",1995)
        degrees = [degree1,degree2]
        self.assert_(ValidateFaculty.degree(degrees,"BSCS","UT",1999) == True)

    def test_degree2 (self) :
        degree1 = Degree("BSCS","UT",2009)
        degree2 = Degree("BSEE","GaTech",1995)
        degrees = [degree1,degree2]
        self.assert_(ValidateFaculty.degree(degrees,"BSCS","GaTech",2009) == True)

    def test_degree3 (self) :
        degree1 = Degree("BSCS","UT",2009)
        degree2 = Degree("BSEE","GaTech",1995)
        degrees = [degree1,degree2]
        self.assert_(ValidateFaculty.degree(degrees,"BSEE","UT",2009) == True)

    def test_degree3 (self) :
        degree1 = Degree("BSCS","UT",2009)
        degree2 = Degree("BSEE","GaTech",1995)
        degrees = [degree1,degree2]
        self.assert_(ValidateFaculty.degree(degrees,"BSCS","UT",2009) == False)

    def test_degree4 (self) :
        degree1 = Degree("BSCS","UT",2009)
        degree2 = Degree("BSEE","GaTech",1995)
        degrees = [degree1,degree2]
        self.assert_(ValidateFaculty.degree(degrees,"BSCS","UT",1899) == False)

    def test_degree5 (self) :
        degree1 = Degree("BSCS","UT",2009)
        degree2 = Degree("BSEE","GaTech",1995)
        degrees = [degree1,degree2]
        self.assert_(ValidateFaculty.degree(degrees,"BSCS","UT",2050) == False)

    # -----------
    #  officeHour
    # -----------

    def test_officeHour1 (self) :
        self.assert_(ValidateFaculty.officeHour("Monday","09:00","10:00") == True)

    def test_officeHour2 (self) :
        self.assert_(ValidateFaculty.officeHour("Tuesday","13:00","15:00") == True)

    def test_officeHour3 (self) :
        self.assert_(ValidateFaculty.officeHour("Wed","09:00","23:00") == True)

    def test_officeHour4 (self) :
        self.assert_(ValidateFaculty.officeHour("Monday","11:00","10:00") == False)

    def test_officeHour5 (self) :
        self.assert_(ValidateFaculty.officeHour("","09:00","10:00") == False)

    def test_officeHour6 (self) :
        self.assert_(ValidateFaculty.officeHour("Monday","","10:00") == False)

    def test_officeHour7 (self) :
        self.assert_(ValidateFaculty.officeHour("Monday","11:00","") == False)

    def test_officeHour8 (self) :
        self.assert_(ValidateFaculty.officeHour("Monday","16:15","16:13") == False)

    # -------------
    #  phone_number
    # -------------

    def test_phone_number1 (self) :
        self.assert_(ValidateFaculty.phone_number("5125551234") == True)

    def test_phone_number2 (self) :
        self.assert_(ValidateFaculty.phone_number("51255512345") == False)

    def test_phone_number3 (self) :
        self.assert_(ValidateFaculty.phone_number("512555123") == False)

    # -------------
    #  email
    # -------------

    def test_email1 (self) :
        self.assert_(ValidateFaculty.email("help@customer_support.com") == True)

    def test_email2 (self) :
        self.assert_(ValidateFaculty.email("help.me@customer_support.com") == True)

    def test_email3 (self) :
        self.assert_(ValidateFaculty.email("help3.me@customer_support.intel.com") == True)

    def test_email4 (self) :
        self.assert_(ValidateFaculty.email("help3@me@customer_support.intel.com") == False)

    # -------------
    #  website
    # -------------

    def test_website1 (self) :
        self.assert_(ValidateFaculty.website("http://www.yahoo.com") == True)

    def test_website2 (self) :
        self.assert_(ValidateFaculty.website("https://www.yahoo.com") == True)

    def test_website3 (self) :
        self.assert_(ValidateFaculty.website("http://cs.utexas.edu") == True)

    def test_website4 (self) :
        self.assert_(ValidateFaculty.website("www.utexas.edu") == False)

    def test_website5 (self) :
        self.assert_(ValidateFaculty.website("http://www.utexas.edu3") == False)

    # -------------
    #  office
    # -------------

    def test_office1 (self) :
        self.assert_(ValidateFaculty.office("TAY","4.114") == True)

    def test_office11 (self) :
        self.assert_(ValidateFaculty.office("TAY","1.11") == True)

    def test_office12 (self) :
        self.assert_(ValidateFaculty.office("ENS","0.11") == True)

    def test_office2 (self) :
        self.assert_(ValidateFaculty.office("TAY","4.") == False)

    def test_office3 (self) :
        self.assert_(ValidateFaculty.office("TAY",".12") == False)

    def test_office4 (self) :
        self.assert_(ValidateFaculty.office("TAY","7.12") == False)

    def test_office5 (self) :
        self.assert_(ValidateFaculty.office("TAY","0.12") == False)

    def test_office6 (self) :
        self.assert_(ValidateFaculty.office("ENS","8.12") == False)



if __name__ == "__main__" :
    unittest.main()


