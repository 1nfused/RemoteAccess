(function () {

  	'use strict';
  	var app = angular.module('RemoteSystemApp', [])

  	app.controller('RemoteSystemController', ['$scope', '$log', '$http',
	  	function($scope, $log, $http) {
	  		$scope.toggle = true;
	  		var base_url = 
	  			'http://' + document.domain + ':' + location.port
	  		var socket = io.connect(base_url + '/latency');

	  		socket.on('connect', function(){
	  			console.log("SOCKET CONNECTED");
	  		});

	  		socket.on('response', function(msg){
	  			console.log(msg);
	  			$scope.latency = "LATENCY " + msg;
	  			console.log($scope.latency);
	  		});

	  		
			$scope.changePitayaState = function(e) {
				$scope.toggle = !$scope.toggle;
				var request = e.target.getAttribute('data-value');
				var url = base_url + '/' + e.target.getAttribute(
					'class').split(" ")[1];

				console.log(url);

		    	$http.post(url, {"request": request})
		    	.success(function(data) {
		    		console.log(data);
		      	})
		    	.error(function(error) {
		        	console.log(error);
		      	});
	  		};
		}
	]);

	app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//');
    });

}());