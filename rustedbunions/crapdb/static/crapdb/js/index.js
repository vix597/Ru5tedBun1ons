// Some browser detection from https://stackoverflow.com/questions/9847580/how-to-detect-safari-chrome-ie-firefox-and-opera-browser

// Opera 8.0+
var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;

// Firefox 1.0+
var isFirefox = typeof InstallTrigger !== 'undefined';

// Safari 3.0+ "[object HTMLElementConstructor]" 
var isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && safari.pushNotification));

// Internet Explorer 6-11
var isIE = /*@cc_on!@*/false || !!document.documentMode;

// Edge 20+
var isEdge = !isIE && !!window.StyleMedia;

// Chrome 1+
var isChrome = !!window.chrome && !!window.chrome.webstore;

// Blink engine detection
var isBlink = (isChrome || isOpera) && !!window.CSS;

$(document).ready(function() {
    // NOTE: Change flag before deploy
    console.log("Does anyone look at the console? Flag={__PLACEHOLDER_FLAG__}");

    if (pageError) {
        localStorage.clear();
    } else {
        session_id = localStorage.getItem("session_id")
        if (session_id) {
            window.location = "/crapdb/main/" + session_id + "/";
        }
    }

    if (!isChrome && !isFirefox) {
        errorAlert("This website works best in the latest Chrome or Firefox", options={
            target: $("#alerts"),
            autoclose: 0
        });
    }
});