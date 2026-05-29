import unittest
from app import create_app, db
from app.models.user import User
from app.models.hotel import Hotel

class SearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_by_city(self):
        u = User(username='owner', email='owner@test.com', role='hotel_owner')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()

        h1 = Hotel(name='Hotel Istanbul 1', city='Istanbul', owner_id=u.id, is_approved=True, star_rating=4)
        h2 = Hotel(name='Hotel Ankara 1', city='Ankara', owner_id=u.id, is_approved=True, star_rating=5)
        db.session.add_all([h1, h2])
        db.session.commit()

        # Istanbul icin arama
        response = self.client.get('/hotels/search?city=Istanbul')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hotel Istanbul 1', response.data)
        self.assertNotIn(b'Hotel Ankara 1', response.data)

    def test_search_by_stars(self):
        u = User(username='owner', email='owner@test.com', role='hotel_owner')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()

        h1 = Hotel(name='Uc Yildizli Otel', city='Izmir', owner_id=u.id, is_approved=True, star_rating=3)
        h2 = Hotel(name='Bes Yildizli Otel', city='Izmir', owner_id=u.id, is_approved=True, star_rating=5)
        db.session.add_all([h1, h2])
        db.session.commit()

        # Minimum 4 yildizli arama
        response = self.client.get('/hotels/search?stars=4')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Uc Yildizli Otel', response.data)
        self.assertIn(b'Bes Yildizli Otel', response.data)

if __name__ == '__main__':
    unittest.main()
