import re
import string
import datetime

# ------------
# phone_number
# ------------

yearLimit = 8+ datetime.datetime.now().year

def award(aws,aw):
    return aw not in aws

def book(bs,b):
    return b not in bs

def conference(confs,name,location,title,date):
    for conf in confs:
        if conf.name == name and conf.title == title and conf.location == location and conf.date == date : return False;
    return yearLimit>int(date)>1900

def article(articles,title,journal,date):
    for article in articles:
        if article.title == title and article.journal == journal and article.date == date: return False;
    return yearLimit>int(date)>1900

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
    return yearLimit>int(date)>1900

def officeHour(day,begin,end):
    if day=="" or begin =="" or end == "": return False;
    begin = string.replace(begin,":","")
    end = string.replace(end,":","")
    return int(begin) < int(end)

def phone_number (phone) :
    return not re.search('^(1|1\s*-)?\s*((\(\d\d\d\))|(\d\d\d))\s*-?\s*\d\d\d\s*-?\s*\d\d\d\d\s*((ext|x|ext.)\s*\d+)?$', phone) is None

def name(name):
    return name=='valid'

def email(email):
    return re.search('^[\w\.]+@(\w+\.)+(com|net|org|gov|edu|mil|biz|info|mobi|name|aero|jobs|museum|[a-zA-Z][a-zA-Z])$', email) is not None
def website(website):
    return re.search('^(https?)://(\w+\.)+(com|net|org|gov|edu|mil|biz|info|mobi|name|aero|jobs|museum|[a-zA-Z][a-zA-Z])$',website) is not None

def office(building, location):
    if location == ""  or building == "": return building == location;
    if re.search('\d+\.\d+',location) is None: return False;
    floor, room = location.split('.')
    return (building == 'TAY' and 0 < int(floor) < 7)\
            or (building == 'PAI' and 0 < int(floor) < 6)\
            or (building == 'ACES' and 0< int(floor) < 7)\
            or (building == 'ENS' and -1<int(floor)<8 )
            
def main():
    print phone_number("1214541439x0")
    print office("TAY","4.11")
    print office("TAY","4.")
    print office("TAY",".11")
    
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