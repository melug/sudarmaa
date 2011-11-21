$ ->
    shelf_label = $('li.create-shelf-text a')
    shelf_form = $('li.create-shelf-form')
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

