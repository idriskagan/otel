import unittest
from app import create_app, db
from app.models.user import User
from app.models.hotel import Hotel
from app.models.review import Review

class ReviewSystemTestCase(unittest.TestCase):
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

    def test_add_review_to_hotel(self):
        u = User(username='user', email='user@test.com', role='user')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()
        
        h = Hotel(name='Test Hotel', city='Bursa', owner_id=u.id, is_approved=True)
        db.session.add(h)
        db.session.commit()

        self.client.post('/auth/login', data={'email': 'user@test.com', 'password': '123'})
        
        response = self.client.post(f'/hotels/{h.id}/review', data={
            'rating': 5,
            'comment': 'Harika bir oteldi!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        
        # Yorum veritabanina eklendi mi?
        review = db.session.query(Review).filter_by(hotel_id=h.id, user_id=u.id).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Harika bir oteldi!')

if __name__ == '__main__':
    unittest.main()
