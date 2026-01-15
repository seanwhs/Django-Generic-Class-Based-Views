# Django REST Framework: The Generic Views Lab

This repository documents my progression through **Django REST Framework (DRF)**, moving from granular, single-purpose views to streamlined, combined generic views.

## 🎯 Learning Objective

The core of this lab is understanding the **DRF Class-Based View (CBV) Hierarchy**. I have implemented two different architectural patterns to compare code efficiency and endpoint mapping.

---

## 🏗️ Architectural Patterns

### 1. The "Granular" Approach (`products` app)

In this app, I used **Single-Purpose Generic Views**. This is excellent for learning exactly how each HTTP method maps to a specific DRF class.

* **Views used:** `ListAPIView`, `CreateAPIView`, `RetrieveAPIView`, `UpdateAPIView`, `DestroyAPIView`.
* **Key Learning:** Using `lookup_field = 'slug'` to move away from primary keys (IDs) to SEO-friendly identifiers.

### 2. The "Combined" Approach (`posts` app)

In this app, I moved up the abstraction ladder by using **Combined Generic Views**.

* **`ListCreateAPIView`**: Handles both `GET` (List) and `POST` (Create) in a single class.
* **`RetrieveUpdateDestroyAPIView`**: Handles `GET` (Retrieve), `PUT/PATCH` (Update), and `DELETE` (Destroy) in one class.
* **Result:** Reduced code volume by **50%** while maintaining the exact same functionality.

---

## 🛠️ API Reference

### Products (Granular)

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/products/` | List all products |
| `POST` | `/api/products/create` | Create a new product |
| `GET` | `/api/products/retrieve/<slug>` | Get a product by slug |
| `PUT` | `/api/products/update/<slug>` | Update a product |
| `DELETE` | `/api/products/destroy/<slug>` | Delete a product |

### Posts (Combined)

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET/POST` | `/api/posts/` | List all posts or Create a post |
| `GET/PUT/DELETE` | `/api/posts/<int:pk>` | Retrieve, Update, or Delete by ID |

---

## 📝 Critical Code Fixes & Lessons

### 1. The "Turtle" Incident

During development, an accidental import from the `turtle` library occurred in the serializer. Corrected to:

```python
# Fixed: Removed 'from turtle import mode'
from rest_framework import serializers
from .models import Post

```

### 2. URL Trailing Slashes

Django's `APPEND_SLASH` behavior means that `/api/products/` and `/api/products` are treated differently. For this lab, I have ensured that the URL configuration matches the request pattern to avoid unnecessary `301` redirects.

### 3. Lookup Fields

By default, DRF looks for `pk`. In the `products` app, I successfully overrode this to use `slug`:

```python
class RetrieveProductAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug' # Enables slug-based routing

```

---

## 🚀 How to Run

1. **Activate Environment:** `source venv/bin/activate` (or `.\venv\Scripts\activate` on Windows).
2. **Install Specs:** `pip install django djangorestframework mysqlclient`.
3. **Migrate:** `python manage.py migrate`.
4. **Run:** `python manage.py runserver`.
