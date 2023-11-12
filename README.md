# int_2_test_task

## Project files purpose

### config.py
Contains important consts responsible for  PostgreSQL database connection.

### db_connector.py
Connects to the database using credentials provided in config.py and writes parsed data
### scanner.py
Connects to remote host via SSH (take a note that it uses password login, not SSH keys) and parses OS version and name, kernel and architecture.
### main.py
Responsible for creating web endpoints used for displaying HTML pages for more convenient data entry  

##Prerequisites
You need to create environment variables: DB_HOST, DB_USER, DB_PORT, DB_PASS, DB_NAME
Secondly you'll need to install all dependencies listed in requiremets.txt
'''
pip install -r requirements.txt
'''

##How to run app
Simply type
'''
uvicorn main:app --reload
'''
And go to localhst webpage in your browser
'''
http://127.0.0.1:8000/
'''
