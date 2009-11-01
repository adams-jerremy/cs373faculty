#!/usr/bin/env python

# ------------------------------------
# projects/python/matlab/TestAdmin.py
# Copyright (C) 2009
# Glenn P. Downing
# ------------------------------------

# To run the tests
#     TestAdmin.py

# To document the tests
#     pydoc -w TestAdmin

import ValidateAdmin
import unittest

# ----------
# TestAdmin
# ----------

class TestAdmin (unittest.TestCase) :

    # --------
    #  eid
    # --------

    def test_eid1 (self) :
        m = "csl452"
        self.assert_(ValidateAdmin.eid(m) == True)

    def test_eid2 (self) :
        m = "csl4522"
        self.assert_(ValidateAdmin.eid(m) == True)

    def test_eid3 (self) :
        m = "cs4522"
        self.assert_(ValidateAdmin.eid(m) == True)

    def test_eid4 (self) :
        m = "cs45"
        self.assert_(ValidateAdmin.eid(m) == True)

    def test_eid5 (self) :
        m = "145"
        self.assert_(ValidateAdmin.eid(m) == False)

    def test_eid6 (self) :
        m = "145a"
        self.assert_(ValidateAdmin.eid(m) == False)

    def test_eid7 (self) :
        m = "abcd12"
        self.assert_(ValidateAdmin.eid(m) == False)

    def test_eid8 (self) :
        m = "a12345"
        self.assert_(ValidateAdmin.eid(m) == False)

    def test_eid9 (self) :
        m = "CSL452"
        self.assert_(ValidateAdmin.eid(m) == False)

    def test_eid10 (self) :
        m = "csl4"
        self.assert_(ValidateAdmin.eid(m) == False)

    # --------
    #  my_time
    # --------

    def test_mt1 (self) :
        m = "00:00"
        self.assert_(ValidateAdmin.my_time(m) == True)

    def test_mt2 (self) :
        m = "12:15"
        self.assert_(ValidateAdmin.my_time(m) == True)

    def test_mt3 (self) :
        m = "23:00"
        self.assert_(ValidateAdmin.my_time(m) == True)

    def test_mt4 (self) :
        m = "23:59"
        self.assert_(ValidateAdmin.my_time(m) == True)

    def test_mt5 (self) :
        m = "0:00"
        self.assert_(ValidateAdmin.my_time(m) == False)

    def test_mt6 (self) :
        m = "0"
        self.assert_(ValidateAdmin.my_time(m) == False)

    def test_mt7 (self) :
        m = "5PM"
        self.assert_(ValidateAdmin.my_time(m) == False)

    def test_mt8 (self) :
        m = "5 PM"
        self.assert_(ValidateAdmin.my_time(m) == False)

    def test_mt9 (self) :
        m = "1:60"
        self.assert_(ValidateAdmin.my_time(m) == False)

    def test_mt10 (self) :
        m = "09:60"
        self.assert_(ValidateAdmin.my_time(m) == False)

    # --------------
    #  course_number
    # --------------

    def test_cn1 (self) :
        m = "CS373"
        self.assert_(ValidateAdmin.course_number(m) == True)

    def test_cn2 (self) :
        m = "CS123"
        self.assert_(ValidateAdmin.course_number(m) == True)

    def test_cn3 (self) :
        m = "CS313K"
        self.assert_(ValidateAdmin.course_number(m) == True)

    def test_cn4 (self) :
        m = "C347"
        self.assert_(ValidateAdmin.course_number(m) == False)

    def test_cn5 (self) :
        m = "cs373"
        self.assert_(ValidateAdmin.course_number(m) == False)

    def test_cn6 (self) :
        m = "CS3777"
        self.assert_(ValidateAdmin.course_number(m) == False)

    def test_cn7 (self) :
        m = "CSS337"
        self.assert_(ValidateAdmin.course_number(m) == False)

    def test_cn8 (self) :
        m = "M313"
        self.assert_(ValidateAdmin.course_number(m) == False)

    def test_cn9 (self) :
        m = "CS373KK"
        self.assert_(ValidateAdmin.course_number(m) == False)

    def test_cn10 (self) :
        m = "CS 373"
        self.assert_(ValidateAdmin.course_number(m) == False)

    # --------------
    #  building
    # --------------

    def test_bd1 (self) :
        m = "JGB"
        self.assert_(ValidateAdmin.building(m) == True)

    def test_bd2 (self) :
        m = "ACES"
        self.assert_(ValidateAdmin.building(m) == True)

    def test_bd3 (self) :
        m = "FC1"
        self.assert_(ValidateAdmin.building(m) == True)

    def test_bd4 (self) :
        m = "ACE2"
        self.assert_(ValidateAdmin.building(m) == True)

    def test_bd5 (self) :
        m = "J1D"
        self.assert_(ValidateAdmin.building(m) == False)

    def test_bd6 (self) :
        m = "AC2E"
        self.assert_(ValidateAdmin.building(m) == False)

    def test_bd7 (self) :
        m = "csl"
        self.assert_(ValidateAdmin.building(m) == False)

    def test_bd8 (self) :
        m = "ACESD"
        self.assert_(ValidateAdmin.building(m) == False)

    def test_bd9 (self) :
        m = "A CE"
        self.assert_(ValidateAdmin.building(m) == False)

    def test_bd10 (self) :
        m = "A 1"
        self.assert_(ValidateAdmin.building(m) == False)

    # --------------
    #  semester
    # --------------

    def test_sm1 (self) :
        m = "Fall 2009"
        self.assert_(ValidateAdmin.semester(m) == True)

    def test_sm2 (self) :
        m = "Summer 2009"
        self.assert_(ValidateAdmin.semester(m) == True)

    def test_sm3 (self) :
        m = "Spring 2009"
        self.assert_(ValidateAdmin.semester(m) == True)

    def test_sm4 (self) :
        m = "Fall 1234"
        self.assert_(ValidateAdmin.semester(m) == True)

    def test_sm5 (self) :
        m = "Fall1234"
        self.assert_(ValidateAdmin.semester(m) == False)

    def test_sm6 (self) :
        m = "Fall 200"
        self.assert_(ValidateAdmin.semester(m) == False)

    def test_sm7 (self) :
        m = "Fall 20001"
        self.assert_(ValidateAdmin.semester(m) == False)

    def test_sm8 (self) :
        m = "SummerFall 2009"
        self.assert_(ValidateAdmin.semester(m) == False)

    def test_sm9 (self) :
        m = "Summer  2010"
        self.assert_(ValidateAdmin.semester(m) == False)

    def test_sm10 (self) :
        m = "2010 Summer"
        self.assert_(ValidateAdmin.semester(m) == False)



if __name__ == "__main__" :
    unittest.main()


