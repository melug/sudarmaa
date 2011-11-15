import re
from django import template
register = template.Library()

@register.filter
def bbcode(value):

    bbdata = [
        (r'\[url\](.+?)\[/url\]', r'<a href="\1">\1</a>'),
        (r'\[url=(.+?)\](.+?)\[/url\]', r'<a href="\1">\2</a>'),
        (r'\[email\](.+?)\[/email\]', r'<a href="mailto:\1">\1</a>'),
        (r'\[email=(.+?)\](.+?)\[/email\]', r'<a href="mailto:\1">\2</a>'),
        (r'\[img\](.+?)\[/img\]', r'<img src="\1">'),
        (r'\[img=(.+?)\](.+?)\[/img\]', r'<img src="\1" alt="\2">'),
        (r'\[b\](.+?)\[/b\]', r'<b>\1</b>'),
        (r'\[i\](.+?)\[/i\]', r'<i>\1</i>'),
        (r'\[u\](.+?)\[/u\]', r'<u>\1</u>'),
        (r'\[h1\](.+?)\[/h1\]', r'<h1>\1</h1>'),
        (r'\[h2\](.+?)\[/h2\]', r'<h2>\1</h2>'),
        (r'\[h3\](.+?)\[/h3\]', r'<h3>\1</h3>'),
        (r'\[h4\](.+?)\[/h4\]', r'<h4>\1</h4>'),
        (r'\[h5\](.+?)\[/h5\]', r'<h5>\1</h5>'),
        (r'\[h6\](.+?)\[/h6\]', r'<h6>\1</h6>'),
        (r'\[quote\](.+?)\[/quote\]', r'<div style="margin-left: 1cm">\1</div>'),
        (r'\[center\](.+?)\[/center\]', r'<div align="center">\1</div>'),
        (r'\[code\](.+?)\[/code\]', r'<tt>\1</tt>'),
        (r'\[big\](.+?)\[/big\]', r'<big>\1</big>'),
        (r'\[small\](.+?)\[/small\]', r'<small>\1</small>'),
        (r'\[youtube\](.+?)\[/youtube\]', r'<iframe width="420" height="315" src="http://www.youtube.com/embed/\1" frameborder="0" allowfullscreen></iframe>')
        ]

    for bbset in bbdata:
        p = re.compile(bbset[0], re.DOTALL)
        value = p.sub(bbset[1], value)

    #The following two code parts handle the more complex list statements
    temp = ''
    p = re.compile(r'\[list\](.+?)\[/list\]', re.DOTALL)
    m = p.search(value)
    if m:
        items = re.split(re.escape('[*]'), m.group(1))
        for i in items[1:]:
            temp = temp + '<li>' + i + '</li>'
        value = p.sub(r'<ul>'+temp+'</ul>', value)

    temp = ''
    p = re.compile(r'\[list=(.)\](.+?)\[/list\]', re.DOTALL)
    m = p.search(value)
    if m:
        items = re.split(re.escape('[*]'), m.group(2))
        for i in items[1:]:
            temp = temp + '<li>' + i + '</li>'
        value = p.sub(r'<ol type=\1>'+temp+'</ol>', value)

    return value
