
import logging

import requests

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from calls.crm_client import CRMClient


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sync users from the external CRM API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without saving",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        User = get_user_model()
        client = CRMClient()

        try:
            crm_users = client.get_users()
        except (requests.RequestException, ValueError) as exc:
            logger.error("CRM synchronization failed: %s", exc)
            raise CommandError(
                "Unable to fetch CRM users"
            ) from exc

        created_count = 0
        updated_count = 0

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN - No changes will be saved")
            )

        with transaction.atomic():
            for crm_user in crm_users:
                crm_id = crm_user.get("id")
                name = crm_user.get("name", "")
                email = crm_user.get("email", "")

                if not isinstance(crm_id, int) or crm_id <= 0:
                    logger.warning("Skipping invalid CRM user ID")
                    continue

                username = f"crm_user_{crm_id}"

                if not isinstance(email, str) or not email:
                    logger.warning(
                        "Skipping CRM user %s: missing email",
                        crm_id,
                    )
                    continue

                existing_user = User.objects.filter(
                    username=username
                ).first()

                if existing_user:
                    updated_count += 1

                    if not dry_run:
                        existing_user.email = email
                        existing_user.first_name = name[:150]
                        existing_user.save(
                            update_fields=["email", "first_name"]
                        )

                    action = "UPDATE"
                else:
                    created_count += 1

                    if not dry_run:
                        user = User(
                            username=username,
                            email=email,
                            first_name=name[:150],
                            role="agent",
                            is_active=False,
                        )
                        user.set_unusable_password()
                        user.save()

                    action = "CREATE"

                if dry_run:
                    self.stdout.write(
                        f"[{action}] {username} - {email}"
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync completed: "
                f"Created {created_count} new users, "
                f"updated {updated_count} existing users."
            )
        )

        if dry_run:
            self.stdout.write(
                "Dry run completed. No database changes saved."
            )
