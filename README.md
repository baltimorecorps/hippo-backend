
WORK
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
http://<IP>:5000/api/contacts
```


**View one contact**

URL

```
http://<IP>:5000/api/contacts/<int:contact_id>
```


**View Profile**

URL

```
http://<IP>:5000/api/contacts/<int:contact_id>/profile
```


**Add contact**

URL
```
http://<IP>:5000/api/contacts
```


**View all experiences**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/
```


**View one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/<int:experience_id>
```


**Add one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/
```


**Delete one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/<int:experience_id>
```



**Update one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/<int:experience_id>
```
