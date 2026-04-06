# 🎨 FeyaWorld - Custom Print Solutions E-Commerce Platform

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)

FeyaWorld is a high-end, conceptual e-commerce platform specializing in custom-printed merchandise. From personalized T-shirts and mugs to bespoke towels and blankets, FeyaWorld bridges the gap between creativity and quality printing.

---

## 🚀 Project Vision
FeyaWorld was built to provide a seamless "Print-on-Demand" experience. The platform focuses on high-quality visual representation, responsive design, and robust backend management for both customers and moderators.

---

## 🛠 Technical Stack & Requirements

### Core Technologies
* **Backend:** Django 5.x (Python 3.10+)
* **API:** Django REST Framework (DRF)
* **Database:** PostgreSQL (Relational)
* **Task Queue:** Celery with Redis (Asynchronous Processing)
* **Frontend:** Django Template Engine, Bootstrap 5, Custom CSS3
* **Environment:** Decoupled settings using `.env`

### Project Architecture (The 5-App Rule)
1.  **Users:** Extended User Model, Profiles, and Authentication.
2.  **Products:** Catalog management, Variants (Size/Stock), and Categories.
3.  **Orders:** Shopping cart, Checkout logic, and Order tracking.
4.  **Reviews:** Customer feedback, Ratings, and Moderation.
5.  **Pages:** Static/Dynamic content like Home and About sections.

---

🔑 User Roles & Permissions
To meet the requirement for distinct user groups, the platform features a Moderator role:
Moderator Promotion: Assign is_moderator = True to any user via the Django Admin (/admin/).
Exclusive Access: Moderators can manage orders, update delivery statuses, and perform full CRUD on products directly via the frontend.
Dynamic UI: Management links like "Управление на поръчки" (Order Management) and "Добави обява" (Add Listing) are visible only to authorized staff.

🔌 RESTful API Integration
The project includes a functional Django REST Framework (DRF) service to demonstrate modern API capabilities.
Endpoint: /products/api/list/
Functionality: Returns a serialized JSON list of all products in the database, including titles, prices, and descriptions.
Technical Details: Implemented using DRF Serializers and Class-Based API Views to ensure data integrity and scalability.
How to Test: Simply navigate to http://127.0.0.1:8000/products/api/list/ in your browser or use a tool like Postman to see the dynamic data output.

## 💎 Key Features (Meeting Academic Requirements)

* **90% Class-Based Views (CBV):** Leverages Django's powerful generic views for CRUD operations.
* **Extended User Model:** Custom user roles (Customer, Moderator) with distinct permissions.
* **Complex Database Schema:** Includes 2+ Many-to-Many and 2+ Many-to-One relationships.
* **Advanced Forms:** 7+ forms with custom clean methods, field exclusions, and read-only attributes.
* **Asynchronous Tasks:** Celery integration for background processing (e.g., sending emails or clearing expired carts).
* **RESTful API:** Integrated DRF endpoints for product data serialization.
* **Security:** Fully protected against CSRF, XSS, and SQL Injection. Sensitive data managed via Environment Variables.
* **Responsive UI:** 15+ dynamic templates with a mobile-first approach.

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ferdi7o/Feya-world.git
