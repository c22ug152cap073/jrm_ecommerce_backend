from rest_framework import serializers
from .models import RecentlyViewed


class RecentlyViewedSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecentlyViewed
        fields = "__all__"