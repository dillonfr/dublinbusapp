var markerStartLat;
var markerStartLng;
var markerEndLat;
var markerEndLng;
var markers = [];

var startPosition = {
	lat: 53.321712,
	lng: -6.266006
};

var endPosition ={
	lat: 53.360863,
	lng: -6.272701
};


function initMap() {
    /* Function that displays the Google map on the web app */
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer({
      suppressMarkers: true
      });

    // Default start positions for draggable markers
    // var startLatLng = {
    //     lat: 53.321712,
    //     lng: -6.266006
    // };

    // var endLatLng = {
    //     lat: 53.360863,
    //     lng: -6.272701
    // };

    // Positions the map
    var mapProp = {
        center: new google.maps.LatLng(53.349976, -6.260354),
        zoom: 11,
        
        styles: [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#444444"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.business","elementType":"geometry.fill","stylers":[{"visibility":"on"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"on"}]},{"featureType":"transit","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#b2d0e3"},{"visibility":"on"}]}]
    };

    // Generates and displays Google map
    var map = new google.maps.Map(document.getElementById("map"), mapProp);
    directionsDisplay.setMap(map);

    // Create our own custom markers
    markerStart = new google.maps.Marker({
        position: startPosition,
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

    markerEnd = new google.maps.Marker({
        position: endPosition,
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
        markerStartLat = evt.latLng.lat().toFixed(3);
        markerStartLng = evt.latLng.lng().toFixed(3);

        startPosition = String(markerStartLat) + "," + String(markerStartLng);
        setTimeout(calcRoute(true), 500) //true indicates the marker was dragged
    });

    // Draggable marker for end location
    google.maps.event.addListener(markerEnd, 'dragend', function (evt) {
        markerEndLat = evt.latLng.lat().toFixed(3);
        markerEndLng = evt.latLng.lng().toFixed(3);

        endPosition = String(markerEndLat) + "," + String(markerEndLng);
        setTimeout(calcRoute(true), 500); //true indicates the marker was dragged
    });

    // Set search options for addresses bound to Dublin
    var defaultBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(52.999804, -6.841221),
      new google.maps.LatLng(53.693350, -5.914248));

    // Setting up Autocomplete search bars
    var input1 = document.getElementById('searchStart'); // start search bar
    var input2 = document.getElementById('searchEnd'); // end search bar

    var options = {
      bounds: defaultBounds,
      strictBounds: true,
    };

    // Create new Autocompletes
    autocompleteStart = new google.maps.places.Autocomplete(input1, options);
    autocompleteEnd = new google.maps.places.Autocomplete(input2, options);

    // Update values of the search bar instantly when a new place is chosen
    autocompleteStart.addListener('place_changed', fillInStartAddress);
    autocompleteEnd.addListener('place_changed', fillInEndAddress);
}

function fillInStartAddress() {
    /* Function that instantly updates the value of the start address element when a new place is chosen from Autocomplete*/
    var place = autocompleteStart.getPlace();

    val = place.formatted_address; // Get address of the place chosen

    startPosition = String(val);

    document.getElementById("searchStart").value = val;
}

function fillInEndAddress() {
    /* Function that instantly updates the value of the end address element when a new place is chosen from Autocomplete*/
    var place = autocompleteEnd.getPlace();

    val = place.formatted_address; // Get address of the place chosen

    endPosition = String(val);

    document.getElementById("searchEnd").value = val;
}


function toggleMarkers() {
    /* Toggles visibility of the markers in the global markers array */
    for (var i = 0; i < markers.length; i++) {
      markers[i].visible ? markers[i].setVisible(false) : markers[i].setVisible(true);
    }
}



function calcRoute(usedDragMarker) {
    /* Function that displays a user's route on the map */

    // Check if user dragged the markers
    usedDragMarker = usedDragMarker || false; // true if user dragged marker, defaults to false

    // If user dragged markers take the markers lat/lng as the start and end
    // if (usedDragMarker) {
    //     var start = markerStartLat + ',' + markerStartLng;
    //     var end = markerEndLat + ',' + markerEndLng;
    // }
    // // Else take the values entered the address search bars
    // else {
    //     var start = document.getElementById('searchStart').value; // This value is captured from the start address search bar
    //     var end = document.getElementById('searchEnd').value; // This value is captured from the end address search bar    
    // } 

    // var start = startPosition;
    // var end = endPosition;

    console.log("Start: " + String(startPosition) + ". End: " + String(endPosition));

    // Set up the request that will be sent to Google
    var request = {
        origin: startPosition,
        destination: endPosition,
        travelMode: 'TRANSIT',
        transitOptions: {
            modes: ['BUS'], // Specifies that we only want Dublin Bus to be considered
            routingPreference: 'FEWER_TRANSFERS',
            //departureTime: new Date(2018, 07, 20, 17, 28), //TODO specify departure time
        },
        provideRouteAlternatives: true
    };

    // Send our request to DirectionsService
    directionsService.route(request, function (response, status) {
        console.log("success")
        console.log(response)
        if (status == 'OK') { // Checks there were no problems with the request and response
            directionsDisplay.setDirections(response); // Displays the route on the map
            
            // Create global array that will contain the routes suggested by Google
            allRoutesArray = [];

            var newStartPosition = response.routes[0].legs[0].start_location;
            var newEndPosition = response.routes[0].legs[0].end_location; //.toUrlValue(6)

            markerStart.setPosition(newStartPosition);
            markerEnd.setPosition(newEndPosition);
            
            // Iterates through every journey suggested by Google's response
            for (var j = 0; j < response.routes.length; j++) {
            
                var numSteps = response.routes[j].legs[0].steps.length; // Number of steps involved in the journey (walk, bus, walk = 3)
                var busStepsArray = []; // Array to store data for each bus on the journey
                var totalWalkingTime = 0;

                // Iterate through each step in the provided journey and extract information needed
                for (var i = 0; i < numSteps; i++) {

                    var travelMode = response.routes[j].legs[0].steps[i].travel_mode; // Check if the step in journey involves walking or bus

                    if (travelMode == "WALKING") {
                        var walkingtime = parseInt(response.routes[j].legs[0].steps[i].duration['text']); // Parse walking time from the response
                        totalWalkingTime += walkingtime;

                    } else if (travelMode == "TRANSIT") {

                        var routeDict = {}; // New dictionary created for each bus
                        var chosenRoute = response.routes[j].legs[0].steps[i].transit.line.short_name; // Route number
                        var distance = parseFloat(response.routes[j].legs[0].steps[i].distance['text']); // Distance travelled on this bus
                        var departureStop = response.routes[j].legs[0].steps[i].transit.departure_stop.name; // Departure address name
                        var arrivalStop = response.routes[j].legs[0].steps[i].transit.arrival_stop.name; // Arrival address name
                        var departureLatLng = response.routes[j].legs[0].steps[i].start_location.lat() + ',' + response.routes[j].legs[0].steps[i].start_location.lng();
                        var arrivalLatLng = response.routes[j].legs[0].steps[i].end_location.lat() + ',' + response.routes[j].legs[0].steps[i].end_location.lng();
                        var numStops = response.routes[j].legs[0].steps[i].transit.num_stops; // Number of stops to take on bus

                        // Add each key/value pair to the dictionary
                        routeDict['route'] = chosenRoute;
                        routeDict['distance'] = distance;
                        routeDict['departureStop'] = departureStop;
                        routeDict['arrivalStop'] = arrivalStop;
                        routeDict['departureLatLng'] = departureLatLng;
                        routeDict['arrivalLatLng'] = arrivalLatLng;
                        routeDict['numStops'] = numStops;

                        // Append the dictionary made for each bus
                        busStepsArray.push(routeDict);
                    }
            }

            // Create a new dictionary to store walking time and append it to the array
            var timedict = {};
            timedict['walkingtime'] = totalWalkingTime;
            busStepsArray.push(timedict);
                
            allRoutesArray.push(busStepsArray); // allRoutesArray: Array of arrays that contain info on each journey suggested by Google

            }

        // Updates everytime a new allRoutesArray is made
        JSONallRoutesArray = JSON.stringify(allRoutesArray); // Convert to JSON so AJAX can send it
        }
    });
}

// AJAX function that deals with POST request and response
$(document).ready(function() {
        $("#journeyForm").submit(function(event){
            event.preventDefault();

            var journeyData = JSON.stringify($(this).serializeArray());

            $.ajax({
                type:"POST",
                url:"/journey/", // Sends post request to the url journey, which calls a function in views.py

                // Collect the data we want to send to Django
                data: {
                        query: journeyData,
                        'origin': $('#searchStart').val(),
                        'destination': $('#searchEnd').val(),
                        'dateChosen': $('#dateChosen').val(),
                        'allRoutes': JSONallRoutesArray, // Contains all the journeys collected from the Google Direction Service object
                    },

                // Gets a response from Django
                success: function(response){
                    console.log("success")
                    console.log(response)
                    $('#message').html("<h2>Journey Form Submitted!</h2>")

                    // Create dictionary with information received from Django/Python
                    var journey = {
                        'origin': response.origin,
                        'destination': response.destination,
                        'dateChosen': response.dateChosen,
                        'lastBusStepPrediction': response.lastBusStepPrediction,
                        'routesToTake': response.routesToTake,
                        'busTime': response.busTime,
                        'walkingTime': response.walkingTime,
                        'totalTime': response.totalTime,
                        'realTimeInfo': response.realTimeInfo,
                        'weatherNowText': response.weatherNowText,
                        'weatherIcon': response.weatherIcon,
                    };

                    displayJourney(journey)
                    displayRealTimeInfo(journey.realTimeInfo)
                    //displayWeatherIcon(journey.weatherIcon)
                    drawPieChart(journey)
                 }
            });
            return false;
       });
});


function displayJourney(journey) {
    //Takes a dictionary containing journey info and puts info into HTML elements

    document.getElementById("journeySummary").innerHTML = `
    <b>Last bus leg of your journey takes:</b> ${journey.lastBusStepPrediction}<br>
    <b>Date:</b> ${journey.dateChosen}<br>
    <b>Routes to take:</b> ${journey.routesToTake}<br>
    <b>Time spent on the bus (minutes):</b> ${journey.busTime}<br>
    <b>Time spent walking:</b> ${journey.walkingTime}<br>
    <b>Total journey time:</b> ${journey.totalTime}<br>
    <b>Weather forecast:</b> ${journey.weatherNowText}<br>
    <b>Weather icon:</b> ${journey.weatherIcon}<br>

`
}

function displayRealTimeInfo(realTimeArray) {
	/* Takes in a list of dictionaries
	Each dict contains route:arrivalTime as key:value
	Displays realtime info on frontend */

	document.getElementById("realTimeInfo").innerHTML = "<b>Real Time information</b><br>"

	var numResults = realTimeArray.length;

	for (var i = 0; i < numResults; i++) {
		// Select single dict from the array
		var busDict = realTimeArray[i];

		// The key is the route
		var route = Object.keys(busDict)[0];

		// The value is the arrival time
		var arrivalTime = Object.values(busDict)[0];

		// Add to frontend
		if (arrivalTime == "Due") {
			document.getElementById("realTimeInfo").innerHTML += "<b>Route:</b> " + route + "<b> Due: </b>Now<br>";
		} else {
			document.getElementById("realTimeInfo").innerHTML += "<b>Route:</b> " + route + "<b> Due: </b>" + arrivalTime + " mins<br>";
		}
	}
}

function drawPieChart(journey) {
	google.charts.load("current", {packages:["corechart"]});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Travel Mode', 'Minutes'],
          ['Walking', 5],
          ['Bus', 20],
          ['Waiting', 7],
        ]);

        var options = {
          title: 'Journey Details',
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
      }

}