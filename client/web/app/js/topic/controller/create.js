define(['angular'], function () {
    'use strict';

    return ['$scope', '$modalInstance', 'RRestangular', 'ApiRestangular', function ($scope, $modalInstance, RRestangular, ApiRestangular) {

        $scope.topic = {title: '', desc: '', tags: '', tag_selected: ''};
        $scope.save = function () {

            // convert tags to array of tokens.
            var tokens = [];
            if ($scope.topic.tags.length) {
                tokens = $scope.topic.tags.replace(' ', '').split(/[,;]/);
            }

            var api = RRestangular.all('topics');
            api.post({
                title: $scope.topic.title,
                tags: tokens,
                desc: $scope.topic.desc,
            }).then(
                null,
                // TODO: error handling
                null
            )['finally'](
                function () {
                    $modalInstance.close();
                }
            );
        };

        $scope.close = function () {
            $modalInstance.dismiss('cancel');
        };

        $scope.is_loading = false;
        $scope.is_loading_setter = function (scope, isloading) {
            scope.is_loading = is_loading;
        };

        $scope.formatter = function (val) {
            if ($scope.topic.tags.length > 0) {
                $scope.topic.tags += ', ';
            }
            $scope.topic.tags += val;

            return $scope.topic.tags;
        }

        $scope.get_tag_suggestion = function (val) {
            var kw = val.replace(/\s/g, '').split(/[,;]/);

            if ($scope.is_loading) {
                return [];
            }

            // seek the last token
            if (kw.length == 0) {
                return [];
            }

            // let's check the last element
            var last_elm = kw[kw.length - 1];
            if (last_elm.length < 3) {
                // we only suggest when keyword is longer than 3
                return [];
            }

            var api = ApiRestangular.all('tags');
            return api.get('q', {
                kw: last_elm
            })
            .then(
                function (data) {
                    return data['suggest'];
                },
                function (err) {
                    return [];
                }
            );
        };

        $scope.$apply();
    }];
});

