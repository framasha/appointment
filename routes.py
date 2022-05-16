from flask import request, jsonify
from models import *
from main import app

#List all coaches
@app.route('/coaches', methods=['GET'])
def coaches():
    all_coaches = Coach.query.all()
    
    output = []
    
    for coach in all_coaches:
        coach_data = {}
        coach_data['id'] = coach.id
        coach_data['name'] = coach.name
        coach_data['email'] = coach.email
        coach_data['session_duration'] = coach.session_duration
        coach_data['working_start_time'] = coach.working_start_time
        coach_data['working_end_time'] = coach.working_end_time
        output.append(coach_data)
        
    return jsonify({'coaches': output}), 200
              
#Coach Crud operations --> get, add, update, delete
@app.route('/coach', methods=['GET', 'POST', 'PUT', 'DELETE'])
def coach_cruds():
    if request.method == 'GET':
        data = request.get_json()
        
        coach = Coach.query.filter_by(id=data['id'])#.first()
    
        output = []
        
        for item in coach:
            coach_data = {}
            coach_data['id'] = coach.id
            coach_data['name'] = coach.name
            coach_data['email'] = coach.email
            coach_data['session_duration'] = coach.session_duration
            coach_data['working_start_time'] = coach.working_start_time
            coach_data['working_end_time'] = coach.working_end_time
            output.append(coach_data)
        
        return jsonify({'coaches': output}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        add_coach = Coach(name=data['name'], email=data['email'], working_start_time=data['working_start_time'], working_end_time=data['working_end_time'])
        db.session.add(add_coach)
        db.session.commit()
        
        return jsonify({'msg': 'Coach added successfully'}), 201
    
    elif request.method == 'POST':
        data = request.get_json()
        
        coach = Coach.query.filter_by(id=data['id']).first()
        
        if data['email']:
            coach['email'] = data['email']
            db.session.commit()
            return jsonify({'msg':'Email updated successfully'}), 200
        
        elif data['name']:
            coach['name'] = data['name']
            db.session.commit()
            return jsonify({'msg':'Name updated successfully'}), 200
        
        else:
            return jsonify({'msg':'Wrong parameter'}), 401
        
    elif request.method == 'DELETE':
        data = request.get_json()
        
        Coach.query.filter_by(id=data['id']).delete()
        db.session.commit()
        
        return jsonify({'msg':'Coach deleted successfully'}), 200
    
    else:
        return jsonify({'msg':'Wrong method'}), 401
        
#List a specific coach’s working hours
@app.route('/coach_hours', methods=['POST'])
def coach_hours():
    data = request.get_json()
    hours = Coach.query.filter_by(id=data['id']).all()
    
    output = []
    
    for hour in hours:
        hour_data = {}
        hour_data['id'] = hour.id
        hour_data['name'] = hour.name
        hour_data['working_start_time'] = hour.working_start_time
        hour_data['working_end_time'] = hour.working_end_time
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
        appointment_data['coach'] = appointment.coach
        appointment_data['start_time'] = appointment.start_time
        appointment_data['end_time'] = appointment.end_time
        output.append(appointment_data)
        
    return jsonify({'appointments': output}), 200

#Make, cancel, edit, view appointment
@app.route('/appointment', methods=['GET', 'POST', 'PUT'])
def appointment_cruds():
    if request.method == 'GET':
        all_appointments = Appointment.query.all()
    
        output = []
        
        for appointment in all_appointments:
            appointment_data = {}
            appointment_data['id'] = appointment.id
            appointment_data['title'] = appointment.title
            appointment_data['coach_id'] = appointment.coach_id
            appointment_data['coach'] = appointment.coach
            appointment_data['start_time'] = appointment.start_time
            appointment_data['end_time'] = appointment.end_time
            output.append(appointment_data)
            
        return jsonify({'appointments': output}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        add_appointment = Appointment(title=data['title'], coach_id=data['coach_id'], start_time=data['start_time'], end_time=data['end_time']).first()
        db.session.add(add_appointment)
        db.session.commit()
        
        return jsonify({'msg': 'Appointment added successfully'}), 201
    
    elif request.method == 'POST':
        data = request.get_json()
        
        appointment = Appointment.query.filter_by(id=data['id']).first()
        
        if data['title']:
            appointment['title'] = data['title']
            db.session.commit()
            return jsonify({'msg':'Title updated successfully'}), 200
        
        elif data['coach_id']:
            appointment['coach_id'] = data['coach_id']
            db.session.commit()
            return jsonify({'msg':'Coach updated successfully'}), 200
        
        elif data['start_time']:
            appointment['start_time'] = data['start_time']
            db.session.commit()
            return jsonify({'msg':'Start time updated successfully'}), 200
        
        elif data['end_time']:
            appointment['end_time'] = data['end_time']
            db.session.commit()
            return jsonify({'msg':'End time updated successfully'}), 200
        
        else:
            return jsonify({'msg':'Wrong parameter'}), 401
        
    elif request.method == 'DELETE':
        data = request.get_json()
        
        appointment = Appointment.query.filter_by(id=data['id']).update(dict(is_active=False))
        db.session.commit()
        
        return jsonify({'msg':'Appointment cancelled successfully'}), 200
    
    else:
        return jsonify({'msg':'Wrong method'}), 401
