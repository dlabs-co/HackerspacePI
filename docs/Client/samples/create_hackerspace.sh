echo '{ 
    "space": "Dlabs Hackerspace",
    "logo": "http://www.dlabs.co/logo.svg",
    "url": "http://www.dlabs.co",
    "csv_issue_report_channels": "email,twitter",
    "location": 
        {
		"address": "camino la mosquetera 41",
		"lat" : "41.651078",
		"lon" : "0.898883"
        }
    , 
    "contact": 
        {
            "twitter": "dlabs_co", 
            "email": "socios@dlabs.co", 
            "list": "socios@dlabs.co",
            "irc": "irc.freenode.net#dlabs_co"
        }
}' | python HackerspaceAPIStatusClient.py "http://localhost:5000" "api/hackerspace" /dev/stdin "admin" "admin"  "post"

