# Tripleadapt Backend


### General Setup
Run flash run from Backend/Server to ...

Change python run configurations to routes.py

To execute another example change the function Call in test() to the function you would like to execute
All Tests are located in Tests/recommendation_test.py

## Overview of packages 

### 1. GlobalController
1. Library: Look up class representing the relationships between tasks and activities 
2. Task: static, only read from the database
3. TaskState: dynamically changed during each iteration of the process



## Connection to mongodb Database 
The currently used User is named Ingo and his entry can also be found in the mongodb database. 
To recent his current scores, delete his entry in the database under tripleadapt/user
Otherwise his task scores are updated each round by +20 and safed in the db





