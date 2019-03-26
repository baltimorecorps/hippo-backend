 #How to run the frontend and backend simultaneously
 ##(1) backend
### Install Python 3.7
###Clone the repository non-hc-api, branch resumeBuilder_v1.2
o Difference between 1.2 and 1.1 version
* added lines to solve the cross-origin problem 
* changed the endpoint of “add one experience” to use the url of api/contacts/:id/experiences instead of api/contacts/:id/experiences/:id

###Create virtual environment and activate it
o $mkdir ~/.virtualenvs
o $python3 -m venv ~/.virtualenvs/myvenv
o $source ~/.virtualenvs/myvenv/bin/activate
###Install required python packages
o pip install -r requirements.txt 
### install flask_cors
o $ pip install -U flask-cors
### Run the API server
o python run.py

##(2) frontend 
###Open a different terminal window:
$npm start
the website page should automatically display on your default browser with the url to be http://localhost:3000

###On the homepage’s nav bar, click “TalentProfile”.
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

##Issues for future discussion:
1 When one edits the first item of experience, that new edited item will appear at the end of the experience column, rather than staying on its original location. My guess is that the current PUT experience method may change how the GET experience function returns the experience items. My suggestion for backend design is to fixed the order by which the GET experience function returns all experiences. If the results are ordered by experience_id, then when we call the put method to revise an experience item, it should stay in its original location.
2 Currently the database design is only having “experience” which consumes education/workExperience/skills. However, in the frontend, we may want to display these different types of experiences separately in different columns; so we may need GET/PUT/POST/DELETE for each type of experience. For example, we need GET Education endpoint to get all education experiences and use this data to display in the webpage’s “Education” Column. 





``
