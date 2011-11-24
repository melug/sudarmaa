
$(function() {
  $('#add-to-shelf').click(function() {
    return $("ul.shelf-list").slideDown(300);
  });
  return $("ul.shelf-list a").click(function() {
    var shelf_id;
    shelf_id = $(this).attr('shelf-id');
    return $.post(add_book, {
      s: shelf_id,
      b: book_id,
      a: 'add'
    }, function(data) {
      if (data.error != null) {
        return alert('error');
      } else {
        return $('ul.shelf-list').slideUp(300);
      }
    }, 'json');
  });
});
