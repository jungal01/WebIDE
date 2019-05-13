// This is the base JS file, it must be loaded after all other JS files are loaded to work properly.
// Author: Kevin Cobble
// Date: 5-8-2019

var languages = { //List of languages that are supported by the site
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

function extractContents(){ //retrieves contents from the code box of the HTML, and other boxes to save and compile
    var code = document.getElementById("codebox").value;
    var lang = document.getElementById("language").value;
    var name = document.getElementById("filename").value;
    save(code, lang, name);
    compile(code, lang, name);
    $("ul").empty();
    loadCookies();
}

function save(code="EmptyCode", language='AI', name='NoName') { //function that calls the save.js
    if (code == ""){code="NoCode"}
    if (language==""){language="AI"}
    if (name==""){name="Defualt"}
    let langCode = language+":::"+code;
    let cookieValue = JSON.stringify(langCode);
    setCookie(name, cookieValue);
}

function loadCookies(){ //pulls the cookies from the local site so that it can load and produce different files, if any were saved
    //setTimeout(donothing,500);
    var cookies = getAllCookies();
    if (cookies.length != 0){
        populateFiles(cookies);
    }
}

function populateFiles(fileList) { // creates the list elements that are on the side of the website that you can click on to load the coad
    var fileBar = document.getElementById("fileList");
    for (var i = 0; i< fileList.length; i++){
        let nameLangCode = fileList[i].split("=");
        let name = nameLangCode[0];
        let langCode = nameLangCode[1];
        let code = JSON.parse(langCode);
        existingFiles[name]=code;
    }
    //location.reload();
    for (var key in existingFiles) { // this is the part that actually creates the elements and the click event for the code files
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

function loadCode(filename){ // this function is used by the function loadFile to load the code to the HTML
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

function saveFiles(){ // this is ment to save all of the current code from the side menu
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

function removeFile(){ // this removes the file from the diction, removes the relevent cookie, and then reloads the files, to remove it completely
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

function saveAll() { //this will iterate over the dictionary that stories the cookies, and resave everything
    saveFiles();
    for (var key in existingFiles) {
        setCookie(key, existingFiles[key]);
    }
    $("ul").empty();
    loadCookies();
}

function emptyAll(){ //this clears the page code box, and file name, and language
    document.getElementById("codebox").value = "";
    document.getElementById("language").value="AI";
    document.getElementById("filename").value="";
    document.getElementById('output').value='';
}



$(window).bind("load", function() { //once the page is loaded, this function populates the aside with the files
    loadCookies();
    // dataCollect();
});




function upload(file){ //passes the file the user wishes to upload to the server
    $.ajax({
        type: "POST",
        url: '/getfile',
        data: {param:file},
        success : loadFile
    });
}

function uploadFile(){  // calls the upload function so that the file can be uploaded to the server, this is used for the button click
    var file = document.getElementById("fileToUpload").value;
    upload(file);
    return false;
}

function loadFile(response){ //a function that is called after an upload to save the information as a cookie and then call loadCode
    var name = response.split("=",1)[0];
    var lang = response.split("=",1)[1].split(":::",1)[0];
    var code = response.split("=",1)[1].split(":::",1)[1];
    save(code, language, name);
    loadCookies();
    loadCode(name);
}
