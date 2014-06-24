define([
    'angular',
    'angular_cookies',
    'angular_sanitize',
    'angular_route',
    'angular_ui_router',
    'angular_bootstrap',
    'restangular',
    'common/service',
    'common/controller',
    'auth/controller',
    'topic/controller',
], function (ng) {
    'use strict';

    return ng.module('webApp', [
        'ngCookies',
        'ngSanitize',
        'ngRoute',
        'restangular',
        'ui.router',
        'ui.bootstrap',

        'svc.common',
        'ctrl.common',
        'ctrl.auth',
        'ctrl.topic',
    ])
    .config(function ($stateProvider, $urlRouterProvider) {
        // default url is root
        $urlRouterProvider.otherwise('/');

        var stateSearchTopicResult = {
            url: '/q?kw',
            views: {
                'content@': {
                    templateUrl: 'view/common/topic/result.html'
                },
            },
        };
        var stateTopic = {
            url: '/t/{topic_id}',
            views: {
                'content@': {
                    templateUrl: 'view/common/topic/detail.html'
                },
            },
        };
        var stateGroup = {
            url: '/t/{topic_id}/g/{group_id}',
            views: {
                'content@': {
                    templateUrl: 'view/common/group/detail.html'
                },
            },
        };
        var stateAbout = {
            url: '/about',
            views: {
                'content@': {
                    templateUrl: 'view/common/about.html'
                },
            },
        };
        var stateContactUs = {
            url: '/contact_us',
            views: {
                'content@': {
                    templateUrl: 'view/common/contact_us.html'
                },
            },
        };
        var stateFAQ = {
            url: '/faq',
            views: {
                'content@': {
                    templateUrl: 'view/common/faq.html'
                },
            },
        };
        var stateError = {
            url: '/error',
            views: {
                'content@': {
                    templateUrl: 'view/common/error.html'
                },
            },
        }

        $stateProvider
        //
        // main states
        //
        .state('home', {
            // just a default state to map urlRouteProvider.otherwise
            url: '/',
            views: {
                // TODO: add some view to notify error.
                // we shouldn't navigate to this state.
            }
        })
        .state('anony', {
            abstract: true,
            url: '/a',
            views: {
                'header': {
                    templateUrl: 'view/anony/header.html'
                },
                'header-padding': {
                    template: '<div class="header-fix-height-82"></div>'
                },
                'footer': {
                    templateUrl: 'view/common/footer.html'
                },
            },
        })
        .state('user', {
            abstract: true,
            url: '/u',
            views: {
                'header': {
                    templateUrl: 'view/user/header.html'
                },
                'header-padding': {
                    template: '<div class="header-fix-height-50"></div>'
                },
               'footer': {
                    templateUrl: 'view/common/footer.html'
                },
            },
        })
        //
        // child state
        // - anonymous
        //
        .state('anony.search_topic_result', ng.copy(stateSearchTopicResult))
        .state('anony.topic', ng.copy(stateTopic))
        .state('anony.group', ng.copy(stateGroup))
        .state('anony.search_topic', {
            url: '/search',
            views: {
                'content@': {
                    templateUrl: 'view/common/topic/search.html'
                },
            },
        })
        .state('anony.sign_up', {
            url: '/sign_up',
            views: {
                'content@': {
                    templateUrl: 'view/common/auth/sign_up.html'
                },
            },
        })
        .state('anony.about', ng.copy(stateAbout))
        .state('anony.contact_us', ng.copy(stateContactUs))
        .state('anony.faq', ng.copy(stateFAQ))
        .state('anony.error', ng.copy(stateError))

        //
        // child state
        // - user (logined)
        //
        .state('user.search_topic_result', ng.copy(stateSearchTopicResult))
        .state('user.topic', ng.copy(stateTopic))
        .state('user.group', ng.copy(stateGroup))
        .state('user.profile', {
            url: '/profile',
            views: {
                'content@': {
                    templateUrl: 'view/user/profile.html'
                },
            },
        })
        .state('user.setting', {
            url: '/setting',
            views: {
                'content@': {
                    templateUrl: 'view/user/setting.html'
                },
            },
        })
        .state('user.about', ng.copy(stateAbout))
        .state('user.contact_us', ng.copy(stateContactUs))
        .state('user.faq', ng.copy(stateFAQ))
        .state('user.error', ng.copy(stateError))
        ;
    })
    .run(['$rootScope', '$state', 'svc_common_ApiRestangular', function ($rootScope, $state, ApiRestangular) {
        // init UI state
        $rootScope.ui_state = {};
        $rootScope.ui_state.login = false;

        // init http-response cache, for error
        $rootScope.http_response = {};
        // init an invalid value to status code
        $rootScope.http_response.status = 0;

        // init global user object
        $rootScope.user = {};
        // query user-email from server, once queried, which
        // means we've login.
        var user = ApiRestangular.one('users/login/');
        user.get().then(
            function (data) {
                $rootScope.user.email = data.email;
                $state.go('user.about');
            },
            function (err) {
                $rootScope.ui_state.login = false;
            }
        );

        // TODO: check cookie for user-id
    }]);
});

