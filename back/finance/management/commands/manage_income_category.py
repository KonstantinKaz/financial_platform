from django.core.management.base import BaseCommand
from finance.models import IncomeCategory

class Command(BaseCommand):
    help = 'Manage income categories (create or delete)'

    def add_arguments(self, parser):
        parser.add_argument('--create', action='store_true', help='Create a new income category')
        parser.add_argument('--delete', action='store_true', help='Delete an existing income category')
        parser.add_argument('title', type=str, help='Title of the income category')

    def handle(self, *args, **options):
        title = options['title']
        create_category = options['create']
        delete_category = options['delete']

        try:
            if create_category and delete_category:
                self.stdout.write(self.style.WARNING('Use either --create or --delete, not both.'))
                return

            if create_category:
                if IncomeCategory.objects.filter(title=title).exists():
                    self.stdout.write(self.style.WARNING(f'Income category with title "{title}" already exists.'))
                else:
                    IncomeCategory.objects.create(title=title, user_id=1)
                    self.stdout.write(self.style.SUCCESS(f'Successfully created a new income category: {title}'))
            elif delete_category:
                if IncomeCategory.objects.filter(title=title).exists():
                    IncomeCategory.objects.filter(title=title).delete()
                    self.stdout.write(self.style.SUCCESS(f'Successfully deleted the income category: {title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Income category with title "{title}" does not exist.'))
            else:
                self.stdout.write(self.style.WARNING('Use either --create or --delete.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))


# commands
#  python manage.py manage_income_category --delete Salary
#  python manage.py manage_income_category --create Salary