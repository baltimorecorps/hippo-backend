# How to run the frontend and backend simultaneously
## (1) backend
### Install Python 3.7
### Clone the repository non-hc-api, branch: non-hc-api-resumeBuilder_v1.2

Difference between branch 1.2 and branch 1.1 version
* added lines to solve the cross-origin problem 
* changed the endpoint of “add one experience” to use the url of api/contacts/:id/experiences instead of api/contacts/:id/experiences/:id

### Create virtual environment and activate it
 $mkdir ~/.virtualenvs
 $python3 -m venv ~/.virtualenvs/myvenv
 $source ~/.virtualenvs/myvenv/bin/activate
### Install required python packages
 $pip install -r requirements.txt 
### install flask_cors
 $ pip install -U flask-cors
### Run the API server
 python run.py

## (2) frontend 

### Open a different terminal window
### clone the branch wensi_resumeBuilder under baltimorecorps/webapp
### cd to webapp-master folder
### start the frontend react app:
$npm start
the website page should automatically display on your default browser with the url to be http://localhost:3000

### On the homepage’s nav bar, click “TalentProfile”.
1Test add experience: 
click the plus icon on the right
fill the form 
click submit
2 Test edit experience:
Click the edit icon
Fill out the form
Click submit
3 Test delete experience:
Click the delete icon

# Issues for future discussion:
## When one edits the first item of experience, that new edited item will appear at the end of the experience column, rather than staying on its original location. My guess is that the current PUT experience method may change how the GET experience function returns the experience items. My suggestion for backend design is to fixed the order by which the GET experience function returns all experiences. If the results are ordered by experience_id, then when we call the put method to revise an experience item, it should stay in its original location.
## Currently the database design is only having “experience” which consumes education/workExperience/skills. However, in the frontend, we may want to display these different types of experiences separately in different columns; so we may need GET/PUT/POST/DELETE for each type of experience. For example, we need GET Education endpoint to get all education experiences and use this data to display in the webpage’s “Education” Column. 





``
