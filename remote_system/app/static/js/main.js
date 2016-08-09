(function () {

  	'use strict';
  	var app = angular.module('RemoteSystemApp', [])
  	app.controller('RemoteSystemController', ['$scope', '$log', '$http',
	  	function($scope, $log, $http) {

			$scope.changePitayaState = function(e) {
				var request = e.target.getAttribute('data-value');
				var url = '/' + e.target.getAttribute(
					'class').split(" ")[1];

				console.log(url)
		    	$http.post(url, {"request": request})
		    	.success(function(results) {
		        	console.log(results);
		      	})
		    	.error(function(error) {
		        	console.log(error);
		      	});
	  		};
		}
	]);
}());