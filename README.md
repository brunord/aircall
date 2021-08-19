# aircall
Simple python ETL aggregating data from Facebook public repositories using GitHub API.
This project is part of an exercise.

to run:
```
$cd <project_root>
$source venv/bin/activate
$python etl.py 

-> http://127.0.0.1:5002/new_contributors to see the results
```
execution steps
-
- get all public repositories names from Facebook github account, using GitHub API
- get All commits from the repositories retrieved
- aggregates the data using spark, and write the output in a static resource file
- exposes a restful API to access the data

notes:
-
- The field used to identify a commit author as unique is "email", because others(login, name, etc) not seems to 
be accurate for any reason. All commits done via web has the same 'login' field value on retrieve API data. 
A better solution could be found.

improvements:
-
- The data retrieved via Commit github API could be stored in a stage directory partitioned by month. That way 
the execution can be done incrementaly fetching only recent missing data on each run. The ideal design is to think
the solution with a first step being a scheduled job retrieving API data in a monthly basis, and then triggering 
the transformation (spark) job to generate a new dataset. 
- Remove hardcoded values (access_token, number of retries, urls) and make everything passed as application arguments
- Improve unit tests. 