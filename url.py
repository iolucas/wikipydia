from urllib.parse import quote, unquote

class URL(object):
    def __init__(self, _quoted, _unquoted):
        self.quoted = _quoted
        self.unquoted = _unquoted

    def __str__(self):
        return self.unquoted

class QuotedURL(URL):
    def __init__(self, _quoted):
        super(QuotedURL, self).__init__(_quoted, unquote(_quoted))

class UnquotedURL(URL):
    def __init__(self, _unquoted):
        super(UnquotedURL, self).__init__(quote(_unquoted), _unquoted)

if __name__ == "__main__":
    unq = UnquotedURL("C++")
    print(unq.quoted)
    print(unq.unquoted)

    quo = QuotedURL("C%2b%2b")
    print(unq.quoted)
    print(unq.unquoted)
