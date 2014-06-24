define(['angular'], function () {
    'use strict';

    return ['$scope', function ($scope) {
        $scope.$on('$routeChangeStart', function (event, next, current) {
            // clear global http_response
            if (current.originalPath == '/error') {
                $scope.http_response = {}
                $scope.http_response.status = 0;
            }
        });
        $scope.$apply();
    }];
});

