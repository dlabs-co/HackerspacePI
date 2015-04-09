HackerspacePI API
==================

The REST API is pretty much self-explaining, exposed api is as follows:
Base_url is /api/, restless makes it so that::
	/api/hackerspaces

will return a list of all hackerspaces, while::
	/api/hackerspaces/1

will return only the first hackerspace

User
----

This API endpoint is used to create new users for the space api.
A user MUST be authenticated to make creation requests to the hackerspace api.
To login, just enter /login page, default user and password is admin/admin
BE CAREFUL: Don't use important passwords here, it's stored as plaintext.

HackerSpace
-----------

This is the main API. Everyone can make get requests to it, only auth users 
may do POST and PATCH requests.

A post request must be in the following form:: 
	{ "space": "Dlabs Hackerspace",
	    "logo": "http://www.dlabs.co/logo.svg",
	    "url": "http://www.dlabs.co",
	    "csv_issue_report_channels": "email,twitter",
	    "location": 
		{
		"address": "camino la mosquetera 41",
		"lat": "2",
		"lon": "1"
		}
	    , 
	    "contact": 
		{
		    "twitter": "dlabs_co", 
		    "email": "socios@dlabs.co", 
		    "list": "socios@dlabs.co",
		    "irc": "irc.freenode.net#dlabs_co"
		}
	    ,
	    "state": 
		{
		    "trigger_person": "xayon", 
		    "open": true,
		    "date": "12-04-2015 20:30"
		}
	     
	}

With this, we'd create a hackerspace, the answer will include the hackerspace ID
Save that ID to use it later (tough it can be checked out by using /api/hackerspaces endpoint

State
-----

This is currently used to save the hackerspace state. Sensors should call to 
this endpoint (AUTHENTICATED!) following the format::
	{
	    "trigger_person": "xayon", 
	    "open": true,
	    "date": "12-04-2015 20:30"
	}
