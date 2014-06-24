define(['angular'], function (ng) {
    'use strict';

    return ng.module('ctrl.common', [])
        .controller('ctrl_common_err', ['svc_common_JSLoad', '$scope', function (JSL, $scope) {
            JSL.invoke_('common/controller/err', this, {'$scope': $scope});
        }])
        .controller('ctrl_common_country', ['svc_common_JSLoad', '$scope', 'svc_common_countryInfo', function (JSL, $scope, countryInfo) {
            JSL.invoke_('common/controller/country', this, {'$scope': $scope, 'countryInfo': countryInfo});
        }]);
});

