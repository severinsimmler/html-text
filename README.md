# Extract plain text from HTML

## Installation

```
$ pip install plainhtml
```

## Example

```python
>>> import plainhtml
>>> html = "<html><body><p>foo</p><p>bar</p></body></html>"
>>> plainhtml.extract_text(html)
'foo\n\nbar'
```
