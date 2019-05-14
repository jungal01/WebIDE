// Author: Kevin Cobble
// Date: 5-8-2019

//The whole purpose of this file is to be passed the code, language, and name of the file from base.js
// upload it to the server
// recieve the output from the server
// and push it back to the HTML
function compile(code, lang, name='nameMe'){
    $.ajax({
        type: "POST",
        url: '/compile',
        data: {
            param1 : code,
            param2 : lang,
            param3 : name
        },
        success : callbackFunc
    });
}

function callbackFunc(response){
    var returned = response.split("::")[1];
    var lang = response.split("::")[0];
    document.getElementById('language').value = lang;
    document.getElementById('output').value=returned;
}
