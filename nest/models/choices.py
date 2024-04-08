from django.db import models

# from django.contrib.gis.db import models as gis_models


# Define Enums
class PropertyType(models.TextChoices):
    HOUSE = "house", "House"
    APARTMENT = "apartment", "Apartment"
    CONDO = "condo", "Condo"
    VILLA = "villa", "Villa"
    OTHER = "other", "Other"


class PropertyStatus(models.TextChoices):
    FOR_SALE = "for_sale", "For Sale"
    FOR_RENT = "for_rent", "For Rent"
    SOLD = "sold", "Sold"
    RENTED = "rented", "Rented"
    OTHER = "other", "Other"


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"


class TransactionType(models.TextChoices):
    SALE = "sale", "Sale"
    RENT = "rent", "Rent"


class InteractionType(models.TextChoices):
    INQUIRY = "inquiry", "Inquiry"
    VIEWING = "viewing", "Viewing"
    OFFER = "offer", "Offer"


class AdminActionType(models.TextChoices):
    APPROVE = "approve", "Approve"
    REJECT = "reject", "Reject"
    PENDING = "pending", "Pending"
    CANCEL = "cancel", "Cancel"
    SOLD = "sold", "Sold"
    RENTED = "rented", "Rented"
    OTHER = "other", "Other"
