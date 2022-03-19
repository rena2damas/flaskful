from apispec_ui.utils import *


def test_parse_url():
    assert url_parse("/path") == "/path/"
    assert url_parse("/path/") == "/path/"
    assert url_parse("/path1/path2") == "/path1/path2/"
    assert url_parse("/path1/path2/") == "/path1/path2/"
    assert url_parse("/") == "/"
    assert url_parse("") == "/"
