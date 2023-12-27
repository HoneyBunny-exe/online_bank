from django.template import loader
from django.utils.html import strip_tags, escape
from django.core.mail import send_mail
import threading


def send_message(subject, plain_message, from_email, recipient_list, html_message):
    thread = threading.Thread(target=send_mail, args=(subject, plain_message),
                              kwargs={"from_email": from_email, "recipient_list": recipient_list,
                                      "html_message": html_message})
    thread.start()


def send_confirm_code(user, confirm_code):
    to = user.email
    username = f"{user.second_name.capitalize()}  {user.first_name.capitalize()} {user.third_name.capitalize()}"
    subject = 'Код подверждения'
    html_message = loader.render_to_string("email/confirm_code.html",
                                           {
                                               "title": subject,
                                               "username": username,
                                               "confirm_code": confirm_code
                                           })
    plain_message = strip_tags(escape(html_message))
    send_message(subject, plain_message, None, [to], html_message)


def send_welcome_message(user, account):
    to = user.email
    username = f"{user.second_name.capitalize()}  {user.first_name.capitalize()} {user.third_name.capitalize()}"
    subject = 'Добро пожаловать'
    html_message = loader.render_to_string("email/welcome.html",
                                           {
                                               "title": subject,
                                               "username": username,
                                               "account": account.account_number
                                           })
    plain_message = strip_tags(escape(html_message))
    send_message(subject, plain_message, None, [to], html_message)
