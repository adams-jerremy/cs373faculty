import re
import string

# ------------
# phone_number
# ------------

def course(cs,c):
    return c not in cs

def graduateStudent(ss,s):
    return s not in ss

def researchArea(ras,ra):
    return ra not in ras

def degree(degrees,type,inst,date):
    if type=="" or inst =="" or date == "": return False;
    for degree in degrees:
        if degree.type == type and degree.institution == inst and degree.date == date: return False;
    return int(date)>1900

def officeHour(day,begin,end):
    if day=="" or begin =="" or end == "": return False;
    begin = string.replace(begin,":","")
    end = string.replace(end,":","")
    return int(begin) < int(end)

def phone_number (phone) :
    return not re.search('^\d\d\d\d\d\d\d\d\d\d$', phone) is None

def name(name):
    return name=='valid'

def email(email):
    return re.search('^[\w\.]+@(\w+\.)+(com|net|org|gov|edu|mil|biz|info|mobi|name|aero|jobs|museum|[a-zA-Z][a-zA-Z])$', email) is not None
def website(website):
    return re.search('^(https?)://(\w+\.)+(com|net|org|gov|edu|mil|biz|info|mobi|name|aero|jobs|museum|[a-zA-Z][a-zA-Z])$',website) is not None

def office(building, location):
    if location == ""  or building == "": return building == location;
    if re.search('\.',location) is None: return False;
    floor, room = location.split('.')
    return (building == 'TAY' and 0 < int(floor) < 7)\
            or (building == 'PAI' and 0 < int(floor) < 6)\
            or (building == 'ACES' and 0< int(floor) < 7)\
            or (building == 'ENS' and -1<int(floor)<8 )
            
def main():
    print hours("8:30","9:30")
    
    print "(",
    for i in xrange(0,24):
        print '"',
        print i,
        print ':00",',
        print '"',
        print i,
        print ':30",',
    print ")"
    
if __name__ == "__main__":
    main()