
function showEventDetails(event) {
    // Get the information for the modal
    console.log('Event info:', event);
    console.log('start date is: ', event.start_date);
    document.getElementById('modalEventTitle').innerHTML = event.title;
    document.getElementById('modalEventDescription').innerHTML = event.description ? event.description : 'No description provided.';
    document.getElementById('modalCreator').innerHTML = 'Creator: ' + event.creator;
    document.getElementById('modalEventParticipants').innerHTML = 'Participants: ' + event.participants;
    document.getElementById('modalStartDate').innerHTML = 'Start date: ' + event.start + ' - ' + event.start_time;
    document.getElementById('modalEndDate').innerHTML = 'End date: ' + (event.end ? event.end : event.start);

    // Display the modal
    let modal = document.getElementById('eventDetailsModal');
    modal.style.display = 'block';
  
    // Get the edit, delete and close button elements
    let closeButton = document.getElementsByClassName('close')[0];
    createDeleteEditButtons(event);
  
    // When the user clicks on the close button, close the modal
    closeButton.onclick = function() {
        modal.style.display = 'none';
    };
  
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
        modal.style.display = 'none';
        }
    };
}

function createDeleteEditButtons(event) {
    let titleContainer = document.getElementById('titleContainer');
    
    // Clear existing buttons
    titleContainer.innerHTML = '';

    

    let deleteButton = document.createElement('button');
    deleteButton.classList.add('btn', 'btn-sm', 'ml-2', 'delete-event-btn');
    let trashIcon = document.createElement('i');
    trashIcon.className = 'far fa-trash-alt';
    deleteButton.appendChild(trashIcon);
    titleContainer.appendChild(deleteButton);

    deleteButton.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete this shit?')) {
            // Call a function to delete the event or perform an AJAX request to the delete route
            deleteEvent(event.id);
        }
    });

    let editButton = document.createElement('button');
    editButton.classList.add('btn', 'btn-sm', 'ml-2', 'edit-event-btn');
    let editIcon = document.createElement('i');
    editIcon.className = 'fas fa-edit';
    editButton.appendChild(editIcon);
    titleContainer.appendChild(editButton);

    // Add event listener for the 'click' event
    editButton.addEventListener('click', function(e) {
        e.preventDefault();
        // Replace 'event_id' with the actual event id
        let eventId = event.id;
        window.location.href = '/edit_event/' + eventId;
    });
}

// Function for deleting events
function deleteEvent(eventId) {
    $.ajax({
      url: '/delete_event/' + eventId,
      type: 'POST',
      success: function(response) {
        if (response.success) {
          alert('Event deleted successfully');
          location.reload(); // Add this line to reload the page
        } else {
           alert('Error deleting event');
        }
      }
    });
}
  