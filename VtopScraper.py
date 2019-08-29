import cv2
import numpy as  np
import pickle 
import requests
from bs4 import BeautifulSoup 
import json 
import os
import base64
import time

class VtopScraper:

	"""
	Parent Class of vtop for login and logout
	"""




	def __init__(self , userid , password):



		self.chars=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']
		self.path = os.getcwd().replace('\\', '/')

		self.urlEnter = 'https://vtop.vitap.ac.in/vtop/'
		self.urlLogin = 'https://vtop.vitap.ac.in/vtop/processLogin'

		self.urlLogout = 'https://vtop.vitap.ac.in/vtop/processLogout'
		
		self.urlPersonalInfo = 'https://vtop.vitap.ac.in/vtop/studentsRecord/SearchRegnoStudent'
		
		# Digital Assignments
		self.urlAssignEnter= "https://vtop.vitap.ac.in/vtop/examinations/StudentDA"
		self.urlAssignSubSelect ="https://vtop.vitap.ac.in/vtop/examinations/doDigitalAssignment"
		self.urlDigitalAssign = 'https://vtop.vitap.ac.in/vtop/examinations/processDigitalAssignment'
		self.urlDigitalAssignSeperate = 'https://vtop.vitap.ac.in/vtop/examinations/doUploadSeparateDAssignment'

		# Attendance
		self.urlAttend = 'https://vtop.vitap.ac.in/vtop/processViewStudentAttendance'
		# Marks View
		self.urlMarkEnter ="https://vtop.vitap.ac.in/vtop/examinations/StudentMarkView"
		self.urlMarkView = "https://vtop.vitap.ac.in/vtop/examinations/doStudentMarkView"
		


		self.userid = userid
		self.password = password
		self.s = str()
		self.char=self.loadChars()
		self.headers={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
		self.semID = {'semesterSubId': 'AP2019201'}
		self.captcha = str()

		self.sessID  = None
		self.startTime = int()
		self.endTime= int()


		




	def _save_file(self , path , content, file):

		if(file=='img'):
			dirPath = self.path+'/'+path
			filePath= self.path +'/' +path+'/'+path+'.jpg'

			if not os.path.exists(dirPath):
				os.makedirs(dirPath)
			with open(filePath  , 'wb') as f:
				f.write(content)
				f.close()

		elif(file=='html'):
			dirPath = self.path+'/'+path
			filePath = self.path+'/'+path+'/'+path+'.html'

			if not os.path.exists(dirPath):
				os.makedirs(dirPath)

			with open(filePath  , 'wb') as f:
				f.write(content)
				f.close()

		else:
			return "Invalid File type"
		return None


	def loadChars(self):
		char ={}
		
		with open(self.path+'/assets/chars.pickle', 'rb') as f:
			kars = pickle.load(f)
			f.close()

		for each1 , each2 in zip(self.chars , kars):
			char[each1] = each2

		return char

	def _get_captcha(self , content):

		cap = self.path+'/captcha/'
		soup = BeautifulSoup(content , 'html.parser')
		for bs in soup.findAll('img' , {'alt':'vtopCaptcha'}):
			img = str(bs)
			img = img.split(', ')[1]
			img = img.split('"/>')[0]
			image = base64.b64decode(img)


		self._save_file('captcha' , image, file='img')


		return cap 



	def _get_num(self , img):

		scores=[]

		for each in self.chars:
			scores.append(cv2.matchTemplate(img, self.char[each] ,cv2.TM_CCOEFF_NORMED)[0][0])

		return self.chars[np.argmax(scores)]


	def _preprocess_capthca(self , img):
		

		_, image = cv2.threshold(img , 0 , 255 , cv2.THRESH_BINARY_INV)


		char1 = self._get_num(image[: , : 30])
		char2 = self._get_num(image[: , 30 : 60])
		char3 = self._get_num(image[: , 60:90])
		char4 = self._get_num(image[: , 90:120])
		char5 = self._get_num(image[: , 120:150])
		char6 = self._get_num(image[: , 150:180])

		return char1 , char2 , char3 , char4 , char5 , char6


	def _stringify(self , charList):

		capt = ''

		for each in charList:
			capt=capt+each 


		return capt



	def CaptchaSolve(self):
		
		"""

		Return:
			Get the captcha's alphabet

		"""
		captcha_r = self.s.get(self.urlEnter , headers = self.headers)
		cap = self._get_captcha(captcha_r.content)
		image = cv2.imread( cap+'captcha.jpg', 0)
		charsList = self._preprocess_capthca(image)

		return self._stringify(charsList)




	def _loginFetch(self):
		
		"""

		Return:
			Log in and establish a session

		"""
		
		if(self.sessID == None ):
			
			self.sessID = time.time()
		elif(self.endTime -  self.sessID<3):
			return "Error "
			

		 
		start_time = time.time()
		self.s = requests.Session()
		self.captcha = self.CaptchaSolve()
		self.login_data={'uname': self.userid, 'passwd': self.password , 'captchaCheck': self.captcha}


		try:

			login_r = self.s.post(self.urlLogin, data = self.login_data , headers = self.headers)

		except:

			return "Login in unsucessful !"

		self.LoginFlag = True
		self.LogoutFlag = False
		return True





		


	# Here Plug in  Digital Assignment

	def _check_each(self ,main ,  sub):
		MainHeader = {**main, **sub}

		
		r_each_topic =  self.s.post(self.urlDigitalAssignSeperate , data =MainHeader,  headers = self.headers)

		soupSubCheck = BeautifulSoup(r_each_topic.content , 'html.parser')

		dangerSoup = soupSubCheck .findAll(class_="danger")[1]
		resp = dangerSoup.find("span").text.strip()
		resp = resp.split()[0]

		return(resp)


		
		return None 

	def _get_each_sub_Assign(self ,sub_header ):
		if(sub_header["type"]=="ELA"):

		
		
			r_each =  self.s.post(self.urlDigitalAssign , data =sub_header,  headers = self.headers)
			self._save_file("save", r_each.content, "html")

			

			soupEachAssign = BeautifulSoup(r_each.content , 'html.parser')


			each_sub_assign=[]


			for i,each in enumerate(soupEachAssign.findAll(class_="danger")):
				for values in each.find_all("span",{"style":"color: green;"}):
					# For checking if we have updated the task yet
					if(values.text !="-" and values.text is not None and each.find("button")):
						each_attr={
						"mCode": str(),
						"maxMark":str(), 
						"dueDate":str(), 
						"code":str(), 
						"optionTitle":str(), 
						"weightageMark":str()	
						}
						# print( each.findAll("td", {"style":"vertical-align:middle;text-align:center;"})[1].text)
						# print( each.findAll("td", {"style":"vertical-align:middle;text-align:center;"})[2].text)
						# print('\n')

						mCode=each.find("td", {"style":"vertical-align:middle;text-align:center;"}).text
						maxMark = each.findAll("td", {"style":"vertical-align:middle;text-align:center;"})[1].text
						dueDate= values.text
						optionTitle= each.findAll("td")[1].text
						# weightageMark=
						# code =

						
						each_attr["mCode"] = "Experiment-"+str(mCode)
						each_attr["code"] = "Experiment-"+str(mCode)
						each_attr["maxMark"] = maxMark
						each_attr["weightageMark"] = maxMark
						each_attr["optionTitle"] = optionTitle
						each_attr["dueDate"] = dueDate

						each_sub_assign.append(each_attr)

			return each_sub_assign
		else:
			r_each =  self.s.post(self.urlDigitalAssign , data =sub_header,  headers = self.headers)
			self._save_file("save", r_each.content, "html")

			

			soupEachAssign = BeautifulSoup(r_each.content , 'html.parser')


			each_sub_assign=[]


			for i,each in enumerate(soupEachAssign.findAll(class_="danger")):
				for values in each.find_all("span",{"style":"color: green;"}):
					# For checking if we have updated the task yet
					if(values.text !="-" and values.text is not None and each.find("button")):
						each_attr={
						"mCode": str(),
						"maxMark":str(), 
						"dueDate":str(), 
						"code":str(), 
						"optionTitle":str(), 
						"weightageMark":str()	
						}
						# print( each.findAll("td", {"style":"vertical-align:middle;text-align:center;"})[1].text)
						# print( each.findAll("td", {"style":"vertical-align:middle;text-align:center;"})[2].text)
						# print('\n')

						mCode=each.find("td", {"style":"vertical-align:middle;text-align:center;"}).text
						maxMark = each.findAll("td", {"style":"vertical-align:middle;text-align:center;"})[1].text
						dueDate= values.text
						optionTitle= each.findAll("td")[1].text
						weightageMark=each.findAll("td", {"style":"vertical-align:middle;text-align:center;"})[2].text
						code = each.find("input").get("value")


						
						each_attr["mCode"] = "Experiment-"+str(mCode)
						each_attr["code"] = code
						each_attr["maxMark"] = maxMark
						each_attr["weightageMark"] = weightageMark
						each_attr["optionTitle"] = optionTitle
						each_attr["dueDate"] = dueDate

						each_sub_assign.append(each_attr)

			return each_sub_assign



	def _GetAssignmentList(self , data_r):


		

		soup = BeautifulSoup(data_r , 'html.parser')
		list_form_data=[]
	# This is for digital assignments
	

		for each in soup.find_all(class_='btn btn-primary'):
			post_attr={
			 	'classId': str(),
			'courseCode':str() ,
			'title': str(),
			'type':str() ,
			'option': str(),
			'slot':str() ,
			'fName': str()}

			cont = each['onclick']
			cont = cont.split('(')[1]
			cont = cont.split(')')[0]
			cont = cont.split(',')
			
			if( True):
				
				post_attr['classId'] = cont[0].replace("'",'')
				post_attr['courseCode'] = cont[1].replace("'",'')
				post_attr['title'] = cont[2].replace("'",'')
				post_attr['type'] = cont[3].replace("'",'')
				post_attr['option'] = cont[4].strip().replace("'",'')
				post_attr['slot'] = cont[5].replace("+", " ").replace("'", '')
				post_attr['fName'] = cont[6].replace("'",'')
				list_form_data.append(post_attr)

		#print(list_form_data)
		return(list_form_data)

		

	def Get_Assignment_Data(self, verbose=False):
		self._loginFetch()
		# Return the list of subjects assigemnts of which assigments are not submitted
		r= self.s.post(self.urlAssignEnter , headers=self.headers)
		r_list = self.s.post(self.urlAssignSubSelect , data =self.semID,  headers = self.headers)
		
		list_from_data = self._GetAssignmentList(r_list.content)
		self.AssignSubHeaders=list_from_data

		sub={}
		

		for each in list_from_data:

			for eachs in self._get_each_sub_Assign(each):
				sub[eachs["optionTitle"]]= {}
				sub[eachs["optionTitle"]][each["title"]]= {}
				sub[eachs["optionTitle"]][each["title"]]=  self._check_each(each, eachs)

		if(not verbose):
			self.s.get(self.urlLogout , headers = self.headers)
		return sub



	# Here Plug in Attendance
	def Get_Attendance_Data(self, verbose=False):
		self._loginFetch()
		r1 =self.s.post(self.urlAttend  , headers = self.headers)
		r4 = self.s.post(self.urlAttend, data = self.semID , headers = self.headers)

		soup = BeautifulSoup(r4.content , 'html.parser')

		post_attr = {

		"CourseId":str(), 
		"CourseName":str(), 
		"AttendClass":str(), 
		"TotalClass":str(), 
		"PercentAttend":str(), 
		"CourseType":str(), 
		"CourseSlot":str()
			
		}
		total=[]



		for each in soup.findAll('tr')[1:-1]:

			post_attr["CourseId"] = each.findAll("td")[1].text.strip()
			post_attr["CourseName"] = each.findAll("td")[2].text.strip()
			post_attr["AttendClass"] = each.findAll("td")[7].text.strip()

			post_attr["TotalClass"] = each.findAll("td")[8].text.strip()
			post_attr["PercentAttend"] = each.findAll("td")[9].text.strip()
			post_attr["CourseType"] = each.findAll("td")[3].text.strip()
			post_attr["CourseSlot"] = each.findAll("td")[4].text.strip()


			total.append(post_attr)
		if(not verbose):
			self.s.get(self.urlLogout , headers = self.headers)

		return total


	# Here plug in Internal Makrs View
	def Get_Internal_Marks_Data(self, verbose=False):
		self._loginFetch()
		r1 = self.s.post(self.urlMarkEnter,  headers = self.headers)
		r2 = self.s.post(self.urlMarkView,data = self.semID , headers = self.headers )

		markView={}

		soup = BeautifulSoup(r2.content , 'html.parser')

		for each in soup.findAll("tr",{"style":"background-color: #d2edf7;"} ):
			
			markView[each.findAll("td")[2].text]={}
			
		# print(markView)

		# for i,key in zip(range(3),markView.keys()):
		# 	print(markView[key])


		for each,key in zip(soup.findAll("table", {"class":"table table-striped table-bordered "}), markView.keys()):
			for e in each.findAll(class_="danger"):
				titleExperiment= e.findAll("output")[1].text
				markView[key][titleExperiment]={}
				markView[key][titleExperiment]["maxMarks"] =e.findAll("output")[2].text
				markView[key][titleExperiment]["Weightage"] =e.findAll("output")[3].text
				markView[key][titleExperiment]["status"] =e.findAll("output")[4].text
				markView[key][titleExperiment]["ScoredMarks"] =e.findAll("output")[5].text
				markView[key][titleExperiment]["WeightageMakrsScores"] = e.findAll("output")[6].text
		if(not verbose):
			self.s.get(self.urlLogout , headers = self.headers)
				
		return (markView)


	def Get_Profile_Data(self, verbose=False):
		self._loginFetch()

		"""

		Returns:
			Name, Data of birth, gender , email id


		"""
		r= self.s.post(self.urlPersonalInfo , headers= self.headers)

		# with open(self.path+'/PersonalInfo/PersonalInfo.html', 'rb') as f:
		# 	details_r = f.read()
		# 	f.close()

		
		soup = BeautifulSoup(r.content , 'html.parser')
		INFO = []

		for each in soup.findAll('td', {'style':'background-color: #f2dede;'}):
			INFO.append(each.text)
		
		if(not verbose):
			self.s.get(self.urlLogout , headers = self.headers)
		return {'Name':INFO[0],
				'DOB': INFO[1],
				'Gender': INFO[2],
				'Email': INFO[28] 

		}


	def Fetch_All_Data(self):
		self._loginFetch()
		all_data={}
		all_data["AssignmentData"] = self.Get_Assignment_Data(verbose=True)
		all_data["AttendanceData"] = self.Get_Attendance_Data(verbose=True)
		all_data["InternalMakrsData"] = self.Get_Internal_Marks_Data()

		return all_data



	def __repr__(self):

		if(self.login):
			return "Main Class:  Currently you are loggin in with user id {}".format(self.userid)
		else:
			return "Main Class: Currently you are not logged in, enter 'object().login()'' "


