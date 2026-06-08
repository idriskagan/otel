from app import create_app

# Render'da çalışırken Render Environment Variables içindeki FLASK_ENV='production' değerini okuyup ona göre ayağa kalkacak.
# Lokalde çalıştırırken ise ortam değişkeni bulamazsa 'development' modunda açılacak.
app = create_app()

if __name__ == '__main__':
    # Burası SADECE kendi bilgisayarında (lokalde) test yaparken çalışır.
    # Render (Gunicorn) bu bloğu tamamen yok sayar, bu yüzden debug=True kalmasında hiçbir sakınca yoktur.
    app.run(debug=True, port=5000)