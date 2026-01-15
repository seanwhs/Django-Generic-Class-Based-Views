# Postman Testing Guide — DRF Generic Views & Permissions (JWT)

This guide explains how to test all API endpoints using Postman with **JWT authentication**, highlighting **when authentication is required** and how **permissions are enforced**.

---

## 🧰 Prerequisites

Before testing, ensure:

* Django server is running:

```bash
python manage.py runserver
```

* Base URL:

```
http://127.0.0.1:8000
```

* At least one superuser exists:

```bash
python manage.py createsuperuser
```

* (Optional) A regular non-admin user exists for testing authenticated access

* JWT installed and configured in Django:

```bash
pip install djangorestframework-simplejwt
```

* In `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

* Add token URLs to `urls.py`:

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

## 🌍 Postman Environment (Recommended)

Create a Postman Environment with:

| Variable       | Value                     |
| -------------- | ------------------------- |
| `BASE_URL`     | `http://127.0.0.1:8000`   |
| `ACCESS_TOKEN` | *(leave blank initially)* |

All requests use `{{BASE_URL}}`.

---

## 🔑 Authentication Strategy (JWT)

* Use `/api/token/` to **get an access token** for login.
* Include the token in the **Authorization header** for requests that require authentication.
* Format:

```
Authorization: Bearer <access_token>
```

---

### 1️⃣ Obtain JWT Token

**Endpoint**

```
POST {{BASE_URL}}/api/token/
```

**Body (JSON)**

```json
{
  "username": "admin",
  "password": "yourpassword"
}
```

**Expected Response**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

* Copy `access` into Postman Environment variable `ACCESS_TOKEN`.

---

### 2️⃣ Refresh JWT Token (Optional)

**Endpoint**

```
POST {{BASE_URL}}/api/token/refresh/
```

**Body (JSON)**

```json
{
  "refresh": "<refresh_token>"
}
```

**Expected Response**

```json
{
  "access": "<new_access_token>"
}
```

* Update `ACCESS_TOKEN` in Postman.

---

## 🧪 Products API Testing (Granular Views)

### 1️⃣ List Products (Public)

```
GET {{BASE_URL}}/api/products/
```

* Auth: ❌ None
* Response: `200 OK`

---

### 2️⃣ Create Product (Admin Only)

```
POST {{BASE_URL}}/api/products/create
```

**Headers**

```
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json
```

**Body (JSON)**

```json
{
  "slug": "laptop-pro",
  "name": "Laptop Pro",
  "price": 1500
}
```

* Anonymous: `401 Unauthorized`
* Admin: `201 Created`

---

### 3️⃣ Retrieve Product (Public)

```
GET {{BASE_URL}}/api/products/retrieve/laptop-pro
```

* Auth: ❌ None
* Response: `200 OK`

---

### 4️⃣ Update Product (Admin Only)

```
PUT {{BASE_URL}}/api/products/update/laptop-pro
```

**Headers**

```
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json
```

**Body (JSON)**

```json
{
  "slug": "laptop-pro",
  "name": "Laptop Pro X",
  "price": 1800
}
```

* Anonymous: `401 Unauthorized`
* Admin: `200 OK`

---

### 5️⃣ Delete Product (Admin Only)

```
DELETE {{BASE_URL}}/api/products/destroy/laptop-pro
```

* Auth: `Authorization: Bearer {{ACCESS_TOKEN}}`
* Anonymous: `401 Unauthorized`
* Admin: `204 No Content`

---

## 🧪 Posts API Testing (Combined Views)

### 1️⃣ List Posts (Public)

```
GET {{BASE_URL}}/api/posts/
```

* Auth: ❌ None
* Response: `200 OK`

---

### 2️⃣ Create Post (Authenticated Only)

```
POST {{BASE_URL}}/api/posts/
```

**Headers**

```
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json
```

**Body (JSON)**

```json
{
  "name": "Sean",
  "message": "First authenticated post"
}
```

* Anonymous: `401 Unauthorized`
* Authenticated user: `201 Created`

---

### 3️⃣ Retrieve Post (Public)

```
GET {{BASE_URL}}/api/posts/1
```

* Auth: ❌ None
* Response: `200 OK`

---

### 4️⃣ Update Post (Authenticated Only)

```
PUT {{BASE_URL}}/api/posts/1
```

**Headers**

```
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json
```

* Anonymous: `401 Unauthorized`
* Authenticated user: `200 OK`

---

### 5️⃣ Delete Post (Authenticated Only)

```
DELETE {{BASE_URL}}/api/posts/1
```

* Anonymous: `401 Unauthorized`
* Authenticated user: `204 No Content`

---

## 🔐 Permission Validation Matrix (JWT)

| Endpoint                 | Anonymous | Authenticated | Admin |
| ------------------------ | --------- | ------------- | ----- |
| GET /products            | ✅         | ✅             | ✅     |
| POST /products/create    | ❌         | ❌             | ✅     |
| PUT /products/update     | ❌         | ❌             | ✅     |
| DELETE /products/destroy | ❌         | ❌             | ✅     |
| GET /posts               | ✅         | ✅             | ✅     |
| POST /posts              | ❌         | ✅             | ✅     |
| PUT /posts               | ❌         | ✅             | ✅     |
| DELETE /posts            | ❌         | ✅             | ✅     |

---

### ✅ Notes

* `401 Unauthorized` = token missing or invalid
* `403 Forbidden` = authenticated but insufficient permissions
* Always test **anonymous → authenticated → admin**
* Use Postman Environment variable `ACCESS_TOKEN` to avoid manual copy/paste
* JWT eliminates CSRF issues, making API testing simpler than session-based auth
