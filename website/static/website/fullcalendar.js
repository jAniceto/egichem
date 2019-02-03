$(function() {

    $('#calendar').fullCalendar({
      defaultView: 'listMonth', // the name of a generic view
      
      header: false,
      // header: {
      //   left:   'prev',
      //   center: 'today',
      //   right:  'next'
      // },
  
      displayEventTime: false, // don't show the time column in list view
      
      themeSystem: 'bootstrap4',
      googleCalendarApiKey: 'AIzaSyB47aCrts9o8mrOJwRFYTQKTyOZbJpxgZo',
      // Egichem Calendar
      events: 'kvtkthdoj8408hc10aja8s1gvg@group.calendar.google.com',
  
      eventClick: function(event) {
        // opens events in a popup window
        window.open(event.url, '_blank', 'width=700,height=600');
        return false;
      }
  
    });
  
  });