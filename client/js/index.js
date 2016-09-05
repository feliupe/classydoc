+function(){

  let $hidden = $('input.hidden');

  $hidden.change(() => {

    $('.file-input > input').val($hidden.val());
    console.log($hidden.val());
  });

  $('.upload-button').click(() => $hidden.trigger('click'));

}();
