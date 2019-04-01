function extractContents(){
    var code = document.getElementById("codebox").value;
    Pythoncall(code, 'py', 0);
}

function Pythoncall(code, lang, api){
    $.ajax({
        type: "POST",
        url: '/compile',
        data: {param1 : code,
            param2 : lang,
            param3 : api
        },
        success : callbackFunc
    });
}

function callbackFunc(response){
    document.getElementById('output').value=response;
}