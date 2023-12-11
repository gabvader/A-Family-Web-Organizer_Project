//SCRIPT FOR RUNNING THE CALENDAR

// Declare variable currentDate as new Date(), an object representing a moment in time, not a string
let currentDate = new Date();


document.addEventListener('DOMContentLoaded', async function () {
  // Get calendar
  var calendarEl = document.getElementById('calendar');

  // Get current userID
  const userId = await fetchCurrentUserId();
  console.log(userId);

  // Get users for the user Family
  const familyUsers = await fetchFamilyUsers();
  console.log(familyUsers);

  // Get events for the user
  const userEvents = await fetchEventsforUser(userId);
  console.log(userEvents);

  // Initialize calendar
  var calendar = new FullCalendar.Calendar(calendarEl, {
    
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: ''
    },
    firstDay: 1,
    initialView: 'dayGridMonth',
    selectable: true,
    events: userEvents,
    
    // Update the currentDate variable if we select a date
    dateClick: function (info) {
      console.log('Clicked info:', info);

      currentDate = new Date(info.dateStr); // Get the clicked date
      console.log('Clicked date:', currentDate);

      // Update dayly events for user
      filterEventsByDay(currentDate, userEvents);

      // Update weekly agenda when selecting a new day
      updateWeeklyAgenda(currentDate);
    }

  });

  calendar.render();

  //Filter and show the dayly events son page load
  filterEventsByDay(currentDate, userEvents);

  // Update the weekly agenda on page load
  updateWeeklyAgenda(currentDate);
  
  let maxWidth = 0;
  
  $('#weekly-agenda .date-column').each(function() {
    maxWidth = Math.max(maxWidth, $(this).width());
  });
  
  $('#weekly-agenda .date-column').css('min-width', maxWidth + 'px');

});

  