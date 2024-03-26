# senior Project - ESS solar panel tracker

## description
* written in python
* end result was hosted on PythonAnywhere for client
* was completed with a Gant timeline and sprint schecule
* code reviews included in course
* client requirements gathered by students
* three person team
* cpnverted their old data from excel to a MySql database
  
The goal of this project was to make a inventory tracker for the equitable solar solutions.
We have a login to this part of their website so that only the people the want to be able to
alter the website/inventory can


### code explanations
routes:
-Home route: greats the user will be a place to put logo and other things for the client
-login: the login to create and read from database- Note that delete will get its own password protection
-update: a route to update the information on a solar panel with testing or other data
-delete: a place to delete a solar panel if it is no longer needed
-view: read the data from the database
-create: add a solar panel to the database

base.hmtl
-this is a base for the html pages that shows links depending on if the user is logged in. Only logged in
people can view the create, delete, update, view

.py
-does the website logic. handles rendering the html pages and connects to the database
