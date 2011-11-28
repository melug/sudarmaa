
$(function() {
  $("input[type=button]").click(function(event) {
    return event.stopPropagation();
  });
  return $("#add-to-bookmark").click(function(event) {
    event.stopPropagation();
    return $.post(bookmark_url, function(data) {
      if (data.error != null) return alert(data.error);
    }, 'json');
  });
});
