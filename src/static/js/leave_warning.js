// Author: Kevin Cobble
// Date: 5-8-2019

// this file is currently not in use, as due to a bug we found we had to disable it
// This file generates a warning when you are about to leave the page. We were intending to implement a feature
// that would disable it if you had recently saved, but had never gotten around to it.
// it could probably be implemented with a timer delay of something like 5 minutes that would trigger whenever a save was hit.

$(window).on("beforeunload", function() {
    return "Are you sure? Your work may not be saved!";
});

$(document).ready(function() {
    $("#myForm").on("submit", function(e) {
        //check form to make sure it is kosher
        //remove the ev
        $(window).off("beforeunload");
        return true;
    });
});
