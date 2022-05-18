# Appointment
API to review and schedule appointments with different coaches.

# Description

You’re tasked with creating an API to review and schedule appointments with different coaches.

- In order to schedule an appointment, a Coach must have an available slot.
- Coaches have working hours, names and session durations.
- Appointments can be scheduled with a Coach and a specific timeslot.
- A coach can only schedule an appointment with one person at a time.

# API Documentation

1. Api for getting user types

    There are two main users in the documentation (coach and client)

    Request:

        GET - http://localhost:5000/usertypes


    Response:

        {
            "usertypes": [
                {
                    "id": 1,
                    "name": "coach"
                },
                {
                    "id": 2,
                    "name": "client"
                }
            ]
        }

2. List all coaches

    Request:

        GET - http://localhost:5000/coaches

    Response: 

        {
            "coaches": [
                {
                    "email": "email@gmail.com",
                    "id": 1,
                    "name": "User Name",
                    "session_duration": "2"
                }
            ]
        }

3. Add user

    Request:

        PUT - http://localhost:5000/user

        {
            "name":"User Name",
            "email":"email@gmail.com",
            "session_duration":"2",
            "usertype_id":"1"
        }

    Response: 

        {
            "msg": "User added successfully"
        }

4. List a specific coach’s working hours

    Request:

        GET - http://127.0.0.1:5000/appointment

        {
            "coach_id":1
        }

    Response:
        
        {
            "coach_hours": [
                {
                    "client": "Coach Name",
                    "coach": "Client Name",
                    "end_time": "Tue, 17 May 2022 07:00:00 GMT",
                    "id": 1,
                    "start_time": "Tue, 17 May 2022 05:00:00 GMT",
                    "title": "Therapy"
                }
            ]
        }

5. Make appointment 

    Request:

        PUT - http://127.0.0.1:5000/appointment

        {
            "title":"Therapy",
            "start_time":"17/05/22 8:00",
            "end_time":"17/05/22 10:00",
            "coach_id":"1",
            "client_id":"2"
        }

    Response:

        {
            "msg": "Appointment added successfully"
        }        

7. Cancel appointment

    Request:

        DELETE - http://127.0.0.1:5000/appointment

        {
            "id":1
        }

    Response:

        {
            "msg": "Appointment cancelled successfully"
        }

8. Edit appointment

    Request:

        POST - http://127.0.0.1:5000/appointment

        {
            "id":1,
            "title":"Advice"
        }

    Response:

        {
            "msg": "Title updated successfully"
        }

    
9. View appointment

    Request:

        GET - http://127.0.0.1:5000/appointment

        {
            "id":1
        }

    Response:

        {
            "appointments": [
                {
                    "client": "User Name",
                    "client_id": 2,
                    "coach": "User Name",
                    "coach_id": 1,
                    "end_time": "Tue, 17 May 2022 07:00:00 GMT",
                    "id": 1,
                    "is_active": true,
                    "start_time": "Tue, 17 May 2022 05:00:00 GMT",
                    "title": "Advice"
                }
            ]
        }

# NOTE

## Features to upgrade

- Authentication - to secure each user (coach/client) data
- Authorization - to avoid insecure direct object reference vulnerability
- Pytest - for automated unit test
- Flask migrate - for database migrations
