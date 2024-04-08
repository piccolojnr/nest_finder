from django.test import TestCase
from nest.models import (
    Address,
    ContactInformation,
    Property,
    User,
    PropertyOwnerProfile,
    Transaction,
    Review,
    SavedSearch,
    Interaction,
    AdminAction,
)


class ModelTestCase(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.address = Address.objects.create(
            street="123 Main St", city="City", state="State", zipcode="12345"
        )
        self.contact_info = ContactInformation.objects.create(
            phone="123-456-7890", email="test@example.com", address=self.address
        )
        self.user = User.objects.create(
            username="test_user",
            email="user@example.com",
            profile_picture="http://example.com/profile.jpg",
            contact_information=self.contact_info,
            role="user",
        )
        self.property = Property.objects.create(
            user=self.user,
            title="Test Property",
            description="Test description",
            type="house",
            address=self.address,
            latitude=1,
            longitude=2,
            price=100000,
            area=1000,
            bedrooms=3,
            bathrooms=2,
            amenities=["Swimming pool", "Garden"],
            images=["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
            status="for_sale",
            analytics={"views": 100, "likes": 50},
        )
        self.property_owner_profile = PropertyOwnerProfile.objects.create(
            user=self.user, contact_information=self.contact_info, bio="Test bio"
        )
        self.transaction = Transaction.objects.create(
            property_id=self.property,
            buyer_id=self.user,
            seller_id=self.property_owner_profile,
            transaction_type="sale",
            transaction_amount=90000,
        )
        self.review = Review.objects.create(
            property_id=self.property,
            reviewer_id=self.user,
            rating=5,
            review_text="Great property!",
        )
        self.saved_search = SavedSearch.objects.create(
            user_id=self.user,
            search_criteria={"type": "house", "price_range": [50000, 150000]},
        )
        self.interaction = Interaction.objects.create(
            property_id=self.property,
            owner_id=self.property_owner_profile,
            interested_user_id=self.user,
            interaction_type="inquiry",
        )
        self.admin_action = AdminAction.objects.create(
            user_id=self.user, action="approve"
        )

    def test_address_creation(self):
        self.assertEqual(self.address.street, "123 Main St")
        self.assertEqual(self.address.city, "City")
        self.assertEqual(self.address.state, "State")
        self.assertEqual(self.address.zipcode, "12345")

    def test_property_creation(self):
        self.assertEqual(self.property.title, "Test Property")
        self.assertEqual(self.property.price, 100000)
        self.assertEqual(self.property.type, "house")
        self.assertEqual(self.property.status, "for_sale")
        self.assertEqual(self.property.analytics["views"], 100)
        self.assertEqual(self.property.images[0], "http://example.com/image1.jpg")
        self.assertEqual(self.property.user, self.user)
        self.assertEqual(self.property.address, self.address)
        self.assertEqual(self.property.latitude, 1)
        self.assertEqual(self.property.longitude, 2)
        self.assertEqual(self.property.area, 1000)
        self.assertEqual(self.property.bedrooms, 3)
        self.assertEqual(self.property.bathrooms, 2)
        self.assertEqual(self.property.amenities[0], "Swimming pool")
        self.assertEqual(self.property.amenities[1], "Garden")
        self.assertEqual(self.property.description, "Test description")
        self.assertEqual(self.property.analytics["likes"], 50)

    def test_property_owner_profile_creation(self):
        self.assertEqual(self.property_owner_profile.bio, "Test bio")
        self.assertEqual(self.property_owner_profile.user, self.user)
        self.assertEqual(
            self.property_owner_profile.contact_information, self.contact_info
        )
        self.assertEqual(self.property_owner_profile.bio, "Test bio")

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.transaction_amount, 90000)
        self.assertEqual(self.transaction.property_id, self.property)
        self.assertEqual(self.transaction.buyer_id, self.user)
        self.assertEqual(self.transaction.seller_id, self.property_owner_profile)
        self.assertEqual(self.transaction.transaction_type, "sale")

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.review_text, "Great property!")
        self.assertEqual(self.review.property_id, self.property)
        self.assertEqual(self.review.reviewer_id, self.user)

    def test_saved_search_creation(self):
        self.assertEqual(self.saved_search.search_criteria["type"], "house")
        self.assertEqual(self.saved_search.user_id, self.user)
        self.assertEqual(
            self.saved_search.search_criteria,
            {"type": "house", "price_range": [50000, 150000]},
        )

    def test_interaction_creation(self):
        self.assertEqual(self.interaction.interaction_type, "inquiry")
        self.assertEqual(self.interaction.property_id, self.property)
        self.assertEqual(self.interaction.owner_id, self.property_owner_profile)
        self.assertEqual(self.interaction.interested_user_id, self.user)

    def test_admin_action_creation(self):
        self.assertEqual(self.admin_action.action, "approve")
        self.assertEqual(self.admin_action.user_id, self.user)
