from django.db import models
from PIL import Image as PilImage, ExifTags
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator, RegexValidator
from django.core.exceptions import ValidationError

SERVICE_CHOICES = [
    ('LyftX'),
    ('LyftXL'),
    ('Lyft Comfort'),
    ('Lyft Black'),
    ('Lyft Black SUV'),
    ('LyftX  Share'),
    ('Lyft Eco'),
]

REGION_CHOICES = [
    ('Central City'),
    ('Gotham City'),
    ('Metropolis'),
]


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Catalogue title")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catalogue title"
        verbose_name_plural = "Catalogue titles"


class Review(models.Model):
    image = models.ImageField(upload_to='reviews/', verbose_name="Criteria photo")
    text = models.CharField(max_length=255, verbose_name="Feedback")

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"


class Certificate(models.Model):
    image = models.ImageField(upload_to='certificate/')


class Application(models.Model):
    description = models.CharField(max_length=127)
    review = models.CharField(max_length=127)
    message = models.CharField(max_length=255)


class Building(models.Model):
    image = models.ImageField(upload_to='buildings/')
    details = models.TextField()


class Driver(models.Model):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=255)


class DriverProfile(models.Model):
    wallet_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_CHOICES,
    )

    region = models.CharField(
        max_length=10,
        choices=REGION_CHOICES,
    )

    def clean(self):
        if self.wallet_balance < 0:
            raise ValidationError("Your wallet balance cannot be negative.")

        service_minimums = {
            'LyftX': 50,
            'LyftXL': 70,
            'Lyft Comfort': 120,
            'Lyft Black': 250,
            'Lyft Black SUV': 350,
            'LyftX  Share': 100,
            'Lyft Eco': 80,
        }


        if self.wallet_balance < service_minimums.get(self.service_type, 0):
            raise ValidationError(f"Insufficient funds for the type of service '{self.service_type}'.")

        if self.region not in dict(REGION_CHOICES).keys():
            raise ValidationError("Wrong region. Only available: Central City, Gotham City, Metropolis")

    def __str__(self):
        return f"The driver {self.id} - {self.service_type} - {self.region}"


class Car(models.Model):
    make = models.CharField(max_length=100, verbose_name="Brand")
    model = models.CharField(max_length=100, verbose_name="Model")
    color = models.CharField(max_length=50, verbose_name="Colour")
    license_plate = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^[A-Z0-9]+$',
            message="The licence plate shall contain only capital letters and numerals"
        )],
        verbose_name="The licence plate"
    )

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class Profile(models.Model):
    IMAGE_CHOICES = [
        ('driver', 'The driver'),
        ('client', 'Customer'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=IMAGE_CHOICES,
        default='client',
        verbose_name="User type"
    )
    image = models.ImageField(upload_to='profile_images/', verbose_name="Image")
    name = models.CharField(max_length=255, verbose_name="Name")
    experience = models.PositiveIntegerField(verbose_name="Experience (years", default=0)
    phone_number = models.CharField(
        max_length=17,
        validators=[RegexValidator(
            regex=r'^\+1\d{10}$',
            message="The phone number should be in the format: '+1XXXXXXXXXX'. 10 digits are required after the country code."
        )],
        blank=True,
        verbose_name="Phone number"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        verbose_name="Rating"
    )
    car = models.OneToOneField(Car, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user_type})"


class Route(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    TRAFFIC_CONDITIONS = [
        (LOW),
        (MEDIUM),
        (HIGH),
    ]

    start_point = models.CharField(max_length=255, verbose_name="Starting point")
    end_point = models.CharField(max_length=255, verbose_name="End point")
    traffic_condition = models.CharField(
        max_length=10,
        choices=TRAFFIC_CONDITIONS,
        default=LOW,
        verbose_name="Traffic congestion"
    )

    def __str__(self):
        return f"Route from {self.start_point} to {self.end_point} with {self.get_traffic_condition_display()} traffic"