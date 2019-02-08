// jQuery
$.getScript('https://maps.googleapis.com/maps/api/js?key=AIzaSyCS1ctp7rWfgpq-rIa6UK4378zagS8iLR8&callback=initMap', function()
{
    // script is now loaded and executed.
    // put your dependent JS here.
    var geocoder;
	var map;
	var marker;

	/*
	 * Google Map with marker
	 */
	function initialize() {
		var initialLat = $('.search_latitude').val();
		var initialLong = $('.search_longitude').val();
		if (navigator.geolocation) {
	        navigator.geolocation.getCurrentPosition(showPosition, showError);
	    }
        
        initialLat = initialLat?initialLat:-6.3646009;
		initialLong = initialLong?initialLong:106.82868860000008;
		var latlng = new google.maps.LatLng(initialLat, initialLong);

		var options = {
			zoom: 16,
			center: latlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};

		map = new google.maps.Map(document.getElementById("geomap"), options);

		geocoder = new google.maps.Geocoder();

		marker = new google.maps.Marker({
			map: map,
			draggable: true,
			position: latlng
		});

		google.maps.event.addListener(marker, "dragend", function () {
			var point = marker.getPosition();
			map.panTo(point);
			geocoder.geocode({'latLng': marker.getPosition()}, function (results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					map.setCenter(results[0].geometry.location);
					marker.setPosition(results[0].geometry.location);
					$('.search_addr').val(results[0].formatted_address);
					$('.search_latitude').val(marker.getPosition().lat());
					$('.search_longitude').val(marker.getPosition().lng());
				}
			});
		});

	}

	function showPosition(position) {
	    var initialLat = position.coords.latitude;
    	var initialLong = position.coords.longitude;
	    var latlng = new google.maps.LatLng(initialLat, initialLong);

		var options = {
			zoom: 16,
			center: latlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};

		map = new google.maps.Map(document.getElementById("geomap"), options);

		geocoder = new google.maps.Geocoder();

		marker = new google.maps.Marker({
			map: map,
			draggable: true,
			position: latlng
		});

		google.maps.event.addListener(marker, "dragend", function () {
			var point = marker.getPosition();
			map.panTo(point);
			geocoder.geocode({'latLng': marker.getPosition()}, function (results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					map.setCenter(results[0].geometry.location);
					marker.setPosition(results[0].geometry.location);
					$('.search_addr').val(results[0].formatted_address);
					$('.search_latitude').val(marker.getPosition().lat());
					$('.search_longitude').val(marker.getPosition().lng());
				}
			});
		});
	}

	function showError(error) {
	    switch(error.code) {
	        case error.PERMISSION_DENIED:
	            console.log("User denied the request for Geolocation.")
	            break;
	        case error.POSITION_UNAVAILABLE:
	            console.log("Location information is unavailable.")
	            break;
	        case error.TIMEOUT:
	            console.log("The request to get user location timed out.")
	            break;
	        case error.UNKNOWN_ERROR:
	            console.log("An unknown error occurred.")
	            break;
	    }
	}

	$(document).ready(function () {
		//load google map
		initialize();
		
		/*
		 * autocomplete location search
		 */
		var PostCodeid = '#search_location';
		$(function () {
			$(PostCodeid).autocomplete({
				source: function (request, response) {
					geocoder.geocode({
						'address': request.term
					}, function (results, status) {
						response($.map(results, function (item) {
							return {
								label: item.formatted_address,
								value: item.formatted_address,
								lat: item.geometry.location.lat(),
								lon: item.geometry.location.lng()
							};
						}));
					});
				},
				select: function (event, ui) {
					$('.search_addr').val(ui.item.value);
					$('.search_latitude').val(ui.item.lat);
					$('.search_longitude').val(ui.item.lon);
					var latlng = new google.maps.LatLng(ui.item.lat, ui.item.lon);
					marker.setPosition(latlng);
					initialize();
				}
			});
		});
		
		/*
		 * Point location on google map
		 */
		$('.get_map').click(function (e) {
			var address = $(PostCodeid).val();
			geocoder.geocode({'address': address}, function (results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					map.setCenter(results[0].geometry.location);
					marker.setPosition(results[0].geometry.location);
					$('.search_addr').val(results[0].formatted_address);
					$('.search_latitude').val(marker.getPosition().lat());
					$('.search_longitude').val(marker.getPosition().lng());
				} else {
					alert("Geocode was not successful for the following reason: " + status);
				}
			});
			e.preventDefault();
		});

		//Add listener to marker for reverse geocoding
		google.maps.event.addListener(marker, 'drag', function () {
			geocoder.geocode({'latLng': marker.getPosition()}, function (results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					if (results[0]) {
						$('.search_addr').val(results[0].formatted_address);
						$('.search_latitude').val(marker.getPosition().lat());
						$('.search_longitude').val(marker.getPosition().lng());
					}
				}
			});
		});
	});
});

// $.ajax({type: 'POST',
// 	url: '/myapp/send/',                            // some data url
// 	data: {param: 'hello', another_param: 5},       // some params  
// 	success: function (response) {                  // callback
// 	    if (response.result === 'OK') {
// 	        if (response.data && typeof(response.data) === 'object') {
// 	            // do something with the successful response.data
// 	            // e.g. response.data can be a JSON object
// 	        }
// 	    } else {
// 	        // handle an unsuccessful response
// 	    }
// 	}
// });