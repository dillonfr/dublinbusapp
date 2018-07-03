function initMap() {
    /* Function that displays the Google map on the web app */

    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();

    var myLatLng = {
        lat: 53.349976,
        lng: -6.260354
    };

    // Positions the map
    var mapProp = {
        center: new google.maps.LatLng(53.349976, -6.260354),
        zoom: 11,
    };

    // Generates and displays Google map
    var map = new google.maps.Map(document.getElementById("map"), mapProp);
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById('directionsPanel'));

    var markerStart = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'Start',
        draggable: true
    });

    var markerEnd = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'Finish',
        draggable: true
    });

    // Draggable marker for start location
    google.maps.event.addListener(markerStart, 'dragend', function (evt) {
        document.getElementById('test1').innerHTML = '<p>Marker dropped: Current Lat: ' + evt.latLng.lat().toFixed(3) + ' Current Lng: ' + evt.latLng.lng().toFixed(3) + '</p>';
    });

    // Draggable marker for end location
    google.maps.event.addListener(markerEnd, 'dragend', function (evt) {
        document.getElementById('test1').innerHTML = '<p>Marker dropped: Current Lat: ' + evt.latLng.lat().toFixed(3) + ' Current Lng: ' + evt.latLng.lng().toFixed(3) + '</p>';
    });
}

function calcRoute() {
    /* Function that displays a user's route on the map
    Called every time the user changes a dropdown option */

    var start = document.getElementById('selectstart').value; // this value is captured from the start dropdown
    var end = document.getElementById('selectend').value; // this value is captured from the end dropdown
    var request = {
        origin: start,
        destination: end,
        //provideRouteAlternatives: true,
        travelMode: 'TRANSIT', // signifies that we want a public transport route
        transitOptions: {
            modes: ['BUS'], // specifies that we only want Dublin Bus to be considered
            routingPreference: 'FEWER_TRANSFERS' // we want the route with the least amount of bus transfers
        }
    };
    directionsService.route(request, function (response, status) {
        if (status == 'OK') { // checks that the returned object contains the correct information
            directionsDisplay.setDirections(response); // displays the route on the map

            //console.log(response);
            //console.log(response.routes[0].legs[0].steps[0].start_point.lat());

            var stepsamount = response.routes[0].legs[0].steps.length; // caluclate how many steps are involved in the journey
            var stepsarray = []; // create an empty array to store data for each bus on the journey
            var totalwalking = 0; // initilaise walking time to 0

            for (var i = 0; i < stepsamount; i++) { // iterates through each step in the provided route

                var travelmode = response.routes[0].legs[0].steps[i].travel_mode; // check if the step in journey involves walking or bus

                if (travelmode == "WALKING") { // If the step is walking, we only care about the length of time the walk takes

                    var walkingtime = parseInt(response.routes[0].legs[0].steps[i].duration['text']);
                    totalwalking += walkingtime; // total walking time involved is captured

                } else if (travelmode == "TRANSIT") {

                    var routedict = {}; // a new dictionary is created for each bus 
                    var chosenroute = response.routes[0].legs[0].steps[i].transit.line.short_name; // route number
                    var distance = parseFloat(response.routes[0].legs[0].steps[i].distance['text']); // distance travelled on this bus
                    var departurestop = response.routes[0].legs[0].steps[i].transit.departure_stop.name; // departure address name
                    var arrivalstop = response.routes[0].legs[0].steps[i].transit.arrival_stop.name; // arrival address name
                    var departurelatlng = response.routes[0].legs[0].steps[i].start_location.lat() + ',' + response.routes[0].legs[0].steps[i].start_location.lng(); // departure lat/lng
                    var arrivallatlng = response.routes[0].legs[0].steps[i].end_location.lat() + ',' + response.routes[0].legs[0].steps[i].end_location.lng(); //arrival lat/lng

                    // add each key/value pair to the dictionary
                    routedict['route'] = chosenroute;
                    routedict['distance'] = distance;
                    routedict['departurestop'] = departurestop;
                    routedict['arrivalstop'] = arrivalstop;
                    routedict['departurelatlng'] = departurelatlng;
                    routedict['arrivallatlng'] = arrivallatlng;

                    // append the dictionary to the array
                    stepsarray.push(routedict);
                }
            }

            // create a new dictionary to store walking time and append it to the array
            var timedict = {};
            timedict['walkingtime'] = totalwalking;
            stepsarray.push(timedict);

            //console.log(totalwalking)
            //console.log(stepsamount);
            console.log(stepsarray);

            console.log(stepsarray[0]['route'])
        }
    });
}

$(".dropdown-menu li a").click(function () {
    $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
    $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
});