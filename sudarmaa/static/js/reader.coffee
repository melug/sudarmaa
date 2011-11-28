$ ->
    $("input[type=button]").click (event) ->
        event.stopPropagation();

    $("#add-to-bookmark").click (event) ->
        event.stopPropagation();
        $.post bookmark_url, (data) ->
            if data.error?
                alert data.error
        , 'json'
