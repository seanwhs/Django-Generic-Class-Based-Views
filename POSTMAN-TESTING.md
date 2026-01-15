# Postman Testing Guide — DRF Generic Views & Permissions

This document explains how to **manually test all API endpoints using Postman**, with explicit guidance on **when authentication is required** and how permissions are enforced.

It is designed to validate that:

* Public endpoints are accessible without login
* Authenticated endpoints require valid login credentials
* Admin-only actions are properly restricted
* Permission rules behave exactly as designed

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

* At least one superuser exists:

  ```bash
  python manage.py createsuperuser
  ```

* (Optional) A regular non-admin user exists for testing authenticated access

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

## 🔐 Authentication Strategy (Session-Based)

This project uses **Django session authentication**.

### Important Rule

> **Only requests that modify data (POST / PUT / DELETE) require login**
> Read-only (`GET`) requests do **not** require authentication.

Postman will automatically reuse the session **after a successful login**, so you only need to log in **once per session**.

---

## 🔑 Login (Required for Authenticated/Admin Requests)

### Login Endpoint

```
POST {{BASE_URL}}/api-auth/login/
```

### Postman Setup

* Method: `POST`
* Authorization tab: **No Auth**
* Headers:

  ```
  Content-Type: application/x-www-form-urlencoded
  ```
* Body → `x-www-form-urlencoded`:

  ```
  username=admin
  password=yourpassword
  ```

✅ On success:

* Response status: `200 OK`
* Session cookie is stored automatically by Postman

⚠️ Ensure **cookies are enabled** in Postman settings

---

## 🧪 Products API Testing (Granular Views)

### 1️⃣ List Products (Public — No Login)

**Request**

```
GET {{BASE_URL}}/api/products/
```

**Login Required**

* ❌ No

**Expected Response**

* `200 OK`
* JSON list (empty or populated)

---

### 2️⃣ Create Product (Anonymous — Should Fail)

**Request**

```
POST {{BASE_URL}}/api/products/create
```

**Login Required**

* ✅ Yes (Admin)

**Auth Used**

* ❌ Not logged in

**Expected Response**

* `403 Forbidden`

---

### 3️⃣ Create Product (Admin — Should Succeed)

🔐 **Login as admin first** (session cookie must be present)

**Request**

```
POST {{BASE_URL}}/api/products/create
```

**Login Required**

* ✅ Yes (Admin)

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

### 4️⃣ Retrieve Product (Public — No Login)

**Request**

```
GET {{BASE_URL}}/api/products/retrieve/laptop-pro
```

**Login Required**

* ❌ No

**Expected Response**

* `200 OK`

---

### 5️⃣ Update Product (Admin Only)

🔐 **Admin login required**

**Request**

```
PUT {{BASE_URL}}/api/products/update/laptop-pro
```

**Login Required**

* ✅ Yes (Admin)

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

🔐 **Admin login required**

**Request**

```
DELETE {{BASE_URL}}/api/products/destroy/laptop-pro
```

**Login Required**

* ✅ Yes (Admin)

**Expected Response**

* `204 No Content`

---

## 🧪 Posts API Testing (Combined Views)

### 1️⃣ List Posts (Public — No Login)

**Request**

```
GET {{BASE_URL}}/api/posts/
```

**Login Required**

* ❌ No

**Expected Response**

* `200 OK`

---

### 2️⃣ Create Post (Anonymous — Should Fail)

**Request**

```
POST {{BASE_URL}}/api/posts/
```

**Login Required**

* ✅ Yes

**Auth Used**

* ❌ Not logged in

**Expected Response**

* `403 Forbidden`

---

### 3️⃣ Create Post (Authenticated — Should Succeed)

🔐 **Login as any authenticated user (admin or regular user)**

**Request**

```
POST {{BASE_URL}}/api/posts/
```

**Login Required**

* ✅ Yes

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

### 4️⃣ Retrieve Post (Public — No Login)

**Request**

```
GET {{BASE_URL}}/api/posts/1
```

**Login Required**

* ❌ No

**Expected Response**

* `200 OK`

---

### 5️⃣ Update Post (Authenticated Only)

🔐 **Login required**

**Request**

```
PUT {{BASE_URL}}/api/posts/1
```

**Login Required**

* ✅ Yes

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

🔐 **Login required**

**Request**

```
DELETE {{BASE_URL}}/api/posts/1
```

**Login Required**

* ✅ Yes

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

* `403 Forbidden` = authenticated but not allowed (expected)
* `401 Unauthorized` = not logged in
* Always test endpoints in this order:

  1. Anonymous
  2. Authenticated user
  3. Admin user
* Session login persists until Postman cookies are cleared


