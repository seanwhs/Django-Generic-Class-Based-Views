# Django REST Framework — Generic Views & JWT Walkthrough

This document is a **complete code walkthrough** for a DRF project using **generic class-based views**, **granular and combined API designs**, and **JWT-based authentication/authorization**. It includes **settings, URLs, view structure, permissions, and Postman testing**.

---

## 🧰 Prerequisites

Before starting:

1. Python virtual environment activated (`venv` recommended).
2. Django, DRF, and JWT installed:

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

3. Create superuser:

```bash
python manage.py createsuperuser
```

4. Run the server:

```bash
python manage.py runserver
```

Base URL:

```
http://127.0.0.1:8000
```

---

## 1️⃣ DRF & JWT Settings (`settings.py`)

```python
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

**Explanation**

* **JWTAuthentication**: Replaces session auth.
* **AllowAny**: Default view-level permissions, overridden per view.
* **Token lifetimes**: 30 min for access, 1 day for refresh.

---

## 2️⃣ Root URL Configuration (`urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App endpoints
    path('api/', include('products.urls')),
    path('api/', include('posts.urls')),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**JWT Endpoints**

| Endpoint              | Method | Description                   |
| --------------------- | ------ | ----------------------------- |
| `/api/token/`         | POST   | Obtain access + refresh token |
| `/api/token/refresh/` | POST   | Refresh access token          |

---

## 3️⃣ Products App — Granular Generic Views

**Models (`products/models.py`)**

```python
from django.db import models

class Product(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
```

**Views (`products/views.py`)**

```python
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .models import Product
from .serializers import ProductSerializer

class ListProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Public read

class RetrieveProductAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]  # Public read

class CreateProductAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]  # Admin-only

class UpdateProductAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]  # Admin-only

class DestroyProductAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]  # Admin-only
```

**URLs (`products/urls.py`)**

```python
from django.urls import path
from .views import (
    ListProductAPIView, CreateProductAPIView, RetrieveProductAPIView,
    UpdateProductAPIView, DestroyProductAPIView
)

urlpatterns = [
    path('products/', ListProductAPIView.as_view(), name='product-list'),
    path('products/create', CreateProductAPIView.as_view(), name='product-create'),
    path('products/retrieve/<slug:slug>', RetrieveProductAPIView.as_view(), name='product-retrieve'),
    path('products/update/<slug:slug>', UpdateProductAPIView.as_view(), name='product-update'),
    path('products/destroy/<slug:slug>', DestroyProductAPIView.as_view(), name='product-destroy'),
]
```

---

## 4️⃣ Posts App — Combined Generic Views

**Models (`posts/models.py`)**

```python
from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Views (`posts/views.py`)**

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
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

**URLs (`posts/urls.py`)**

```python
from django.urls import path
from .views import ListCreatePostAPIView, RetrieveUpdateDestroyPostAPIView

urlpatterns = [
    path('posts/', ListCreatePostAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>', RetrieveUpdateDestroyPostAPIView.as_view(), name='post-detail'),
]
```

---

## 5️⃣ Permissions Flow (ASCII Diagram)

```
                    ┌──────────────┐
                    │  Anonymous   │
                    └──────┬───────┘
                           │
                GET /products/ & GET /posts/
                           │
                        ✅ Allowed
                           │
                    ┌──────▼───────┐
                    │ Authenticated│
                    └──────┬───────┘
                           │
        POST /posts/  PUT /posts/<id>  DELETE /posts/<id>
                           │
                        ✅ Allowed
                           │
                    ┌──────▼───────┐
                    │    Admin     │
                    └──────┬───────┘
                           │
POST /products/create  PUT /products/update/<slug> DELETE /products/destroy/<slug>
                           │
                        ✅ Allowed
```

---

## 6️⃣ Postman Testing Guide (JWT)

### Step 1 — Obtain Token

```
POST {{BASE_URL}}/api/token/
```

Body:

```json
{
  "username": "admin",
  "password": "supersecret"
}
```

Response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

---

### Step 2 — Use Token in Requests

Headers:

```
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json
```

---

### Step 3 — Example Endpoints

| Endpoint                        | Method | Auth Required | Role Allowed  |
| ------------------------------- | ------ | ------------- | ------------- |
| `/api/products/`                | GET    | No            | Any           |
| `/api/products/create`          | POST   | Yes           | Admin         |
| `/api/products/retrieve/<slug>` | GET    | No            | Any           |
| `/api/products/update/<slug>`   | PUT    | Yes           | Admin         |
| `/api/products/destroy/<slug>`  | DELETE | Yes           | Admin         |
| `/api/posts/`                   | GET    | No            | Any           |
| `/api/posts/`                   | POST   | Yes           | Authenticated |
| `/api/posts/<int:pk>`           | GET    | No            | Any           |
| `/api/posts/<int:pk>`           | PUT    | Yes           | Authenticated |
| `/api/posts/<int:pk>`           | DELETE | Yes           | Authenticated |

---

## 7️⃣ Key Takeaways

* DRF **generic views** allow clear API structure (granular vs combined).
* **JWT authentication** removes CSRF issues and scales for APIs.
* **Permissions are explicit per-view**, making the system predictable.
* Always test **anonymous → authenticated → admin** flows.
* **Slug-based lookup** improves URL readability and API clarity.

---

This document is now a **full reference for code, endpoints, JWT auth, and Postman testing**, suitable for a **portfolio or documentation repository**.

