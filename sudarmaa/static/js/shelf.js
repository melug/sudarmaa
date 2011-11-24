
$(function() {
  var create_button, current_counter, shelf_close, shelf_form, shelf_label, shelf_name_input;
  shelf_label = $('li.create-shelf-text a');
  shelf_form = $('li.create-shelf-form');
  current_counter = $("li.current-shelf span.book-count");
  shelf_name_input = shelf_form.find('input[type=text]');
  shelf_label.click(function() {
    $(this).parent().remove();
    shelf_form.show();
    return shelf_name_input.focus();
  });
  create_button = shelf_form.find('input[type=button]');
  create_button.click(function() {
    var shelf_name;
    shelf_name = shelf_name_input.val();
    return $.post(shelf_create_url, {
      title: shelf_name
    }, function(data) {
      if (data === 'OK') {
        return window.location.reload();
      } else if (data === 'Fail') {
        return alert('Failed for some reason');
      } else {
        return alert('Undefined situation');
      }
    });
  });
  shelf_close = $('img.close');
  return shelf_close.click(function(event) {
    var book_id, parent;
    event.preventDefault();
    parent = $(this).parents('ul.media-grid > li');
    book_id = parent.attr('book-id');
    return $.post(shelf_action, {
      s: shelf_id,
      b: book_id,
      a: 'remove'
    }, function(data) {
      if (data.error != null) {
        return alert('error on server');
      } else {
        current_counter.html(parseInt(current_counter.html()) - 1);
        return parent.hide();
      }
    }, 'json');
  });
});
