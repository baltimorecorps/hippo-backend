# Resumer Builder API
## Run on local server

### Getting Started:
- Install Python 3.7

- Clone the repository

- Create virtual environment and activate it

`python3 -m venv`

`source venv/bin/activate`

- Install required python packages

`pip install -r requirements.txt`

- Run the API server 

`python run.py` 

### Using the API

**View all contacts**

URL

```
curl --request GET http://<IP>:5000/api/contacts 
```

Sample call
```
curl --request GET http://127.0.0.1:5000/api/contacts 
```

Output
```
[
    {
        "id": "6",
        "first_name": "Benson",
        "last_name": "Alexander",
        "email": "bensonalexander@zounds.com"
    }
]
```

**View one contact**

URL

```
http://<IP>:5000/api/contacts/<int:contact_id>
```

Sample call
```
curl --request GET http://127.0.0.1:5000/api/contacts/1 
```

Output

```
{
    "status": "success",
    "data": {
        "id": 1,
        "first_name": "Benson",
        "last_name": "Alexander",
        "email": "bensonalexander@zounds.com",
        "phone_primary": "401-111-2222",
        "profile_id": 111,
        "gender": "Male",
        "race_all": "Asian",
        "birthdate": "1990-01-02"
    }
}
```
