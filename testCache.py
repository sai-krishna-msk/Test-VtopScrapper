
# from  newScrapper import *
from  VtopScraperCache import *
obj = VtopScraper('17BCD7094', 'mskat135793579')
# print(obj.loginFetch(verbose=True))
obj.loginFetch()
Attendance_data = obj.loginFetch()
InnternalMarks_data = obj.InternalMarks()
Attnedance_data = obj.GetAttendance()
Assignment_data = obj.Get_Assignment_Status()



