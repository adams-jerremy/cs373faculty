import re
import string
import datetime

# ------------
# phone_number
# ------------

yearLimit = 8+ datetime.datetime.now().year
"""
This function validates awards.
"""
def award(aws,aw):
    return aw not in aws
"""
This function validates books.
"""
def book(bs,b):
    return b not in bs
"""
This function validates conferences.
"""
def conference(confs,name,location,title,date):
    if name == "" or location == "" or title == "" or date == "": return False;
    for conf in confs:
        if conf.name == name and conf.title == title and conf.location == location and conf.date == date : return False;
    return yearLimit>int(date)>1900
"""
This function validates articles.
"""
def article(articles,title,journal,date):
    if title == "" or journal == "" or date == "": return False;
    for article in articles:
        if article.title == title and article.journal == journal and article.date == date: return False;
    return yearLimit>int(date)>1900
"""
This function validates courses.
"""
def course(cs,c):
    return c not in cs
"""
This function validates graduate students.
"""
def graduateStudent(ss,s):
    return s not in ss
"""
This function validates research areas.
"""
def researchArea(ras,ra):
    return ra not in ras
"""
This function validates degrees.
"""
def degree(degrees,type,inst,date):
    if type=="" or inst =="" or date == "": return False;
    for degree in degrees:
        if degree.type == type and degree.institution == inst and degree.date == date: return False;
    return yearLimit>int(date)>1900
"""
This function validates office hours.
"""
def officeHour(day,begin,end):
    if day=="" or begin =="" or end == "": return False;
    begin = string.replace(begin,":","")
    end = string.replace(end,":","")
    return int(begin) < int(end)
"""
This function validates phone numbers.
"""
def phone_number (phone) :
    return not re.search('^(1|1\s*-)?\s*((\(\d\d\d\))|(\d\d\d))\s*-?\s*\d\d\d\s*-?\s*\d\d\d\d\s*((ext|x|ext.)\s*\d+)?$', phone) is None
"""
This function validates names.
"""
def name(name):
    return re.search('^[\w\. ]+$',name) is not None
"""
This function validates emails.
"""
def email(email):
    return re.search('^[\w\.]+@(\w+\.)+(com|net|org|gov|edu|mil|biz|info|mobi|name|aero|jobs|museum|[a-zA-Z][a-zA-Z])$', email) is not None
"""
This function validates websites.
"""
def website(website):
    return re.search('^(https?)://(\w+\.)+(com|net|org|gov|edu|mil|biz|info|mobi|name|aero|jobs|museum|[a-zA-Z][a-zA-Z])([\w\.]+/?)*$',website) is not None

def year(year):
    return re.search('^/d/d/d/d$',year) is not None
"""
This function validates offices.
"""
def office(building, location):
    if location == ""  or building == "": return building == location;
    if re.search('\d+\.\d+',location) is None: return False;
    floor, room = location.split('.')
    return (building == 'TAY' and 0 < int(floor) < 7)\
            or (building == 'PAI' and 0 < int(floor) < 6)\
            or (building == 'ACES' and 0< int(floor) < 7)\
            or (building == 'ENS' and -1<int(floor)<8 )
        
def main():
    print name("jerremy adams")
    
    
if __name__ == "__main__":
    main()