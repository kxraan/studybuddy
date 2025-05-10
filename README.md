StudyBuddy

StudyBuddy is a collaborative web app built with Flask designed to help students schedule study sessions, form study groups, and share class-specific resources.

Project Overview

StudyBuddy helps users:

* Create and join study groups organized by course
* Schedule collaborative study sessions (e.g., via Zoom)
* Upload and share class notes, links, and other resources
* Comment on shared resources and sessions

---

Features for Logged-In Users

Only authenticated users can:

* Create study groups and schedule sessions
* Upload or download study materials
* Post comments on resources and sessions
* Join and participate in study rooms

---

## 📝 Forms

1. Register Form
   Fields: username, email, password

2. Login Form
   Fields: email, password

3. Create Study Group Form
   Fields: course name, description, tags

4. Session Scheduler Form
   Fields: date/time, Zoom link, group name

---

Routes and Blueprints

auth Blueprint

* /register – Register a new user
* /login – User login
* /logout – Log out

study Blueprint

* /create-group – Create a new study group
* /group/<id> – View group details, post sessions/resources/comments
* /schedule-session – Schedule a collaborative session
* /upload-resource – Upload or link to study materials

---

MongoDB Collections

Using PyMongo to interact with the database:

* users – Stores user credentials and profiles
* groups – Stores study group metadata
* sessions – Stores scheduled study sessions
* resources – Stores uploaded files and links
* comments – Stores comments on sessions and resources

Database Operations

* Creating a group inserts into groups
* Scheduling a session inserts into sessions
* Viewing a group queries resources and sessions

---

Flask-Mail Integration

Flask-Mail is used to enhance collaboration and engagement:

Sends email notifications to group members when:

* A new session is scheduled
* A new resource is uploaded