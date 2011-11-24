$ ->
    $('#add-to-shelf').click ->
        $("ul.shelf-list").slideDown(300)
    $("ul.shelf-list a").click ->
        shelf_id = $(this).attr('shelf-id')
        $.post add_book, { s: shelf_id, b: book_id, a: 'add' }, (data) ->
            if data.error?
                alert 'error'
            else
                $('ul.shelf-list').slideUp(300)
        , 'json'

