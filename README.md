StudyBuddy
StudyBuddy is a collaborative web application built with Flask to help students schedule study sessions, form study groups, share resources, and practice with quizzes based on chosen topics.

Project Overview
StudyBuddy allows users to:

Create and join study groups organized by course

Schedule collaborative study sessions (e.g., via Zoom)

Upload and share class notes, links, and other resources

Comment on shared resources and sessions

Take quizzes generated from a Trivia API to test knowledge

Features for Logged-In Users
Only authenticated users can:

Create study groups and schedule sessions

Upload or download study materials

Post comments on resources and sessions

Join and participate in study rooms

Take topic-based quizzes and receive instant feedback

Forms
Register Form
Fields: username, email, password

Login Form
Fields: email, password

Create Study Group Form
Fields: course name, description, tags

Session Scheduler Form
Fields: date/time, Zoom link, group name

Trivia Quiz Form
Fields: topic selection, number of questions

Routes and Blueprints
Auth Blueprint
/register – Register a new user

/login – User login

/logout – Log out

Study Blueprint
/create-group – Create a new study group

/group/<id> – View group details, post sessions/resources/comments

/schedule-session – Schedule a collaborative session

/upload-resource – Upload or link to study materials

/quiz – Choose a quiz topic and answer questions

MongoDB Collections
Using PyMongo to interact with the database:

users – Stores user credentials and profiles

groups – Stores study group metadata

sessions – Stores scheduled study sessions

resources – Stores uploaded files and links

comments – Stores comments on sessions and resources

quizzes – (Optional) Stores quiz attempts and user scores

Database Operations
Creating a group inserts into groups

Scheduling a session inserts into sessions

Viewing a group queries resources and sessions

Submitting quiz answers may log results (optional)

Flask-Mail Integration
Flask-Mail is used to send email notifications to group members when:

A new session is scheduled

A new resource is uploaded

Trivia API Integration
StudyBuddy integrates with a Trivia API to:

Fetch multiple-choice questions based on selected topics

Generate quizzes dynamically

Evaluate submitted answers and display results

This encourages active learning and collaboration within study groups.