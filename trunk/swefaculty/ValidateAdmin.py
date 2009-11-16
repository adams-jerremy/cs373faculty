                                                                     
                                                                     
                                                                     
                                             
# ----------------
# ValidateAdmin.py
# ----------------

'''
Only a few fields are worth validating on the Admin page.  We assume
that in general the admins know what they are doing, and it's hard
to validate long strings such as journal names, etc anyway.

eid - assume they are one, two, or three lower case letters
      followed by 2-4 #s
building - 3-4 upper case letters, last one can be a number
my_time - 00:00 through 23:59
course_number - CS followed by 3 digits, followed by optional capital letter
semester - Spring, Summer, or Fall, followed by space, followed by a year.
'''

import re


def faculty_email (s) :
    return True

def student_eid (s) :
    return eid (s)

def eid (s) :
    return not re.search('^[a-z]([a-z])?([a-z])?\d\d(\d)?(\d)?$', s) is None

def faculty_type (s) :
    return True

def research_area (s) :
    return True

def building (s) :
    return not re.search('^[A-Z][A-Z]([A-Z])?([A-Z,1-8])$', s) is None

def start_time (s) :
    return my_time(s)

def end_time (s) :
    return my_time(s)

def my_time (s) :
    return not re.search('^((0[0-9])|(1[0-9])|(2[0-3])):[0-5]\d$', s) is None

def degree_type (s) :
    return True

def degree_name (s) :
    return True

def institution (s) :
    return True

def conference_name (s) :
    return True

def location (s) :
    return True

def journal_name (s) :
    return True

def publisher (s) :
    return True

def student_type (s) :
    return True

def course_type(s):
    return True

def course_number (s) :
    return not re.search('^CS\d\d\d([A-Z])?$', s) is None

def course_name (s) :
    return True


def semester (s) :
    return not re.search('^((Spring)|(Summer)|(Fall)) \d\d\d\d$', s) is None

def award_name (s) :
    return True

def award_type (s) :
    return True

