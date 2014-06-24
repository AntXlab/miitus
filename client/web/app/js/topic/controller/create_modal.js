 define(['angular'], function () {
    'use strict';

    return ['$scope', '$modal', function ($scope, $modal) {

        $scope.launch_modal = function () {
            var modal_instance = $modal.open({
                templateUrl: 'view/common/topic/create.html',
                controller: 'ctrl_topic_create',
            });

            modal_instance.result.then(
                null,
                null
            );
        };

        $scope.$apply();
    }];
});

