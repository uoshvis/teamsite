from rest_framework import serializers
from teamapp.models import Team
from ringapp.models import Member


class MemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Member
        fields = ('id', 'firstname', 'lastname', 'username', 'email')


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    members = MemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ('id', 'team_name', 'members')

    def create(self, validated_data):
        if 'id' in validated_data:
            validated_data.pop('id')
        # members only; validated_data lieka tik team
        members_data = validated_data.pop('members')
        team = Team.objects.create(**validated_data)
        for member_data in members_data:
            if 'id' in member_data:
                member_data.pop('id')
            Member.objects.create(team=team, **member_data)
        return team

    def update(self, instance, validated_data):
        instance.team_name = validated_data.get('team_name', instance.team_name)
        instance.save()
        instance_members = validated_data.get('members')
        object_members = instance.get_members()
        object_ids = [object_member.id for object_member in object_members]

        if instance_members:
            instance_ids = [instance_member.get('id', None) for instance_member in instance_members]
            for object_member in object_members:
                if object_member.id not in instance_ids:
                    object_member.delete()

            for instance_member in instance_members:
                instance_id = instance_member.get('id', None)
                if instance_id in object_ids:
                    object_member = object_members.get(id=instance_id)
                    object_member.firstname = instance_member.get('firstname', object_member.firstname)
                    object_member.lastname = instance_member.get('lastname', object_member.lastname)
                    object_member.save()
                else:

                    if 'id' in instance_member:
                        instance_member.pop('id')
                    Member.objects.create(team=instance, **instance_member)

        return instance
