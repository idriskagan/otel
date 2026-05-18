import unittest
from app import create_app, db
from app.models.user import User

class AuthUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        # Testler sırasında form güvenliğinin (CSRF) bizi engellemesini durduruyoruz
        self.app.config['WTF_CSRF_ENABLED'] = False 
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
         # Veritabanını her testten önce sıfırdan oluşturur
         db.create_all()

    def tearDown(self):
        with self.app.app_context(): # Bu satırı ekleyerek context içine alıyoruz
            db.session.remove()
            db.drop_all()

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
        """OTEL-15: /register API'sine veri gönderildiğinde yanıt dönme testi."""
        response = self.client.post('/auth/register', data={
            'username': 'yeni_kullanici',
            'email': 'test@example.com',
            'password': 'Sifre123!',
            'confirm_password': 'Sifre123!',
            'role': 'user',    # İşte bu eksik olan parçaydı!
            'submit': True
        }, follow_redirects=True)
        
        # 400 hatasından kurtulup 200 veya 302 görmeyi bekliyoruz
        self.assertIn(response.status_code, [200, 201, 302])
if __name__ == '__main__':
    unittest.main(verbosity=2)