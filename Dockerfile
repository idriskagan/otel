# ============================================================
# Dockerfile — Otel Rezervasyon Web Uygulaması
# ============================================================
# Kullanım:
#   docker build -t otel-app .
#   docker run -p 5000:5000 -e FLASK_ENV=production otel-app
# ============================================================

# -------- Build Stage --------
FROM python:3.11-slim AS builder

WORKDIR /app

# Python çevresi
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Bağımlılıkları ayrı bir katmanda yükle (cache optimizasyonu)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn==23.0.0 && \
    pip install --no-cache-dir -r requirements.txt

# -------- Production Stage --------
FROM python:3.11-slim

WORKDIR /app

# Python çevresi
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_APP=run.py

# Build aşamasından pip paketlerini kopyala
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Uygulama kodunu kopyala
COPY . .

# Statik dosyalar ve uploads için dizinleri oluştur
RUN mkdir -p /app/app/static/uploads && \
    useradd -m -r appuser && \
    chown -R appuser:appuser /app

# Uygulamayı kısıtlı kullanıcı ile çalıştır
USER appuser

# Port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Gunicorn ile production sunucusu
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]
