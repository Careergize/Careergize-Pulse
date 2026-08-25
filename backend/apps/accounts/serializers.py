from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.organizations.models import Organization
from apps.teams.models import Agent, Team

from .models import User


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "status", "timezone", "created_at", "updated_at"]
        read_only_fields = ["id", "slug", "status", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password]
    )
    organization = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "organization",
            "name",
            "email",
            "phone",
            "role",
            "status",
            "last_login",
            "created_at",
            "updated_at",
            "password",
        ]
        read_only_fields = ["id", "last_login", "created_at", "updated_at"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if password is None:
            validated_data["status"] = User.Status.INVITED
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save(update_fields=["password", "updated_at"])
        return instance


class CurrentUserSerializer(UserSerializer):
    organization_detail = OrganizationSerializer(source="organization", read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields[:-1] + ["organization_detail"]


class TeamSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source="manager.name", read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "manager", "manager_name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_manager(self, manager):
        request = self.context["request"]
        if manager and manager.organization_id != request.user.organization_id:
            raise serializers.ValidationError("Manager must belong to your organization")
        return manager


class AgentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)
    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = Agent
        fields = [
            "id",
            "user",
            "user_name",
            "team",
            "team_name",
            "external_provider_agent_id",
            "extension",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        organization_id = self.context["request"].user.organization_id
        for field in ("user", "team"):
            value = attrs.get(field)
            if value and value.organization_id != organization_id:
                raise serializers.ValidationError({field: "Must belong to your organization"})
        return attrs
