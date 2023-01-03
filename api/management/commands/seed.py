from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group


USERS = [
    {
        "name": "admin",
        "password": "admin",
        "is_staff": True,
        "is_superuser": True,
        "groups": ["admin"],
    },
    {
        "name": "support_user",
        "password": "foobarbaz",
        "is_staff": True,
        "is_superuser": False,
        "groups": ["support"],
    },
    {
        "name": "sales_user",
        "password": "foobarbaz",
        "is_staff": True,
        "groups": ["sales"],
    },
]


def _create_users(users):
    for user in users:
        print(f"Trying to create user {user['name']}...")
        u, created = User.objects.get_or_create(username=user["name"])
        if created:
            u.is_staff = user.get("is_staff", False)
            u.is_superuser = user.get("is_superuser", False)
            u.email = user.get("email", "fakemail@fakemail.com")
            u.set_password(user["password"])
            u.save()
            print(f"User {user['name']} created successfully.")
        else:
            print(f"User {user['name']} already exists, updating instead.")

        for group_name in user["groups"]:
            print(f"Adding {user['name']} to group {group_name}.")
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                print(f"/!\\ Group '{group_name}' not found. /!\\")
            else:
                group.user_set.add(u)


class Command(BaseCommand):
    help = "Create groups and add basic users."

    def handle(self, *args, **options):
        # _create_groups(GROUPS)
        _create_users(USERS)
        # _create_contract_statuses()
        # _create_event_statuses()
