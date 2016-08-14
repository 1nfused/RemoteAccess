'use strict';
var app = angular.module('RemoteSystemApp', ['ngRoute']);

app.factory('connectedPitaya', function($rootScope) {
	console.log("CONNECTED PITAYA");
	var shared_rp = {};
	var rp_init = {
		'ip': 'DISCONNECTED',
		'name': '--',
		'active': '--',
		'version': '--',
		'fs': '--',
		'fpga': '--',
		'connected': false
	};

	shared_rp.rp = rp_init;
	shared_rp.prepBroadCastPitaya = function(data, connected){
		if (data) {
			this.rp = data;
			this.rp.connected = true;
		} else {
			this.rp = rp_init;
		}
		//Broadcast message to all other controllers
		this.broadCastPitaya();
	};

	shared_rp.broadCastPitaya = function() {
		$rootScope.$broadcast('handleBroadcast');
	}

	return shared_rp;
});

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
	    	redirectTo : "/index"
	    });
	}
);

app.config( 
	function($interpolateProvider) {
		$interpolateProvider.startSymbol('{$').endSymbol('$}');
	}
);

app.controller('basePageController', [
	'$scope', '$http', '$rootScope', 'connectedPitaya', 
	function($scope, $http, $rootScope, connectedPitaya) {

	$scope.connected = connectedPitaya.rp.connected;
	$scope.rp = connectedPitaya.rp;

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

	$scope.$on('handleBroadcast', function() {
		$scope.rp = connectedPitaya.rp;
		$scope.connected = connectedPitaya.rp.connected;
	});		
}]);

app.controller('mainPageController', [
	'$scope', '$http', '$rootScope', 'connectedPitaya',
	function($scope, $http, $rootScope, connectedPitaya) {

		$scope.connected = connectedPitaya.connected;
		$scope.rp = connectedPitaya.rp;

		$scope.changePitayaState = function(cls, ip, name) {
    		
    		$scope.base_url =
	  			'http://' + document.domain + ':' + location.port
	  		var init_url = $scope.base_url + '/' + cls;
			$http.post(init_url, {'ip': ip, 'name': name})
				.success(function(data) {
					if (cls == 'connect') {
						connectedPitaya.prepBroadCastPitaya(
							data.data.rp,
							true);
					} else {
						connectedPitaya.prepBroadCastPitaya(
							null,
							false);
					}
	  			})
				.error(function(error) {
	    			console.log(error);
	  		});
		};

		$scope.$on('handleBroadcast', function() {
			console.log("BROADCAST");
			$scope.rp = connectedPitaya.rp;
			$scope.connected = connectedPitaya.rp.connected;
		});
	}
]);