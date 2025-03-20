from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import UserProfile


class Command(BaseCommand):
    help = 'Creates UserProfile objects for users without one'

    def handle(self, *args, **kwargs):
        users_without_profile = []
        for user in User.objects.all():
            try:
                # Check if profile exists
                user.userprofile
            except User.userprofile.RelatedObjectDoesNotExist:
                # Create profile if it doesn't exist
                UserProfile.objects.create(user=user)
                users_without_profile.append(user.username)
        
        if users_without_profile:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created profiles for {len(users_without_profile)} users: {", ".join(users_without_profile)}' # noqa
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All users already have profiles')
            ) 