from rest_framework import serializers

from apps.annexes.models import Certificate, Application, Building, Driver, Route, Category, Review, Profile, Car


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'color', 'license_plate']


class ProfileSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user_type', 'image', 'name', 'experience', 'phone_number', 'rating', 'car']

    def create(self, validated_data):
        car_data = validated_data.pop('car', None)
        profile = Profile.objects.create(**validated_data)
        if car_data:
            car, created = Car.objects.get_or_create(**car_data)
            profile.car = car
            profile.save()
        return profile

    def update(self, instance, validated_data):
        car_data = validated_data.pop('car', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if car_data:
            car, created = Car.objects.get_or_create(**car_data)
            instance.car = car
        instance.save()
        return instance


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'start_point', 'end_point', 'traffic_condition']