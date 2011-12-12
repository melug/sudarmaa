$ ->
    dictHolder = new DictionaryHolder $ 'div.dictionary'

class DictionaryHolder
    constructor : (@dom)->
        @dictionary_text = @dom.find('input[type=text]')
        @width = @dictionary_text.css 'width'
        @dom.css { right: "-#{@width}"}
        dom = @dom
        width = @width
        result = @dom.find('div.dictionary-result')
        @dom.find('img').click ->
            if dom.css('right') is "-#{width}"
                dom.animate { right: "0px" }
            else
                dom.animate { right: "-#{width}" }
        @dictionary_text.focusout ->
            dom.animate { right: "-#{width}" }
        @dictionary_text.keyup ->
            $.get dictionary_url, { w: $(this).val() }, (data) ->
                result.html(data)
            
