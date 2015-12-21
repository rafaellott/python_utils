# -*- coding: utf-8 -*-
"""Email templates to be used in Django 1.9 projects."""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.signing import Signer
from ecommerce.models import Token
from django.utils import timezone


class _Mail():

    def __init__(
            self, recipient_list=None, subject=None, msg=None, token=None,
            sender="nao-responda@veredaeditora.com.br", fail_silently=True,
            base_url=""):
        self.recipient_list = recipient_list
        self.subject = subject
        self.msg = msg
        self.token = token
        self.sender = sender
        self.fail_silently = fail_silently
        self.base_url = "http://" + base_url

    def send_newsletter(self, corpo, cliente):
        signer = Signer()
        cancel_token = signer.sign(
            'cancel' + timezone.datetime.now().strftime("%d%m%y%H%M")
        ).replace('cancel', 'c')

        # Email body
        plaintext = get_template('email/newsletter.txt')
        htmly = get_template('email/newsletter.html')

        d = {
            'fullname': cliente.user.get_user_name(),
            'destinatario': cliente.user.email,
            'cancel_token': cancel_token,
            'base_url': self.base_url,
            'msg': corpo,
        }

        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(
            self.subject, text_content, self.sender, self.recipient_list)
        msg.attach_alternative(html_content, "text/html")
        return msg.send()

    def send_singup_conf(self, cliente):
        signer = Signer()
        token = signer.sign(
            'validate' + timezone.datetime.now().strftime("%d%m%y%H%M")
        ).replace('validate', 'v')

        delete_token = signer.sign(
            'delete' + timezone.datetime.now().strftime("%d%m%y%H%M")
        ).replace('delete', 'd')

        t = Token(cliente=cliente, token=token)
        t.save()
        del t
        t = Token(cliente=cliente, token=delete_token)
        t.save()
        del t

        # Email body
        plaintext = get_template('email/confirma.txt')
        htmly = get_template('email/confirma.html')

        d = {
            'fullname': cliente.user.get_user_name(),
            'destinatario': cliente.user.email,
            'delete_token': delete_token,
            'base_url': self.base_url,
            'token': token,
        }

        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(
            self.subject, text_content, self.sender, self.recipient_list)
        msg.attach_alternative(html_content, "text/html")
        return msg.send()

    def send_ec_checkout(self, msg):
        pass

    def send_ec_abandones_co(self, msg):
        pass

    def validate_token(self):
        if self.token[0:1] == 'v':  # SIGNUP
            check_token = "validate" + self.token[1:]
            token_type = "v"
        elif self.token[0:1] == 'c':  # CANCEL NEWSLETTER
            check_token = "cancel" + self.token[1:]
            token_type = "c"
        elif self.token[0:1] == 'k':  # RETURN CART
            check_token = "cart" + self.token[1:]
            token_type = "k"
        elif self.token[0:1] == 'd':  # DELETE ACCOUNT
            check_token = "delete" + self.token[1:]
            token_type = "d"

        try:
            Signer().unsign(check_token)
            return token_type
        except:
            # LOG
            return False
