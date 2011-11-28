var add_bookmark, remove_bookmark;

remove_bookmark = function(remove_url, callback) {
  return $.post(remove_url, function(data) {
    if (data.error != null) {
      return alert('Error!');
    } else if (callback != null) {
      return callback();
    }
  }, 'json');
};

add_bookmark = function(add_url, callback) {
  return $.post(add_url, function(data) {
    if (data.error != null) {
      return alert(data.error);
    } else if (callback != null) {
      return callback();
    }
  }, 'json');
};
