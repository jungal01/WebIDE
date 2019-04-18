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
    document.getElementById('output').value=response;
}

