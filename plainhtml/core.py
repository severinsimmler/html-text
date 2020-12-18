from plainhtml.parser import Parser


def extract(html: str) -> str:
    """[summary]

    Parameters
    ----------
    html : str
        [description]

    Returns
    -------
    str
        [description]
    """
    if html is None or not html.strip():
        return ""
    parser = Parser(html)
    return parser.extract()
