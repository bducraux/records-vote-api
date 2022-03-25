#Proposed Problem

```
record1 = [{"annotator1": "voteA", "annotator2": "voteB"}], record1.created_time
record2 = [{"annotator3": "voteA", "annotator2": "voteC"}], record1.created_time

records ~5B
how many times "annotatorX" ends up with "voteY"
```

## Solution explanation 
I tried to find a way to solve this problem without having to go through all the records to find the sum of votes.

So I developed a solution where when we write to the records table it increments a counter to another table. If an item in records is deleted the counter for all votes found in that deleted item is decreased by 1.

#How to run the project

#####Clone the project 
```
git clone git@github.com:bducraux/records-vote-api.git
```

#####Create a virtual environment to isolate our package dependencies locally
```
cd records-vote-api
python3 -m venv .venv

source .venv/bin/activate
```

#####Install required packages
```
pip install -r requirements.txt 
```

#####Run migrations
```
python manage.py migrate
```

####Adding new records
Open the url:
http://127.0.0.1:8000/records/ on browser

some samples insertions are:
```
[{"annotator1": "voteA"}, {"annotator2": "voteB"}]

[{"annotator3": "voteA"}, {"annotator2": "voteC"}]

[{"annotator4": "voteC"}, {"annotator1": "voteA"}]

[{"annotator5": "voteA"}, {"annotator3": "voteC"}, {"annotator1": "voteA"}, {"annotator2": "voteB"}]

[{"annotator4": "voteA"}, {"annotator5": "voteA"}]

[{"annotator5": "voteC"}, {"annotator3": "voteB"}, {"annotator1": "voteA"}, {"annotator2": "voteB"}]

[{"annotator1": "voteC"}, {"annotator2": "voteB"}, {"annotator3": "voteA"}, {"annotator4": "voteB"}, {"annotator5": "voteB"}]
```

####Vote counting endpoint
list all vote counters:
http://127.0.0.1:8000/vote-counter/

get information of one specific annotador:
http://127.0.0.1:8000/vote-counter/?annotator=annotator2

get information of one specific annotador and vote:
http://127.0.0.1:8000/vote-counter/?annotator=annotator2&vote=voteB

get information of one specific vote:
http://127.0.0.1:8000/vote-counter/?vote=voteB

get total sum of a specific vote:
http://127.0.0.1:8000/vote-counter/?vote_sum=voteB