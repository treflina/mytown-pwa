const { src, dest, series, parallel, watch } = require("gulp");
const sass = require("gulp-sass")(require("sass"));
const cssnano = require("gulp-cssnano");
const autoprefixer = require("gulp-autoprefixer");
const rename = require("gulp-rename");
const babel = require("gulp-babel");
const uglify = require("gulp-uglify");
const imagemin = require("gulp-imagemin");
const sourcemaps = require("gulp-sourcemaps");
const clean = require("gulp-clean");
const browserSync = require("browser-sync").create();
const reload = browserSync.reload;
const exec = require("child_process").exec;

const paths = {
    sass: "./src/sass/**/*.scss",
    js: "./src/js/**/*.js",
    img: "./src/img/*",
    css: "./src/css/**/*.css",
    dist: "./static",
    sassDest: "./static/css",
    jsDest: "./static/js",
    imgDest: "./static/img",
};

function sassCompiler(done) {
    src(paths.sass)
        .pipe(sourcemaps.init())
        .pipe(sass().on("error", sass.logError))
        .pipe(autoprefixer())
        .pipe(dest(paths.sassDest))
        .pipe(cssnano({ zindex: false }))
        .pipe(rename({ suffix: ".min" }))
        .pipe(sourcemaps.write())
        .pipe(dest(paths.sassDest));
    done();
}
function cssCompiler(done) {
    src(paths.css).pipe(dest(paths.sassDest));
    done();
}

function javaScript(done) {
    src(paths.js)
        .pipe(sourcemaps.init())
        .pipe(babel({ presets: ["@babel/env"] }))
        .pipe(uglify())
        .pipe(rename({ suffix: ".min" }))
        .pipe(sourcemaps.write())
        .pipe(dest(paths.jsDest));
    done();
}

function convertImages(done) {
    src(paths.img).pipe(imagemin()).pipe(dest(paths.imgDest));
    done();
}

function cleanStuff(done) {
    src(paths.dist, { read: false }).pipe(clean());
    done();
}

function runserver(done) {
    const proc = exec("python manage.py runserver");
    new Promise(function (resolve, reject) {
        console.log("HTTP Server Started");
        resolve();
    });
    done();
}

function startBrowserSync(done) {
    browserSync.init({
        notify: false,
        port: 8000,
        proxy: "localhost:8000",
    });

    done();
}

function watchForChanges(done) {
    watch("./*.html").on("change", reload);
    watch([paths.sass, paths.js], parallel(sassCompiler, javaScript)).on(
        "change",
        reload
    );
    done();
}

const mainFunctions = parallel(sassCompiler, cssCompiler, javaScript);
exports.cleanStuff = cleanStuff;
exports.convertImages = convertImages;
exports.default = series(
    mainFunctions,
    runserver,
    startBrowserSync,
    watchForChanges
);
