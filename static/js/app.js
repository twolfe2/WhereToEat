'use strict';

var myApp = angular.module('myApp',[
    'ngRoute'

]);

myApp.config(['$routeProvider',
     function($routeProvider) {
         $routeProvider.
             when('/', {
                 templateUrl: '/static/partials/home.html',
             }).
             when('/about', {
                 templateUrl: '/static/partials/about.html',
             }).
             when('/cityInfo', {
                 templateUrl: '/static/partials/cityInfo.html',
                 //controller: 'LoginController'
             }).
             //when('/logout', {
             //    templateUrl: '../static/partials/home.html',
             //    controller: 'LogoutController'
             //}).
             //when('/signup', {
             //    templateUrl: '../static/partials/signup.html',
             //    controller: 'SignupController'
             //}).
             //when('/reports', {
             //    templateUrl: '../static/partials/reports.html',
             //    controller: 'ReportsController'
             //}).
             otherwise({
                 redirectTo: '/'
             });
    }]);


angular.module( "myApp", ['ngAutocomplete'])
  .controller("TestCtrl",function ($scope) {

    $scope.result1 = '';
    $scope.options1 = {
      country: 'us',
      types: '(cities)'
    };
    $scope.details1 = '';


  });