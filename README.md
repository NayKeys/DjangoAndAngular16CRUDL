# A simple and generic Django and sveltejs Table CRUD app

This project is design to work with as many as different data sources type you want.

You fetch your data, transforms it into a python object (I'm using petl as an example) give it to me, I send it back to the front-end.
A config file allows you to configure which user has READ/WRITE/UPDATE/DELETE access to your different type of data.

In this project users are authentified using my school's CAS url as an example.

# How to use it ?

## Step 1
Edit the config.py file /datahub/ and specify your views (your tables). Each view should refer to a single data source, meaning each view is a single table. Generic table which columns may be from different data sources are not supported yet. Be sure to specify the method and the url with passwords and everything for each view like shown in the example.

## Step 2 Permissions and roles
Still in the /datahub/config.py file you can specify in your views persmissions for each custom roles.

## Step 3 Roles users
Edit the config.py in /users/ to specify which users has which roles
### Feel free to instead edit /users/authentification.py to allow role creation and handling with cas auth (natively supported by the project). 


## Go further
To this day only SQL is natively supported by this project, however the is scalable and any data source that looks pretty much like a table is supported by this project.

# How to add support for a new datasource ?
## Step 1
/datahub/pipelines/ is the directoy including every data sources pipelines supported to this day. If your needs aren't met feel free to add your own {data_source_type}_pipeline.py file to this directory.

## Step2
Edit /datahub/pipelines/hub.py functions to include your new pipeline. Make sure that your pipeline returns a python dict in case of fetching and a boolean for action performing requests.