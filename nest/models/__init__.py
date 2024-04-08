from django.db import models
from django.contrib.auth.models import User
from .choices import (
    PropertyStatus,
    PropertyType,
    AdminActionType,
    InteractionType,
    TransactionType,
    UserRole,
)


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)


class ContactInformation(models.Model):
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)


class Property(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=PropertyType.choices)
    address = models.ForeignKey("Address", on_delete=models.CASCADE)
    # location = gis_models.PointField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    price = models.FloatField()
    area = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True, default=0)
    bathrooms = models.IntegerField(null=True, blank=True, default=0)
    amenities = models.JSONField(null=True, blank=True)
    images = models.JSONField()
    status = models.CharField(max_length=10, choices=PropertyStatus.choices)
    analytics = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    contact_information = models.OneToOneField(
        ContactInformation, on_delete=models.CASCADE
    )
    role = models.CharField(max_length=10, choices=UserRole.choices)
    propert_owner_profile = models.ForeignKey(
        "PropertyOwnerProfile",
        on_delete=models.CASCADE,
        related_name="property_owner",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PropertyOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_information = models.OneToOneField(
        ContactInformation, on_delete=models.CASCADE
    )
    bio = models.TextField()
    owned_properties = models.ManyToManyField(Property)


class Transaction(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer_transactions"
    )
    seller_id = models.ForeignKey(
        PropertyOwnerProfile,
        on_delete=models.CASCADE,
        related_name="seller_transactions",
    )
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.FloatField()


class Review(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField(null=True, blank=True)
    date_of_review = models.DateTimeField(auto_now_add=True)


class SavedSearch(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    search_criteria = models.JSONField()
    date_saved = models.DateTimeField(auto_now_add=True)


class Interaction(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(PropertyOwnerProfile, on_delete=models.CASCADE)
    interested_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=InteractionType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)


class AdminAction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=AdminActionType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
