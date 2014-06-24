// Karma configuration
// http://karma-runner.github.io/0.10/config/configuration-file.html

module.exports = function(config) {
  config.set({
    // base path, that will be used to resolve files and exclude
    basePath: '',

    // testing framework to use (jasmine/mocha/qunit/...)
    frameworks: ['jasmine', 'requirejs'],

    // list of files / patterns to load in the browser
    files: [
      'app/bower_components/angular/angular.js',
      'app/bower_components/angular-mocks/angular-mocks.js',
      'app/bower_components/angular-cookies/angular-cookies.js',
      'app/bower_components/angular-sanitize/angular-sanitize.js',
      'app/bower_components/angular-route/angular-route.js',
      'app/bower_components/jquery/jquery.js',

      // ---- bootstrap js files, need to handle include order manually.
      'app/bower_components/bootstrap-sass/js/dropdown.js',

      'app/bower_components/restangular/dist/restangular.min.js',
      // ---- files needs to be loaded by requirejs
      'app/bower_components/requirejs/require.js',
      {pattern: 'app/js/*.js', included: false},
      {pattern: 'app/js/**/*.js', included: false},
      {pattern: 'app/bower_components/requirejs-domready/domReady.js', included: false},
      {pattern: 'app/bower_components/lodash/dist/lodash.compat.min.js', included: false},

      // test-spec
      {pattern: 'test/mock/**/*.js', included: false},
      {pattern: 'test/spec/**/*.js', include: false},

      // config-file for requirejs when testing
      'test/main.js',
    ],

    // list of files / patterns to exclude
    exclude: [
      'app/js/main.js'
    ],

    // web server port
    port: 8080,

    // level of logging
    // possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: false,


    // Start these browsers, currently available:
    // - Chrome
    // - ChromeCanary
    // - Firefox
    // - Opera
    // - Safari (only Mac)
    // - PhantomJS
    // - IE (only Windows)
    browsers: ['Chrome'],


    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: false,

  });
};
