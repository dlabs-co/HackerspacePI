echo '{ "space": "Dlabs Hackerspace",
    "logo": "http://dlabs.co/logo.svg",
    "url": "http://dlabs.co",
    "issue_report_channels": "twotter",
    "location": [
        {
        "address": "camino la mosquetera 41",
        "lat": "foo",
        "lon": "bar"
        }
    ], 
    "contact": [
        {
            "twitter": "dlabs_co", 
            "email": "socios@dlabs.co", 
            "ml": "socios@dlabs.co",
            "irc": "irc.freenode.net#dlabs_co"
        }
    ],
    "state": [
        {
            "trigger_person": "xayon", 
            "status": "open", 
            "date": "foo"
        }
    ] 
}'  | python HackerspaceAPIStatusClient.py "http://localhost:5000" "api/hackerspace" /dev/stdin "admin" "admin"  "post"

