/*
Template Name: Niche
Author: UXLiner
Updated for FullCalendar 7.x
*/
(function($) {
    "use strict";

    $(document).ready(function() {

        // Daily view makes event titles readable on phones. Remember the desktop
        // view across breakpoint changes without overriding manual view selection.
        var mobileCalendar = window.matchMedia('(max-width: 767px)');
        function adaptCalendar(calendar) {
            var desktopView = 'dayGridMonth';
            mobileCalendar.addEventListener('change', function (event) {
                if (event.matches) {
                    desktopView = calendar.view.type;
                    calendar.changeView('timeGridDay');
                } else {
                    calendar.changeView(desktopView);
                }
            });
        }

        /* initialize the external events
         -----------------------------------------------------------------*/
        var externalEvents = document.getElementById('external-events');
        if (externalEvents) {
            new FullCalendar.Interaction.Draggable(externalEvents, {
                itemSelector: '.external-event',
                eventData: function (element) {
                    var style = window.getComputedStyle(element);
                    return {
                        title: element.textContent.trim(),
                        color: style.backgroundColor
                    };
                }
            });
        }

        /* initialize the calendar
         -----------------------------------------------------------------*/
        //Date for the calendar events (dummy data)
        var date = new Date()
        var d    = date.getDate(),
            m    = date.getMonth(),
            y    = date.getFullYear()

        // Check if calendar element exists before initializing
        if ($('#calendar').length > 0) {
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                initialView: mobileCalendar.matches ? 'timeGridDay' : 'dayGridMonth',
                editable: true,
                droppable: true, // this allows things to be dropped onto the calendar
                events: [
                    {
                        title: 'All Day Event',
                        allDay: true,
                        start: new Date(y, m, 1),
                        color: '#c23728' //red
                    },
                    {
                        title: 'Long Event',
                        allDay: true,
                        start: new Date(y, m, d - 5),
                        end: new Date(y, m, d - 2),
                        color: '#aa6400' //yellow
                    },
                    {
                        title: 'Meeting',
                        start: new Date(y, m, d, 10, 30),
                        allDay: false,
                        color: '#0073b7' //Blue
                    },
                    {
                        title: 'Lunch',
                        start: new Date(y, m, d, 12, 0),
                        end: new Date(y, m, d, 14, 0),
                        allDay: false,
                        color: '#087d82' //Info (aqua)
                    },
                    {
                        title: 'Birthday Party',
                        start: new Date(y, m, d + 1, 19, 0),
                        end: new Date(y, m, d + 1, 22, 30),
                        allDay: false,
                        color: '#087d43' //Success (green)
                    },
                    {
                        title: 'Click for Google',
                        allDay: true,
                        start: new Date(y, m, 28),
                        end: new Date(y, m, 29),
                        url: 'http://google.com/',
                        color: '#226f9b' //Primary (light-blue)
                    }
                ],
                eventReceive: function (info) {
                    // FullCalendar creates the event; only remove the source if requested.
                    if ($('#drop-remove').is(':checked')) {
                        $(info.draggedEl).remove();
                    }
                }
            });

            calendar.render();
            adaptCalendar(calendar);
        }

        /* ADDING EVENTS */
        var currColor = '#226f9b' //Light blue by default
        //Color chooser button
        var colorChooser = $('#color-chooser-btn')
        $('#color-chooser > li > a').click(function (e) {
            e.preventDefault()
            //Save color
            currColor = $(this).css('color')
            //Add color effect to button
            $('#add-new-event').css({ 'background-color': currColor, 'border-color': currColor })
        })
        $('#add-new-event').click(function (e) {
            e.preventDefault()
            //Get value and make sure it is not null
            var val = $('#new-event').val().trim()
            if (val.length == 0) {
                return
            }

            //Create events
            var event = $('<div />')
            event.css({
                'background-color': currColor,
                'border-color': currColor,
                'color': '#fff'
            }).addClass('external-event')
            event.text(val)
            $('#external-events').prepend(event)

            // Delegated FullCalendar dragging also handles this new event.

            //Remove event from text input
            $('#new-event').val('')
        })

        /*Basic View Calendar */

        /* initialize the calendar
           -----------------------------------------------------------------*/
        //Date for the calendar events (dummy data)
        var date1 = new Date()
        var d1    = date1.getDate(),
            m1    = date1.getMonth(),
            y1    = date1.getFullYear()

        // Check if calendar1 element exists before initializing
        if ($('#calendar1').length > 0) {
            var calendarEl1 = document.getElementById('calendar1');
            var calendar1 = new FullCalendar.Calendar(calendarEl1, {
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                initialView: mobileCalendar.matches ? 'timeGridDay' : 'dayGridMonth',
                editable: true,
                droppable: true, // this allows things to be dropped onto the calendar
                events: [
                    {
                        title: 'All Day Event',
                        allDay: true,
                        start: new Date(y1, m1, 1),
                        color: '#c23728' //red
                    },
                    {
                        title: 'Long Event',
                        allDay: true,
                        start: new Date(y1, m1, d1 - 5),
                        end: new Date(y1, m1, d1 - 2),
                        color: '#aa6400' //yellow
                    },
                    {
                        title: 'Meeting',
                        start: new Date(y1, m1, d1, 10, 30),
                        allDay: false,
                        color: '#0073b7' //Blue
                    },
                    {
                        title: 'Lunch',
                        start: new Date(y1, m1, d1, 12, 0),
                        end: new Date(y1, m1, d1, 14, 0),
                        allDay: false,
                        color: '#087d82' //Info (aqua)
                    },
                    {
                        title: 'Birthday Party',
                        start: new Date(y1, m1, d1 + 1, 19, 0),
                        end: new Date(y1, m1, d1 + 1, 22, 30),
                        allDay: false,
                        color: '#087d43' //Success (green)
                    },
                    {
                        title: 'Click for Google',
                        allDay: true,
                        start: new Date(y1, m1, 28),
                        end: new Date(y1, m1, 29),
                        url: 'http://google.com/',
                        color: '#226f9b' //Primary (light-blue)
                    }
                ],
                eventReceive: function (info) {
                    // FullCalendar creates the event; only remove the source if requested.
                    if ($('#drop-remove').is(':checked')) {
                        $(info.draggedEl).remove();
                    }
                }
            });

            calendar1.render();
            adaptCalendar(calendar1);
        }
    });

})(jQuery);
