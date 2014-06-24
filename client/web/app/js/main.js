require.config({
    baseUrl: 'js',

    paths: {
        angular: '../bower_components/angular/angular',
        angular_cookies: '../bower_components/angular-cookies/angular-cookies',
        angular_sanitize: '../bower_components/angular-sanitize/angular-sanitize',
        angular_route: '../bower_components/angular-route/angular-route',
        angular_ui_router: '../bower_components/angular-ui-router/release/angular-ui-router.min',
        angular_bootstrap: '../bower_components/angular-bootstrap/ui-bootstrap-tpls.min',
        jquery: '../bower_components/jquery/jquery',
        bootstrap: '../bower_components/bootstrap-sass/js',
        requirejs_domready: '../bower_components/requirejs-domready/domReady',
        restangular: '../bower_components/restangular/dist/restangular.min',
        lodash: '../bower_components/lodash/dist/lodash.compat.min'
    },

    shim: {
        'angular': {
            exports: 'angular'
        },
        'angular_cookies': {
            deps: ['angular']
        },
        'angular_sanitize': {
            deps: ['angular']
        },
        'angular_route': {
            deps: ['angular']
        },
        'angular_ui_router': {
            deps: ['angular'],
        },
        'angular_bootstrap': {
            deps: ['angular'],
        },
        'restangular': {
            deps: ['lodash'],
        },
    },
});

// refer to http://docs.angularjs.org/guide/bootstrap
// 'Deferred Bootstrap'
window.name = 'NG_DEFER_BOOTSTRAP!';

require([
    'angular',
    'app',
    'requirejs_domready',
], function (ng, app) {
    'use strict';

    // trigger bootstrap for the 1st time.
    ng.bootstrap(document, [app.name]);
    ng.resumeBootstrap();
});

