u"""Arquivo responsável por criar o manual de uso do script."""
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# @name:        ajuda.py
# @author:      rafaellott
# @version:     1.0
# @created:     25/11/2015
# ----------------------------------------------------------------------


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


class Ajuda(object):
    """Class responsible to create the manual page for an script."""

    def __init__(self):
        """Constructor Class.

        Keyword arguments:
        name        => Section NAME (Contains the script name)
        syntax      => Section SYNTAX (Show how to script syntax)
        description => Section DESCRIPTION (More detail for the script)
        arguments   => Section ARGUMENTS (Sections with the script arguments)
        others      => Section OTHERS (If you need to create more sections)
        """
        self.name = ''
        self.syntax = ''
        self.description = ''
        self.arguments = ''
        self.others = ''

    def add_section_name(self, text):
        """Add the string for the section NAME (In portuguese).

        Keyword arguments:
        text -- the string that will be shown (string - required)
        """
        self.add_section("NOME", text)

    def add_section_syntax(self, text):
        """Add the string for the section SYNTAX (In portuguese).

        Keyword arguments:
        text -- the string that will be shown (string - required)
        """
        self.add_section("SINTAXE", text)

    def add_section_description(self, text):
        """Add the string for the section DESCRIOPTION (In portuguese).

        Keyword arguments:
        text -- the string that will be shown (string - required)
        """
        self.add_section("DESCRIÇÃO", text)

    def add_section(self, name, text):
        """Add a new section based on the parameter given.

        Keyword arguments:
        name -- section title (string - required)
        text -- section description that will be shown (string - required)
        """
        name = to_encode(name.upper())
        text = to_encode(text)
        if name == "NOME":
            self.name = (
                self.color(name, "BOLD") + '\n\t' + text + '\n\n')
        elif name == "SINTAXE":
            self.syntax = (
                self.color(name, "BOLD") + '\n\t' + text + '\n\n')
        elif name == "DESCRIÇÃO":
            self.description = (
                self.color(name, "BOLD") + '\n\t' + text + '\n\n')
        else:
            name = to_encode(name)
            text = to_encode(text)
            self.others = self.others + (
                self.color(name, "BOLD") + '\n\t' + text + '\n\n')

    def add_arguments(
        self, name, description, type_arg, opt=None, default=None,
        mandatory=False
    ):
        """Add a each parameter in section ARGUMENTS.

        Keyword arguments:
        name -- parameter name (string - required)
        descriptiion -- description for the parameter (string - required)
        type_arg -- type of the parameter (string - required)
        opt -- possible options for parameter (string - default:None)
        default -- dafault value for parameter (string - default:None)
        mandatory -- if parameter is required (boolean - default: None)
        """
        name = to_encode(name)
        description = to_encode(description)
        type_arg = to_encode(type_arg)
        mandatory = to_encode(u'OBRIGATÓRIO') if mandatory else 'none'
        opt = to_encode(opt) if opt else 'none'
        default = to_encode(default) if default else 'none'

        if not self.arguments:
            self.arguments = self.color("PARÂMETROS", "BOLD") + '\n\t'
            self.arguments += (
                self.color(
                    "nome_do_parametro [tipo][opções][valor_padrão]" +
                    "[obrigatório]\n\n",
                    "UNDERLINE"
                )
            )

        self.arguments += (
            '\t' + self.color(name, 'BOLD') + ' [' + type_arg + ']' +
            '[' + opt + '][' + default + '][' + mandatory + ']\n' +
            '\t\t' + description + '\n\n'
        )

    def color(self, text, *colors):
        """Print message with color, bold or underline.

        Keyword arguments:
        text -- text that will be customize (string - required)
        colors -- color name to be printed (array|string - required)

        Colors options:
        PURPLE, CYAN, DARKCYAN, BLUE, GREEN, YELLOW, RED, BOLD, UNDERLINE
        """
        COLOR = {
            'PURPLE': '\033[95m',
            'CYAN': '\033[96m',
            'DARKCYAN': '\033[36m',
            'BLUE': '\033[94m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m',
            'END': '\033[0m'
        }
        resp = ''
        for cor in colors:
            resp += COLOR[cor.upper()]
        resp += text
        resp += COLOR['END']
        return resp

    def to_string(self):
        """Add a each parameter in section ARGUMENTS.

        Keyword arguments:
        name -- parameter name (string - required)
        descriptiion -- description for the parameter (string - required)
        type_arg -- type of the parameter (string - required)
        opt -- possible options for parameter (string - default:None)
        default -- dafault value for parameter (string - default:None)
        mandatory -- if parameter is required (boolean - default: None)
        """
        if not (self.name and self.syntax and self.description):
            print("[ERROR] Seções obrigatórias não foram preenchidas!")
        else:
            print(
                to_encode(self.name) + to_encode(self.syntax) +
                to_encode(self.description) +
                to_encode(self.arguments) +
                to_encode(self.others)
            )
