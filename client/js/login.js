$(document).ready(function(){

  const {ipcRenderer} = require('electron')

  $('.login-form').submit(function(e){
    e.preventDefault();

    tmp = $(this).serializeArray()
    obj = {}
    $(tmp).each((i,o) => obj[tmp[i].name] = tmp[i].value)
    console.log(obj)
    ipcRenderer.send('user-login', obj)
  });

  ipcRenderer.on('authorization', (event, arg) => {
    alert(arg)
  })

});
