# Generated by Django 4.0.6 on 2022-09-15 07:58

from django.db import migrations
from django.contrib.auth.models import Group, Permission


def _create_contract_statuses(apps, schema_editor):
    ContractStatus = apps.get_model("api", "ContractStatus")
    statuses = ["signed", "pending"]

    for status in statuses:
        print(f"Trying to create contract status '{status}'...")
        s, created = ContractStatus.objects.get_or_create(label=status)
        if created:
            print(f"Contract status '{status}' created successfully.")
        else:
            print(f"Contract status '{status}' already exists.")


def _delete_contract_statuses(apps, schema_editor):
    print("deleting contract statuses from the database...")
    ContractStatus = apps.get_model("api", "ContractStatus")
    ContractStatus.objects.all().delete()


def _create_event_statuses(apps, schema_editor):
    EventStatus = apps.get_model("api", "EventStatus")
    statuses = ["started", "pending", "done"]

    for status in statuses:
        print(f"Trying to create event status '{status}'...")
        s, created = EventStatus.objects.get_or_create(label=status)
        if created:
            print(f"Event status '{status}' created successfully.")
        else:
            print(f"Event status '{status}' already exists.")


def _delete_event_statuses(apps, schema_editor):
    print("deleting event statuses from the database...")
    EventStatus = apps.get_model("api", "EventStatus")
    EventStatus.objects.all().delete()


def _create_groups(apps, schema_editor):
    groups = [
        {
            "name": "admin",
            "permissions": {
                "user": ("view", "add", "change", "delete"),
                "group": ("view", "add", "change", "delete"),
                "customer": ("view", "add", "change", "delete"),
                "contract": ("view", "add", "change", "delete"),
                "event": ("view", "add", "change", "delete"),
                "eventstatus": ("view", "add", "change", "delete"),
                "contractstatus": ("view", "add", "change", "delete"),
            },
        },
        {
            "name": "sales",
            "permissions": {
                "customer": ("view", "add", "change", "delete"),
                "contract": ("view", "add", "change", "delete"),
            },
        },
        {
            "name": "support",
            "permissions": {
                "customer": ("view",),
                "event": ("view", "add", "change", "delete"),
            },
        },
    ]

    for group in groups:
        group_name = group["name"]
        permissions = [
            f"{perm}_{model}"
            for model, perms in group["permissions"].items()
            for perm in perms
        ]

        print(f"Trying to create group '{group_name}'...")
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Group {group_name} created successfully.")
        else:
            print(f"Group {group_name} already exists, updating group instead.")

        perms_list = []
        for codename in permissions:
            print(f"Adding permission '{codename}' to group '{group_name}'.")
            try:
                perm = Permission.objects.get(codename=codename)
            except Permission.DoesNotExist:
                print(f"Permission codename '{codename}' not found.")
            except Exception as e:
                print(f"QWACK {e}")
            else:
                perms_list.append(perm)
        group.permissions.clear()
        group.permissions.add(*perms_list)


def _delete_groups(apps, schema_editor):
    print("\ndeleting groups from database...")
    Group.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(_create_contract_statuses, _delete_contract_statuses),
        migrations.RunPython(_create_event_statuses, _delete_event_statuses),
        migrations.RunPython(_create_groups, _delete_groups),
    ]
