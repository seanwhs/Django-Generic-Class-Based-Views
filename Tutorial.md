# 🛠️ Django REST Framework — Full Tutorial: Generic Views, JWT, Swagger & Logging

This tutorial walks you **step by step** through creating a Django project that demonstrates:

* **Granular vs Combined Generic Views**
* **JWT Authentication using SimpleJWT**
* **Swagger / OpenAPI auto-generated documentation**
* **Custom middleware for API request/response logging**
* **Explicit REST API design and permission enforcement**

This project is primarily a **personal refresher** on DRF generic views, but it’s structured for clarity, maintainability, and production-ready patterns.

---

## 1️⃣ Project Scaffolding

### 1.1 Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 1.2 Install dependencies

```bash
pip install Django==6.0.1
pip install djangorestframework==3.16.1
pip install djangorestframework_simplejwt==5.5.1
pip install drf-spectacular==0.29.0
pip install drf-spectacular-sidecar==2026.1.1
pip install PyJWT==2.10.1
```

---

### 1.3 Start the project

```bash
django-admin startproject config .
```

---

### 1.4 Create apps

```bash
python manage.py startapp products
python manage.py startapp posts
```

---

### 1.5 Folder Structure

```
project_root/
├─ config/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ middleware.py  # <- custom logging middleware
├─ products/
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  ├─ urls.py
│  └─ admin.py
├─ posts/
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  ├─ urls.py
│  └─ admin.py
├─ db.sqlite3
└─ manage.py
```

---

## 2️⃣ Settings.py — Required Changes

Open `config/settings.py` and **highlighted changes**:

### 2.1 Installed apps

```python
INSTALLED_APPS += [
    'rest_framework',   # DRF
    'drf_spectacular',  # Swagger
    'products',         # Custom app
    'posts',            # Custom app
]
```

### 2.2 Middleware

Add custom logging middleware:

```python
MIDDLEWARE += [
    'config.middleware.DRFRequestResponseLoggingMiddleware',
]
```

### 2.3 DRF & JWT

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### 2.4 Swagger / OpenAPI

```python
SPECTACULAR_SETTINGS = {
    "TITLE": "Products & Posts API",
    "DESCRIPTION": "A DRF project demonstrating generic views, JWT, Swagger & logging",
    "VERSION": "1.0.0",
}
```

### 2.5 Logging

```python
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = DEFAULT_LOGGING.copy()
LOGGING.setdefault('formatters', {})
LOGGING['formatters']['api'] = {
    'format': '[{levelname}] {asctime} {name} {message}',
    'style': '{',
}
LOGGING.setdefault('handlers', {})
LOGGING['handlers']['api_file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': str(LOG_DIR / 'api.log'),
    'formatter': 'api',
}
LOGGING.setdefault('loggers', {})
LOGGING['loggers']['api.requests'] = {
    'handlers': ['api_file'],
    'level': 'INFO',
    'propagate': False,
}
```

---

## 3️⃣ Custom Middleware for Logging

Create `config/middleware.py`:

```python
import logging

logger = logging.getLogger('api.requests')

class DRFRequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log incoming request
        logger.info(f"Incoming {request.method} request to {request.path}")
        response = self.get_response(request)
        # Log response status
        logger.info(f"Response {response.status_code} for {request.method} {request.path}")
        return response
```

---

## 4️⃣ Models

### 4.1 Products (Granular)

```python
# products/models.py
from django.db import models

class Product(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
```

### 4.2 Posts (Combined)

```python
# posts/models.py
from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 5️⃣ Serializers

### 5.1 Products

```python
# products/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

### 5.2 Posts

```python
# posts/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
```

---

## 6️⃣ Views — Generic Views

### 6.1 Products — Granular Views

```python
# products/views.py
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Product
from .serializers import ProductSerializer

class ListProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class RetrieveProductAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class CreateProductAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class UpdateProductAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]

class DestroyProductAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
```

### 6.2 Posts — Combined Views

```python
# posts/views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class ListCreatePostAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RetrieveUpdateDestroyPostAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

---

## 7️⃣ URLs

### 7.1 Root URLs (`config/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App APIs
    path('api/', include('products.urls')),
    path('api/', include('posts.urls')),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc (optional)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

### 7.2 Products URLs

```python
# products/urls.py
from django.urls import path
from .views import ListProductAPIView, CreateProductAPIView, RetrieveProductAPIView, UpdateProductAPIView, DestroyProductAPIView

urlpatterns = [
    path('products/', ListProductAPIView.as_view(), name='product-list'),
    path('products/create', CreateProductAPIView.as_view(), name='product-create'),
    path('products/retrieve/<slug:slug>', RetrieveProductAPIView.as_view(), name='product-retrieve'),
    path('products/update/<slug:slug>', UpdateProductAPIView.as_view(), name='product-update'),
    path('products/destroy/<slug:slug>', DestroyProductAPIView.as_view(), name='product-destroy'),
]
```

### 7.3 Posts URLs

```python
# posts/urls.py
from django.urls import path
from .views import ListCreatePostAPIView, RetrieveUpdateDestroyPostAPIView

urlpatterns = [
    path('posts/', ListCreatePostAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>', RetrieveUpdateDestroyPostAPIView.as_view(), name='post-retrieve-update-destroy'),
]
```

---

## 8️⃣ Database & Admin Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 9️⃣ Run the Server

```bash
python manage.py runserver
```

Swagger docs are now available at:

* [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) (Swagger UI)
* [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/) (ReDoc UI)

---

## 10️⃣ Summary of Design Choices

| Feature  | Products (Granular) | Posts (Combined)   |
| -------- | ------------------- | ------------------ |
| List     | ✅ Public            | ✅ Public           |
| Create   | Admin only          | Authenticated      |
| Retrieve | ✅ Public            | ✅ Public           |
| Update   | Admin only          | Authenticated      |
| Delete   | Admin only          | Authenticated      |
| Views    | 5 separate classes  | 2 combined classes |
| Lookup   | slug                | id (PK)            |

---

## 11️⃣ Key Lessons

* **Granular vs Combined views**: trade-offs between control vs brevity.
* **JWT Authentication**: stateless, works perfectly with Swagger and Postman.
* **Swagger (drf-spectacular)**: automatically generates OpenAPI 3 schema.
* **Logging**: custom middleware provides observability for all API requests.
* **Permissions**: explicit enforcement per view reduces security mistakes.

---

## 12️⃣ DRF Generic Views — Visual Diagram

```
Products App (Granular)
┌─────────────┐
│ ListAPIView │ GET /products/ ✅ Public
└─────────────┘
┌─────────────┐
│ CreateAPIView │ POST /products/create ✅ Admin
└─────────────┘
┌──────────────┐
│RetrieveAPIView│ GET /products/retrieve/<slug> ✅ Public
└──────────────┘
┌─────────────┐
│UpdateAPIView │ PUT /products/update/<slug> ✅ Admin
└─────────────┘
┌──────────────┐
│DestroyAPIView│ DELETE /products/destroy/<slug> ✅ Admin
└──────────────┘

Posts App (Combined)
┌──────────────────────┐
│ ListCreateAPIView     │ GET /posts/ ✅ Public
│                       │ POST /posts/ ✅ Authenticated
└──────────────────────┘
┌──────────────────────────────┐
│ RetrieveUpdateDestroyAPIView  │ GET /posts/<id> ✅ Public
│                               │ PUT /posts/<id> ✅ Authenticated
│                               │ DELETE /posts/<id> ✅ Authenticated
└──────────────────────────────┘
```


