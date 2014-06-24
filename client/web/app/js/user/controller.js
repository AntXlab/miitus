define(['angular'], function (ng) {
    'use strict';

    return ng.module('ctrl.user', [])
        .controller('ctrl_user_profile', ['svc_common_JSLoad', '$scope', function (JSL, $scope) {
            JSL.invoke_('user/controller/profile', this, {'$scope': $scope});
        }])
        .controller('ctrl_user_setting', ['svc_common_JSLoad', '$scope', function (JSL, $scope) {
            JSL.invoke_('user/controller/setting', this, {'$scope': $scope});
        }])
        ;
});
