$ ->
    $('tr.books input[type=checkbox]').change ->
        pk = $(this).val()
        notification_holder = $("#notification-#{pk}")
        if this.checked
            $.post publish_url, { pk: pk, pu: 1 }, (data) ->
                if data.error?
                    notify(notification_holder, 'Error occured')
                else
                    notify(notification_holder, 'Published')
            , 'json'
        else
            $.post publish_url, { pk: pk, pu: 0 }, (data) ->
                if data.error?
                    notify(notification_holder, 'Error occured')
                else
                    notify(notification_holder, 'Unpublished')
            , 'json'

notify = (elem, text) ->

