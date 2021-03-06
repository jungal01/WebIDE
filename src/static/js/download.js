// Author: Eros

function clickedOn(booleanVal) {
    console.log("clicked on")

  if (booleanVal == false) {
    setTimeout(clickedOn(true),20000)
  }
  window.location.reload()
}

  //opening and closing the side menu
function openNav() {
  document.getElementById("sidenav").style.width = "250px";
}
function closeNav() {
  document.getElementById("sidenav").style.width = "0";
}

  //Copy text to clipboard
function copytext() {
  var copyText = document.getElementById("codebox");
  copyText.select();
  document.execCommand("copy");
}

function getBitFiles(lang, name){
  $.ajax({
      type: "POST",
      url: '/bitcode',
      data: {
          param1 : lang,
          param2 : name
      },
      success : downloadBitFiles
  });
}

function downloadBitFiles(response){
  var textToWrite = response[1];
  var textFileAsBlob = new Blob([byteArray], {type: "application/octet-stream"});
  var fileNameToSaveAs = response[0];

  var downloadLink = document.createElement("a");
  downloadLink.download = fileNameToSaveAs;
  downloadLink.innerHTML = "Download File";
  if (window.webkitURL != null) {
      // Chrome allows the link to be clicked
      // without actually adding it to the DOM.
    downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
  } else {
      // Firefox requires the link to be added to the DOM
      // before it can be clicked.
    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
    <!--downloadLink.onclick = destroyClickedElement;-->
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
  }

  downloadLink.click();
}

  //Export function
function saveTextAsFile() {
  var textToWrite = document.getElementById('codebox').value;
  var textFileAsBlob = new Blob([textToWrite], {type: 'text/plain'});
  var lang = document.getElementById("language").value;
  var name = document.getElementById("filename").value;
  var fileNameToSaveAs = name+lang;

  var downloadLink = document.createElement("a");
  downloadLink.download = fileNameToSaveAs;
  downloadLink.innerHTML = "Download File";
  if (window.webkitURL != null) {
      // Chrome allows the link to be clicked
      // without actually adding it to the DOM.
    downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
  } else {
      // Firefox requires the link to be added to the DOM
      // before it can be clicked.
    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
    <!--downloadLink.onclick = destroyClickedElement;-->
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
  }

  downloadLink.click();
  getBitFiles(lang, name);
}
