# ACADEMIC & PROFESSIONAL PROJECT REPORT
## Assessment Plan A - Final Submission
### Full-Stack Responsive Local Business Web Application & Secure Admin Panel

---

**Project Title:** LuxeCraft Interior Studio - Web Application & Admin Management System  
**Business Domain:** Local Interior Design & Architectural Studio  
**Technology Stack:** Python 3.9+, Flask, MySQL / SQLite, HTML5, CSS3 (Vanilla Glassmorphism), Vanilla JavaScript  
**Submission Date:** August 2026  

---

## 1. Business Problem

### 1.1 Context & Background
**LuxeCraft Interior Studio** is a premier local interior design and architectural planning business specializing in high-end villa renovations, corporate office spatial planning, and custom handcrafted timber furniture. Prior to implementing this project, LuxeCraft operated primarily through offline referrals, print portfolios, and manual messaging apps.

### 1.2 Identified Operational Bottlenecks
1. **Inefficient Portfolio Presentation**: Physical photo albums and static brochures limited prospective clients from viewing photorealistic 3D renders and completed spatial projects dynamically on mobile devices.
2. **Unstructured Client Consultations**: Inquiries received via phone calls and fragmented emails resulted in missed leads, delayed site audits, and poor client tracking.
3. **Lack of Centralized Administrative Control**: Updating service packages, modifying design pricing, and adding new staff bios required manual code changes or external webmaster assistance.
4. **Security & Data Isolation Risks**: Sensitive client contact records and project proposals were stored in unencrypted spreadsheets without access restrictions.

---

## 2. Proposed Solution & System Architecture

### 2.1 Technical Architecture Overview
To solve LuxeCraft’s operational challenges, a robust, full-stack web application with a secure administrative dashboard was engineered using Python Flask and MySQL.

```
                  +-----------------------------------+
                  |         Client Browsers           |
                  |  (Desktop, Tablet, Mobile)        |
                  +-----------------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  |       Flask Web Server            |
                  | (Routing, Auth, Upload Handler)   |
                  +-----------------------------------+
                                    |
                  +-----------------+-----------------+
                  |                                   |
                  v                                   v
    +---------------------------+       +---------------------------+
    |   MySQL Relational DB     |       |  Static Assets & Uploads  |
    |  (luxecraft_db Engine)    |       |  (static/css, /uploads)   |
    +---------------------------+       +---------------------------+
```

### 2.2 Relational Database Design
The application utilizes a normalized MySQL relational database consisting of **6 interconnected tables** with enforced Primary Keys, Foreign Keys (`ON DELETE SET NULL`), and indexing:

1. **`users`**: Secure store for admin accounts containing hashed passwords (`Werkzeug.security`).
2. **`categories`**: Master classifications for residential, commercial, architectural, and custom furniture services.
3. **`services`**: Active design packages linked via `category_id` to `categories.id`.
4. **`gallery`**: Portfolio showcase items linked via `category_id` to `categories.id`.
5. **`team_members`**: Designer profiles, roles, and headshots.
6. **`inquiries`**: Client submissions linked via `service_id` to `services.id`.

### 2.3 Key Functionalities Implemented
- **Multi-Page Responsive Frontend**: 4 core pages (Home, About Us, Services & Pricing, Contact Us) styled with a dark glassmorphic design system.
- **Secure Admin Panel & Authentication**: Password-protected dashboard with session control, metric counters, and authorization gates (`@admin_required`).
- **Full CRUD Capabilities**: Add, Edit, Delete operations for Services, Gallery showcase items, and Team members.
- **Image File Upload Pipeline**: Dynamic upload handling (`secure_filename`, timestamping) for service photography, portfolio renders, and staff headshots.
- **Interactive Contact & Inquiry Tracking**: Client form submissions with real-time status toggling (`Pending`, `In Review`, `Contacted`, `Closed`).

---

## 3. AI Tools Utilized

AI tools were strategically integrated throughout the development lifecycle to accelerate coding, optimize UI aesthetics, and generate domain-specific copy.

| AI Tool / Engine | Application Phase | Specific Tasks Accomplished | Efficiency Gain |
| :--- | :--- | :--- | :--- |
| **Google Gemini 3.6** | System Architecture & Code Generation | Designed Flask route handlers, dual-engine database abstraction (MySQL + SQLite fallback), and CRUD endpoint structure. | **~65% Time Saved** |
| **Antigravity AI Agent** | Frontend UI & CSS Engineering | Built custom CSS design tokens, modern glassmorphic card layouts, responsive navigation drawers, and animations. | **~70% Time Saved** |
| **AI Schema Generator** | Database Engineering | Formatted normalized MySQL DDL script (`schema.sql`) with foreign key constraints and realistic sample seed data. | **~50% Time Saved** |
| **AI Content Drafter** | Copywriting & Documentation | Drafted luxury interior design service descriptions, realistic customer testimonials, and academic project report structure. | **~80% Time Saved** |

---

## 4. Challenges Faced & Solutions Implemented

### Challenge 1: Dynamic Image Upload Handling & Security
* **Problem**: Handling file uploads poses security risks (directory traversal, file overwrites, invalid file extensions) and breaking image links on frontend templates.
* **Resolution**: Implemented `secure_filename()` combined with unique UNIX timestamp prefixes for saved files in `static/uploads/`. Added strict MIME-type and extension validation (`ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}`) along with default fallback image rendering.

### Challenge 2: MySQL Environment Portability & Instant Local Demo
* **Problem**: Setting up MySQL on various student or evaluator machines can fail if local MySQL servers are uninstalled or running on custom ports.
* **Resolution**: Built a dual-engine database abstraction class (`Database`) in `project.py`. The app first attempts to connect to MySQL (`pymysql`). If MySQL is unreachable, it automatically creates and seeds a local SQLite database (`luxecraft.db`), ensuring **100% instant zero-configuration demo execution**.

### Challenge 3: Responsive UI Layout across Mobile and Desktop Devices
* **Problem**: Complex table displays and multi-column grid layouts broke on smaller smartphone viewports.
* **Resolution**: Engineered CSS Flexbox and Grid layouts with media queries (`@media (max-width: 768px)`), overflow-x containers for data tables, and a mobile hamburger menu drawer.

---

## 5. Conclusion & Verification Summary

The LuxeCraft Interior Studio Web Application fully satisfies all requirements specified in **Assessment Plan A Guidelines**:
- ✅ 4-5 responsive pages developed for a real local business model.
- ✅ Secure Admin Panel with hashed login authentication.
- ✅ Full CRUD functionality (Add, Edit, Delete) for services, gallery, and team members.
- ✅ Secure image upload handling.
- ✅ Relational MySQL database (`schema.sql`) with 6 related tables.
- ✅ Live demo verified on localhost.
- ✅ Source code structured and commented for production deployment.
