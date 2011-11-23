
$(function() {
  var rating_notification;
  rating_notification = $("div.rating-notification");
  return $("div.star").raty({
    path: "" + static_root + "raty/img",
    start: start_rating,
    click: function(score, evt) {
      return $.getJSON("" + this_url + "rate/" + score + "/", function(data) {
        var count;
        rating_notification.html(data.message);
        if ((data.error != null) && data.error === 9) {
          rating_notification.css('color', 'red');
          return rating_notification.slideDown(300);
        } else {
          count = parseInt($("#rating-count").html());
          $("#rating-count").html(count + 1);
          return rating_notification.slideDown(300).delay(1500).fadeOut(300);
        }
      });
    }
  });
});
