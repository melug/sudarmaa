var DictionaryHolder;
$(function() {
  var dictHolder;
  return dictHolder = new DictionaryHolder($('div.dictionary'));
});
DictionaryHolder = (function() {
  function DictionaryHolder(dom) {
    var dictionary_text, result, width;
    this.dom = dom;
    this.dictionary_text = this.dom.find('input[type=text]');
    this.width = this.dictionary_text.css('width');
    this.dom.css({
      right: "-" + this.width
    });
    dom = this.dom;
    width = this.width;
    dictionary_text = this.dictionary_text;
    result = this.dom.find('div.dictionary-result');
    this.dom.find('img').click(function() {
      if (dom.css('right') === ("-" + width)) {
        return dom.animate({
          right: "0px"
        });
      } else {
        return dom.animate({
          right: "-" + width
        });
      }
    });
    this.dictionary_text.focusout(function() {
      dom.animate({
        right: "-" + width
      });
      dictionary_text.val('');
      return result.html('');
    });
    this.dictionary_text.keyup(function() {
      return $.get(dictionary_url, {
        w: $(this).val()
      }, function(data) {
        return result.html(data);
      });
    });
  }
  return DictionaryHolder;
})();