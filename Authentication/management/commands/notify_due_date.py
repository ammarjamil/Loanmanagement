from datetime import date, timedelta
from django.core.management.base import BaseCommand
from Authentication.models import LoanRequest

class Command(BaseCommand):
    help = 'Send notifications to users before two days of due date'

    def handle(self, *args, **options):
        # Retrieve loan requests two days away from due date
        due_date_threshold = date.today() + timedelta(days=2)
        loan_requests = LoanRequest.objects.filter(due_date=due_date_threshold)

        # Iterate over loan requests and send notifications to users
        for loan_request in loan_requests:
            user = loan_request.user
            # Send notification to the user (e.g., via email, SMS, etc.)
            # Your notification implementation goes here

        self.stdout.write(self.style.SUCCESS('Notifications sent successfully.'))