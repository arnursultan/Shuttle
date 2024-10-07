import redis
from django.conf import settings
from rest_framework import serializers
from django.core.exceptions import ValidationError

r = redis.Redis(
    host=getattr(settings, 'REDIS_HOST', 'localhost'),
    port=getattr(settings, 'REDIS_PORT', 6379),
    db=0
)


class TwoFactorAuthSerializer(serializers.Serializer):
    phone = serializers.CharField()
    verification_code = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get('phone')
        verification_code = data.get('verification_code')

        block_key = f'block_{phone}'
        try:
            if r.get(block_key):
                raise ValidationError("Attempts exhausted. Try again in 10 minutes.")

            redis_key = f'verification_{phone}'
            if r.get(redis_key) != verification_code:
                attempts_key = f'attempts_{phone}'
                attempts = r.incr(attempts_key)

                if attempts >= 5:
                    r.set(block_key, 'blocked', ex=600)
                    r.delete(attempts_key)
                raise ValidationError("Incorrect verification code.")

            r.delete(redis_key)
            r.delete(attempts_key)
        except redis.RedisError as e:
            raise ValidationError(f"Redis error: {str(e)}")

        return data
