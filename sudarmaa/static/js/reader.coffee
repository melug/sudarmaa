$ ->
    $("input[type=button]").click (event) ->
        event.stopPropagation();

    $("#bookmark").click (event) ->
        event.stopPropagation();
        if this.checked
            add_bookmark add_bookmark_url
        else
            remove_bookmark remove_bookmark_url

