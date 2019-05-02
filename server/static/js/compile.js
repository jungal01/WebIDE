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
    var returned = response.split(":::")[1];
    var lang = response.split(":::")[0];
    document.getElementById('language').value = lang;
    document.getElementById('output').value=returned;
}
