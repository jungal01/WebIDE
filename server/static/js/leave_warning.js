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