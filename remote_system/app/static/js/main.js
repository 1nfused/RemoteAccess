'use strict';
var app = angular.module('RemoteSystemApp', ['ngRoute']);

app.config(
	function($routeProvider) {
		$routeProvider.
	    when("/index", {
	        templateUrl: "/static/templates/main.html"
	    }).
	    when("/gpio", {
	    	templateUrl: "/static/templates/io_pins.html"
	    }).
	    otherwise({
	    	redirectTo : "/#/index"
	    });
	}
);

app.config( 
	function($interpolateProvider) {
		$interpolateProvider.startSymbol('{$').endSymbol('$}');
	}
);

app.controller('basePageController', [
	'$scope', '$http', function($scope, $http) {

	$scope.base_url =
	  		'http://' + document.domain + ':' + location.port
	var url = $scope.base_url + '/index'

	$http.post(url)
		.success(function(response) {
			console.log("SUCCESS");
			$scope.avaliable_pitaya = response.data;
  		})
		.error(function(response) {
    		console.log(response.success);
  	});
}]);

app.controller('mainPageController', [
	'$scope', '$http', function($scope, $http) {

		$scope.state = true;

		$scope.changePitayaState = function(cls, ip, name) {
			console.log(ip)
    		$scope.base_url =
	  			'http://' + document.domain + ':' + location.port
	  		var init_url = $scope.base_url + '/' + cls;
	  		console.log(cls);
			$http.post(init_url, {'ip': ip, 'name': name})
				.success(function(data) {
					if (cls == 'connect') {
						$scope.rp = data.data.rp;
					} else {
						$scope.rp = {
							'ip': '---',
							'name': '---',
							'active': '---',
							'version': '---',
							'fs': '---',
							'fpga': '---'
						}
					}		
	  		})
				.error(function(error) {
	    			console.log(error);
	  		});
		};
	}
]);