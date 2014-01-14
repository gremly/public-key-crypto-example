from django.shortcuts import get_object_or_404
from rest_framework import serializers

from cipher.models import PublicKey

from M2Crypto import RSA, BIO
import base64

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


class ValidationSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    clear = serializers.CharField(max_length=512)
    crypted = serializers.CharField(max_length=512)

    def validate(self, attrs):
        """
        Tries to decrypt request data with public key
        related to id one.
        """

        # Try to get PublicKey with requested id
        pkey = get_object_or_404(PublicKey, pk=attrs.get('id'))

        #Load public key
        bio = BIO.MemoryBuffer(pkey.key.encode())
        key = RSA.load_pub_key_bio(bio)

        # Try to decrypt using public key
        try:
            decrypted = key.public_decrypt(base64.b64decode(attrs.get('crypted')), RSA.pkcs1_padding)

            # Validate if decrypted text is the same as clear requested one. 
            if decrypted != attrs.get('clear'):
                raise
        except:
            self.errors['encryption error'] = 'Not valid'

        return attrs
