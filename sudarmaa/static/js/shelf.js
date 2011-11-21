
$(function() {
  var create_button, shelf_form, shelf_label, shelf_name_input;
  shelf_label = $('li.create-shelf-text a');
  shelf_form = $('li.create-shelf-form');
  shelf_name_input = shelf_form.find('input[type=text]');
  shelf_label.click(function() {
    $(this).parent().remove();
    shelf_form.show();
    return shelf_name_input.focus();
  });
  create_button = shelf_form.find('input[type=button]');
  return create_button.click(function() {
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
});
