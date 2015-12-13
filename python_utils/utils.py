# -*- coding: utf-8 -*-
"""File contains util public functions to be used daily."""
# ----------------------------------------------------------------------
# @name:        utils.py
# @author:      rafaellott
# @version:     1.0
# @created:     01/12/2015
# ----------------------------------------------------------------------


# version 1.0
def to_unicode(s, encodings=['utf-8', 'latin-1']):
    """Try to decode string to Unicode format."""
    if isinstance(s, (list, tuple)):
        return [to_unicode(i) for i in s]
    if isinstance(s, dict):
        in_dict = {}
        for key in s:
            in_dict[to_unicode(key)] = to_unicode(s[key])
        return in_dict
    elif isinstance(s, str):
        for encoding in encodings:
            try:
                return s.decode(encoding)
            except:
                pass
    return s


# version 1.0
def to_encode(s, encoding='utf-8', errors='strict'):
    """Encode "DEEP" S using the codec registered for encoding.

    Errors may be given to set a different error handling scheme.  Default
    is 'strict' meaning that encoding errors raise a UnicodeEncodeError. Other
    possible values are 'ignore', 'replace' and 'xmlcharrefreplace'
    as well as any other name registered with codecs. Register_error that can
    handle UnicodeEncodeErrors.
    """
    s = to_unicode(s)
    if isinstance(s, unicode):
        return s.encode(encoding, errors)
    if isinstance(s, (list, tuple)):
        return [to_encode(i, encoding=encoding, errors=errors) for i in s]
    if isinstance(s, dict):
        new_dict = {}
        for key in s:
            new_dict[
                to_encode(key, encoding=encoding, errors=errors)
            ] = to_encode(s[key], encoding=encoding, errors=errors)
        return new_dict
    return s
