from datetime import datetime, timedelta
from django.db.models import Q

from events.models import Ticket


def find_tickets_without_payments():
    thirty_minutes_ago = datetime.now() - timedelta(minutes=30)

    Ticket.objects.filter(
        Q(is_paid=False) & Q(pub_date__lt=thirty_minutes_ago)
    ).delete()



