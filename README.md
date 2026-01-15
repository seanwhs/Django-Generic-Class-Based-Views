# Django REST Framework: Views & ViewSets Lab

This repository is a hands-on learning lab for mastering **Django REST Framework (DRF)**. It focuses on the transition from manual logic to high-level abstractions using ViewSets and Routers.

## 🚀 Project Overview

The goal of this project is to compare and contrast the two primary ways of building API endpoints in DRF:

1. **Explicit ViewSets:** Manually defining `list`, `create`, `retrieve`, etc. (Control-focused).
2. **Automated ViewSets:** Using `ModelViewSet` to handle everything via inheritance (Efficiency-focused).

---

## 🏗️ Architecture Comparison

### 1. Contacts App (`ModelViewSet`)

* **Pattern:** High-level abstraction.
* **Key Feature:** Minimal code. By inheriting from `viewsets.ModelViewSet`, we get all CRUD operations automatically without writing a single method.
* **Logic:**
* `queryset`: Tells DRF which data to fetch.
* `serializer_class`: Tells DRF how to transform that data.



### 2. Products App (`Manual ViewSet`)

* **Pattern:** Explicit implementation.
* **Key Feature:** Complete control over the request/response lifecycle.
* **Methods Implemented:**
* `list()`: GET all products.
* `create()`: POST new product with validation.
* `retrieve()`: GET single product via `slug`.
* `update()` / `partial_update()`: PUT/PATCH logic.
* `destroy()`: DELETE logic.



---

## 🛠️ API Surface Map

| Endpoint | Method | Action | App |
| --- | --- | --- | --- |
| `/api/contacts/` | GET | List all contacts | Contacts |
| `/api/contacts/` | POST | Create contact | Contacts |
| `/api/products/` | GET | List all products | Products |
| `/api/products/` | POST | Create product | Products |
| `/api/products/<slug>/` | GET | Retrieve product | Products |
| `/api/products/<slug>/` | DELETE | Remove product | Products |

---

## 📝 Lessons Learned

* **Trailing Slashes:** DRF Routers strictly enforce trailing slashes. `.../api/products/` works, while `.../api/products` may fail.
* **Status Codes:** Always use uppercase constants from `rest_framework.status` (e.g., `status.HTTP_201_CREATED`).
* **Slug Lookups:** By setting `lookup_field = 'slug'`, we move away from boring IDs to SEO-friendly URLs.
* **DRF Routers:** The `DefaultRouter` automates the URL configuration, mapping HTTP verbs to ViewSet methods.

---

## 🔧 Installation & Setup

1. **Clone and Enter Environment:**
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

```


2. **Install Dependencies:**
```bash
pip install django djangorestframework mysqlclient

```


3. **Database Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate

```


4. **Run Server:**
```bash
python manage.py runserver

```

