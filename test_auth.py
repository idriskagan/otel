import unittest
from app import create_app, db
from app.models.user import User

class AuthUnitTestCase(unittest.TestCase):
    def setUp(self):
        # 1. Test için yalıtılmış uygulama ve veritabanı kuruyoruz
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

    def tearDown(self):
        # 2. Test bitince ortalığı temizliyoruz
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_sifre_guvenligi_hashleme(self):
        """OTEL-14: Şifrelerin açık metin yerine hashlenerek kaydedildiğinin testi."""
        u = User(username='test_kullanici', email='test@mail.com')
        u.set_password('cokgizlisifre123')
        
        # Şifrenin açık haliyle veritabanındakinin aynı OLMAMASI lazım
        self.assertNotEqual(u.password_hash, 'cokgizlisifre123')
        # Doğru şifreyle check edildiğinde True dönmeli
        self.assertTrue(u.check_password('cokgizlisifre123'))
        # Yanlış şifreyle False dönmeli
        self.assertFalse(u.check_password('yanlissifre'))

    def test_kayit_olma_endpointi(self):
        """OTEL-14: /register API'sine veri gönderildiğinde yanıt dönme testi."""
        response = self.client.post('/register', data={
            'username': 'yeni_kullanici',
            'email': 'yeni@mail.com',
            'password': 'password123'
        })
        
        # Kağan henüz API kodunu tam yazmadığı için bu test şimdilik geçemeyecek (Fail olacak)!
        self.assertIn(response.status_code, [200, 201, 302]) 

if __name__ == '__main__':
    unittest.main(verbosity=2)