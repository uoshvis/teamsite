from rest_framework import serializers
from .models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'username', 'email',
                  'firstname', 'lastname', 'role')
        fields = fields + ('date_created', 'date_modified')
