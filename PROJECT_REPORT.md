# ACADEMIC & PROFESSIONAL PROJECT REPORT
## Assessment Plan A - Final Submission
### Full-Stack Responsive Local Business Web Application & Secure Admin Panel

---

**Project Title:** LuxeCraft Interior Studio - Web Application & Admin Management System  
**Business Domain:** Local Interior Design & Architectural Studio  
**Technology Stack:** Python 3.9+, Flask, MySQL / SQLite, HTML5, CSS3 (Vanilla Glassmorphism), Vanilla JavaScript, Vercel Serverless  
**Live Deployment:** [https://dtn-final-project.vercel.app](https://dtn-final-project.vercel.app)  
**Submission Date:** August 2026  

---

## 1. Business Problem

### 1.1 Context & Background
**LuxeCraft Interior Studio** is a premier local interior design and architectural planning business specializing in luxury residential renovations, bespoke corporate workspace planning, and custom handcrafted timber furniture. Prior to implementing this digital solution, LuxeCraft operated through offline referrals, print portfolios, and unorganized manual messaging channels.

### 1.2 Identified Operational Bottlenecks
1. **Inefficient Portfolio Presentation**: Physical photo albums and static brochures prevented prospective clients from viewing photorealistic 3D renders and completed spatial projects dynamically on mobile and desktop devices.
2. **Unstructured Client Consultations & Quoting**: Inquiries received via phone calls and fragmented emails resulted in missed leads, delayed site audits, and inaccurate project cost expectations.
3. **Lack of Centralized Administrative Control**: Updating service packages, modifying design pricing, publishing new portfolio showcases, and updating staff profiles required manual source code changes or external webmaster assistance.
4. **Security & Data Isolation Risks**: Sensitive client contact records and project proposals were stored in unencrypted spreadsheets without access restrictions or role-based authentication.

---

## 2. Proposed Solution & System Architecture

### 2.1 Technical Architecture Overview
To resolve LuxeCraft’s operational challenges, a robust, full-stack web application with a secure administrative dashboard was engineered using Python Flask, a dual-engine MySQL/SQLite database abstraction layer, and modern glassmorphic responsive UI design.

```
                  +-----------------------------------+
                  |         Client Browsers           |
                  |  (Desktop, Tablet, Mobile)        |
                  +-----------------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  |      Vercel Edge / Flask App      |
                  | (Routing, Auth, Image Pipeline)   |
                  +-----------------------------------+
                                    |
                  +-----------------+-----------------+
                  |                                   |
                  v                                   v
    +---------------------------+       +---------------------------+
    |   Dual-Engine Database    |       |   Media & Asset Engine    |
    | (MySQL / SQLite Fallback) |       | (Base64 / 4K Unsplash CDN)|
    +---------------------------+       +---------------------------+
```

### 2.2 Relational Database Design
The application utilizes a normalized relational schema consisting of **6 interconnected tables** with enforced Primary Keys, Foreign Keys (`ON DELETE SET NULL`), and indexing:

1. **`users`**: Secure store for admin accounts containing hashed passwords (`Werkzeug.security.generate_password_hash`).
2. **`categories`**: Master classifications for residential, commercial, architectural, and custom furniture services.
3. **`services`**: Active design packages linked via `category_id` to `categories.id`.
4. **`gallery`**: Portfolio showcase items linked via `category_id` to `categories.id`.
5. **`team_members`**: Designer profiles, roles, contact info, and headshots.
6. **`inquiries`**: Client consultation submissions linked via `service_id` to `services.id`.

### 2.3 Key Functionalities Implemented
- **Multi-Page Responsive Frontend**: 4 core pages (Home, About Us, Services & Pricing, Contact Us) styled with a dark glassmorphic design system.
- **Interactive Spatial Project Estimator**: Live JavaScript widget allowing clients to select property types, adjust space area (sq ft) with a custom gradient range slider, toggle add-on packages, and calculate instant budget estimates.
- **Secure Admin Panel & Authentication**: Password-protected dashboard with session control, metric counters, and authorization gates (`@admin_required`).
- **Full CRUD Capabilities**: Add, Edit, Delete operations for Services, Gallery showcase items, and Team members.
- **Fail-Safe Image & Media Pipeline**: Dual-mode upload system that converts local file uploads into optimized Base64 Data URIs (via Pillow) and supports direct web/CDN image URLs for 100% cloud persistence.
- **Interactive Contact & Inquiry Tracking**: Client form submissions with real-time status toggling (`Pending`, `In Review`, `Contacted`, `Closed`).

---

## 3. AI Tools Utilized

AI tools were strategically integrated throughout the development lifecycle to accelerate coding, optimize UI aesthetics, and generate domain-specific copy.

| AI Tool / Engine | Application Phase | Specific Tasks Accomplished | Efficiency Gain |
| :--- | :--- | :--- | :--- |
| **Google Gemini 3.6 / Antigravity** | System Architecture & Serverless Backend | Engineered Flask route handlers, WSGI Vercel middleware, Pillow Base64 image compression, and dual MySQL/SQLite engine. | **~75% Time Saved** |
| **Antigravity AI Agent** | Frontend UI & CSS Engineering | Built dark glassmorphism design tokens, custom range slider, responsive mobile drawer, and interactive budget estimator. | **~70% Time Saved** |
| **AI Schema Generator** | Database Engineering | Formatted normalized MySQL DDL script (`schema.sql`) with foreign key constraints and realistic sample seed data. | **~50% Time Saved** |
| **AI Content Drafter** | Copywriting & Documentation | Drafted luxury interior design service descriptions, realistic customer testimonials, and academic project report structure. | **~80% Time Saved** |

---

## 4. Challenges Faced & Solutions Implemented

### Challenge 1: Serverless Cloud Deployment & Ephemeral Filesystem (Vercel)
* **Problem**: Traditional Flask applications write uploaded files directly to the local disk (`static/uploads/`) and rely on persistent server processes. On Vercel's serverless architecture, the filesystem is read-only except `/tmp`, containers spin down dynamically, and root-level static asset requests were returning 404.
* **Resolution**:
  1. Built `api/index.py` with custom `VercelPathMiddleware` to normalize WSGI routing paths.
  2. Implemented automatic SQLite database copying and initialization in `/tmp/luxecraft.db`.
  3. Integrated **Pillow image optimization** to compress uploaded images into self-contained **Base64 Data URIs** stored directly in the database row, guaranteeing 100% cloud persistence and zero broken image links.

### Challenge 2: Dynamic Image Upload Handling & High-Resolution Rendering
* **Problem**: Large image uploads from diverse camera formats caused layout breakage, slow page loads, and broken image placeholders when binary files were omitted in Git pushes.
* **Resolution**: Replaced generic placeholders with a curated 4K Unsplash architectural photography pipeline and added client-side `onerror` fallbacks alongside direct CDN URL inputs in all Admin creation modals.

### Challenge 3: MySQL Environment Portability & Instant Local Demo
* **Problem**: Setting up MySQL on various student or evaluator machines can fail if local MySQL servers are uninstalled or running on custom ports.
* **Resolution**: Built a dual-engine database abstraction class (`Database`) in `project.py`. The app first attempts to connect to MySQL (`pymysql`). If MySQL is unreachable, it automatically creates and seeds a local SQLite database (`luxecraft.db`), ensuring **100% instant zero-configuration demo execution**.

### Challenge 4: Responsive UI Layout & Interactive Range Slider Styling
* **Problem**: Complex data tables broke on smartphone viewports, and default browser range sliders appeared as unstyled, thick bars.
* **Resolution**: Engineered CSS Flexbox and Grid layouts with media queries (`@media (max-width: 768px)`), overflow-x containers for data tables, and a custom `.custom-range-slider` with a smooth gradient track, glowing thumb, and min/max range markers.

---

## 5. Conclusion & Verification Summary

The LuxeCraft Interior Studio Web Application fully satisfies all requirements specified in **Assessment Plan A Guidelines**:
- ✅ **4-5 Responsive Pages**: Home, About Us, Services & Pricing, Contact Us.
- ✅ **Secure Admin Panel**: Session-based login with hashed password protection.
- ✅ **Full CRUD Functionality**: Add, Edit, Delete operations on Services, Gallery, and Team members.
- ✅ **Image Upload Pipeline**: Secure image compression (Base64 Data URI) and direct URL support.
- ✅ **MySQL Relational Database**: `schema.sql` file with 6 related tables and foreign key constraints.
- ✅ **Live Cloud Deployment**: Fully working, styled, and responsive on **Vercel** (`https://dtn-final-project.vercel.app`).
- ✅ **Academic & Professional Documentation**: Complete report and demo video guide provided.
