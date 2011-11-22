$ ->
    $("div.star").raty({
        path: "#{static_root}raty/img"
        start: start_rating
        half: true
        click: (score, evt) ->
            $.get "#{this_url}rate/#{score}/", (data) ->
                count = parseInt($("#rating-count").html())
                $("#rating-count").html(count+1)
            $("div.rating-notification").slideDown(300).delay(1500).fadeOut(300)
    })
