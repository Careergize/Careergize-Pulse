import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User
from apps.calls.models import Call, CallEvent, CallOutcome, PhoneNumber
from apps.campaigns.models import Campaign
from apps.contacts.models import Contact
from apps.organizations.models import Organization
from apps.teams.models import Agent, Team

OUTCOMES = [
    "Interested",
    "Not Interested",
    "Follow-up Required",
    "Converted",
    "Wrong Number",
    "No Response",
    "Support Request",
    "Existing Customer",
    "Spam",
]


class Command(BaseCommand):
    help = "Seed deterministic, provider-independent call data"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=500)
        parser.add_argument("--organization", default="careergize")

    def handle(self, *args, **options):
        rng = random.Random(20260825)
        org = Organization.objects.get(slug=options["organization"])
        teams = [
            Team.objects.get_or_create(organization=org, name=name)[0]
            for name in ("Admissions", "Sales", "Support")
        ]
        agents = []
        for index in range(8):
            user, _ = User.objects.get_or_create(
                email=f"agent{index + 1}@example.com",
                defaults={
                    "organization": org,
                    "name": f"Agent {index + 1}",
                    "role": User.Role.AGENT,
                },
            )
            agents.append(
                Agent.objects.get_or_create(
                    organization=org,
                    user=user,
                    defaults={"team": teams[index % len(teams)], "extension": str(101 + index)},
                )[0]
            )
        outcomes = [
            CallOutcome.objects.get_or_create(
                organization=org, name=name, defaults={"sort_order": i}
            )[0]
            for i, name in enumerate(OUTCOMES)
        ]
        numbers = [
            PhoneNumber.objects.get_or_create(
                organization=org,
                number=f"+91980000{1000 + i}",
                defaults={"label": f"Tracked line {i + 1}", "team": teams[i % 3]},
            )[0]
            for i in range(6)
        ]
        campaigns = [
            Campaign.objects.get_or_create(organization=org, name=name)[0]
            for name in ("August Intake", "Referral", "Re-engagement")
        ]
        contacts = [
            Contact.objects.get_or_create(
                organization=org,
                name=f"Prospect {i + 1}",
                defaults={"phone_number": f"+9199{i:08d}"},
            )[0]
            for i in range(120)
        ]
        statuses = list(Call.Status.values)
        sources = ["Google Ads", "Website", "Referral", "Organic", "Direct"]
        now = timezone.now()
        created = 0
        for i in range(options["count"]):
            agent = rng.choice(agents)
            contact = rng.choice(contacts)
            tracked = rng.choice(numbers)
            direction = rng.choice(Call.Direction.values)
            status = rng.choices(statuses, weights=[2, 3, 12, 5, 3, 75])[0]
            started = now - timedelta(minutes=rng.randint(0, 60 * 24 * 120))
            ring = rng.randint(3, 45)
            talk = (
                rng.randint(20, 1800)
                if status in {Call.Status.ANSWERED, Call.Status.COMPLETED}
                else 0
            )
            call, was_created = Call.objects.get_or_create(
                organization=org,
                provider="seed",
                provider_call_id=f"seed-{i + 1}",
                defaults={
                    "direction": direction,
                    "caller_number": contact.phone_number
                    if direction == Call.Direction.INBOUND
                    else tracked.number,
                    "receiver_number": tracked.number
                    if direction == Call.Direction.INBOUND
                    else contact.phone_number,
                    "contact": contact,
                    "agent": agent,
                    "team": agent.team,
                    "tracked_number": tracked,
                    "status": status,
                    "started_at": started,
                    "answered_at": started + timedelta(seconds=ring) if talk else None,
                    "ended_at": started + timedelta(seconds=ring + talk),
                    "ring_duration": ring,
                    "talk_duration": talk,
                    "total_duration": ring + talk,
                    "source": rng.choice(sources),
                    "campaign": rng.choice(campaigns),
                    "outcome": rng.choice(outcomes),
                    "follow_up_required": rng.random() < 0.22,
                },
            )
            if was_created:
                created += 1
                CallEvent.objects.create(
                    organization=org,
                    call=call,
                    event_type="initiated",
                    timestamp=started,
                    payload={"seed": True},
                )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {created} calls ({Call.objects.filter(organization=org).count()} total)"
            )
        )
