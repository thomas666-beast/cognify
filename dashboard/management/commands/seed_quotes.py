from django.core.management.base import BaseCommand
from dashboard.models import AntiSpyQuote

class Command(BaseCommand):
    help = 'Seed the database with initial anti-spy quotes'

    def handle(self, *args, **options):
        quotes_data = [
            {
                'quote': "In the digital age, privacy isn't about hiding - it's about controlling what you share and with whom. Your data is your sovereignty.",
                'author': "Digital Rights Advocate"
            },
            {
                'quote': "The greatest weapon against surveillance is awareness. Know your digital footprint, protect your personal space, and reclaim your online autonomy.",
                'author': "Cyber Security Expert"
            },
            {
                'quote': "They watch your every click, track your every move, but they cannot capture your thoughts. Protect your mind as fiercely as you protect your data.",
                'author': "Privacy Philosopher"
            },
            {
                'quote': "Encryption is not a tool for criminals; it's the seal on your digital envelope. Everyone deserves private conversations.",
                'author': "Security Researcher"
            },
            {
                'quote': "When everything is monitored, nothing is sacred. Fight for your right to digital solitude and the freedom to think without being watched.",
                'author': "Digital Freedom Fighter"
            }
        ]

        created_count = 0

        for quote_data in quotes_data:
            quote, created = AntiSpyQuote.objects.get_or_create(
                quote=quote_data['quote'],
                defaults={'author': quote_data['author'], 'is_active': True}
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created quote: {quote_data["quote"][:50]}...')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} quotes')
        )
