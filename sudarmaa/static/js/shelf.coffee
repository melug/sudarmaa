$ ->
    shelf_label = $('li.create-shelf-text a')
    shelf_form = $('li.create-shelf-form')
    current_counter = $("li.current-shelf span.book-count")
    shelf_name_input = shelf_form.find 'input[type=text]'
    shelf_label.click ->
        $(this).parent().remove()
        shelf_form.show()
        shelf_name_input.focus()
    create_button = shelf_form.find 'input[type=button]'
    create_button.click ->
        shelf_name = shelf_name_input.val()
        $.post shelf_create_url, { title: shelf_name }, (data) ->
            if data == 'OK'
                window.location.reload()
            else if data == 'Fail'
                alert 'Failed for some reason'
            else
                alert 'Undefined situation'
    shelf_close = $ 'img.close'
    shelf_close.click (event) ->
        event.preventDefault()
        parent = $(this).parents('ul.media-grid > li')
        book_id = parent.attr('book-id')
        $.post shelf_action, { s: shelf_id, b: book_id, a: 'remove' }, (data) ->
            if data.error?
                alert 'error on server'
            else
                current_counter.html(parseInt(current_counter.html())-1)
                parent.fadeOut(1000)
        , 'json'

