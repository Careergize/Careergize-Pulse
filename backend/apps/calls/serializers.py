from rest_framework import serializers

from .models import Call, CallEvent, CallNote, CallOutcome, PhoneNumber


class CallOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallOutcome
        fields = ["id", "name", "active", "sort_order", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class PhoneNumberSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = PhoneNumber
        fields = [
            "id",
            "number",
            "label",
            "provider",
            "provider_number_id",
            "team",
            "team_name",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CallEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallEvent
        fields = [
            "id",
            "call",
            "event_type",
            "provider_event_id",
            "timestamp",
            "payload",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class CallNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = CallNote
        fields = ["id", "call", "author", "author_name", "text", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]


class CallSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source="contact.name", read_only=True)
    agent_name = serializers.CharField(source="agent.user.name", read_only=True)
    team_name = serializers.CharField(source="team.name", read_only=True)
    tracked_number_value = serializers.CharField(source="tracked_number.number", read_only=True)
    outcome_name = serializers.CharField(source="outcome.name", read_only=True)
    campaign_name = serializers.CharField(source="campaign.name", read_only=True)
    events = CallEventSerializer(many=True, read_only=True)
    notes = CallNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Call
        fields = [
            "id",
            "provider",
            "provider_call_id",
            "direction",
            "caller_number",
            "receiver_number",
            "contact",
            "contact_name",
            "agent",
            "agent_name",
            "team",
            "team_name",
            "tracked_number",
            "tracked_number_value",
            "status",
            "started_at",
            "answered_at",
            "ended_at",
            "ring_duration",
            "talk_duration",
            "total_duration",
            "recording_url",
            "source",
            "campaign",
            "campaign_name",
            "outcome",
            "outcome_name",
            "follow_up_required",
            "events",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "events", "notes"]

    def validate(self, attrs):
        org_id = self.context["request"].user.organization_id
        for field in ("contact", "agent", "team", "tracked_number", "campaign", "outcome"):
            value = attrs.get(field)
            if value and value.organization_id != org_id:
                raise serializers.ValidationError({field: "Must belong to your organization"})
        started = attrs.get("started_at", getattr(self.instance, "started_at", None))
        answered = attrs.get("answered_at", getattr(self.instance, "answered_at", None))
        ended = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if answered and started and answered < started:
            raise serializers.ValidationError({"answered_at": "Cannot precede started_at"})
        if ended and started and ended < started:
            raise serializers.ValidationError({"ended_at": "Cannot precede started_at"})
        return attrs
