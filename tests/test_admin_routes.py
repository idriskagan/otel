import unittest
from app import create_app, db
from app.models.user import User
from app.models.hotel import Hotel

class AdminRoutesTestCase(unittest.TestCase):
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

    def test_admin_dashboard_access_denied_for_normal_user(self):
        # Normal kullanici
        u = User(username='normal', email='normal@test.com', role='user')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()

        # Login
        self.client.post('/auth/login', data={'email': 'normal@test.com', 'password': '123'})
        
        # Admin sayfasina gitmeyi dene
        response = self.client.get('/admin/dashboard')
        # role_required genelde 403 doner ya da redirect (302) atar
        self.assertIn(response.status_code, [302, 403])

    def test_admin_dashboard_access_granted_for_admin(self):
        # Admin kullanici
        admin = User(username='admin', email='admin@test.com', role='admin')
        admin.set_password('123')
        db.session.add(admin)
        db.session.commit()

        # Login
        self.client.post('/auth/login', data={'email': 'admin@test.com', 'password': '123'})
        
        # Admin sayfasina git
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_admin_can_approve_hotel(self):
        admin = User(username='admin', email='admin@test.com', role='admin')
        admin.set_password('123')
        
        owner = User(username='owner', email='owner@test.com', role='hotel_owner')
        owner.set_password('123')
        db.session.add_all([admin, owner])
        db.session.commit()

        # Onaysiz bir otel ekle
        h = Hotel(name='Test Hotel', city='Izmir', owner_id=owner.id, is_approved=False)
        db.session.add(h)
        db.session.commit()

        self.client.post('/auth/login', data={'email': 'admin@test.com', 'password': '123'})
        
        # Onayla
        response = self.client.post(f'/admin/hotels/{h.id}/approve', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Otel onaylandi mi kontrol et
        self.assertTrue(h.is_approved)

if __name__ == '__main__':
    unittest.main()
