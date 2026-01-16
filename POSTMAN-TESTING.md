# Postman Testing Guide — DRF Generic Views, Permissions, JWT & Swagger

This guide explains how to test all API endpoints using **Postman** with **JWT authentication**, clearly showing **when authentication is required**, how **permissions are enforced**, and how **admin vs authenticated vs anonymous access** behaves.

It also notes where **Swagger (OpenAPI)** can be used as a secondary testing and discovery tool alongside Postman.

---

## 🧰 Prerequisites

Before testing, ensure:

* Django development server is running:

```bash
python manage.py runserver
```

* Base URL:

```
http://127.0.0.1:8000
```

* At least one **superuser** exists (for admin-only endpoints):

```bash
python manage.py createsuperuser
```

* (Optional) A regular **non-admin user** exists for authenticated-only testing

* JWT authentication is installed and configured:

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

* Token endpoints exist in root `urls.py`:

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

## 📘 Swagger (Optional but Recommended)

In addition to Postman, this project exposes **interactive Swagger documentation**:

```
http://127.0.0.1:8000/api/docs/
```

Swagger can be used to:

* Discover available endpoints
* Inspect request/response schemas
* Authenticate using JWT
* Perform quick exploratory testing

**Postman remains the authoritative testing tool** for permission validation and repeatable request workflows.

---

## 🌍 Postman Environment Setup (Recommended)

Create a Postman Environment with:

| Variable       | Value                     |
| -------------- | ------------------------- |
| `BASE_URL`     | `http://127.0.0.1:8000`   |
| `ACCESS_TOKEN` | *(leave blank initially)* |

All requests reference:

```
{{BASE_URL}}
```

---

## 🔑 Authentication Strategy (JWT)

* Use `/api/token/` to **obtain an access token**
* Include the token in the **Authorization header**
* JWT format:

```
Authorization: Bearer <access_token>
```

Tokens are required for:

* Admin-only product writes
* Authenticated-only post creation and modification

---

## 1️⃣ Obtain JWT Token

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

**Postman Tip**

Save `access` into the environment variable:

```
ACCESS_TOKEN
```

---

## 2️⃣ Refresh JWT Token (Optional)

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

Update `ACCESS_TOKEN` in Postman when refreshed.

---

## 🧪 Products API Testing — Granular Generic Views

Products use **single-responsibility views**, making permission enforcement explicit.

---

### 1️⃣ List Products (Public)

```
GET {{BASE_URL}}/api/products/
```

* Auth: ❌ None
* Expected: `200 OK`

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

**Expected Behavior**

* Anonymous → `401 Unauthorized`
* Authenticated non-admin → `403 Forbidden`
* Admin → `201 Created`

---

### 3️⃣ Retrieve Product (Public)

```
GET {{BASE_URL}}/api/products/retrieve/laptop-pro
```

* Auth: ❌ None
* Expected: `200 OK`

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

* Anonymous → `401 Unauthorized`
* Admin → `200 OK`

---

### 5️⃣ Delete Product (Admin Only)

```
DELETE {{BASE_URL}}/api/products/destroy/laptop-pro
```

* Auth: `Authorization: Bearer {{ACCESS_TOKEN}}`
* Anonymous → `401 Unauthorized`
* Admin → `204 No Content`

---

## 🧪 Posts API Testing — Combined Generic Views

Posts use **combined views**, where permissions apply per HTTP method.

---

### 1️⃣ List Posts (Public)

```
GET {{BASE_URL}}/api/posts/
```

* Auth: ❌ None
* Expected: `200 OK`

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

* Anonymous → `401 Unauthorized`
* Authenticated user → `201 Created`

---

### 3️⃣ Retrieve Post (Public)

```
GET {{BASE_URL}}/api/posts/1
```

* Auth: ❌ None
* Expected: `200 OK`

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

* Anonymous → `401 Unauthorized`
* Authenticated user → `200 OK`

---

### 5️⃣ Delete Post (Authenticated Only)

```
DELETE {{BASE_URL}}/api/posts/1
```

* Anonymous → `401 Unauthorized`
* Authenticated user → `204 No Content`

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

## ✅ Notes & Best Practices

* `401 Unauthorized` → token missing or invalid
* `403 Forbidden` → authenticated but insufficient role
* Always test **anonymous → authenticated → admin**
* Use Postman environment variables to avoid manual token copy/paste
* JWT removes CSRF concerns, making API testing cleaner
* Swagger is ideal for discovery; Postman is ideal for validation

---

This guide serves as a **complete, practical reference** for testing DRF APIs with **JWT authentication, permissions, Postman workflows, and Swagger support**, suitable for both **learning and professional documentation**.
