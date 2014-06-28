require.config({
    baseUrl: '/base/app/js',

    paths: {
        angular: '../bower_components/angular/angular',
        angular_cookies: '../bower_components/angular-cookies/angular-cookies',
        angular_sanitize: '../bower_components/angular-sanitize/angular-sanitize',
        angular_route: '../bower_components/angular-route/angular-route',
        jquery: '../bower_components/jquery/jquery',
        bootstrap: '../bower_components/bootstrap-sass/js',
        requirejs_domready: '../bower_components/requirejs-domready/domReady',
        restangular: '../bower_components/restangular/dist/restangular.min',
        lodash: '../bower_components/lodash/dist/lodash.compat.min',

        test: '../../test',
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
        'restangular': {
            deps: ['lodash'],
        },
        // not beautiful, shim didn't allow wildchar
        // we have to declare deps for each bootstrap module
        // we included.
        'bootstrap/dropdown': {
            deps: ['jquery'],
            exports: '$.fn.popover'
        },
    },

    deps: [ 
      'app',

      // application js, all loaded in sync
      'controllers/sign_up',
      'controllers/login',

      // testing js, all loaded in sync
      'test/spec/controllers/sign_up',
    ],

    callback: window.__karma__.start
});

