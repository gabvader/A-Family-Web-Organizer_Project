from flask import render_template, flash, redirect, url_for, abort, request, jsonify
from datetime import datetime
from app import app, db
from app.models import User, Event, EventType
from flask_login import current_user, login_required
from app.forms import EventForm, EditEventForm

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    
    form.participants.choices = [(u.id, u.username) for u in current_user.family.users]
    # EventType.query.all(): queries the database to fetch all the records from the EventType table.
    # et is a temporary variable that takes the value of each EventType instance returned by EventType.query.all()
    # populates the event_type field of the form with the existing event types from your EventType model as well as an additional option, 'New Event Type', with an identifier of -1. By using a negative value, it ensures that it doesn't conflict with any existing ids in the EventType table.
    form.event_type.choices = [(et.id, et.name) for et in EventType.query.all()] + [(-1, 'New Event Type')]
    
    if form.validate_on_submit():
        if form.event_type.data == -1:
            new_event_type = EventType(name=form.new_event_type.data)
            db.session.add(new_event_type)
            db.session.commit()
            event_type_id = new_event_type.id
        else:
            event_type_id = form.event_type.data
        
        event = Event(
            title=form.title.data, 
            description=form.description.data, 
            start_date= form.start_date.data,
            start_time=form.start_time.data,
            end_date=form.end_date.data if form.end_date.data else form.start_date.data,
            end_time=form.end_time.data, 
            creator_id=current_user.id, 
            family_id=current_user.family_id, 
            type_id=event_type_id
        )
        db.session.add(event)
        db.session.commit()
        
        if not form.participants.data:  # If no participants are selected
            participants = current_user.family.users  # Get all users from the family
        else:
            participants = [User.query.get(participant_id) for participant_id in form.participants.data]
            event.whole_family = False
        for participant in participants:
            event.participants.append(participant)
        
        db.session.commit()
    
        return redirect(url_for('index'))

    selected_date = request.args.get('selected_date')
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        print(selected_date)
        
    return render_template('create_event.html', title='Create Event', form=form, selected_date=selected_date)


@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    # If the event is not found, it raises 404 error 'not found' in case the user tries to delete something that does not exist
    event = Event.query.get_or_404(event_id)
    # If the current user is not the creator, it is forbidden (403) to delete it
    if event.creator_id != current_user.id:
        response = {
            'success': False,
            'message': 'You are not authorized to delete this event'
        }
        return jsonify(response), 403
    
    db.session.delete(event)
    db.session.commit()
    
    response = {
        'success': True,
        'message': 'Event has been deleted!'
    }
    return jsonify(response), 200



@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator_id != current_user.id:
        abort(403)
        
    form = EditEventForm()
    form.participants.choices = [(u.id, u.username) for u in current_user.family.users]
    form.event_type.choices = [(et.id, et.name) for et in EventType.query.all()] + [(-1, 'New Event Type')]
    
    if form.validate_on_submit():

        fields_to_update = ['title', 'description', 'start_date', 'start_time', 'end_time']

        for field in fields_to_update:
            form_data = getattr(form, field).data
            if form_data:
                setattr(event, field, form_data)
        
        if form.event_type.data:      
            if form.event_type.data == -1:
                new_event_type = EventType(name=form.new_event_type.data)
                db.session.add(new_event_type)
                db.session.commit()
                event_type_id = new_event_type.id
            else:
                event_type_id = form.event_type.data
            event.type_id = event_type_id

        if form.end_date.data:
            event.end_date = form.end_date.data
        else:
            event.end_date = event.start_date
        
        if not form.participants.data:
            participants = current_user.family.users
        else:
            participants = [User.query.get(participant_id) for participant_id in form.participants.data]
            event.whole_family = False
        event.participants = participants
        
        db.session.commit()
        
        
        return redirect(url_for('index'))
    
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.start_date.data = event.start_date
        form.start_time.data = event.start_time
        form.end_date.data = event.end_date
        form.end_time.data = event.end_time
        form.participants.data = [participant.id for participant in event.participants]
        form.event_type.data = event.type_id

    return render_template('edit_event.html', title='Edit Event', form=form)



@app.route('/get_events_for_day', methods=['GET'])
@login_required
def get_events_for_day():
    date_str = request.args.get('user_id')
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    events = current_user.get_events_for_day(date)
    events_data = [
        {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start_date': event.start_date.strftime('%Y-%m-%d'),
            'start_time': event.start_time.strftime('%H:%M') if event.start_time else None,
            'end_date': event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
            'end_time': event.end_time.strftime('%H:%M') if event.end_time else None,
            'type': event.event_type.name,
            'creator': event.creator.alias if event.creator.alias else event.creator.username,
            'participants': [
                participant.alias if participant.alias else participant.username
                for participant in event.participants
            ],
        } for event in events
    ]

    return jsonify(events_data)


@app.route('/get_events_for_day_user', methods=['GET'])
@login_required
def get_events_for_day_user():
    print('get_events_for_week_user called')
    date_str = request.args.get('date')
    user_id = request.args.get('user_id')
    
    print('date_str:', date_str)
    
    print('user_id:', user_id)
    

    if not date_str:
        return jsonify({'error': 'Date is required'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    
    user = User.query.get(user_id)
    if user not in current_user.family.users:
        return jsonify({'error': 'User not found in family'}), 400
    
    events = user.get_events_for_day(date)
    print(events)
    
    events_data = [
        {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start_date': event.start_date.strftime('%Y-%m-%d'),
            'start_time': event.start_time.strftime('%H:%M') if event.start_time else None,
            'end_date': event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
            'end_time': event.end_time.strftime('%H:%M') if event.end_time else None,
            'type': event.event_type.name,
            'creator': event.creator.alias if event.creator.alias else event.creator.username,
            'participants': [
                participant.alias if participant.alias else participant.username
                for participant in event.participants
            ],
        } for event in events
    ]
    
    return jsonify(events_data)


@app.route('/get_events_for_user', methods=['GET'])
@login_required
def get_events_for_user():
    print('get_events_for_user called')
    user_id = request.args.get('user_id')

    
    print('user_id:', user_id)
    
    
    user = User.query.get(user_id)
    if user not in current_user.family.users:
        return jsonify({'error': 'User not found in family'}), 400
    
    events = user.participating_events
    
    events_data = [
        {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start': event.start_date.strftime('%Y-%m-%d'),
            'start_time': event.start_time.strftime('%H:%M') if event.start_time else None,
            'end': event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
            'end_time': event.end_time.strftime('%H:%M') if event.end_time else None,
            'type': event.event_type.name,
            'creator': event.creator.alias if event.creator.alias else event.creator.username,
            'participants': [
                participant.alias if participant.alias else participant.username
                for participant in event.participants
            ],
        } for event in events
    ]
    
    return jsonify(events_data)


@app.route('/get_family_users', methods=['GET'])
@login_required
def get_family_users():

    family_users = current_user.family.users
    
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'alias': user.alias,
            'events': [
                {
                    'id': event.id,
                    'title': event.title,
                    'start_date': event.start_date.strftime('%Y-%m-%d'),
                    'end_date': event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
                } for event in user.participating_events
            ], 
        } for user in family_users
    ]
    
    return jsonify(users_data)
    
@app.route('/current_user', methods=['GET'])
@login_required
def get_current_user():
    user_id = current_user.id  
    print(current_user.id)
    print(user_id)
    if user_id:
        return jsonify({'user_id': user_id})
    else:
        return jsonify({'user_id': None})
