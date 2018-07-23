var markerStartLat;
var markerStartLng;
var markerEndLat;
var markerEndLng;
var markers = [];
var allRoutesArray = ["15B Sample"];


function initMap() {
    /* Function that displays the Google map on the web app */
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer({
      suppressMarkers: true
      });

    // Default start positions for draggable markers
    var startLatLng = {
        lat: 53.349976,
        lng: -6.260354
    };

    var endLatLng = {
        lat: 53.352573,
        lng: -6.261665
    };

    // Positions the map
    var mapProp = {
        center: new google.maps.LatLng(53.349976, -6.260354),
        zoom: 11,
    };

    // Generates and displays Google map
    var map = new google.maps.Map(document.getElementById("map"), mapProp);
    directionsDisplay.setMap(map);
    //directionsDisplay.setPanel(document.getElementById('directionsPanel'));

    var markerStart = new google.maps.Marker({
        position: startLatLng,
        map: map,
        title: 'Start',
        draggable: true,
        visible: true,
        icon: {
          path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
          scale: 7,
          strokeColor: 'green',
          strokeWeight: 3
        },

    });

    var markerEnd = new google.maps.Marker({
        position: endLatLng,
        map: map,
        title: 'Finish',
        draggable: true,
        visible: true,
        icon: {
          path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
          scale: 7,
          strokeColor: 'red',
          strokeWeight: 3
        },
    });

    markers.push(markerStart);
    markers.push(markerEnd);

    // Draggable marker for start location
    google.maps.event.addListener(markerStart, 'dragend', function (evt) {
        console.log("changed start");
        markerStartLat = evt.latLng.lat().toFixed(3);
        markerStartLng = evt.latLng.lng().toFixed(3);
        calcRoute(true);
    });

    // Draggable marker for end location
    google.maps.event.addListener(markerEnd, 'dragend', function (evt) {
        markerEndLat = evt.latLng.lat().toFixed(3);
        markerEndLng = evt.latLng.lng().toFixed(3);
        calcRoute(true);
        //document.getElementById('test1').innerHTML = '<p>Marker dropped: Current Lat: ' + evt.latLng.lat().toFixed(3) + ' Current Lng: ' + evt.latLng.lng().toFixed(3) + '</p>';
    });

    // Search options for addresses bound to Dublin
    var defaultBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(52.999804, -6.841221),
      new google.maps.LatLng(53.693350, -5.914248));

    var input1 = document.getElementById('searchStart');
    var input2 = document.getElementById('searchEnd');

    var options = {
      bounds: defaultBounds,
      strictBounds: true,
    };

    autocompleteStart = new google.maps.places.Autocomplete(input1, options);
    autocompleteEnd = new google.maps.places.Autocomplete(input2, options);

    autocompleteStart.bindTo('bounds', map);
    autocompleteEnd.bindTo('bounds', map);

    autocompleteStart.addListener('place_changed', fillInStartAddress);
    autocompleteEnd.addListener('place_changed', fillInEndAddress);
}

function fillInStartAddress() {
    var place = autocompleteStart.getPlace();
    console.log(place.formatted_address);
    val = place.formatted_address;
    document.getElementById("searchStart").value = val;
    console.log(document.getElementById("searchStart").value);
}

function fillInEndAddress() {
    var place = autocompleteEnd.getPlace();
    console.log(place.formatted_address);
    val = place.formatted_address;
    document.getElementById("searchEnd").value = val;
    console.log(document.getElementById("searchEnd").value);
}

function calcRoute(usedDragMarker) {
    /* Function that displays a user's route on the map
    Called by button "Find Route" */

    usedDragMarker = usedDragMarker || false; //sets usedDragMarker to argument passed in or false by default

    // If user dragged markers take the marker lat long as start/end
    if (usedDragMarker) {
        var start = markerStartLat + ',' + markerStartLng;
        var end = markerEndLat + ',' + markerEndLng;
    }
    // Else take the values entered the address search bars
    else {
        console.log("Used the search option");
        var start = document.getElementById('searchStart').value; // this value is captured from the start dropdown
        var end = document.getElementById('searchEnd').value; // this value is captured from the end dropdown        
    } 



    var request = {
        origin: start,
        destination: end,
        travelMode: 'TRANSIT', // signifies that we want a public transport route
        transitOptions: {
            modes: ['BUS'], // specifies that we only want Dublin Bus to be considered
            routingPreference: 'FEWER_TRANSFERS', // we want the route with the least amount of bus transfers
            //departureTime: new Date(2018, 07, 20, 17, 28), //TODO specify departure time
        },
        provideRouteAlternatives: true
    };

    directionsService.route(request, function (response, status) {
        console.log(response)
        if (status == 'OK') { // checks that the returned object contains the correct information
            directionsDisplay.setDirections(response); // displays the route on the map
            
            alternativeArray = [];
            
            console.log("RESPONSE TO DIRECTION SERVICES")
            console.log(response);
            //console.log(response.routes[0].legs[0].steps[0].start_point.lat());
            
            for (var j = 0; j < response.routes.length; j++) {
            
            var stepsamount = response.routes[j].legs[0].steps.length; // caluclate how many steps are involved in the journey
            var stepsarray = []; // create an empty array to store data for each bus on the journey
            var totalwalking = 0; // initilaise walking time to 0

            for (var i = 0; i < stepsamount; i++) { // iterates through each step in the provided route

                var travelmode = response.routes[j].legs[0].steps[i].travel_mode; // check if the step in journey involves walking or bus

                if (travelmode == "WALKING") { // If the step is walking, we only care about the length of time the walk takes

                    var walkingtime = parseInt(response.routes[j].legs[0].steps[i].duration['text']);
                    totalwalking += walkingtime; // total walking time involved is captured

                } else if (travelmode == "TRANSIT") {

                    var routedict = {}; // a new dictionary is created for each bus 
                    var chosenroute = response.routes[j].legs[0].steps[i].transit.line.short_name; // route number
                    var distance = parseFloat(response.routes[j].legs[0].steps[i].distance['text']); // distance travelled on this bus
                    var departurestop = response.routes[j].legs[0].steps[i].transit.departure_stop.name; // departure address name
                    var arrivalstop = response.routes[j].legs[0].steps[i].transit.arrival_stop.name; // arrival address name
                    var departurelatlng = response.routes[j].legs[0].steps[i].start_location.lat() + ',' + response.routes[j].legs[0].steps[i].start_location.lng(); // departure lat/lng
                    var arrivallatlng = response.routes[j].legs[0].steps[i].end_location.lat() + ',' + response.routes[j].legs[0].steps[i].end_location.lng(); //arrival lat/lng
                    var numstops = response.routes[j].legs[0].steps[i].transit.num_stops; // number of stops to take on bus

                    // add each key/value pair to the dictionary
                    routedict['route'] = chosenroute;
                    routedict['distance'] = distance;
                    routedict['departurestop'] = departurestop;
                    routedict['arrivalstop'] = arrivalstop;
                    routedict['departurelatlng'] = departurelatlng;
                    routedict['arrivallatlng'] = arrivallatlng;
                    routedict['numstops'] = numstops;

                    // append the dictionary to the array
                    stepsarray.push(routedict);
                }
            }

            // create a new dictionary to store walking time and append it to the array
            var timedict = {};
            timedict['walkingtime'] = totalwalking;
            stepsarray.push(timedict);
                
            alternativeArray.push(stepsarray);
            }

            //console.log(totalwalking)
            //console.log(stepsamount);
            console.log("Here is steps array:");
            console.log(stepsarray);
            console.log(alternativeArray);

            allRoutesArray = alternativeArray;

            //console.log(stepsarray[0]['route'])
        }
    });
}

function toggleMarkers() {
    for (var i = 0; i < markers.length; i++) {
      markers[i].visible ? markers[i].setVisible(false) : markers[i].setVisible(true);
    }
}


// var allRoutesArray = 
$(document).ready(function() {
       $("#journeyForm").submit(function(event){
            event.preventDefault();

            var journeyData = JSON.stringify($(this).serializeArray());
            allRoutesArray = JSON.stringify(allRoutesArray);

            $.ajax({
                 type:"POST",
                 url:"/journey/",
                 data: {
                        'testInput': $('#testInput').val(), // from form
                        'origin': $('#searchStart').val(),
                        'destination': $('#searchEnd').val(),
                        'dateChosen': $('#dateChosen').val(),
                        query: journeyData,
                        'allRoutes': allRoutesArray,
                        },
                 success: function(response){
                    console.log("success")
                    console.log(response)
                    $('#message').html("<h2>Journey Form Submitted!</h2>")

                    //response is a list coming back from python with the variables or data we need
                    testInput = response[1]
                    origin = response[2]
                    destination = response[3]
                    journeyTime = response[4]
                    dateChosen = response[5]
                    bestRoute = response[6]
                    busTime = response[7]

                    var journey = {
                      'testInput': testInput,
                      'origin': origin,
                      'destination': destination,
                      'journeyTime': journeyTime,
                      'dateChosen': dateChosen,
                      'bestRoute': bestRoute,
                      'busTime': busTime,
                    };

                    displayJourney(journey)
                 }
            });
            return false;
       });

});

function displayJourney(journey) {
    //Takes a dictionary containing journey info and puts info into HTML elements
        console.log(journey);
        document.getElementById("journeySummary").innerHTML = `
        <b>Text Input:</b> ${journey.testInput}<br>
        <b>Origin:</b> ${journey.origin}<br>
        <b>Destination:</b> ${journey.destination}<br>
        <b>Last bus leg of your journey takes:</b> ${journey.journeyTime}<br>
        <b>Date:</b> ${journey.dateChosen}<br>
        <b>Routes to take:</b> ${journey.bestRoute}<br>
        <b>Time spent on the bus (minutes):</b> ${journey.busTime}<br>
`
}