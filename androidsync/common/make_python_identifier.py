# Based on
# https://gist.github.com/JamesPHoughton/3a3f87c6662bf5c9eccc9f2206e228fd

__all__ = [
    "make_python_identifier"
]

from re import (
    compile
)
from keyword import (
    kwlist
)


_spaces = compile("[\\s\\t\\n]+")
_invalid = compile("[^0-9a-zA-Z_]")
_leading_non_letters = compile("^[^a-zA-Z_]+")
_numbered_id = compile(".*?_(\d+)$")


def make_python_identifier(string,
    namespace = None,
    reserved_words = None,
    convert = 'drop',
    handle = 'force'
):
    """
    Takes an arbitrary string and creates a valid Python identifier.
    If the python identifier created is already in the namespace,
    or if the identifier is a reserved word in the reserved_words
    list, or is a python default reserved word,
    adds _1, or if _1 is in the namespace, _2, etc.

    Parameters
    ----------
    string : <basestring>
        The text to be converted into a valid python identifier
    namespace : <dictionary>
        Map existing python identifiers.
        This is to ensure that two strings are not translated into
        the same python identifier and no existing identifier is not
        overwritten.
    reserved_words : <list of strings>
        List of words that are reserved (because they have other meanings
        in this particular program, such as also being the names of
        libraries, etc.
    convert : <string>
        Tells the function what to do with characters that are not
        valid in python identifiers
        - 'hex' implies that they will be converted to their hexidecimal
                representation. This is handy if you have variables that
                have a lot of reserved characters
        - 'drop' implies that they will just be dropped altogether
    handle : <string>
        Tells the function how to deal with namespace conflicts
        - 'force' will create a representation which is not in conflict
                  by appending _n to the resulting variable where n is
                  the lowest number necessary to avoid a conflict
        - 'throw' will raise an exception

    Returns
    -------
    identifier : <string>
        A vaild python identifier based on the input string
    namespace : <dictionary>
        An updated map python identifiers with new identifier pointing to the
        original string.

    References
    ----------
    Identifiers must follow the convention outlined here:
        https://docs.python.org/2/reference/lexical_analysis.html#identifiers
    """

    if namespace is None:
        namespace = {}

    if reserved_words is None:
        reserved_words = []

    # create a working copy (and make it lowercase, while we're at it)
    s = string.lower()

    # remove leading and trailing whitespace
    s = s.strip()

    # Make spaces into underscores
    s = _spaces.sub('_', s)

    if convert == "hex":
        # Convert invalid characters to hex
        s = ''.join([c.encode("hex") if _invalid.findall(c) else c for c in s])

    elif convert == "drop":
        # Remove invalid characters
        s = _invalid.sub('', s)

    # Remove leading characters until we find a letter or underscore
    s = _leading_non_letters.sub('', s)

    # Check that the string is not a python identifier
    while (s in kwlist or
           s in namespace or
           s in reserved_words):
        if handle == "throw":
            raise NameError(s +
                " already exists in namespace or is a reserved word"
            )
        if handle == "force":
            mi = _numbered_id.match(s)
            if mi:
                i = mi.group(1)
                s = s.strip('_' + i) + '_' + str(int(i) + 1)
            else:
                s += "_1"

    namespace[s] = string

    return s, namespace


if __name__ == "__main__":
    print(repr(make_python_identifier('Capital')))
    print("('capital', {'capital': 'Capital'})")

    print(repr(make_python_identifier('multiple words')))
    print("('multiple_words', {'multiple_words': 'multiple words'})")

    print(repr(make_python_identifier('multiple     spaces')))
    print("('multiple_spaces', {'multiple_spaces': 'multiple     spaces'})")

    # When the name is a python keyword, add '_1' to differentiate it
    print(repr(make_python_identifier('for')))
    print("('for_1', {'for_1': 'for'})")

    # TODO: adapt rest
    """
    Remove leading and trailing whitespace
    >>> make_python_identifier('  whitespace  ')
    ('whitespace', {'  whitespace  ': 'whitespace'})

    Remove most special characters outright:
    >>> make_python_identifier('H@t tr!ck')
    ('ht_trck', {'H@t tr!ck': 'ht_trck'})

    Replace special characters with their hex representations
    >>> make_python_identifier('H@t tr!ck', convert='hex')
    ('h40t_tr21ck', {'H@t tr!ck': 'h40t_tr21ck'})

    remove leading digits
    >>> make_python_identifier('123abc')
    ('abc', {'123abc': 'abc'})

    namespace conflicts
    >>> make_python_identifier('Variable$', namespace={'Variable@':'variable'})
    ('variable_1', {'Variable@': 'variable', 'Variable$': 'variable_1'})
    """

    print(repr(make_python_identifier('Variable$',
        namespace = {'variable': 'Variable@', 'variable_1': 'Variable%'}
    )))
    print("('variable_2', {'variable': 'Variable@', 'variable_1': 'Variable%', 'variable_2': 'Variable$'})")

    """
    throw exception instead
    >>> make_python_identifier('Variable$', namespace={'Variable@':'variable'}, handle='throw')
    Traceback (most recent call last):
     ...
    NameError: variable already exists in namespace or is a reserved word
    """
