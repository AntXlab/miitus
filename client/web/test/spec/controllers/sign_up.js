
describe('Sign_Up controller', function () {

    beforeEach(module('webApp'));
    beforeEach(inject(function (service_JSLoad) {
        service_JSLoad.set_sync(true);
    }));

    var sign_up = null, scope = null;
    beforeEach(inject(function ($rootScope, $controller) {
        scope = $rootScope.$new();
        sign_up = $controller('ctrl_signUp', {
            $scope: scope
        });
    }));

    it('default status', function () {
        // submit button
        expect(scope.submit_failed).toBe(false);
        expect(scope.err_msg).toBe('');
        // gender
        expect(scope.gender_sel).toBe(0);
    });

    it('should show warning message when password is weak', function () {
        scope.login_psswd = '1';
        scope.$digest();
        expect(scope.show_password_warning).toBe(true);
    });

    it('should throw exception when gender index is invalid', function () {
        expect(function () { scope.select_gender(0); }).toThrow();
        expect(function () { scope.select_gender(scope.genders.length); }).toThrow();

        scope.select_gender(1);
        expect(scope.gender_sel).toBe(1);
    });
});

describe('Sign Up controller, submit to server part', function () {
    
    beforeEach(module('webApp'));
    beforeEach(inject(function (service_JSLoad) {
        service_JSLoad.set_sync(true);
    }));

    var sign_up = null, scope = null, httpB = null;
    beforeEach(inject(function ($rootScope, $controller, $httpBackend) {
        scope = $rootScope.$new();
        httpB = $httpBackend;

        sign_up = $controller('ctrl_signUp', {
            $scope: scope,
        });

        // initialize input
        scope.email = 'q@q.com';
        scope.login_psswd = '123';
        scope.select_gender(1);

    }));

    afterEach(function() {
        httpB.verifyNoOutstandingExpectation();
        httpB.verifyNoOutstandingRequest();
    });

    it ('show http status when no data.error', function () {
        // init status should be ok.
        expect(scope.submit_failed).toBe(false);
        expect(scope.err_msg).toBe('');

        httpB.expectPOST('/r/users/', undefined).respond(502, '');

        // trigger user submittion
        scope.submit_user();

        scope.$digest();
        httpB.flush();

        expect(scope.submit_failed).toBe(true);
        expect(scope.err_msg).toBe('submit failed: http[502]');
    });

    it ('show error message when data.error exists', function () {
        // init status should be ok.
        expect(scope.submit_failed).toBe(false);
        expect(scope.err_msg).toBe('');

        var msg = 'expected failure, never mind.';
        httpB.expectPOST('/r/users/', undefined).respond(502, {'error': msg});

        // trigger user submittion
        scope.submit_user();

        scope.$digest();
        httpB.flush();

        expect(scope.submit_failed).toBe(true);
        expect(scope.err_msg).toBe(msg);
    });

    it ('switch to home page when successful register.', function () {
        // TODO: it's not implemented yet.
    });
});

