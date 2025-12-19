# Errday Sportwear - Premium E-commerce Platform

A sophisticated, Django-powered e-commerce platform for high-performance sportswear. Featuring a premium dark-themed UI with glassmorphism, optimized backend architecture, and a dedicated business logic layer.

## ✨ Premium UI Features

- **Modern Aesthetic**: Stunning dark theme with sophisticated purple and pink gradient accents.
- **Glassmorphism Design**: High-end translucent interface elements with advanced backdrop-filter blur effects.
- **Dynamic Animations**: 
  - Subtle breathing background gradients.
  - Interactive product card hover effects (top-border slide, zoom, and elevation).
  - Premium button ripple and glow interactions.
- **Advanced Layout**: 
  - Sophisticated Hero section with parallax-style "Fixed" background.
  - Category-based showcase with interactive zoom cards.
  - Polished footer with gradient-header columns.

## 📋 Comprehensive Features

- **Storefront**: High-performance product catalog with real-time size selection and stock status indicators.
- **Intelligent Cart**: Modern shopping cart with AJAX-powered quantity updates and size persisting.
- **Universal Checkout**: Secure multi-step checkout flow supporting both authenticated and guest users.
- **Responsive Design**: Fully optimized for mobile, tablet, and desktop viewing.
- **Customer Profiles**: One-to-one user profiles with extensible information fields.
- **Architecture**: Decoupled service layer handling complex business logic for cart and order management.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone and Enter Repository**
   ```bash
   cd "c:\Users\Gh_o_st\Desktop\Errday Sportwear\Errday-Sportswear"
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install Optimized Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   ```bash
   copy .env.example .env
   # Update .env with your sensitive keys and settings
   ```

5. **Initialize Optimized Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Seed Premium Data**
   ```bash
   # Add sample sportswear products with high-res assets
   python manage.py shell < create_sample_products.py
   python manage.py shell < update_products_images.py
   ```

7. **Launch Platform**
   ```bash
   python manage.py runserver
   ```

## 📁 Optimized Project Structure

```
Errday-Sportswear/
├── ecommerce/          # System Configuration
│   ├── settings.py     # Secure, environment-driven settings
│   ├── urls.py         # Global routing
│   └── middleware.py   # Advanced Security Headers & CSP
├── store/              # Core Application
│   ├── models.py       # High-performance DB models with composite indexing
│   ├── services.py     # Dedicated Business Logic Layer (Cart, Orders, Products)
│   ├── views.py        # Optimized, documented controllers with specific error handling
│   ├── utils.py        # Documented helper functions with robust logging
│   └── templates/      # Enhanced HTML5/Django templates
├── static/             # Assets (8,600+ redundant files removed)
│   ├── css/            # Premium Design System (Glassmorphism + Gradients)
│   ├── js/             # Clean Vanilla JS logic
│   └── images/         # High-resolution sportswear assets
├── README.md           # Documentation
└── manage.py           # Management script
```

## 🗄️ Enhanced Database Models

Models have been refactored for performance and scalability:
- **Product**: Indexed names, stock tracking, and size variations.
- **Customer**: Linked 1-to-1 with Users, featuring email and name composite indexes.
- **Order**: Indexed transaction IDs and cart management status.
- **Timestamps**: Every model now features reliable `created_at` and `updated_at` fields.

## 🛠️ Infrastructure & Maintenance

- **Service Layer**: Business logic is abstracted into `services.py` for better testability and reuse.
- **Logging**: Comprehensive system logging across all views and utilities.
- **Modern CSS**: 100% bespoke design system without heavy frameworks.

## 🔒 Security & Performance

- **Security Headers**: Custom middleware for CSP, XSS-Protection, and Frame-Options.
- **DB Optimization**: Strategic database indexing on frequently queried fields.
- **Asset Cleanup**: Massive cleanup of 8,600+ unnecessary files for faster development.
- **Query Optimization**: Extensive use of `select_related()` to eliminate N+1 query problems.

## 🤝 Project Standards

- **PEP 8**: 100% compliance with Python style guidelines.
- **Documentation**: 100% docstring coverage for all logic-heavy functions.
- **Typing**: Use of Type Hints for better development experience.

---

**Version**: 1.1.0 (Premium UI Update)
**Last Major Refactor**: December 19, 2025
**Design System**: Custom Glassmorphism Framework
