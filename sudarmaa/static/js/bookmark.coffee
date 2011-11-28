remove_bookmark = (remove_url, callback) ->
    $.post remove_url, (data) ->
        if data.error?
            alert 'Error!'
        else if callback?
            callback()
    , 'json'
    
add_bookmark = (add_url, callback) ->
    $.post add_url, (data) ->
        if data.error?
            alert data.error
        else if callback?
            callback()
    , 'json'

