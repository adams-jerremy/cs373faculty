import cgi

from google.appengine.ext import webapp

import ValidateFaculty

class Faculty:

    def __init__(self):
        self.phone = ""
        self.name = ""
        self.building = ""
        self.room = ""
        self.email = ""
        self.website = ""
        self.officeHours = []
        
class OfficeHour:
    days = ("","M","T","W","R","F")
    times = ("","0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30")
    def __init__(self):
        self.day = ""
        beginTime = ""
        endTime = ""

def officeHourDayDropDown():
    s = '<select name="officeHrDay">'
    for d in OfficeHour.days :
        s+='<option value="'
        s+=d
        s+='">'
        s+=d
        s+='</option>'
    s+='</select>' 
    return s

def officeHourTimeDropDown(t):
    s = '<select name="'+t+'">'
    for t in OfficeHour.times :
        s+='<option value="'
        s+=t
        s+='">'
        s+=t
        s+='</option>'
    s+='</select>' 
    return s

    
def officeHoursTextBox(f):
    s = '<textarea rows ="' + len(f.officeHours)+1+'" cols="25" readonly="readonly">'
#    for officeHour in f.officeHours:
#        s+=officeHour.day
#        s+= ' from '
#        s+=officeHour.beginTime
#        s+= ' to '
#        s+=officeHour.endTime
    s+='</textarea>'
    return '<textarea rows="3" cols="25" readonly="readonly">this is in the text areas</textarea>'

def buildingDropDown(facultyMember):
    buildings = ("TAY","PAI","ACES","ENS")
    s = '<select name="building">'
    for b in buildings :
        s+='<option value="'
        s+=b
        s+=('" selected>' if b==facultyMember.building else '">')
        s+=b
        s+='</option>'
    s+='</select>' 
    return s

class MainPage (webapp.RequestHandler) :
    id = ""
    facs = {}
    type = "" 
    def get (self) :
        self.response.out.write('<form action="/faculty" method="post">')
        if MainPage.facs.has_key(MainPage.id):
            MainPage.type = "submit"
            self.response.out.write('ID:')
            self.response.out.write(MainPage.id);
            fac = MainPage.facs[MainPage.id]
            self.response.out.write('<br />Faculty Name<br />')
            self.response.out.write('<input type="text" name="name" value = "' +fac.name+ '" />')
            self.response.out.write('<br/>Faculty Office Building<br/>')
            self.response.out.write(buildingDropDown(fac))
            self.response.out.write('<br/>Faculty Room Number<br/>')
            self.response.out.write('<input type="text" name="room" value = "' +fac.room+ '" />')
            self.response.out.write('<br/>Faculty Phone<br/>')
            self.response.out.write('<input type="text" name="phone" value = "' +fac.phone+ '" />')
            self.response.out.write('<br/>Faculty email<br/>')
            self.response.out.write('<input type="text" name="email" value = "' +fac.email+ '" />')
            self.response.out.write('<br/>Faculty website<br/>')
            self.response.out.write('<input type="text" name="website" value = "' +fac.website+ '" />')
            self.response.out.write('<br/>Faculty Office Hours<br/>')
            self.response.out.write(officeHoursTextBox(fac))
            
        else:
            MainPage.type = "Login"
            self.response.out.write('ID:')
            self.response.out.write('<input type="text" name="FacID"  />')
        self.response.out.write('<input type="submit" value="Submit" /> </form><br />')
        self.response.out.write('<form action="/" method="get"><input type="submit" value="Logout!"></form>')
        
    def post (self) :
        if MainPage.type == "Login":
            MainPage.id = cgi.escape(self.request.get('FacID'))
            if not MainPage.facs.has_key(MainPage.id):
                MainPage.facs[MainPage.id] = Faculty()
        else :
            fac = MainPage.facs[MainPage.id]
            name = cgi.escape(self.request.get('name'))
            building = cgi.escape(self.request.get('building'))
            room = cgi.escape(self.request.get('room'))
            phone = cgi.escape(self.request.get('phone'))
            email = cgi.escape(self.request.get('email'))
            website = cgi.escape(self.request.get('website'))
            
            if ValidateFaculty.name(name):
                fac.name = name
            else:
                self.response.out.write('Invalid name<br />')
            
            fac.building = building
            if ValidateFaculty.office(building, room) :
                fac.room = room
            else :
                self.response.out.write('Invalid Office.<br />')
                
            if ValidateFaculty.phone_number(phone) :
                fac.phone = phone
            else :
                self.response.out.write('Invalid number.<br />')
            if ValidateFaculty.email(email) :
                fac.email = email
            else :
                self.response.out.write('Invalid email.<br />')
            if ValidateFaculty.website(website) :
                fac.website = website
            else :
                self.response.out.write('Invalid Website.<br />')
        self.get()

if __name__ == "__main__":
    main()
