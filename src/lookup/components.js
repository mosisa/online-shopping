  
function getCookie(name) {
    var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
    return cookieValue;
}

export function backendLookup(method,endpoint,callback,data){
  let jsondata;
  if(data){
     jsondata= JSON.stringify(data)
  }
  const xhr= new XMLHttpRequest()
  const url= `http://localhost:8000/api${endpoint}`
  xhr.responseType = "json"
  var csrftoken = getCookie('csrftoken');
  xhr.open(method,url)
  xhr.setRequestHeader("Content-Type","application/json")
  if(csrftoken){
   // xhr.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With","XMLHttpRequest")
    xhr.setRequestHeader("X-CSRFToken",csrftoken)
  }
  xhr.onload = function(){
     if(xhr.status === 403){
       const detail = xhr.response.detail
       console.log( detail)
       if(detail==="Authentication credentials were not provided."){
         window.location.href="/login?showLoginRequired=true"
       }
     }
     callback(xhr.response,xhr.status)
}
xhr.onerror = function(e){
  callback ({"message":"the request was an error"},400)
}
xhr.send(jsondata)  
}

