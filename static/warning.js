$(window).on("beforeunload", function() {
    return "Are you sure? You didn't finish the form!";
});

$(document).ready(function() {
    $("#myForm").on("submit", function(e) {
        //check form to make sure it is kosher
        //remove the ev
        $(window).off("beforeunload");
        return true;
    });
});