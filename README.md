# aircall
Simple python ETL aggregating data from Facebook public repositories using GitHub API

to run:
$cd <project_root>
$source venv/bin/activate
$python etl.py 
hit http://127.0.0.1:5002/new_contributors to see the results

execution steps:
- get all public repositories names from Facebook github account, using GitHub API
- get All commits from the repositories retrieved
- aggregates the data using spark, and write the output in a static resource file
- exposes a restful API to access the data
