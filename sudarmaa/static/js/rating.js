$(function() {
  return $("div.star").raty({
    path: "" + static_root + "raty/img",
    start: start_rating,
    click: function(score, evt) {
      $.get("" + this_url + "rate/" + score + "/", function(data) {
        var count;
        count = parseInt($("#rating-count").html());
        return $("#rating-count").html(count + 1);
      });
      return $("div.rating-notification").slideDown(300).delay(1500).fadeOut(300);
    }
  });
});