# Django REST Framework — Generic Views & Permissions

A focused Django REST Framework project demonstrating **generic class-based views**, **API design trade-offs**, and **permission-driven access control**.

This repository compares **granular vs combined DRF generic views** while progressively layering in **realistic authentication and authorization rules**, reflecting how production APIs are structured.

---

## 🎯 Project Goals

This project was built to demonstrate:

* Mastery of **DRF Generic Class-Based Views**
* Intentional API design choices (clarity vs abstraction)
* Practical use of **permission classes** to secure endpoints
* Clean, readable, maintainable REST architecture

---

## 🧠 Architectural Overview

The project contains two apps, each showcasing a different design philosophy.

---

## 🧱 Products App — Granular Generic Views

The `products` app uses **single-responsibility generic views**, where each HTTP action maps to a specific DRF class.

### Views Used

* `ListAPIView`
* `CreateAPIView`
* `RetrieveAPIView`
* `UpdateAPIView`
* `DestroyAPIView`

### Key Characteristics

* Explicit, readable request → response flow
* Uses `slug` instead of `pk` for resource lookup
* Admin-only write access
* Public read access

### Why This Matters

This approach prioritizes **clarity and control**, making it ideal for sensitive resources such as inventory, pricing, or administrative data.

---

## 🧩 Posts App — Combined Generic Views

The `posts` app uses **higher-level combined generic views** to reduce boilerplate.

### Views Used

* `ListCreateAPIView`
* `RetrieveUpdateDestroyAPIView`

### Key Characteristics

* Fewer classes, same functionality
* Public read access
* Authenticated-only write access

### Why This Matters

This pattern is common for content-driven APIs (blogs, comments, feeds), where readability and speed of development matter.

---

## 🔐 Permissions & Access Control

Permissions are applied **per view**, not globally, allowing fine-grained control while keeping the configuration simple.

### Permission Rules

| Resource | Read   | Write               |
| -------- | ------ | ------------------- |
| Products | Public | Admin only          |
| Posts    | Public | Authenticated users |

### Permission Classes Used

* `AllowAny`
* `IsAuthenticatedOrReadOnly`
* `IsAdminUser`

---

## 🔎 Permissions Flow (ASCII Diagram)

```
                    ┌──────────────┐
                    │   Anonymous  │
                    │     User     │
                    └──────┬───────┘
                           │
               ┌───────────┴───────────┐
               │                       │
        GET /products/           GET /posts/
        GET /products/<slug>     GET /posts/<id>
               │                       │
            ✅ Allowed              ✅ Allowed
               │                       │
               └───────────┬───────────┘
                           │
                    ┌──────▼───────┐
                    │ Authenticated│
                    │     User     │
                    └──────┬───────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
     POST /posts/                  PUT /posts/<id>
     DELETE /posts/<id>            PATCH /posts/<id>
            │                             │
         ✅ Allowed                    ✅ Allowed
            │
            └───────────┬───────────┐
                        │
                  ┌─────▼─────┐
                  │   Admin   │
                  │   User    │
                  └─────┬─────┘
                        │
        ┌───────────────┴────────────────┐
        │                                │
 POST /products/create         PUT /products/update/<slug>
 DELETE /products/destroy/<slug>
        │
     ✅ Allowed
```

---

## 🛠️ API Reference

### Products API (Granular)

| Method   | Endpoint                        | Access | Description      |
| -------- | ------------------------------- | ------ | ---------------- |
| `GET`    | `/api/products/`                | Public | List products    |
| `POST`   | `/api/products/create`          | Admin  | Create product   |
| `GET`    | `/api/products/retrieve/<slug>` | Public | Retrieve product |
| `PUT`    | `/api/products/update/<slug>`   | Admin  | Update product   |
| `DELETE` | `/api/products/destroy/<slug>`  | Admin  | Delete product   |

---

### Posts API (Combined)

| Method   | Endpoint              | Access        | Description   |
| -------- | --------------------- | ------------- | ------------- |
| `GET`    | `/api/posts/`         | Public        | List posts    |
| `POST`   | `/api/posts/`         | Authenticated | Create post   |
| `GET`    | `/api/posts/<int:pk>` | Public        | Retrieve post |
| `PUT`    | `/api/posts/<int:pk>` | Authenticated | Update post   |
| `DELETE` | `/api/posts/<int:pk>` | Authenticated | Delete post   |

---

## 🧪 Notable Lessons Learned

### IDE Autocomplete Can Bite

A stray import from Python’s `turtle` module made it into a serializer. Removed and corrected — a reminder to **read imports carefully**.

### Trailing Slashes Matter

Django treats `/endpoint` and `/endpoint/` differently. URL patterns were written deliberately to avoid unnecessary redirects.

### Lookup Fields Are API Design

Switching from `pk` to `slug` dramatically improves URL readability and mirrors real-world REST conventions.

---

## 🚀 Running the Project

```bash
# Activate environment
source venv/bin/activate

# Install dependencies
pip install django djangorestframework mysqlclient

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
```

Authentication testing is available at:

```
/api-auth/login/
```

---

## ✅ Key Takeaways

* DRF generic views scale cleanly from explicit to abstract
* Permissions should be **intentional, visible, and testable**
* Cleaner code does not require sacrificing control
* Good APIs communicate intent through structure


