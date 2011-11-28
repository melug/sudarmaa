
$(function() {
  $("input[type=button]").click(function(event) {
    return event.stopPropagation();
  });
  return $("#bookmark").click(function(event) {
    event.stopPropagation();
    if (this.checked) {
      return add_bookmark(add_bookmark_url);
    } else {
      return remove_bookmark(remove_bookmark_url);
    }
  });
});
