var languages = {
    "AI": "Ai Detirmined",
    "C": ".c",
    "C++": ".cpp",
    "Java": ".java",
    "JavaScript": ".js",
    "Python": ".py",
    "Rust": ".rs",
    "Ruby" :".rb",
    "Bash" :".sh",
    "Lua": ".lua",
    "Go": ".go",
    "Fortran": ".f90",
    "Objective C" :".m",
    "Objective C++" :".mm",
    "ADA": ".adb"
};

var cookies=[];
var existingFiles = {};
console.log(existingFiles)

function extractContents(){
    var code = document.getElementById("codebox").value;
    var lang = document.getElementById("language").value;
    var name = document.getElementById("filename").value;
    save(code, lang, name);
    compile(code, lang, name);
    $("ul").empty();
    loadCookies();
}

function save(code="EmptyCode", language='AI', name='NoName') {
    if (code == ""){code="NoCode"}
    if (language==""){language="AI"}
    if (name==""){name="Defualt"}
    let langCode = language+":::"+code;
    let cookieValue = JSON.stringify(langCode);
    setCookie(name, cookieValue);
}

function loadCookies(){
    //setTimeout(donothing,500);
    var cookies = getAllCookies();
    if (cookies.length != 0){
        populateFiles(cookies);
    }
}

function populateFiles(fileList) {
    var fileBar = document.getElementById("fileList");
    for (var i = 0; i< fileList.length; i++){
        let nameLangCode = fileList[i].split("=");
        let name = nameLangCode[0];
        let langCode = nameLangCode[1];
        let code = JSON.parse(langCode);
        existingFiles[name]=code;
    }
    //location.reload();
    for (var key in existingFiles) {
      if (key != ''){
        let name = key
        console.log(name)
        let data = existingFiles[name];
        console.log(data);
        let langCode = data.split(":::");
        console.log(langCode);
        console.debug(langCode);
        let lang = langCode[0];
        let code = langCode[1].toString();
        let para = document.createElement("li");
        para.innerHTML="&emsp; &#x1F4C4; "+name;
        para.onclick = function(){
            document.getElementById("language").value = lang;
            document.getElementById("filename").value = name;
            document.getElementById("codebox").value = code;
        }
        para.style.color = "white";
        fileBar.appendChild(para);
      }
    }
}

function loadCode(filename){
    var code = document.getElementById("codebox").value;
    var lang = document.getElementById("language").value;
    var name = document.getElementById("filename").value;
    save(code, language, name)
    var langCode = existingFiles[filename].split(":::");
    var lang = langCode[0];
    var code = langCode[1];
    document.getElementById("language").value = lang;
    document.getElementById("filename").value = filename;
    document.getElementById("codbox").value = code;

}

function saveFiles(){
    var txt = "Saving this file will overwrite any previous file with the same name. Are you sure you wish to continue?"
    var r = confirm(txt);
    if (r == true) {
        var code = document.getElementById("codebox").value;
        var lang = document.getElementById("language").value;
        var name = document.getElementById("filename").value;
        console.log(code);
        save(code, lang, name);
    }
    $("ul").empty();
    loadCookies();

}

function removeFile(){
    document.getElementById("codebox").value = "";
    document.getElementById("language").value="AI";
    var name = document.getElementById("filename").value;
    document.getElementById("filename").value="";
    document.getElementById("output").value ="";
    for (var key in existingFiles) {
        if (key == name){
            delete existingFiles[key];
            deleteCookie(key)
        }
    }
    for (var key in existingFiles) {
        setCookie(key, existingFiles[key]);
    }
    $("ul").empty();
    //document.getElementById('fileList').empty();
    loadCookies();
}

function saveAll() {
    saveFiles();
    for (var key in existingFiles) {
        setCookie(key, existingFiles[key]);
    }
    $("ul").empty();
    loadCookies();
}

function emptyAll(){
    document.getElementById("codebox").value = "";
    document.getElementById("language").value="AI";
    document.getElementById("filename").value="";
    document.getElementById('output').value='';
}

// function dataCollect(){
//     var data = document.getElementById('fileDataUploaded').value;
//     if (data != ""){
//         var nameRest = data.split('=.');
//         var name = nameRest[0];
//         var langCode = data.split[1].split(':');
//         var lang = '.'+langCode[0];
//         var code = langCode[1];
//         document.getElementById("filename").value = name;
//         document.getElementById("codbox").value = code;
//         if (lang in languages){document.getElementById("language").value = lang;}
//     }
// }

$(window).bind("load", function() {
    loadCookies();
    // dataCollect();
});




function upload(file){
    $.ajax({
        type: "POST",
        url: '/getfile',
        data: {param:file},
        success : loadFile
    });
}

function uploadFile(){
    var file = document.getElementById("fileToUpload").value;
    upload(file);
    return false;
}

function loadFile(response){
    var name = response.split("=",1)[0];
    var lang = response.split("=",1)[1].split(":::",1)[0];
    var code = response.split("=",1)[1].split(":::",1)[1];
    save(code, language, name);
    loadCookies();
    loadCode(name);
}


//function handler(event){
    //var target = $(event.target);
    //if (target.is("p")){
        //loadCode(target.text);
    //}
//}
//$("p").click(handler).find("aside");
