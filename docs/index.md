# Contents

### [Introduction](#intro)

### [Usage](#usage)

### [Features](#features)

### [How to Use](#htc)

### [Response](#resp)
<br>

<a name="intro"></a>

## Introduction

#### VtopScrapper is an API to VIT-AP's Student portal which enables you to build applications using the data provided by the portal

#### This is a 3rd party API (unofficial) so the service does not have direct access to the database instead it's consists of scrapping scripts in the backend (making it a little slower )<a name="usage"></a>
<br>

<a name="usage"></a>
## Usage

#### **Package** 

If the user intends to use it in a python application then he/she may directly install the package from Pypi(like most python packages)

```
pip install vtopscrapper
```

#### **Web API** 

If an app you intend to build restricts you from using python (like android app in which case you most likely are to use JAVA) in that case you can make http requests to the API

#### **Note** 

Project is expected to make progress towards providing the services on maximum possible languages in near future eliminating the need of using it over web (Instead just downloading the package) but for now it is only available in python.


<br>

<a name="features"></a>

## Features

First You will have to login with your credentials and then you will have access to following data

   #### **Fetch Attendance Data**

  	You will get data regarding attendance course wise for both theory and labs as in total number of classes which happened till date, number of attended and the percentage of attendance

   #### **Fetch Digital Assignments Data** 

   You will have get data regarding any digital Assignment's which has to be submitted but not has been for both theory and lab again course wise

   #### **Fetch internal marks**

   View You will get data regarding all the internal marks updated on the portal till date courseware for both theory and lab

#### **Fetch Profile Information**

​	Get Profile Information registered in the Portal 


#### **Fetch all the data in one go**

<br>

<a name="htc"></a>

## How to use

### **Package**



> #### Fetch Attendance Data

```python
from  VtopScraperCache import *

obj = VtopScraper(RegisterartionID, <password>)

Attendance_data = obj.Get_Attendance_Data()
```



> #### Fetch Digital Assignments Data

```python
from  VtopScraperCache import *

obj = VtopScraper(RegisterartionID, <password>)

Assignment_data     = obj.Get_Assignment_Data()
```



> #### Fetch internal marks

```python
from  VtopScraperCache import *

obj = VtopScraper(RegisterartionID, <password>)

Internal_data = obj.Get_Internal_Marks_Data()
```



> #### Fetch Profile Information

```python
from  VtopScraperCache import *

obj = VtopScraper(RegisterartionID, <password>)

Internal_data = obj.Get_Profile_Data()
```



> #### Fetch All of them

```python
from  VtopScraperCache import *

obj = VtopScraper(RegisterartionID, <password>)

all_data = obj.Fetch_All_Data()

```

**Web API**

<br>


<a name="resp"></a>

## Response

> #### Fetch Attendance Data

```json
[
"CourseID":
"CourseName":
"AttendClass":
"TotalClass":
"PercentAttend":
]
```



> #### Fetch Digital Assignments Data

```json
{"Name_of_Assignment":
 {"Name_of_course":
  "status":
 }
}
```

*Status here indicated whether you have submitted or not*



> #### Get internal marks

```json
{"Name_of_Course":
	{
	  "Name_of_the_Assignment":{
				     "maxMarks":
				      "Weightage":
				      "status":
				      "ScoresMarks":
				      "WeightageMarksScores":
				    }
	}
}
```

*Here status indicates whether you were marked present or absent on the day assignment was assigned*



> #### Fetch Profile Information

```json
{
    "Name":
    "DOB":
    "Gender":
    "Email"
}
```



> #### Fetch All of them

```json
{
"AssignmentData":{},
"AttendanceData":{}, 
"InternalMakrsData":{}
}
```

