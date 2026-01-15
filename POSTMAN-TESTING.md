# Postman Testing Guide — DRF Generic Views & Permissions

This document describes how to **manually test all API endpoints using Postman**, with a focus on **authentication, permissions, and expected responses**.

It is designed to validate that:

* Public endpoints are accessible
* Protected endpoints are correctly restricted
* Admin-only actions are enforced
* Permissions behave as intended

---

## 🧰 Prerequisites

Before testing, ensure:

* The Django server is running:

  ```bash
  python manage.py runserver
  ```
* Base URL:

  ```
  http://127.0.0.1:8000
  ```
* A superuser exists:

  ```bash
  python manage.py createsuperuser
  ```

---

## 🌍 Postman Environment (Recommended)

Create a Postman Environment with the following variable:

| Variable   | Value                   |
| ---------- | ----------------------- |
| `BASE_URL` | `http://127.0.0.1:8000` |

All requests below assume usage of:

```
{{BASE_URL}}
```

---

## 🔓 Authentication Strategy (Session-Based)

This project uses **Django session authentication** for testing.

### Login Endpoint

```
POST {{BASE_URL}}/api-auth/login/
```

### Postman Setup

* Method: `POST`
* Authorization: **No Auth**
* Headers:

  ```
  Content-Type: application/x-www-form-urlencoded
  ```
* Body → `x-www-form-urlencoded`:

  ```
  username=admin
  password=yourpassword
  ```

✅ On success, Postman stores the session cookie automatically
⚠️ Cookies must be enabled in Postman settings

---

## 🧪 Products API Testing (Granular Views)

### 1️⃣ List Products (Public)

**Request**

```
GET {{BASE_URL}}/api/products/
```

**Auth**

* None

**Expected Response**

* `200 OK`
* JSON list (empty or populated)

---

### 2️⃣ Create Product (Anonymous — Should Fail)

**Request**

```
POST {{BASE_URL}}/api/products/create
```

**Auth**

* None

**Body (JSON)**

```json
{
  "slug": "test-product",
  "name": "Test Product",
  "price": 100
}
```

**Expected Response**

* `403 Forbidden`

---

### 3️⃣ Create Product (Admin — Should Succeed)

🔐 Ensure you are logged in as admin first.

**Request**

```
POST {{BASE_URL}}/api/products/create
```

**Body (JSON)**

```json
{
  "slug": "laptop-pro",
  "name": "Laptop Pro",
  "price": 1500
}
```

**Expected Response**

* `201 Created`

---

### 4️⃣ Retrieve Product (Public)

**Request**

```
GET {{BASE_URL}}/api/products/retrieve/laptop-pro
```

**Expected Response**

* `200 OK`

---

### 5️⃣ Update Product (Admin Only)

**Request**

```
PUT {{BASE_URL}}/api/products/update/laptop-pro
```

**Body (JSON)**

```json
{
  "slug": "laptop-pro",
  "name": "Laptop Pro X",
  "price": 1800
}
```

**Expected Response**

* `200 OK`

---

### 6️⃣ Delete Product (Admin Only)

**Request**

```
DELETE {{BASE_URL}}/api/products/destroy/laptop-pro
```

**Expected Response**

* `204 No Content`

---

## 🧪 Posts API Testing (Combined Views)

### 1️⃣ List Posts (Public)

**Request**

```
GET {{BASE_URL}}/api/posts/
```

**Expected Response**

* `200 OK`

---

### 2️⃣ Create Post (Anonymous — Should Fail)

**Request**

```
POST {{BASE_URL}}/api/posts/
```

**Body (JSON)**

```json
{
  "name": "Anonymous User",
  "message": "This should not work"
}
```

**Expected Response**

* `403 Forbidden`

---

### 3️⃣ Create Post (Authenticated — Should Succeed)

🔐 Login as any authenticated user.

**Request**

```
POST {{BASE_URL}}/api/posts/
```

**Body (JSON)**

```json
{
  "name": "Sean",
  "message": "First authenticated post"
}
```

**Expected Response**

* `201 Created`

---

### 4️⃣ Retrieve Post (Public)

**Request**

```
GET {{BASE_URL}}/api/posts/1
```

**Expected Response**

* `200 OK`

---

### 5️⃣ Update Post (Authenticated Only)

**Request**

```
PUT {{BASE_URL}}/api/posts/1
```

**Body (JSON)**

```json
{
  "name": "Sean",
  "message": "Updated post content"
}
```

**Expected Response**

* `200 OK`

---

### 6️⃣ Delete Post (Authenticated Only)

**Request**

```
DELETE {{BASE_URL}}/api/posts/1
```

**Expected Response**

* `204 No Content`

---

## 🔐 Permission Validation Matrix

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

## 🧠 Notes & Best Practices

* **403 Forbidden** = permission denied (expected behavior)
* **401 Unauthorized** = authentication missing or invalid
* Always verify behavior as **anonymous first**, then authenticated
* Use Postman environments to avoid hardcoding URLs

---

## ✅ What This Confirms

* Permissions are correctly enforced per view
* Public vs protected endpoints behave as designed
* The API is safe against unauthorized writes
* The project reflects real-world DRF security patterns


