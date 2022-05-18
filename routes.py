from http import client
from shutil import ExecError
from sqlite3 import IntegrityError
from unicodedata import name
from flask import request, jsonify
from models import *
from main import app

#User types
#TODO (Temporary way of adding user types)
@app.route('/usertypes', methods=['GET'])
def usertypes():
    
    users = ['coach', 'client'] 
        
    user_exists = Usertype.query.all()
    
    for user in users:
        if not user_exists:
            user_type_add = Usertype(name=user)
            db.session.add(user_type_add)
            db.session.commit()
        else:
            for db_user in user_exists:
                if db_user.name not in users:
                    user_type_add = Usertype(name=user)
                    db.session.add(user_type_add)
                    db.session.commit()
            
    all_usertypes = Usertype.query.all()
    
    output = []
    
    for usertype in all_usertypes:
        usertype_data = {}
        usertype_data['id'] = usertype.id
        usertype_data['name'] = usertype.name
        output.append(usertype_data)
        
    return jsonify({'usertypes': output}), 200

#List all coaches
@app.route('/coaches', methods=['GET'])
def coaches():
    #TODO: Fix hardcoded value
    all_coaches = User.query.filter_by(usertype_id=1).all()
    
    output = []
    
    for coach in all_coaches:
        coach_data = {}
        coach_data['id'] = coach.id
        coach_data['name'] = coach.name
        coach_data['email'] = coach.email
        coach_data['session_duration'] = coach.session_duration
        output.append(coach_data)
        
    return jsonify({'coaches': output}), 200
              
#Users Crud operations --> get, add, update, delete
@app.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_cruds():
    if request.method == 'GET':
        data = request.get_json()
        
        user = User.query.filter_by(id=data['id'])#.first()
    
        output = []
        
        for item in user:
            user_data = {}
            user_data['id'] = item.id
            user_data['name'] = item.name
            user_data['email'] = item.email
            user_data['session_duration'] = item.session_duration
            user_data['usertype_id'] = item.usertype_id
            user_data['usertype'] = item.usertype.name
            output.append(user_data)
        
        return jsonify({'users': output}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        session_duration = data['session_duration'] if 'session_duration' in data else None
        
        add_user = User(name=data['name'], email=data['email'], session_duration=session_duration, usertype_id=data['usertype_id'])
        db.session.add(add_user)
        db.session.commit()
        
        return jsonify({'msg': 'User added successfully'}), 201
    
    elif request.method == 'POST':
        data = request.get_json()
        
        user = User.query.filter_by(id=data['id'])#.first()
        
        if data['email']:
            user.update({'email':data['email']})
            db.session.commit()
            return jsonify({'msg':'Email updated successfully'}), 200
        
        elif data['name']:
            user.update({'name':data['name']})
            db.session.commit()
            return jsonify({'msg':'Name updated successfully'}), 200
        
        else:
            return jsonify({'msg':'Wrong parameter'}), 401
        
    elif request.method == 'DELETE':
        data = request.get_json()
        
        User.query.filter_by(id=data['id']).delete()
        db.session.commit()
        
        return jsonify({'msg':'User deleted successfully'}), 200
    
    else:
        return jsonify({'msg':'Wrong method'}), 401
        
#List a specific coach’s working hours
@app.route('/coach_hours', methods=['POST'])
def coach_hours():
    data = request.get_json()
    hours = Appointment.query.filter_by(coach_id=data['coach_id']).all()
    
    output = []
    
    for hour in hours:
        hour_data = {}
        hour_data['id'] = hour.id
        hour_data['coach'] = hour.coach.name
        hour_data['client'] = hour.client.name
        hour_data['title'] = hour.title
        hour_data['start_time'] = hour.start_time
        hour_data['end_time'] = hour.end_time
        # hour_data['total_hours'] = pass
        
        output.append(hour_data)
        
    return jsonify({'coach_hours': output}), 200

#List all appointments
@app.route('/appointments', methods=['GET'])
def appointments():
    all_appointments = Appointment.query.all()
    
    output = []
    
    for appointment in all_appointments:
        appointment_data = {}
        appointment_data['id'] = appointment.id
        appointment_data['title'] = appointment.title
        appointment_data['coach_id'] = appointment.coach_id
        appointment_data['coach'] = appointment.coach.name
        appointment_data['client_id'] = appointment.client_id
        appointment_data['client'] = appointment.client.name
        appointment_data['start_time'] = appointment.start_time
        appointment_data['end_time'] = appointment.end_time
        appointment_data['is_active'] = appointment.is_active
        output.append(appointment_data)
        
    return jsonify({'appointments': output}), 200

#Make, cancel, edit, view appointment
@app.route('/appointment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def appointment_cruds():
    if request.method == 'GET':
        all_appointments = Appointment.query.all()
    
        output = []
        
        for appointment in all_appointments:
            appointment_data = {}
            appointment_data['id'] = appointment.id
            appointment_data['title'] = appointment.title
            appointment_data['coach_id'] = appointment.coach_id
            appointment_data['coach'] = appointment.coach.name
            appointment_data['client_id'] = appointment.client_id
            appointment_data['client'] = appointment.client.name
            appointment_data['start_time'] = appointment.start_time
            appointment_data['end_time'] = appointment.end_time
            appointment_data['is_active'] = appointment.is_active
            output.append(appointment_data)
            
        return jsonify({'appointments': output}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        #Convert string time to python datetime
        start_time = datetime.strptime(data['start_time'], '%d/%m/%y %H:%M')
        end_time = datetime.strptime(data['end_time'], '%d/%m/%y %H:%M')
        
        #Check if slot is available
        times = Appointment.query.filter_by(is_active=True).all()
        
        # Get session duration
        initial_duration = User.query.filter_by(id=data['coach_id']).first().session_duration
        
        for time in times:
            diff = end_time - start_time
            
            #difference in minutes
            diff = diff.total_seconds() / 60
            
            #duration in minutes
            duration = int(initial_duration) * 60
            
            #Cast to integer
            diff = int(diff)
            duration = int(duration)
            
            if diff != duration:
                return jsonify({'msg': f'Session duration should be {initial_duration} hours'}), 401
            
            if start_time >= time.start_time and end_time <= time.end_time:
                return jsonify({'msg': 'Appointment not successfully, that session is already booked'}), 401
            
        add_appointment = Appointment(title=data['title'], coach_id=data['coach_id'], client_id=data['client_id'], start_time=start_time, end_time=end_time, is_active=True)
        db.session.add(add_appointment)
        db.session.commit()
        
        return jsonify({'msg': 'Appointment added successfully'}), 201
    
    elif request.method == 'POST':
        data = request.get_json()
        
        appointment = Appointment.query.filter_by(id=data['id'])#.first()
        
        if data['title']:
            appointment.update({'title':data['title']})
            db.session.commit()
            return jsonify({'msg':'Title updated successfully'}), 200
        
        elif data['coach_id']:
            appointment.update({'coach_id':data['coach_id']})
            db.session.commit()
            return jsonify({'msg':'Coach updated successfully'}), 200
        
        elif data['client_id']:
            appointment.update({'client_id':data['client_id']})
            db.session.commit()
            return jsonify({'msg':'Client updated successfully'}), 200
        
        elif data['start_time']:
            appointment.update({'start_time':datetime.strptime(data['start_time'], '%d/%m/%y %H:%M')})
            db.session.commit()
            return jsonify({'msg':'Start time updated successfully'}), 200
        
        elif data['end_time']:
            appointment.update({'end_time':datetime.strptime(data['end_time'], '%d/%m/%y %H:%M')})
            db.session.commit()
            return jsonify({'msg':'End time updated successfully'}), 200
        
        else:
            return jsonify({'msg':'Wrong parameter'}), 401
        
    elif request.method == 'DELETE':
        #Soft Delete
        data = request.get_json()
        
        appointment = Appointment.query.filter_by(id=data['id']).update(dict(is_active=False))
        db.session.commit()
        
        return jsonify({'msg':'Appointment cancelled successfully'}), 200
    
    else:
        return jsonify({'msg':'Wrong method'}), 401
