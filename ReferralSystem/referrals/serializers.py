from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    referral_invite_code = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'invite_code', 'referral_invite_code', 'referrals']

    def get_referral_invite_code(self, obj):
        if obj.referral:
            return obj.referral.invite_code
        return None

    def get_referrals(self, obj):
        referral_list = Profile.objects.filter(referral=obj)
        referral_usernames = [referral.username for referral in referral_list]
        return referral_usernames