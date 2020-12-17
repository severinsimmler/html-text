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
    parser = Parser(html)
    return parser.extract()
