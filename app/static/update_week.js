function updateWeeklyAgenda(startDate) {
    // Calculate the endDate by adding 6 days to the startDate
    let endDate = new Date(startDate);
    endDate.setDate(endDate.getDate() + 6);
    console.log('endDate: ', endDate);

    // Fetch family users
    fetchFamilyUsers().then(function (family_users) {
        // Clear the current weekly agenda table
        let weeklyAgendaTable = document.getElementById('weekly-agenda');
        while (weeklyAgendaTable.firstChild) {
            weeklyAgendaTable.removeChild(weeklyAgendaTable.firstChild);
        }

        // Create header row
        let headerRow = document.createElement('tr');
        let dateHeader = document.createElement('th');
        dateHeader.classList.add('date-column');
        dateHeader.innerText = 'Date';
        headerRow.appendChild(dateHeader);

        // Add user headers
        family_users.forEach(function (user) {
            let userTh = document.createElement('th');
            userTh.classList.add('user-column');
            userTh.innerText = user.alias || user.username;
            headerRow.appendChild(userTh);
        });

        weeklyAgendaTable.appendChild(headerRow);

        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

        // Add date rows and fetch events for each user
        for (let i = 0; i <= 6; i++) {

            let updatedDate = new Date(startDate);
            updatedDate.setDate(updatedDate.getDate() + i);

            let row = document.createElement('tr');
            let dateCell = document.createElement('td');
            let weekDay = document.createElement('div');
            let monthDay = document.createElement('div');
            weekDay.classList.add('week-day');
            monthDay.classList.add('month-day');

            weekDay.innerHTML = days[(updatedDate.getDay())];
            
            
            monthDay.innerHTML = updatedDate.getDate() + ' ' + months[updatedDate.getMonth()];
            dateCell.appendChild(weekDay);
            dateCell.appendChild(monthDay);
            row.appendChild(dateCell);

            family_users.forEach(function (user) {
                let eventsCell = document.createElement('td');
                eventsCell.setAttribute('data-userid', user.id);
                row.appendChild(eventsCell);

                fetchEventsForDayUser(user.id, updatedDate).then(function (events) {
                    events.forEach(function (event) {
                        console.log('event in table: ', event);
                        let eventBlockId = 'event-block-' + event.id + user.id;

                        if (!document.getElementById(eventBlockId)){
            

                            let eventBlock = document.createElement('div');
                            eventBlock.classList.add('event-block');
                            eventBlock.id = event.id;
                            eventBlock.innerText = event.title;

                            if (event.start_time) {
                                let eventTime = document.createElement('div');
                                eventTime.classList.add('event-time');
                                if (event.end_time) {
                                    eventTime.innerText = ' (' + event.start_time + '-' + event.end_time + ')';
                                }
                                else {
                                    eventTime.innerText = ' (' + event.start_time + ')';
                                }
                                
                                eventBlock.appendChild(eventTime);
                            }


                            eventsCell.appendChild(eventBlock);
  
                        }
                        
                        
                    });
                });
            });

            weeklyAgendaTable.appendChild(row);
        }
    });
}




function fetchEventsForDayUser(user_id, date) {
    let newDate = date.toISOString().slice(0, 10);
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/get_events_for_day_user',
            
            data: {
                date: newDate,
                user_id: user_id
            },
            type: 'GET',
            success: function(response) {
                resolve(response);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}


function fetchFamilyUsers() {
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/get_family_users', 
            method: 'GET',
            success: function(data) {
                resolve(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}

