# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# @name:        ajuda.py
# @author:      rafaellott
# @version:     1.0
# @created:     25/11/2015
# ----------------------------------------------------------------------


def to_unicode(s, encodings=['utf-8', 'latin-1']):
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
    # Encodes "DEEP" S using the codec registered for encoding. encoding
    # defaults to the default encoding. errors may be given to set a different
    # error handling scheme. Default is 'strict' meaning that encoding errors
    # raise a UnicodeEncodeError. Other possible values are 'ignore', 'replace'
    # and 'xmlcharrefreplace' as well as any other name registered with
    # codecs.register_error that can handle UnicodeEncodeErrors.
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
    """docstring for """
    def __init__(self):
        self.name = ''
        self.syntax = ''
        self.description = ''
        self.arguments = ''
        self.others = ''

    def add_section_name(self, text):
        self.add_section("NOME", text)

    def add_section_syntax(self, text):
        self.add_section("SINTAXE", text)

    def add_section_description(self, text):
        self.add_section("DESCRIÇÃO", text)

    def add_section(self, name, text):
        # bold SECTION_NAME end_bold \n
        #   \tTEXT\n\n
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
        name = to_encode(name)
        description = to_encode(description)
        type_arg = to_encode(type_arg)
        opt = to_encode((u'[' + opt + ']')) if opt else ''
        default = to_encode((u'[' + default + ']')) if default else ''

        if not self.arguments:
            self.arguments = self.color("PARÂMETROS", "BOLD") + '\n\t'
            self.arguments += (
                self.color(
                    "nome_do_parametro [tipo][opções][valor_padrão]" +
                    "[obrigatório]\n\n",
                    "UNDERLINE"
                )
            )

        mandatory = to_encode((u'[OBRIGATÓRIO]')) if mandatory else ''

        self.arguments += (
            '\t' + self.color(name, 'BOLD') + " [" + type_arg + "]" + opt +
            default + mandatory + '\n' + '\t\t' + description + '\n\n'
        )

    def color(self, text, *colors):
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
            resp += COLOR[cor]
        resp += text
        resp += COLOR['END']
        return resp

    def to_string(self):
        if not (self.name and self.syntax and self.description):
            print("[ERROR] Seções obrigatórias não foram preenchidas!")
        else:
            print(
                to_encode(self.name) + to_encode(self.syntax) +
                to_encode(self.description) +
                to_encode(self.arguments) +
                to_encode(self.others)
            )
