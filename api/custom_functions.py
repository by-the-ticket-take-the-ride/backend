import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import weasyprint
from django.template.loader import render_to_string

from events.models import Ticket
from users.models import User


def draw_ticket_to_pdf(ticket: Ticket) -> bytes:
    """Формирует билет в формате PDF и возвращает его."""
    rendered_html = render_to_string('ticket_pdf.html',
                                     context={'ticket': ticket})

    return weasyprint.HTML(string=rendered_html).write_pdf()


def get_text_email(user: User, ticket: Ticket) -> str:
    """Формирует текст для письма пользователю, который купил билет"""
    name = user.get_full_name() if user.is_authenticated else 'Дорогой друг'
    link_main = 'ticketera.ru'  # Заглушка
    link_tickets = 'ticketera.ru/my_tickets'  # Заглушка
    return (f'Здравствуйте, {name}!<br>'
            f'Во вложении письма находятся '
            f'билеты из вашего заказа {ticket.id}<br>'
            f'{ticket.event.name}\n{ticket.event.description}'
            f'{ticket.event.place.address}<br>'
            f'{ticket.event.date_event} {ticket.event.time_event}<br>'
            f'Ряд: {ticket.row} Место {ticket.seat}<br>'
            f'Для зарегистрированных пользователей сайта '
            f'<a href="{link_main}">TICKETERA</a> билеты '
            f'также доступны для скачивания в личном кабинете в '
            f'разделе <a href="{link_tickets}">Мои билеты</a><br>'
            f'Желаем вам хорошо провести время!<br><br>'
            f'<b>Если письмо пришло вам по ошибке, просто '
            f'проигнорируйте его</b>'
            )


def send_ticket_to_user(ticket: Ticket, user: User) -> None:
    """Функция используется для отправки билета пользователю."""
    email = 'django-test23@yandex.ru'
    password = 'hdgsezhljxqbwwfz'
    target_email = user.email

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = target_email
    msg['Subject'] = f'Билет успешно приобретен {datetime.now()}'
    text_for_email = get_text_email(user, ticket)
    msg.attach(MIMEText(text_for_email, 'html'))

    # Добавление вложения в письмо
    ticket = draw_ticket_to_pdf(ticket)
    attachment = MIMEApplication(ticket, Name="ticket")
    attachment['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
    msg.attach(attachment)

    try:
        mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(email, password)

        mailserver.sendmail(email, target_email, msg.as_string())

        mailserver.quit()
    except smtplib.SMTPException as e:
        print(f'Ошибка: Невозможно отправить сообщение - {str(e)}')
