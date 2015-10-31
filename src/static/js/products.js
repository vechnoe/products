// CRSF protect
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    function getCookie(name) {
      var cookieValue = null;
        if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1));
                break;
              }
          }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  }
});


$(document).ready(function() {
  // remove django messages
  setTimeout(function() {
    $('.alert-success').remove();
  }, 10000);
});

$('.make-like').click(function() {
  var product_id = $(this).attr('value');
  var button = this;
  $.ajax({
    url : '/send-like/',
    type : 'POST',
    dataType: 'json',
    data : {
      "productId": product_id
    },
    success: function(response){
      $(button).attr('disabled', true);
      var val = $(button).children(".text-like").text();
      $(button).children(".text-like").text(Number(val) + 1);

      $('#product-messages').html(
        '<div class="alert alert-success" role="alert">' +
          '<p>' + response.message + '<p>' +
        '</div>'
      );

      setTimeout(function() {
        $('.alert-success').remove();
      }, 10000);
    }
  });
});