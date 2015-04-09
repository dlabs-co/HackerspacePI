echo '{ "space": "Dlabs Hackerspace",
    "logo": "http://www.dlabs.co/logo.svg",
    "url": "http://www.dlabs.co",
    "csv_issue_report_channels": "email,twitter",
    "location": 
        {
        "address": "camino la mosquetera 41",
        "lat": "foo",
        "lon": "bar"
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
            "date": "foo"
        }
     
}'  | python HackerspaceAPIStatusClient.py "http://localhost:5000" "api/hackerspace" /dev/stdin "admin" "admin"  "post"

