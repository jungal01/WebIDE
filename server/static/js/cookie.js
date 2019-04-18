function setCookie(filename, code) {
  var d = new Date();
  d.setTime(d.getTime() + (60*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = filename + "=" + code + ";" + expires + ";path=/";
}

function getCookie(filename) {
  var name = filename + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function getAllCookies(){
  var decodedCookies = decodeURIComponent(document.cookie);
  return decodedCookies.split(';');
}

function deleteCookie(name){
  document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}