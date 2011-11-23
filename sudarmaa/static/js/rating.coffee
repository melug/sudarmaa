$ ->
    rating_notification = $("div.rating-notification")
    $("div.star").raty({
        path: "#{static_root}raty/img"
        start: start_rating
        click: (score, evt) ->
            $.getJSON "#{this_url}rate/#{score}/", (data) ->
                rating_notification.html(data.message);
                if data.error? and data.error is 9
                    rating_notification.css('color', 'red')
                    rating_notification.slideDown(300).delay(1500).fadeOut(300)
                else
                    count = parseInt($("#rating-count").html())
                    $("#rating-count").html(count+1)
                    rating_notification.slideDown(300).delay(1500).fadeOut(300)
    })
