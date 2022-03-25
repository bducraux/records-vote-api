## Proposed Problem

```
record1 = [{"annotator1": "voteA", "annotator2": "voteB"}], record1.created_time
record2 = [{"annotator3": "voteA", "annotator2": "voteC"}], record1.created_time

records ~5B
how many times "annotatorX" ends up with "voteY"
```

## Solution explanation 
I tried to find a way to solve this problem without having to go through all the records to find the sum of votes.

So I developed a solution where when we write to the records table it increments a counter to another table. If an item in records is deleted the counter for all votes found in that deleted item is decreased by 1.

## How to run the project

##### Clone the project 
```
git clone 
```

#####Create a virtual environment to isolate our package dependencies locally
```
python3 -m venv env
```