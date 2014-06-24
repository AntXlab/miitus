define(['angular'], function (ng) {
    'use strict';

    return ['$scope', '$state', 'countryInfo', 'RRestangular', function ($scope, $state, countryInfo, RRestangular) {

        $scope.submit_failed = false;
        $scope.err_msg = '';
        $scope.country_name = '';

        $scope.submit_user = function () {
            $scope.submit_failed = false;
            $scope.err_msg = '';

            var Users = RRestangular.all('users');
            Users.post({
                email: $scope.email,
                password: $scope.login_psswd,
                gender: $scope.genders[$scope.gender_sel],
                loc: countryInfo.get_code($scope.country_name),
                bday: $scope.bday,
            }).then(
                function(data) {
                    $state.go('user.profile');
                },
                function(err) {
                    if ('data' in err && typeof(err.data) === 'object' && 'error' in err.data) {
                        $scope.err_msg = err.data.error;
                    } else {
                        $scope.err_msg = 'submit failed: http[' + err.status + ']';
                    }
                    $scope.submit_failed = true;
                }
            );
        };

        // Password
        $scope.login_psswd = '';
        $scope.show_password_warning = false;
        $scope.check_psswd_strength = function () {
            if (ng.isDefined($scope.login_psswd)) {
                if ($scope.login_psswd.length > 8) {
                    $scope.show_password_warning = false;
                } else {
                    $scope.show_password_warning = true;
                }
            }
        };
        $scope.$watch('login_psswd', $scope.check_psswd_strength);

        // gender
        $scope.gender_sel = 0;
        $scope.genders = ['Gender', 'male', 'female', 'bisexual', 'none'];
        $scope.select_gender = function (idx) {
            if (idx <= 0 || idx >= $scope.genders.length) {
                throw 'invalid index for gender [' + idx + ']';
            }
            $scope.gender_sel = idx;
        };

        $scope.$apply();
    }];
});

