$('.votebtn').each(function(i, obj) {
  $(this).click(function() {
    $.ajax({
      url: url_array[i],
      data: {
        'choice_id': $(this).val(),
      },
      dataType: 'json',
      success: function(data) {
        var message = "<h3>You selected team: " + data.msg + "</h3><br>";
        $('.totalVotes').html(data.new_total);
        $('.messages').html(message);
      }
    });
    $('.votebtn').each(function() {
      $(this).prop('disabled', true);
    });
  })
});
