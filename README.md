# Django REST Framework — Generic Views, Permissions, JWT, Swagger & Logging

A focused Django REST Framework (DRF) project demonstrating:

* **Generic class-based views** (both granular and combined)
* **REST API design trade-offs**
* **Permission-driven access control**
* **JWT authentication** (via SimpleJWT)
* **Automatic Swagger / OpenAPI documentation**
* **Request/response logging via custom middleware**

This repository intentionally contrasts **granular vs combined generic views** while layering in real-world concerns such as authentication, authorization, observability, and documentation — closely mirroring how production APIs are built.

---

## 🎯 Project Goals

* Master **DRF Generic Class-Based Views**
* Explore **intentional REST API design patterns**
* Implement fine-grained **permission enforcement**
* Maintain **clean, extensible Django architecture**
* Integrate **JWT-based authentication**
* Generate **automatic Swagger / OpenAPI documentation**
* Log requests/responses via **custom middleware**
* Follow production-oriented configuration practices

---

## 📦 Tech Stack & Dependencies

**Core dependencies:**

```
Django==6.0.1
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
drf-spectacular==0.29.0
drf-spectacular-sidecar==2026.1.1
PyJWT==2.10.1
sqlparse==0.5.5
tzdata==2025.3
```

Supporting libraries provide **schema validation, OpenAPI utilities, and typing helpers** for Swagger generation and JWT handling.

---

## 🧠 Architectural Overview

The project consists of **two apps** demonstrating different DRF design philosophies:

* **Products App** – granular, single-responsibility generic views
* **Posts App** – combined, higher-level generic views

Both apps share **centralized authentication, Swagger documentation, and logging**.

---

## 🧱 Products App — Granular Generic Views

The **Products app** maps each HTTP action to a dedicated DRF generic view.

**Views:**

* `ListAPIView`
* `CreateAPIView`
* `RetrieveAPIView`
* `UpdateAPIView`
* `DestroyAPIView`

**Key Characteristics:**

* Explicit request → response mapping
* Uses `slug` for lookups
* **Admin-only write access**, **public read access**

**Use Case:**

Ideal for sensitive resources (e.g., inventory, pricing) where **clarity, auditability, and fine-grained permissions** are critical.

---

## 🧩 Posts App — Combined Generic Views

The **Posts app** combines multiple HTTP methods in fewer classes.

**Views:**

* `ListCreateAPIView`
* `RetrieveUpdateDestroyAPIView`

**Key Characteristics:**

* Fewer classes, same REST behavior
* **Public read access**, **authenticated write access**

**Use Case:**

Suitable for content-driven APIs (blogs, feeds), prioritizing **developer speed and maintainability** over granular control.

---

## 🔐 Permissions & Access Control

**Rules per resource:**

| Resource | Read Access | Write Access  |
| -------- | ----------- | ------------- |
| Products | Public      | Admin only    |
| Posts    | Public      | Authenticated |

**Classes used:**

* `AllowAny`
* `IsAuthenticatedOrReadOnly`
* `IsAdminUser`

---

## 🔑 Authentication — JWT (SimpleJWT)

**Token Endpoints:**

```
POST /api/token/
POST /api/token/refresh/
```

* `/api/token/` returns `access` and `refresh` tokens
* Use `Authorization: Bearer <access_token>` in request headers

**Benefits:**

* Stateless authentication
* Eliminates CSRF
* Works seamlessly with Swagger, Postman, and frontend apps

---

## 📚 API Documentation — Swagger & OpenAPI

* Powered by **drf-spectacular**
* Generates **interactive OpenAPI 3 documentation** from views, serializers, permissions, and JWT settings
* No manual documentation is required

**Endpoints:**

| Tool           | URL            | Description              |
| -------------- | -------------- | ------------------------ |
| Swagger UI     | `/api/docs/`   | Interactive API explorer |
| ReDoc          | `/api/redoc/`  | Clean, readable docs     |
| OpenAPI Schema | `/api/schema/` | Raw OpenAPI 3 spec       |

**Swagger Usage:**

1. Visit `http://127.0.0.1:8000/api/docs/`
2. Browse endpoints
3. Authenticate using JWT
4. Execute API requests directly

---

## 🪵 Logging & Observability

Custom **API request/response logging** via `DRFRequestResponseLoggingMiddleware`.

**Highlights:**

* Logs written to `logs/api.log`
* Captures HTTP method, path, status codes, timestamps
* Uses custom Django logger for isolated auditing

---

## 🛠️ API Reference

### Products API (Granular)

| Method | Endpoint                        | Access | Description      |
| ------ | ------------------------------- | ------ | ---------------- |
| GET    | `/api/products/`                | Public | List products    |
| POST   | `/api/products/create`          | Admin  | Create product   |
| GET    | `/api/products/retrieve/<slug>` | Public | Retrieve product |
| PUT    | `/api/products/update/<slug>`   | Admin  | Update product   |
| DELETE | `/api/products/destroy/<slug>`  | Admin  | Delete product   |

### Posts API (Combined)

| Method | Endpoint              | Access        | Description   |
| ------ | --------------------- | ------------- | ------------- |
| GET    | `/api/posts/`         | Public        | List posts    |
| POST   | `/api/posts/`         | Authenticated | Create post   |
| GET    | `/api/posts/<int:pk>` | Public        | Retrieve post |
| PUT    | `/api/posts/<int:pk>` | Authenticated | Update post   |
| DELETE | `/api/posts/<int:pk>` | Authenticated | Delete post   |

---

## 🧪 Lessons Learned

* **IDE Autocomplete Can Bite** – always audit imports
* **Trailing Slashes Matter** – `/endpoint` ≠ `/endpoint/`
* **Lookup Fields Shape APIs** – `slug` improves readability
* **JWT vs Session Auth** – stateless, header-based, clean Swagger/Postman integration

---

## 🧠 Products vs Posts — Core Takeaways

This project is a personal refresher on **DRF generic views**, illustrating why **different patterns exist**:

* **Products (Granular)**

  * One class per action
  * Clear permission boundaries
  * Maximum control
  * Easy to extend

* **Posts (Combined)**

  * Multiple methods per class
  * Less boilerplate
  * Shared permissions
  * Faster iteration

Side-by-side implementation with shared auth, logging, and Swagger makes the distinction concrete.

---

## ✅ Key Takeaways

* DRF generic views scale from **explicit** to **abstract**
* Products vs Posts demonstrates **intentional design choices**
* Permissions must be **visible and enforced**
* JWT simplifies authentication
* Swagger keeps docs **accurate and self-updating**
* Logging is essential for production observability
* API structure communicates architectural intent

---

## 🖼️ DRF Generic Views — Unified Diagram (Hierarchy + Endpoints + Methods + Permissions)

```
                     ┌─────────────────────────┐
                     │  Django REST Framework  │
                     │      Generic Views      │
                     └────────────┬──────────┘
                                  │
          ┌───────────────────────┴───────────────────────┐
          │                                               │
    ┌───────────────┐                               ┌───────────────┐
    │  Products App │                               │  Posts App    │
    │  (Granular)   │                               │  (Combined)   │
    └──────┬────────┘                               └──────┬────────┘
           │                                               │
           │                                               │
┌─────────────┐   ┌──────────────┐                   ┌──────────────────────────┐
│ ListAPIView │   │ CreateAPIView│                   │ ListCreateAPIView       │
│ /products/  │   │ /products/create│                │ /posts/                 │
│ GET ✅ P    │   │ POST ✅ AD     │                   │ GET ✅ P  POST ✅ A      │
└─────────────┘   └──────────────┘                   └──────────────────────────┘
       │                 │
┌─────────────┐   ┌─────────────┐                   ┌──────────────────────────┐
│RetrieveAPIView│ │UpdateAPIView│                   │RetrieveUpdateDestroyAPIView│
│ /products/retrieve/<slug> │ /products/update/<slug> │ /posts/<id>             │
│ GET ✅ P     │ │ PUT ✅ AD   │                   │ GET ✅ P  PUT ✅ A  DELETE ✅ A │
└─────────────┘   └─────────────┘                   └──────────────────────────┘
       │
┌─────────────┐
│DestroyAPIView│
│ /products/destroy/<slug> │
│ DELETE ✅ AD │
└─────────────┘
```

**Legend:** P = Public, A = Authenticated, AD = Admin

---

### 📝 Endpoint → Methods → Permissions (Quick Reference)

#### Products (Granular)

| Endpoint                        | GET | POST | PUT | DELETE | Permissions |
| ------------------------------- | --- | ---- | --- | ------ | ----------- |
| `/api/products/`                | ✅   |      |     |        | Public      |
| `/api/products/create`          |     | ✅    |     |        | Admin       |
| `/api/products/retrieve/<slug>` | ✅   |      |     |        | Public      |
| `/api/products/update/<slug>`   |     |      | ✅   |        | Admin       |
| `/api/products/destroy/<slug>`  |     |      |     | ✅      | Admin       |

#### Posts (Combined)

| Endpoint          | GET | POST | PUT | DELETE | Permissions                          |
| ----------------- | --- | ---- | --- | ------ | ------------------------------------ |
| `/api/posts/`     | ✅   | ✅    |     |        | GET=Public, POST=Authenticated       |
| `/api/posts/<id>` | ✅   |      | ✅   | ✅      | GET=Public, PUT/DELETE=Authenticated |

