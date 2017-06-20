from rest_framework import serializers
from django.db.models import Q
from teamapp.models import Team
from ringapp.models import Member


class MemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Member
        fields = ('id', 'firstname', 'lastname', 'username', 'email', 'role')
        extra_kwargs = {'username': {'validators': []},
                        'email': {'validators': []}}


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    members = MemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ('id', 'team_name', 'members')

    def validate_unique_email(self, validated_data, members_delete):
        '''
        Validate unique email before update
        '''
        instance_id = validated_data.get('id')
        instance_members = validated_data.get('members')
        delete_emails = [member_delete.email
                         for member_delete in members_delete]
        instance_emails = [instance_member.get('email', None)
                           for instance_member in instance_members]
        is_unique = (len(set(instance_emails)) == len(instance_emails))
        if not is_unique:
            raise serializers.ValidationError('Your update data contains duplicate emails.')
        for instance_email in instance_emails:
            if instance_email not in delete_emails and \
               Member.objects.filter(email=instance_email).filter(~Q(team_id=instance_id)).exists():
                raise serializers.ValidationError('Email must be unique.')

    def validate_unique_username(self, validated_data, members_delete):
        '''
        Validate unique username before update
        '''
        instance_id = validated_data.get('id')
        instance_members = validated_data.get('members')
        delete_usernames = [member_delete.username
                            for member_delete in members_delete]
        instance_usernames = [instance_member.get('username', None)
                              for instance_member in instance_members]
        is_unique = (len(set(instance_usernames)) == len(instance_usernames))
        if not is_unique:
            raise serializers.ValidationError('Your update data contains duplicate usernames.')
        for instance_username in instance_usernames:
            if instance_username not in delete_usernames \
               and Member.objects.filter(username=instance_username).filter(~Q(team_id=instance_id)).exists():
                raise serializers.ValidationError('Username must be unique.')

    def validate_unique(self, members_data):
        '''
        Validate unique username and email before creation
        '''
        for member_data in members_data:
            if Member.objects.filter(username=member_data.get('username')).exists():
                raise serializers.ValidationError('Username %s already exists.'
                                                  % (member_data.get('username')))
            elif Member.objects.filter(email=member_data.get('email')).exists():
                raise serializers.ValidationError('%s email already exists.'
                                                  % (member_data.get('email')))

    def create(self, validated_data):
        if 'id' in validated_data:
            validated_data.pop('id')        
        members_data = validated_data.pop('members')    # members only; validated_data pasilieka tik team
        self.validate_unique(members_data)
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
            members_delete = Member.objects.exclude(id__in=instance_ids).exclude(~Q(team_id=instance.id))
            self.validate_unique_email(validated_data, members_delete)
            self.validate_unique_username(validated_data, members_delete)
            members_delete.delete()

            for instance_member in instance_members:
                instance_id = instance_member.get('id', None)

                if instance_id in object_ids:
                    object_member = object_members.get(id=instance_id)
                    object_member.firstname = instance_member.get('firstname', object_member.firstname)
                    object_member.lastname = instance_member.get('lastname', object_member.lastname)
                    object_member.username = instance_member.get('username', object_member.username)
                    object_member.email = instance_member.get('email', object_member.email)
                    object_member.role = instance_member.get('role', object_member.role)
                    object_member.save()
                else:
                    if 'id' in instance_member:
                        instance_member.pop('id')
                    Member.objects.create(team=instance, **instance_member)

        return instance


'''
{
    "id": 18,
    "team_name": "SUPER" ,
    "members": [
        {
            "id": 1,
            "username": "Chab",
            "email": "chab@asd.as",
            "firstname": "FoFo",
            "lastname": "Aliba",
            "role": "defender"
        },
        {
            "id": 2,
            "username": "Chda2",
            "email":"akaa@asd.as",
            "firstname": "GaGa",
            "lastname": "Mago",
            "role": "important"
        },
                {
            "id": 3,
            "username": "Chadd3",
            "email":"aja@asd.as",
            "firstname": "GoGo",
            "lastname": "Vago",
            "role": "manager"
        }

    ]
'''
