define(['angular'], function () {
    'use strict';

    return ['$scope', 'countryInfo', function ($scope, countryInfo) {
        $scope.name_list = countryInfo.get_full_name_list();
        $scope.$apply();
    }];
});
