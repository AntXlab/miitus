define(['angular'], function (ng) {
    'use strict';

    return ng.module('ctrl.auth', [])
        .controller('ctrl_auth_session', ['svc_common_JSLoad', '$scope', 'svc_common_ApiRestangular', function (JSL, $scope, ApiRestangular) {
            JSL.invoke_('auth/controller/session', this, {'$scope': $scope, 'ApiRestangular': ApiRestangular});
        }])
        .controller('ctrl_auth_sign_up', ['svc_common_JSLoad', '$scope', '$state', 'svc_common_countryInfo', 'svc_common_RRestangular', function (JSL, $scope, $state, countryInfo, RRestangular) {
            JSL.invoke_('auth/controller/sign_up', this, {'$scope': $scope, '$state': $state, 'countryInfo': countryInfo, 'RRestangular': RRestangular});
        }]);
});

