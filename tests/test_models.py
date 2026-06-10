import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models.hotel import Hotel, HotelImage
from app.models.reservation import Reservation
from app.models.user import User

class ModelsUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_hotel_primary_image(self):
        user = User(username='owner', email='owner@test.com', role='hotel_owner')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()

        hotel = Hotel(name='Test Hotel', city='Istanbul', owner_id=user.id)
        db.session.add(hotel)
        db.session.commit()

        self.assertIsNone(hotel.primary_image)

        img1 = HotelImage(hotel_id=hotel.id, image_path='img1.jpg', is_primary=False)
        img2 = HotelImage(hotel_id=hotel.id, image_path='img2.jpg', is_primary=True)
        db.session.add_all([img1, img2])
        db.session.commit()

        self.assertEqual(hotel.primary_image, 'img2.jpg')

    def test_reservation_nights(self):
        user = User(username='guest', email='guest@test.com', role='user')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()

        check_in = datetime.utcnow().date()
        check_out = check_in + timedelta(days=3)

        reservation = Reservation(
            user_id=user.id,
            hotel_id=1, 
            room_type_id=1, 
            check_in=check_in,
            check_out=check_out,
            total_price=300.0
        )

        self.assertEqual(reservation.nights, 3)

if __name__ == '__main__':
    unittest.main()
