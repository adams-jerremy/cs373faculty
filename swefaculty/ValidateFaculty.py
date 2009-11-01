import re

# ------------
# phone_number
# ------------

def phone_number (phone) :
    return not re.search('^\d\d\d\d\d\d\d\d\d\d$', phone) is None

def name(name):
    return name=='valid'

def email(email):
    return re.search('^[\w\.]+@(\w+\.)+(com|net|org|gov|edu|mil|biz|info|mobi|name|aero|jobs|museum|[a-zA-Z][a-zA-Z])$', email) is not None
def website(website):
    return re.search('^(https?)://(\w+\.)+(com|net|org|gov|edu|mil|biz|info|mobi|name|aero|jobs|museum|[a-zA-Z][a-zA-Z])$',website) is not None

def office(building, location):
    floor, room = location.split('.')
    return (building == 'TAY' and 0 < int(floor) < 7)\
            or (building == 'PAI' and 0 < int(floor) < 6)\
            or (building == 'ACES' and 0< int(floor) < 7)\
            or (building == 'ENS' and -1<int(floor)<8 )
            
def main():
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