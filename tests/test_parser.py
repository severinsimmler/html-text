import plainhtml


def test_extract_no_text_html():
    html = (
        '<!DOCTYPE html><html><body><p><video width="320" height="240" '
        'controls><source src="movie.mp4" type="video/mp4"><source '
        'src="movie.ogg" type="video/ogg"></video></p></body></html>'
    )
    assert plainhtml.extract(html) == ""


def test_extract():
    html = "<html><style>.div {}</style>" "<body><p>Hello,   world!</body></html>"
    assert plainhtml.extract(html) == "Hello, world!"


def test_declared_encoding():
    html = (
        '<?xml version="1.0" encoding="utf-8" ?>'
        "<html><style>.div {}</style>"
        "<body>Hello,   world!</p></body></html>"
    )
    assert plainhtml.extract(html) == "Hello, world!"


def test_empty():
    assert plainhtml.extract("") == ""
    assert plainhtml.extract(" ") == ""
    assert plainhtml.extract(None) == ""


def test_inline_tags_whitespace():
    html = "<span>field</span><span>value  of</span><span></span>"
    assert plainhtml.extract(html) == "field value of"


def test_nbsp():
    html = "<h1>Foo&nbsp;Bar</h1>"
    assert plainhtml.extract(html) == "Foo Bar"


def test_adjust_newline():
    html = u"<div>text 1</div><p><div>text 2</div></p>"
    assert plainhtml.extract(html) == "text 1\n\ntext 2"
def test_punct_whitespace_preserved():
    html = (u'<div><span>по</span><span>ле</span>, and  ,  '
            u'<span>more </span>!<span>now</div>a (<b>boo</b>)')
    text = plainhtml.extract(html)
    assert text == u'по ле, and , more ! now a (boo)'

"""

def test_punct_whitespace():
    html = '<div><span>field</span>, and more</div>'
    assert plainhtml.extract(html) == "nice"



def test_punct_whitespace_preserved():
    html = (u'<div><span>по</span><span>ле</span>, and  ,  '
            u'<span>more </span>!<span>now</div>a (<b>boo</b>)')
    text = plainhtml.extract(html)
    assert text == u'по ле, and , more ! now a (boo)'


def test_guess_layout():
    html = (u'<title>  title  </title><div>text_1.<p>text_2 text_3</p>'
            '<p id="demo"></p><ul><li>text_4</li><li>text_5</li></ul>'
            '<p>text_6<em>text_7</em>text_8</p>text_9</div>'
            '<script>document.getElementById("demo").innerHTML = '
            '"This should be skipped";</script> <p>...text_10</p>')

    text = 'title text_1. text_2 text_3 text_4 text_5 text_6 text_7 ' \
           'text_8 text_9 ...text_10'
    assert plainhtml.extract(html, guess_punct_space=False, guess_layout=False) == text

    text = ('title\n\ntext_1.\n\ntext_2 text_3\n\ntext_4\ntext_5'
            '\n\ntext_6 text_7 text_8\n\ntext_9\n\n...text_10')
    assert plainhtml.extract(html, guess_punct_space=False, guess_layout=True) == text

    text = 'title text_1. text_2 text_3 text_4 text_5 text_6 text_7 ' \
           'text_8 text_9...text_10'
    assert plainhtml.extract(html, guess_punct_space=True, guess_layout=False) == text

    text = 'title\n\ntext_1.\n\ntext_2 text_3\n\ntext_4\ntext_5\n\n' \
           'text_6 text_7 text_8\n\ntext_9\n\n...text_10'
    assert plainhtml.extract(html, guess_punct_space=True, guess_layout=True) == text


def test_basic_newline():
    html = u'<div>a</div><div>b</div>'
    assert plainhtml.extract(html, guess_punct_space=False, guess_layout=False) == 'a b'
    assert plainhtml.extract(html, guess_punct_space=False, guess_layout=True) == 'a\nb'
    assert plainhtml.extract(html, guess_punct_space=True, guess_layout=False) == 'a b'
    assert plainhtml.extract(html, guess_punct_space=True, guess_layout=True) == 'a\nb'


def test_personalize_newlines_sets():
    html = (u'<span><span>text<a>more</a>'
            '</span>and more text <a> and some more</a> <a></a> </span>')

    text = plainhtml.extract(html, guess_layout=True,
                        newline_tags=NEWLINE_TAGS | {'a'})
    assert text == 'text\nmore\nand more text\nand some more'

    text = plainhtml.extract(html, guess_layout=True,
                        double_newline_tags=DOUBLE_NEWLINE_TAGS | {'a'})
    assert text == 'text\n\nmore\n\nand more text\n\nand some more'

"""
