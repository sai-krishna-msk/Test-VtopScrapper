---
layout: default
title: Home
nav_order: 1
description: "Vtop Scraper is an api"
permalink: /
---

# Contents

[Introduction](#intro)

[Usage](#usage)

[Features](#features)

[How to Use](#htc)

<a name="intro"></a>

## Introduction

VtopScrapper is an API to VIT-AP's Student portal which enables you to build applications using the data provided by the portal

This is a 3rd party API (unofficial) so the service does not have direct access to the database instead it's consists of scrapping scripts in the backend (making it a little slower )<a name="usage"></a>

## Usage

**Package** If the user intends to use it in a python application then he/she may directly install the package from Pypi(like most python packages)

    pip install vtopscrapper

**Web API** If an app you intend to build restricts you from using python (like android app in which case you most likely are to use JAVA) in that case you can make http requests to the API

**Note** : Project is expected to make progress towards providing the services on maximum possible languages in near future eliminating the need of using it over web (Instead just downloading the package) but for now it is only available in python.

<a name="features"></a>

## Features

First You will have to login with your credentials and then you will have access to following data

   **Get Attendance Data**
    You will get data regarding attendance course wise for both theory and labs as in total number of classes which happened till date, number of attended and the percentage of attendance

   **Get Digital Assignments Data** 
   You will have get data regarding any digital Assignment's which has to be submitted but not has been for both theory and lab again course wise

   **Get internal marks**
    view You will get data regarding all the internal marks updated on the portal till date courseware for both theory and lab

   **You can get all the data in one go.**

<a name="htc"></a>

## How to use

**Package**

__Getting Attendance Data__

```python
from  VtopScraperCache import *
obj = VtopScraper(RegisterartionID, <password>)
# Creates a Session
obj.loginFetch()
Attendance_data = obj.GetAttendance()
#Session ends here

# If you need to continue session then 
Attendance_data = obj.GetAttendance(True)
```

__Get Digital Assignments Data__

```python
from  VtopScraperCache import *
obj = VtopScraper(RegisterartionID, <password>)
# Creates a Session
obj.loginFetch()
Assignment_data = obj.Get_Assignment_Status()
#Session ends here

# If you need to continue session then 
Attendance_data = obj.Get_Assignment_Status(True)
```

__Get internal marks__

```python
from  VtopScraperCache import *
obj = VtopScraper(RegisterartionID, <password>)
# Creates a Session
obj.loginFetch()
InternalMarks_data = obj.InternalMarks()
#Session ends here

# If you need to continue session then 
Attendance_data = obj.InternalMarks(True)
```

__Getting All of them__
```python
from  VtopScraperCache import *

obj = VtopScraper(RegisterartionID, <password>)

all_data = obj.loginFetch(True)

```




**Web API**