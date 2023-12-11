from flask import render_template, request
from datetime import datetime
from app.helpers import generate_weekly_days
from app import app
from app.models import Event
from flask_login import current_user, login_required



@app.route('/')
@app.route('/index')
@login_required
def index():
    # In the Event model definition, we establish a many-to-many
    # relationship between 'User' and 'Event' with the table 'event_participants' and
    # a backreference named 'participating_events' for the 'User' model.
    user_events = current_user.participating_events
    family_events = Event.query.filter_by(family_id=current_user.family_id, whole_family=True)
    combined_events = user_events.union(family_events).order_by(Event.start_time).all()
    family = current_user.family
    
    
    
    selected_date = request.args.get('selected_date')
    
    if selected_date:
        date = datetime(selected_date)
        weekly_days = generate_weekly_days(date)
        month_name = date.strftime('%B')
        print(month_name)
        
    else:
        date =datetime.now()
        weekly_days = generate_weekly_days(date)
        month_name = date.strftime('%B')
        print(month_name)
    
    return render_template('index.html', title='Home', user_events = user_events, events=combined_events, user=current_user, family=family, weekly_days=weekly_days, selected_date=selected_date, month_name=month_name)











