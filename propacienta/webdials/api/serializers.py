from rest_framework import serializers

from ..models import WebDial


class DialSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebDial
        exclude = [
            "uuid",
            "end_webdial_reason",
            # "webdial_happen"
        ]
