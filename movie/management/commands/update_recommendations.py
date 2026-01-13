from django.core.management.base import BaseCommand
from movie.recommendations import compute_all_recommendations

class Command(BaseCommand):
    help = 'Pre-computes movie recommendations and caches them.'

    def handle(self, *args, **options):
        self.stdout.write("Starting recommendation update...")
        try:
            compute_all_recommendations()
            self.stdout.write(self.style.SUCCESS("Successfully updated recommendations."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error updating recommendations: {str(e)}"))
