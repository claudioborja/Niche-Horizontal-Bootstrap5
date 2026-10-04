/*
Template Name: Niche
Author: UXLiner
Updated for FullCalendar 6.x
*/
(function($) {
    "use strict";

    $(document).ready(function() {

        /* initialize the external events
         -----------------------------------------------------------------*/
        var externalEvents = document.getElementById('external-events');
        if (externalEvents) {
            new FullCalendar.Draggable(externalEvents, {
                itemSelector: '.external-event',
                eventData: function (element) {
                    var style = window.getComputedStyle(element);
                    return {
                        title: element.textContent.trim(),
                        backgroundColor: style.backgroundColor,
                        borderColor: style.borderColor
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
                initialView: 'dayGridMonth',
                editable: true,
                droppable: true, // this allows things to be dropped onto the calendar
                events: [
                    {
                        title: 'All Day Event',
                        start: new Date(y, m, 1),
                        backgroundColor: '#f56954', //red
                        borderColor: '#f56954' //red
                    },
                    {
                        title: 'Long Event',
                        start: new Date(y, m, d - 5),
                        end: new Date(y, m, d - 2),
                        backgroundColor: '#f39c12', //yellow
                        borderColor: '#f39c12' //yellow
                    },
                    {
                        title: 'Meeting',
                        start: new Date(y, m, d, 10, 30),
                        allDay: false,
                        backgroundColor: '#0073b7', //Blue
                        borderColor: '#0073b7' //Blue
                    },
                    {
                        title: 'Lunch',
                        start: new Date(y, m, d, 12, 0),
                        end: new Date(y, m, d, 14, 0),
                        allDay: false,
                        backgroundColor: '#00c0ef', //Info (aqua)
                        borderColor: '#00c0ef' //Info (aqua)
                    },
                    {
                        title: 'Birthday Party',
                        start: new Date(y, m, d + 1, 19, 0),
                        end: new Date(y, m, d + 1, 22, 30),
                        allDay: false,
                        backgroundColor: '#00a65a', //Success (green)
                        borderColor: '#00a65a' //Success (green)
                    },
                    {
                        title: 'Click for Google',
                        start: new Date(y, m, 28),
                        end: new Date(y, m, 29),
                        url: 'http://google.com/',
                        backgroundColor: '#3c8dbc', //Primary (light-blue)
                        borderColor: '#3c8dbc' //Primary (light-blue)
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
        }

        /* ADDING EVENTS */
        var currColor = '#3c8dbc' //Red by default
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
                initialView: 'dayGridMonth',
                editable: true,
                droppable: true, // this allows things to be dropped onto the calendar
                events: [
                    {
                        title: 'All Day Event',
                        start: new Date(y1, m1, 1),
                        backgroundColor: '#f56954', //red
                        borderColor: '#f56954' //red
                    },
                    {
                        title: 'Long Event',
                        start: new Date(y1, m1, d1 - 5),
                        end: new Date(y1, m1, d1 - 2),
                        backgroundColor: '#f39c12', //yellow
                        borderColor: '#f39c12' //yellow
                    },
                    {
                        title: 'Meeting',
                        start: new Date(y1, m1, d1, 10, 30),
                        allDay: false,
                        backgroundColor: '#0073b7', //Blue
                        borderColor: '#0073b7' //Blue
                    },
                    {
                        title: 'Lunch',
                        start: new Date(y1, m1, d1, 12, 0),
                        end: new Date(y1, m1, d1, 14, 0),
                        allDay: false,
                        backgroundColor: '#00c0ef', //Info (aqua)
                        borderColor: '#00c0ef' //Info (aqua)
                    },
                    {
                        title: 'Birthday Party',
                        start: new Date(y1, m1, d1 + 1, 19, 0),
                        end: new Date(y1, m1, d1 + 1, 22, 30),
                        allDay: false,
                        backgroundColor: '#00a65a', //Success (green)
                        borderColor: '#00a65a' //Success (green)
                    },
                    {
                        title: 'Click for Google',
                        start: new Date(y1, m1, 28),
                        end: new Date(y1, m1, 29),
                        url: 'http://google.com/',
                        backgroundColor: '#3c8dbc', //Primary (light-blue)
                        borderColor: '#3c8dbc' //Primary (light-blue)
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
        }
    });

})(jQuery);
