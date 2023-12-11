// Get events for the day
function filterEventsByDay(date, events){
    formattedDate = date.toISOString().slice(0, 10);
    // Filter the events array to show only the events that fall on the clicked date
    const eventsOnDate = events.filter(event => {
        const eventStart = event.start.split('T')[0];
        const eventEnd = event.end ? event.end.split('T')[0] : event.start.split('T')[0];
        
        if (eventStart == eventEnd) {
            return formattedDate >= eventStart && formattedDate <= eventEnd;
        }
        else {
            return formattedDate >= eventStart && formattedDate < eventEnd;
        }
        
      });

      console.log('Events on clicked date:', eventsOnDate);
      console.log(eventsOnDate.length);

      let dailyEvents = document.getElementById('daily-events');
      dailyEvents.innerHTML = '';

      if (eventsOnDate.length > 0) {
        eventsOnDate.forEach(event => {
          createEventDiv(event, dailyEvents);
        })
      }
      else {
        dailyEvents.innerHTML = 'No events';
        console.log('empty');
      }
}

// Function for creating event containers
function createEventDiv(event, dailyEvents) {
    
    
    let eventDiv = document.createElement('div');
    eventDiv.classList.add('event-container');

    // Create a grid container div for the event details
    let gridContainer = document.createElement('div');
    gridContainer.classList.add('event-grid-container');

    let eventTitle = document.createElement('div');
    eventTitle.classList.add('event-title');
    eventTitle.innerHTML = event.title;
    gridContainer.appendChild(eventTitle);

    let eventType = document.createElement('div');

    if (event.type === 'birthday'){
        eventDiv.classList.add('birthday');
        let icon = document.createElement('i');
        icon.className = 'fas fa-birthday-cake';
        eventType.appendChild(icon);
    }

    else if (event.type === 'vacation'){
        eventDiv.classList.add('vacation');
        let icon = document.createElement('i');
        icon.className = 'fas fa-umbrella-beach';
        eventType.appendChild(icon);
    }
    
    else if (event.type === 'work'){
        eventDiv.classList.add('work');
        let icon = document.createElement('i');
        icon.className = 'fas fa-briefcase';
        eventType.appendChild(icon);
    }

    else if (event.type === 'medical appointment'){
        eventDiv.classList.add('medical');
        let icon = document.createElement('i');
        icon.className = 'fas fa-hospital-symbol';
        eventType.appendChild(icon);
    }

    else {
        eventType.innerHTML = event.type ? event.type : '';
    }
    
    gridContainer.appendChild(eventType);

    let eventStartTime = document.createElement('div');
    eventStartTime.innerHTML = event.start_time ? event.start_time : '';
    gridContainer.appendChild(eventStartTime);

    let eventParticipants = document.createElement('p');
    eventParticipants.classList.add('participants')
    eventParticipants.innerHTML = event.participants.join(', ');
    gridContainer.appendChild(eventParticipants);

    // Append the grid container div to the main eventDiv
    eventDiv.appendChild(gridContainer);

    eventDiv.addEventListener('click', function () {
        showEventDetails(event);
    });

    dailyEvents.appendChild(eventDiv);
}


function fetchEventsforUser(user_id) {
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/get_events_for_user', 
            
            data: {
                user_id: user_id
            },
            method: 'GET',
            success: function(data) {
                resolve(data);
            },
            error: function(errorThrown) {
                reject(errorThrown);
            }
        });
    });
}

function fetchCurrentUserId() {
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/current_user', 
            method: 'GET',
            success: function(data) {
                resolve(data.user_id);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}

