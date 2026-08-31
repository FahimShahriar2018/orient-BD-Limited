# Orient Computers & Engineering — E-Commerce & Retail Management Platform

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-4.2%20LTS-092e20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952b3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

An enterprise-grade, full-stack Django E-Commerce and Retail Management System developed for **Orient Computers & Engineering**, Dhaka, Bangladesh. The platform combines customer-facing storefront capabilities with Bangladeshi localization (MFS payments, administrative division/district cascade, showroom branches, warranty RMA claims) and a full executive back-office management console.

---

## 📑 Table of Contents

- [Overview & Key Capabilities](#-overview--key-capabilities)
- [System Architecture & Tech Stack](#-system-architecture--tech-stack)
- [10 Core Functional Modules](#-10-core-functional-modules)
- [Project Directory Structure](#-project-directory-structure)
- [Getting Started & Installation](#-getting-started--installation)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Setup](#step-by-step-setup)
- [Default User Accounts & Credentials](#-default-user-accounts--credentials)
- [Configured Test Coupons](#-configured-test-coupons)
- [API & URL Routing Summary](#-api--url-routing-summary)
- [Running Automated Tests](#-running-automated-tests)
- [Showroom & Branch Network](#-showroom--branch-network)

---

## 🌟 Overview & Key Capabilities

- **Bangladeshi Commerce Localization**: Native support for **bKash**, **Nagad**, and Cash on Delivery (COD), 8-Division / 64-District dynamic address selector, and BDT (৳) currency formatting.
- **Enterprise Hardware Catalog**: Engineered for complex technical products (PC Components, AVRs, Online/Offline UPS, IPS, Solar Power Systems, Industrial Batteries, Office Equipment) with structured JSON specification matrices and brand directories.
- **Executive Administrative Back-Office**: Custom `/admin-panel/` featuring real-time revenue velocity charts (Chart.js), order fulfillment pipelines, low-stock warnings, and dynamic key-value spec builders.
- **Live Order Tracking**: Public tracking interface (`ORIENT-YYYY-XXXXXX`) featuring 5-stage milestone progression without mandatory customer login.
- **RMA & Warranty Management**: Customer service portal with automated RMA warranty claims submission and repair tracking.

---

## 🛠 System Architecture & Tech Stack

| Layer | Technologies |
|---|---|
| **Backend Framework** | Python 3.10+, Django 4.2 LTS (MVT Architecture) |
| **Database** | SQLite (Default for zero-config local development) / PostgreSQL Ready |
| **Frontend & UI** | Django Templates, Bootstrap 5.3, Bootstrap Icons, Vanilla JS (ES6+) |
| **Data Visualization** | Chart.js 4.4 (Revenue analytics, order status distribution) |
| **Forms & Styling** | Django Crispy Forms, Crispy Bootstrap 5, Custom Responsive CSS (`orient.css`) |
| **Static & Media** | WhiteNoise, Pillow (Image Processing) |
| **Configuration** | Python-Decouple (`.env` file support) |

---

## 📦 10 Core Functional Modules

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ORIENT COMPUTERS PLATFORM ECOSYSTEM                      │
├──────────────────────────────┬──────────────────────────────────────────────┤
│ CUSTOMER STOREFRONT          │ EXECUTIVE BACK-OFFICE & SERVICE              │
│ • Universal Debounced Search │ • Executive KPI Dashboard (Chart.js)         │
│ • Promotional Engine & Deals │ • Product Catalog CRUD & Spec Builder        │
│ • Faceted Filter & Catalog   │ • 5-Stage Order Pipeline Management          │
│ • Technical Specs PDP Matrix │ • Showroom Branch Locator (8 Locations)      │
│ • Session Cart & Wishlist    │ • Warranty RMA Claim & Complaint Portal      │
│ • Multi-Step Local Checkout  │ • Customer Account & Order History Portal    │
└──────────────────────────────┴──────────────────────────────────────────────┘
```

### Module 1: Global Navigation & Universal Live Search
- Sticky navigation bar with corporate support contact (`+880 1711-000001`), Motijheel flagship indicator, and official warranty promise badge.
- **300ms debounced live search** with category dropdown filter and real-time product thumbnail preview.
- Dynamic cart count counter badge and slide-out Offcanvas cart drawer.
- Sticky bottom navigation bar optimized for mobile viewports.

### Module 2: Storefront Homepage & Promotional Engine
- Hero promotional slider showcasing flagship enterprise solutions and seasonal hardware deals.
- Dynamic hardware departments grid with live inventory counters.
- **Flash Deals Section** with real-time JavaScript countdown timer (`HH:MM:SS`).
- Catalog spotlight tabs: *Featured*, *New Arrivals*, and *Top Selling*.
- Brand partner carousel featuring official distributors (Intel, AMD, NVIDIA, ASUS, MSI, APC, Apollo, Luminous, etc.).

### Module 3: Multi-Facet Product Catalog & Exploration
- Faceted filtering: Category tree, multi-brand selection, dual min/max BDT price sliders, in-stock only toggle, and customer star rating thresholds.
- Dynamic sorting: Price (Low to High / High to Low), Customer Rating, Popularity, and Date Added.
- Instant Grid and List view switcher preserving active query parameters.
- SEO-friendly URL query state with pagination controls.

### Module 4: Product Details Page (PDP) & Technical Specs Matrix
- High-resolution product image gallery with interactive thumbnail switcher.
- Pricing with calculated discount savings (`SAVE X%`), SKU identifier, and live stock indicator.
- Structured **Technical Specification Matrix** dynamically generated from JSON fields.
- Key specification bullet highlights.
- Verified customer review engine with 5-star distribution histogram and submission form.
- Automated related and compatible hardware recommendations.

### Module 5: Shopping Cart & Wishlist Subsystems
- Session-backed cart persistence with instant quantity increment/decrement controls.
- Real-time subtotal calculation and free nationwide shipping progress bar (৳50,000 threshold).
- Promotional voucher system supporting percentage discounts and flat value deductions (`ORIENT10`, `ORIENT500`, `GAMING2026`).
- Slide-out Cart Drawer (Offcanvas) for seamless browsing without leaving pages.
- Persistent Wishlist with single-click "Move to Cart" action.

### Module 6: Multi-Step Checkout & Bangladeshi Localization
- Pre-filled customer contact details for authenticated users.
- **Dynamic Administrative Cascade**: Selecting one of Bangladesh's 8 Divisions instantly filters and populates its corresponding Districts (64 total).
- 4 Courier & Delivery Options:
  - *Inside Dhaka City Courier* (৳100)
  - *Outside Dhaka Courier Delivery* (৳200)
  - *Express Same-Day Delivery* (৳300)
  - *Store Showroom Pickup* (Free)
- Payment Gateway Integrations:
  - **bKash** (Merchant Payment flow with instructions and TrxID verification field)
  - **Nagad** (Merchant Payment flow with instructions and TrxID verification field)
  - **Cash on Delivery (COD)**
- Atomic inventory stock reservation and decrement upon order confirmation.

### Module 7: Order Management, Invoicing & 5-Stage Live Tracking
- Automated tracking code generation (`ORIENT-YYYY-XXXXXX`).
- Public **5-Stage Live Order Tracker** (Pending ➔ Confirmed ➔ Processing ➔ Shipped ➔ Delivered).
- Visual timeline history recording timestamped order milestones.
- Customer dashboard order history and detail inspection.
- Browser-printable, clean commercial **Tax/VAT Invoice** (`@media print` stylesheet).

### Module 8: User Authentication, Profile & Customer Portal
- Custom `User` model extending `AbstractUser` with RBAC (`customer` and `admin` roles).
- Self-service registration, login, and password management.
- Customer account dashboard with saved delivery address book and profile avatar.
- Comprehensive order history with direct access to tracking and PDF/printable invoices.

### Module 9: Executive Back-Office & Administrative Management
- Dedicated administrative portal at `/admin-panel/` guarded by `@admin_required` decorators.
- Real-time KPI summary metrics: *Gross Revenue (৳)*, *Total Orders*, *Active Inventory SKUs*, and *Registered Customer Base*.
- **Chart.js Visualizations**: 7-Day Revenue Velocity bar chart and Order Status breakdown doughnut chart.
- Low-stock inventory alert board (< 5 units in stock).
- Comprehensive Product CRUD with dynamic key-value technical spec builder in JavaScript.
- Order fulfillment control center with 1-click status advancement and tracking updates.

### Module 10: Customer Service, Branches & Feedback Subsystem
- Physical showroom branch directory (Motijheel Corporate, IDB Bhaban, Multiplan Center, Uttara, Chattogram, Sylhet, etc.) with operating hours, phone lines, and direct Google Maps navigation.
- Dedicated **Warranty / RMA Claim submission** portal for hardware repairs and replacements.
- Customer inquiry and feedback messaging system.

---

## 📂 Project Directory Structure

```
orientInternshipProject/
├── apps/
│   ├── accounts/          # User authentication, RBAC, customer profiles, address book
│   │   ├── models.py      # Custom User model (role-based)
│   │   ├── views.py       # Login, register, profile, dashboard views
│   │   └── urls.py
│   ├── adminpanel/        # Custom back-office executive dashboard & management
│   │   ├── views.py       # KPI analytics, Product CRUD, Order management
│   │   └── urls.py
│   ├── cart/              # Session-based shopping cart and wishlist
│   │   ├── cart.py        # Cart context and session calculation engine
│   │   ├── views.py       # Cart drawer, update, remove, wishlist actions
│   │   └── urls.py
│   ├── catalog/           # Product catalog, categories, brands, specs & reviews
│   │   ├── models.py      # Category, Brand, Product, ProductImage, Review, Wishlist
│   │   ├── views.py       # Filtered catalog, product detail, brand directory
│   │   └── urls.py
│   ├── core/              # Storefront homepage, universal search & seed script
│   │   ├── views.py       # Homepage, live search JSON API, static info pages
│   │   ├── management/    # Database seeding command (seed_data.py)
│   │   └── urls.py
│   ├── orders/            # Checkout, BD division cascade, order tracking & invoices
│   │   ├── models.py      # Order, OrderItem, Coupon, OrderTimeline
│   │   ├── views.py       # Multi-step checkout, tracking portal, invoice view
│   │   └── urls.py
│   └── service/           # Branches / showrooms, warranty RMA claims & contact
│       ├── models.py      # Branch, ServiceRequest (RMA), ContactMessage
│       ├── views.py       # Branch locator, warranty claim form
│       └── urls.py
├── media/                 # Uploaded product images, brand logos, category banners
├── orient/                # Django project root configuration
│   ├── settings.py        # Application settings, middleware, static/media paths
│   ├── urls.py            # Global URL router
│   └── wsgi.py
├── static/
│   ├── css/
│   │   └── orient.css     # Custom corporate UI styles & print invoice rules
│   └── js/
│       └── orient.js      # Live search, cart steppers, BD geodata, specs builder
├── templates/             # Modular HTML templates with Bootstrap 5.3
│   ├── accounts/          # Login, registration, profile, password templates
│   ├── adminpanel/        # Executive dashboard, product CRUD, order admin
│   ├── base.html          # Global layout wrapper
│   ├── cart/              # Shopping cart and wishlist views
│   ├── catalog/           # Product grid, product detail page, brand list
│   ├── home/              # Homepage with hero slider and deals
│   ├── orders/            # Checkout form, order confirmation, tracking, invoice
│   ├── partials/          # Header, footer, cart drawer, mega menu
│   └── service/           # Branches list, warranty RMA submission
├── .env.example           # Example environment variable file
├── db.sqlite3             # Local development database
├── manage.py              # Django management utility
└── requirements.txt       # Python project dependencies
```

---

## 🚀 Getting Started & Installation

### Prerequisites
- **Python 3.10+** installed on your system
- **Git** for version control
- `pip` and virtual environment support (`venv`)

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/orientInternshipProject.git
cd orientInternshipProject
```

#### 2. Create and Activate a Virtual Environment
- **On Windows (PowerShell / Command Prompt):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Copy `.env.example` to `.env` and adjust the variables if necessary:
- **On Windows:**
  ```powershell
  copy .env.example .env
  ```
- **On macOS / Linux:**
  ```bash
  cp .env.example .env
  ```

#### 5. Apply Database Migrations
```bash
python manage.py makemigrations accounts catalog orders service
python manage.py migrate
```

#### 6. Seed the Database with Catalog & Showroom Data
Run the custom seed command to populate categories, brands, sample hardware products, 8 showroom branches, coupons, and demo accounts:
```bash
python manage.py seed_data
```

#### 7. Run the Development Server
```bash
python manage.py runserver
```
Navigate to **`http://127.0.0.1:8000/`** in your browser to view the live platform.

---

## 🔐 Default User Accounts & Credentials

The seed command creates predefined accounts for administrative testing and customer workflows:

| Role | Username | Password | Email | Access Scope |
|---|---|---|---|---|
| **Store Administrator** | `admin` | `admin123` | `admin@orientcomputers.com.bd` | Executive Back-Office (`/admin-panel/`) & Django Admin (`/django-admin/`) |
| **Demo Customer** | `fahim` | `customer123` | `fahim@orient.bd` | Customer Portal (`/account/`), Checkout & Reviews |

---

## 🎟 Configured Test Coupons

You can use the following promotional codes during checkout:

| Coupon Code | Discount Type | Threshold / Conditions | Description |
|---|---|---|---|
| **`ORIENT10`** | 10% Off | No minimum order | 10% percentage discount on entire basket |
| **`ORIENT500`** | ৳500 Flat Off | Min order ৳5,000 | ৳500 flat deduction on qualifying orders |
| **`GAMING2026`** | 15% Off | Min order ৳50,000 | 15% discount on premium & enterprise hardware |

---

## 🌐 API & URL Routing Summary

| Endpoint URL | View / Purpose | Module |
|---|---|---|
| `/` | Storefront Homepage with hero banners, flash deals, and spotlight tabs | Module 2 |
| `/api/search/` | Debounced live JSON search API with category filters | Module 1 |
| `/shop/` | Multi-facet catalog with dynamic filter sidebar & sorting | Module 3 |
| `/shop/<slug>/` | Product detail page with specs matrix and review system | Module 4 |
| `/brand/` | Brand partner directory indexed alphabetically | Module 3 |
| `/brand/<slug>/` | Brand-specific product catalog | Module 3 |
| `/cart/` | Shopping cart overview with promo coupon engine | Module 5 |
| `/cart/wishlist/` | Customer wishlist with one-click move to cart | Module 5 |
| `/checkout/` | Multi-step checkout with division/district cascades & MFS payments | Module 6 |
| `/checkout/track/` | Public 5-stage live order tracking portal | Module 7 |
| `/checkout/invoice/<order_id>/` | Printable commercial VAT/Tax invoice | Module 7 |
| `/account/dashboard/` | Customer account dashboard & address management | Module 8 |
| `/admin-panel/` | Executive administrative back-office & Chart.js analytics | Module 9 |
| `/service/branches/` | Showroom locator with opening hours & Google Maps | Module 10 |
| `/service/warranty/` | Warranty RMA claim & hardware repair request submission | Module 10 |

---

## 🧪 Running Automated Tests

Run the test suite using Django's built-in test runner:

```bash
python manage.py test apps.catalog
```

To run tests across the entire project:
```bash
python manage.py test
```

---

## 🏢 Showroom & Branch Network

Orient Computers maintains 8 physical branches across Bangladesh:
1. **Motijheel Flagship Corporate Branch** (Rahmania International Complex, Motijheel C/A, Dhaka)
2. **IDB Bhaban Branch** (BCS Computer City, Agargaon, Dhaka)
3. **Multiplan Center Branch** (ECS Computer City, Elephant Road, Dhaka)
4. **Power House Branch** (Sundarban Square Market, Nawabpur, Gulistan, Dhaka)
5. **Uttara Branch** (SGC Computer City, Jashimuddin Avenue, Uttara, Dhaka)
6. **Chattogram Branch** (R F Johora Tower, Agrabad C/A, Chattogram)
7. **Sylhet Branch** (Karim Ullah Market, Bondor Bazar, Sylhet)
8. **Bogura Branch** (Amir Complex, Bogura)

---

## 📄 License & Attribution

This project is developed for **Orient Computers & Engineering**, Dhaka, Bangladesh.
All rights reserved © 2026. Designed for enterprise computer hardware, power engineering, and ICT infrastructure retail.
