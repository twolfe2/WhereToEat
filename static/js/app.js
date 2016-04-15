'use strict';

var myApp = angular.module('myApp', [
    'ngRoute',
]);


myApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: '/',
            controller: 'MainController',
            controllerAs: 'mainCtrl',
        }).when('/about', {
            templateUrl: '/static/partials/about.html',
        }).when('/cityInfo', {
            templateUrl: '/static/partials/cityInfo.html',
            controller: 'CityController',
            controllerAs: 'cityCtrl',

        }).otherwise({
            redirectTo: '/'
        });
    }]);





myApp.controller('CityController', function ($scope) {
    $scope.greeting = 'Hola!';

});


myApp.controller('MainController', function ($scope) {
    $scope.hello = 'Hola!';
    console.log($scope.hello);

});

//angular.module( "myApp", ['ngAutocomplete'])
//  .controller("TestCtrl",function ($scope) {
//
//    $scope.result1 = '';
//    $scope.options1 = {
//      country: 'us',
//      types: '(cities)'
//    };
//    $scope.details1 = '';
//
//      $scope.mySubmit = function(){
//          $scope.submitted = 'submitted';
//      }
//
//
//  });