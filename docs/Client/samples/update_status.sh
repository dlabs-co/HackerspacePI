echo "{
    \"trigger_person\": \"$1\",
    \"open\": $2,
    \"date\": \"$3\",
    \"expiration\": \"$4\",
    \"hs_id\": 1
}" | python ../HackerspaceAPIStatusClient.py "http://localhost:5000" "api/state" /dev/stdin "admin" "admin"  "post"

