import unittest
from app import create_app, db
from app.models.hotel import Hotel
from app.models.user import User

class ReservationRoutesTestCase(unittest.TestCase):
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

    def test_reserve_requires_login(self):
        """OTEL-17.4: Giriş yapmamış kullanıcının rezervasyon yapamaması (302 ile login'e atar)."""
        u = User(username='owner', email='owner@test.com', role='hotel_owner')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()
        
        h = Hotel(name='Test', city='Istanbul', owner_id=u.id, is_approved=True)
        db.session.add(h)
        db.session.commit()

        # POST isteği atıyoruz
        response = self.client.post(f'/hotels/{h.id}/reserve', data={
            'room_type_id': 1,
            'check_in': '2030-01-01',
            'check_out': '2030-01-05',
            'guests': 2
        })
        # login_required bizi /login sayfasına redirect etmeli (302)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers.get('Location', ''))

if __name__ == '__main__':
    unittest.main()
