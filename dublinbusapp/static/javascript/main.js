// Global variables needed to pass around the marker information
var markerStartLat;
var markerStartLng;
var markerEndLat;
var markerEndLng;
var markers = [];
var startAddress;
var endAddress;

// Default positions of markers
var startPosition = {
	lat: 53.307837,
	lng: -6.236875
};

var endPosition ={
	lat: 53.352620,
	lng: -6.261336
};

function initMap() {
    /* Function that displays the Google map on the web app */
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer({
      suppressMarkers: true
      });

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
          url: "/static/images/start.png",
          scaledSize: new google.maps.Size(64,64),

        },

    });

    markerEnd = new google.maps.Marker({
        position: endPosition,
        map: map,
        title: 'End',
        draggable: true,
        visible: true,
        icon: {
          url: "/static/images/end.png",
          scaledSize: new google.maps.Size(64,64),
        },
    });

    // Add markers to global array
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

    // Set autocomplete search options for addresses bound to Dublin area
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

    var unixDateChosen = findUnixDateChosen();

    // Set up the request that will be sent to Google
    var request = {
        origin: startPosition,
        destination: endPosition,
        travelMode: 'TRANSIT',
        transitOptions: {
            modes: ['BUS'], // Specifies that we only want Dublin Bus to be considered
            routingPreference: 'FEWER_TRANSFERS',
            departureTime: new Date(unixDateChosen),
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
            var newEndPosition = response.routes[0].legs[0].end_location;

            markerStart.setPosition(newStartPosition);
            markerEnd.setPosition(newEndPosition);

	    startAddress = response.routes[0].legs[0].start_address;
	    startAddress = startAddress.split(",", 2);
	    startAddress = startAddress.join(",");
	    console.log(startAddress);
	    console.log("START ABOVE");

	    endAddress = response.routes[0].legs[0].end_address;
	    endAddress = endAddress.split(",", 2);
	    endAddress = endAddress.join(",");

            // Go through the best (first) route suggested by Google's response
            for (var j = 0; j < 1; j++) { // To iterate through every route change j < 1 to j < response.routes.length

                var numSteps = response.routes[j].legs[0].steps.length; // Number of steps involved in the journey (walk, bus, walk = 3)
                var busStepsArray = []; // Array to store data for each bus on the journey
                var totalWalkingTime = 0;
                var totalLuasTime = 0;

                // Iterate through each step in the provided journey and extract information needed
                for (var i = 0; i < numSteps; i++) {

                    var travelMode = response.routes[j].legs[0].steps[i].travel_mode; // Check if the step in journey involves walking or bus

                    if (travelMode == "WALKING") {
                        var walkingtime = parseInt(response.routes[j].legs[0].steps[i].duration['text']); // Parse walking time from the response
                        totalWalkingTime += walkingtime;

                    } else if (travelMode == "TRANSIT") {

                        // Error check to see if the journey is on the Luas based on the instructions received from Google
                        var instructions = response.routes[j].legs[0].steps[i].instructions; // String e.g. "Tram towards Milltown", "Bus towards Ongar St"

                        if (instructions.slice(0, 5) == "Tram") {
                            var luasTravelTime = response.routes[j].legs[0].steps[i].duration['value']; // Travel time on Luas in seconds
                            totalLuasTime += luasTravelTime
                            continue;
                        }

                        var routeDict = {}; // New dictionary created for each bus
                        var chosenRoute = response.routes[j].legs[0].steps[i].transit.line.short_name; // Route number
                        var distance = parseFloat(response.routes[j].legs[0].steps[i].distance['text']); // Distance travelled on this bus
                        var departureStop = response.routes[j].legs[0].steps[i].transit.departure_stop.name; // Departure address name
                        var arrivalStop = response.routes[j].legs[0].steps[i].transit.arrival_stop.name; // Arrival address name
                        var departureLatLng = response.routes[j].legs[0].steps[i].start_location.lat() + ',' + response.routes[j].legs[0].steps[i].start_location.lng();
                        var arrivalLatLng = response.routes[j].legs[0].steps[i].end_location.lat() + ',' + response.routes[j].legs[0].steps[i].end_location.lng();
                        var numStops = response.routes[j].legs[0].steps[i].transit.num_stops; // Number of stops to take on bus
                        var googleTime = response.routes[j].legs[0].steps[i].duration['value'] // Google's estimated journey time

                        // Add each key/value pair to the dictionary
                        routeDict['route'] = chosenRoute;
                        routeDict['distance'] = distance;
                        routeDict['departureStop'] = departureStop;
                        routeDict['arrivalStop'] = arrivalStop;
                        routeDict['departureLatLng'] = departureLatLng;
                        routeDict['arrivalLatLng'] = arrivalLatLng;
                        routeDict['numStops'] = numStops;
                        routeDict['googleTime'] = googleTime;

                        // Append the dictionary made for each bus
                        busStepsArray.push(routeDict);
                    }
            }

            // Create a new dictionary to store walking time and append it to the array
            var timedict = {};
            timedict['walkingtime'] = totalWalkingTime;
            timedict['totalLuasTime'] = totalLuasTime;

            // Find out how long it takes to walk to the first bus stop if walking is the first part of the journey
            if (response.routes[0].legs[0].steps[0].travel_mode == "WALKING") {
                walkTimeToStop = response.routes[0].legs[0].steps[0].duration['text'] // Returns walk time as a minutes string e.g. "3 mins"
            } else {
                walkTimeToStop = "0 mins";
            }

            timedict['walkTimeToStop'] = walkTimeToStop;

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
                url:"/journey/", // Sends post request to the url '/journey', which calls a function in views.py

                // Collect the data we want to send to Django
                data: {
                        query: journeyData,
                        'dateChosen': $('#dateChosen').val(),
                        'allRoutes': JSONallRoutesArray, // Contains all the journeys collected from the Google Direction Service object
                    },

                // Gets a response from Django
                success: function(response){
                    console.log("success")
                    console.log(response)

                    // Create dictionary with information received from Django/Python
                    try {
                        var journey = {
                            'dateChosen': response.dateChosen,
                            'routesToTake': response.routesToTake,
                            'busTime': response.busTime,
                            'walkingTime': response.walkingTime,
                            'walkTimeToStop': response.walkTimeToStop,
                            'totalLuasTime': response.totalLuasTime,
                            'totalTime': response.totalTime,
                            'realTimeInfo': response.realTimeInfo,
                            'weatherNowText': response.weatherNowText,
                            'weatherIcon': response.weatherIcon,
                            'temperature': response.temperature,
                        };
                        displayJourney(journey)
                        displayRealTimeInfo(journey.realTimeInfo, journey.walkTimeToStop)
                        drawPieChart(journey)
                    }
                    catch(err) {
                        somethingIsBroken(response)
                    }
                 }
            });
            return false;
       });
});


function displayJourney(journey) {
    //Takes a dictionary containing journey info and puts info into HTML elements

    // Display text at top of popup window
    if (journey.routesToTake.length > 1) {
        var isMultiRoute = true;
        var label = "Routes";
    } else {
        var isMultiRoute = false;
        var label = "Route";
    }

    document.getElementById("modalBody").innerHTML = `<b class='popupheading'>Start:</b> ${startAddress} <br>`
    document.getElementById("modalBody").innerHTML += `<b class='popupheading'>End:</b> ${endAddress} <br>`


    if (isMultiRoute == false) {
        document.getElementById("modalBody").innerHTML += `<b class='popupheading'>` + label + `:</b> ${journey.routesToTake} <br>`

    } else {
        document.getElementById("modalBody").innerHTML += `<b>` + label + `:</b> ${journey.routesToTake[0]}`
        for (var i = 1; i < journey.routesToTake.length; i++) {
            document.getElementById("modalBody").innerHTML += ` <i class="fa fa-arrow-right"></i> `
            document.getElementById("modalBody").innerHTML += `${journey.routesToTake[i]}`
        }
        document.getElementById("modalBody").innerHTML += ` <br>`
    }

    document.getElementById("modalBody").innerHTML += `
    <div style="margin-top:20px;margin-bottom:0px;"><b class='popupheading'>Journey Time:</b> ${journey.totalTime} mins</div>`

    // Create divs that info will be put into
    // Hide pie chart for phone users (not displaying properly)
    document.getElementById("modalBody").innerHTML += `<div id="piechart" class="hidden-phone"></div>`
    document.getElementById("modalBody").innerHTML += `<div id="weatherForecast"></div>`
    document.getElementById("modalBody").innerHTML += `<div id="realTimeInfo"></div>`



    // Display weather icon
    var icon = getWeatherIcon(journey.weatherIcon);

    document.getElementById("weatherForecast").innerHTML = `

    <p><b class="popupheading">Forecast:</b><br><img src="/static/images/weather_icon/` + icon + `"></p>`


}

function displayRealTimeInfo(realTimeArray, walkTimeToStop) {
	/* Displays realtime info on frontend
    Takes in a list of dictionaries
	Each dict contains route:arrivalTime as key:value
	 */


	document.getElementById("realTimeInfo").innerHTML = `<p>First Stop Real Time Information:`

	var numResults = realTimeArray.length;

    if (numResults > 5) {
        numResults = 5; // Limit number of results to 5
    }

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

    document.getElementById("realTimeInfo").innerHTML += "<br><b>Walk Time to First Stop: </b>" + walkTimeToStop +"</p>"


}

function drawPieChart(journey) {
    // Draw pie chart showing time spent on bus versus walking
	google.charts.load("current", {packages:["corechart"]});
    google.charts.setOnLoadCallback(drawChart);


    function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Travel Mode', 'Minutes'],
          ['Total Walking Time: ' + String(journey.walkingTime) + ' mins', journey.walkingTime],
          ['Total Bus Time: ' + String(journey.busTime) + ' mins', journey.busTime],
        ]);

        var options = {
//          title: 'Journey Breakdown',
          pieHole: 0.6,
          enableInteractivity: false,
          pieSliceText: 'none',
          legend: { position:'labeled', textStyle: {color: 'white', fontSize: '2rem'} },
          backgroundColor: 'transparent',
          slices:{
              0:{color:'#b2d0e3'},
              1:{color:'#5483a1'},
              2:{color:'#f9f8eb'},
          }
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
      }

}

function findUnixDateChosen() {
    // Converts date chosen into a unix time
    var dateChosen =  document.getElementById("dateChosen").value;
    var unixDateChosen;

    // Convert dateChosen into unix timestamp
    if ( (dateChosen == "") || Date.parse(dateChosen) < Date.now() ) {
        unixDateChosen = Date.now();
    } else {
        unixDateChosen = Date.parse(dateChosen);
    }

    console.log(unixDateChosen);

    return unixDateChosen + 3600000; // Add 3.6 million milliseconds to the time (adding 1 hour) to correct for timezone difference
    // Returns datetime with an hour too early if you dont add the milliseconds needed
}

function getWeatherIcon(weatherIconText) {
    /* Function that matches the weather forecast text received from DarkSky API with an icon from OpenWeather API
    DarkSky does not provide its own icons
    The icon text is added to the src tag of an element to display the icon using OpenWeather url
    E.g. http://openweathermap.org/img/w/09d.png
    */
    console.log(weatherIconText);
    switch(weatherIconText) {
        case "clear-day":
            icon = "sun.png";
            break;
        case "clear-night":
            icon = "moon.png";
            break;
        case "rain":
            icon = "rain.png";
            break;
        case "snow":
        case "sleet":
            icon = "snow.png";
            break;
        case "wind":
        case "fog":
            icon = "cloud.png";
            break;
        case "cloudy":
            icon = "cloud.png";
            break;
        case "partly-cloudy-day":
            icon = "cloud_day.png";
            break;
        case "partly-cloudy-night":
            icon = "cloud_night.png";
            break;
        default:
            icon = "cloud.png"; // Default to cloud icon
            break;
    }

    console.log("ICON");
    console.log(icon);

    return icon;
}

function somethingIsBroken(response) {
    // Displays error response message and picture
    document.getElementById("modalBody").innerHTML = response;
    document.getElementById("modalBody").innerHTML += "<img id='busErrorPic' src='https://i.imgur.com/QS9hkyX.jpg' />";
}
