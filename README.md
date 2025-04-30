# studybuddy
Collaborative Flask app for scheduling, studying, and sharing resources.


Q1 Description of your final project idea:
80 Points
Grading comment:
StudyBuddy - A collaborative study planner and resource sharing app that helps students form study groups, create shared schedules, and exchange class-specific resources. Users can sign up, create study rooms for specific courses, schedule collaborative sessions, upload/share notes or links, and comment on resources.
Q2 Describe what functionality will only be available to logged-in users:
4 Points
Grading comment:
Only logged-in users can create study rooms, upload or download notes/resources, comment on sessions/resources and join study groups
Q3 List and describe at least 4 forms:
4 Points
Grading comment:
Register Form – username, email, password
Login Form – email, password 
Create Study Group Form – course name, description, tags 
Session Scheduler Form – date/time, Zoom link, group name
Q4 List and describe your routes/blueprints (don’t need to list all routes/blueprints you may have–just enough for the requirement):
4 Points
Grading comment:
auth Blueprint:
- /register – user registration  
- /login – user login  
- /logout – user logout

study Blueprint:
- /create-group – create a new study group  
- /group/<id> – view group, post sessions/resources/comments  
- /schedule-session – schedule collaborative study session  
- /upload-resource – upload or link study material
Q5 Describe what will be stored/retrieved from MongoDB:
4 Points
Grading comment:
Collections:
- users – user profiles and credentials  
- groups – course-specific study groups  
- sessions – scheduled group study sessions  
- resources – uploaded files/links  
- comments – threaded or flat comments on resources

We’ll use PyMongo to interact with the DB:
- When a group is created, we insert into groups.
- When a session is created, we insert into sessions.
- When viewing a group, we query resources and sessions.
Q6 Describe what Python package or API you will use and how it will affect the user experience:
4 Points
Grading comment:
Flask-Mail
- Sends email confirmations to group members when:
  - A new session is created
  - A new resource is added
