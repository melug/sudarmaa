var remove_bookmark;

remove_bookmark = function(elem, remove_url) {
  return $.post(remove_url, {}, function(data) {
    if (data.error != null) {
      return alert('Error!');
    } else {
      return $(elem).parents('table.bookmark-list tr').remove();
    }
  }, 'json');
};
