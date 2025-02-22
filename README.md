# whsaa-birthday-list

this tool creates the json file needed to drive the birthday list function on this page:  
https://waggeneralumni.org  
  
### quick steps

- run this utility - it makes the birthday.json file
- delete the birthday.json file from wordpress site / media
- upload the new birthday.json file to the wordpress site manually
- modify the filename in the javascript on the home page to fetch that file (name has changed)*

#### *issue

- until i have to dig in to this, this step is required.
- it seems the json file is no longer retruned from the permalink, so must use the fiull file name (which changes every new upload)
- the permalink is the same for each successive upload
- there may be a plug-in conflict, don't have time to run that down right now
