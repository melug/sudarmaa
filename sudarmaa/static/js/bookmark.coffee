remove_bookmark = (elem, remove_url) ->
    $.post remove_url, { }, (data) ->
        if data.error?
            alert 'Error!'
        else
            $(elem).parents('table.bookmark-list tr').remove()
    , 'json'
    
