var notify;

$(function() {
  return $('tr.books input[type=checkbox]').change(function() {
    var notification_holder, pk;
    pk = $(this).val();
    notification_holder = $("#notification-" + pk);
    if (this.checked) {
      return $.post(publish_url, {
        pk: pk,
        pu: 1
      }, function(data) {
        if (data.error != null) {
          return notify(notification_holder, 'Error occured');
        } else {
          return notify(notification_holder, 'Published');
        }
      }, 'json');
    } else {
      return $.post(publish_url, {
        pk: pk,
        pu: 0
      }, function(data) {
        if (data.error != null) {
          return notify(notification_holder, 'Error occured');
        } else {
          return notify(notification_holder, 'Unpublished');
        }
      }, 'json');
    }
  });
});

notify = function(elem, text) {};
