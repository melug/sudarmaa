$ ->
    alert "#{static_root}jquery.raty/img/star-on.png"
    $("div.star").raty({
        starOn: "#{static_root}jquery.raty/img/star-on.png"
        starOff: "#{static_root}jquery.raty/img/star-off.png"
    })
