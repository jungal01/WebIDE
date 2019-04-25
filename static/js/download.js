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
}


