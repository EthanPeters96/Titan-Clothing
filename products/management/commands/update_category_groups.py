from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Updates existing categories with appropriate navigation groups'

    def handle(self, *args, **options):
        # Define category groupings
        clothing_categories = ['hoodies', 't-shirts']
        accessories_categories = ['bags', 'shoes']

        # Update clothing categories
        updated_count = 0
        for category_name in clothing_categories:
            try:
                category = Category.objects.get(name=category_name)
                if not category.group:
                    category.group = 'Clothing'
                    category.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated {category.name} to Clothing group'
                        )
                    )
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Category {category_name} not found'
                    )
                )

        # Update accessories categories
        for category_name in accessories_categories:
            try:
                category = Category.objects.get(name=category_name)
                if not category.group:
                    category.group = 'Accessories'
                    category.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated {category.name} to Accessories group'
                        )
                    )
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Category {category_name} not found'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} categories'
            )
        )
