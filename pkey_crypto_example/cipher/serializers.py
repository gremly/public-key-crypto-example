from rest_framework import serializers

from cipher.models import PublicKey

class PublicKeySerializer(serializers.ModelSerializer):
    """
    Main class to manage fields serialization and
    deserialization according to rules defined on PublicKey
    model.
    """
    class Meta:
        model = PublicKey
        fields = ('id', 'key',)
        readonly_fields = ('id',)
