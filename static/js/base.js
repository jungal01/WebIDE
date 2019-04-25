var languages = {
    "AI": "Ai Detirmined",
    "C": ".c",
    "C++": ".cpp",
    "Java": ".java",
    "JavaScript": ".js",
    "Python": ".py",
    "Rust": ".rs"
};

var cookies=[];
var existingFiles = {};
console.log(existingFiles)

function extractContents(){
    var code = document.getElementById("codebox").value;
    var lang = document.getElementById("language").value;
    var name = document.getElementById("filename").value;
    compile(code, lang, name);
    save(code, lang, name);
}

function save(code="No Code", language, name='Default') {
    cookieValue = language+"::"+code;
    setCookie(name, cookieValue);
}

function loadCookies(){
    var cookies = getAllCookies();
    if (cookies.length != 0){
        populateFiles(cookies);
    }
}

function populateFiles(fileList) {
    var fileBar = document.getElementById("fileNav");
    for (var i = 0; i< fileList.length; i++){
        var nameLangCode = fileList[i].split("=");
        var name = nameLangCode[0];
        var langCode = nameLangCode[1];
        existingFiles[name]=langCode;
    }
    //location.reload();
    for (var key in existingFiles) {
        var name = key
        console.log(name)
        var data = existingFiles[key];
        console.log(data);
        var langCode = data.split("::");
        console.log(langCode);
        console.debug(langCode);
        var lang = langCode[0];
        var code = langCode[1];
        var para = document.createElement("p");
        para.innerHTML="&emsp; &#x1F4C4; "+name;
        para.onclick = function(){
            document.getElementById("language").value = lang;
            document.getElementById("filename").value = key;
            document.getElementById("codebox").value = code;
        }
        para.style.color = "white";
        fileBar.appendChild(para);
        
    }
}

function loadCode(filename){
    var code = document.getElementById("codebox").value;
    var lang = document.getElementById("language").value;
    var name = document.getElementById("filename").value;
    save(code, language, name)
    var langCode = existingFiles[filename].split(":");
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
        save(code, lang, name);
    } 
    location.reload();
    
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
    location.reload();
}

function saveAll() {
    saveFiles();
    for (var key in existingFiles) {
        setCookie(key, existingFiles[key]);
    }
    location.reload();
}

function emptyAll(){
    document.getElementById("codebox").value = "";
    document.getElementById("language").value="AI";
    document.getElementById("filename").value="";
    document.getElementById('output').value='';
}

function dataCollect(){
    var data = document.getElementById('fileDataUploaded').value;
    if (data != ""){
        var nameRest = data.split('=.');
        var name = nameRest[0];
        var langCode = data.split[1].split('::');
        var lang = '.'+langCode[0];
        var code = langCode[1];
        document.getElementById("filename").value = name;
        document.getElementById("codbox").value = code;
        if (lang in languages){document.getElementById("language").value = lang;}
    }
}

$(window).bind("load", function() {
    loadCookies();
    dataCollect();
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
    var lang = response.split("=",1)[1].split(":",1)[0];
    var code = response.split("=",1)[1].split(":",1)[1];
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