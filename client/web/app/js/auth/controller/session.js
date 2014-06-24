define(['angular'], function () {
    'use strict';

    return ['$scope', '$state', 'ApiRestangular', function ($scope, $state, ApiRestangular) {
        // TODO: check if we alreay logined.

        $scope.err_msg = '';
        $scope.user = {};

        $scope.oauth = function () {
            // TODO: await for server side oauth
        };

        $scope.login = function () {
            var login = ApiRestangular.all('users/login/');
            login.post({
                email: $scope.user.email,
                password: $scope.user.password
            }).then(
                function (data) {
                    // go to default state for logined-users.
                    $state.go('user.profile');
                },
                function (err) {
                    // TODO: show error message
                    $scope.err_msg = err.data.error;
                }
            );
        };

        $scope.logout = function () {
            var api = ApiRestangular.one('users/logout/');
            api.get().then(
                function (data) {
                    $state.go('anony.search_topic');
                },
                function (err) {
                }
            );
        };

        $scope.dismiss = function () {
            $scope.err_msg = '';
        };

        $scope.$apply();
    }];
});

