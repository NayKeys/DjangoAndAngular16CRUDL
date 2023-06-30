# users/management/commands/generate_users.py

from django.core.management.base import BaseCommand
from users.models import generate_users

class Command(BaseCommand):
  help = 'Generates users based on the config.py file'

  def handle(self, *args, **options):
    generate_users()
    self.stdout.write(self.style.SUCCESS('Successfully generated users'))