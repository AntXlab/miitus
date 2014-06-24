define(['angular'], function () {
    'use strict';

    return ['$scope', 'svc_common_ApiRestangular', function ($scope, ApiRestangular) {
        $scope.search = {};
        $scope.search_title = function () {
            var api = ApiRestangular.all('topics');
            api.get('q', {
                kw: $scope.search.keyword
            }).then(
                function (data) {
                    console.log(data);
                },
                function (err) {
                }
            );
        };

        $scope.$apply();
    }];
});


