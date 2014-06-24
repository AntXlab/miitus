define(['angular'], function (ng) {
    'use strict';

    return ng.module('svc.common', [])
        .factory('svc_common_RRestangular', function (Restangular) {
            return Restangular.withConfig(function (RestangularConfigurer) {
                RestangularConfigurer.setBaseUrl('/r');
                RestangularConfigurer.setRequestSuffix('/');
            });
        })
        .factory('svc_common_ApiRestangular', function (Restangular) {
            return Restangular.withConfig(function (RestangularConfigurer) {
                RestangularConfigurer.setBaseUrl('/p');
            });
        })
        .service('svc_common_JSLoad', ['$injector', function ($injector) {
            // load async by default
            this.sync_load = false;

            // config function
            this.set_sync = function (bSync) {
                this.sync_load = bSync;
            };

            this.invoke_ = function (ctrl, pThis, param) {
                if (this.sync_load) {
                    var c = require(ctrl);
                    $injector.invoke(c, pThis, param);
                } else {
                    require([ctrl,], function (c) {
                        $injector.invoke(c, pThis, param);
                    });
                }
            };
        }])
        .service('svc_common_countryInfo', ['svc_common_JSLoad', function (JSL) {
            JSL.invoke_('common/service/country', this, {});
        }])
        .factory('svc_common_errInterceptor', function ($q, $location, $rootScope) {
            return {
                'responseError': function (response) {
                    if (response.status == 401) {
                        // TODO: redirect to a specific login page
                        $location.path('/a/search');
                    } else if (response.status >= 500 && response.status < 600) {
                        // cache the response
                        $rootScope.http_response = response;
                        // server side error, redirect to error page.
                        $location.path('/error');
                    }

                    // always continue to process this response.
                    // don't eat it.
                    return $q.reject(response);
                }
            };
        })
        .config(function ($httpProvider) {
            $httpProvider.interceptors.push('svc_common_errInterceptor');
        });
});

