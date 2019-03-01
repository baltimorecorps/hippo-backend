# Contacts REST API
1) Requirements

python 3.7

2) Clone the repo

3) Create virtual environment 

`python3 -m venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

4) Execute `python run.py` to interact with the API

## Test API

Open browser and go to URL: 
### ContactAll
GET 
`http://<IP>:5000/api/contacts`
POST 
PUT 
DELETE 

### ContactOne
GET 
`http://<IP>:5000/api/contacts/<int:contact_id>`
POST 
PUT 
DELETE 

