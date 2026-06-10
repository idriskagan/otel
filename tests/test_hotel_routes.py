import unittest
from app import create_app, db
from app.models.hotel import Hotel
from app.models.user import User

class HotelRoutesTestCase(unittest.TestCase):
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

    def test_main_index_page(self):
        """OTEL-17: Ana sayfanın başarıyla yüklenmesi."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_hotel_detail_not_found(self):
        """Olmayan veya onaysız bir otel detayına gidildiğinde listeye yönlendirme (302)."""
        response = self.client.get('/hotels/999')
        self.assertEqual(response.status_code, 302)

    def test_hotel_detail_approved(self):
        """Onaylı otel detay sayfasının yüklenmesi (200)."""
        u = User(username='owner', email='owner@test.com', role='hotel_owner')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()
        
        h = Hotel(name='Test Hotel', city='Istanbul', owner_id=u.id, is_approved=True)
        db.session.add(h)
        db.session.commit()

        response = self.client.get(f'/hotels/{h.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
