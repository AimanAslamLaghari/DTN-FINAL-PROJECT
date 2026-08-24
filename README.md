# LuxeCraft Interior Studio - Full-Stack Web Application & Admin Panel
> **Assessment Plan A - Final Project Deliverable Package**

A modern, responsive full-stack website and secure Admin Management Panel built for **LuxeCraft Interior Studio** (a real local business model) using Python (Flask), MySQL / SQLite, HTML5, CSS3 (Glassmorphism), and JavaScript.

---

## 🌐 Live Cloud Deployment

* **Live Website URL:** [https://dtn-final-project.vercel.app](https://dtn-final-project.vercel.app)
* **Admin Login Portal:** [https://dtn-final-project.vercel.app/admin/login](https://dtn-final-project.vercel.app/admin/login)
* **GitHub Repository:** [https://github.com/AimanAslamLaghari/DTN-FINAL-PROJECT](https://github.com/AimanAslamLaghari/DTN-FINAL-PROJECT)

---

## 📢 Assessment Plan A Deliverables Checklist

- [x] **Responsive 4-5 Page Website**: Home, About Us, Services & Pricing, Contact Us.
- [x] **Secure Admin Panel**: Session-based login with hashed password protection (`Werkzeug.security`).
- [x] **Full CRUD Functionality**: Add, Edit, and Delete Services, Gallery Items, Team Members, and Inquiries.
- [x] **Image Upload & Media Pipeline**: Dual-mode upload system supporting file uploads (auto-compressed into Base64 Data URIs) and direct CDN/Web links.
- [x] **MySQL Database (.sql export)**: `schema.sql` file containing 6 related tables with relational foreign keys and seed data.
- [x] **Automatic SQLite Fallback**: Zero-config instant local execution if MySQL server is offline.
- [x] **Serverless Cloud Compatibility**: Production-ready deployment configuration on Vercel via WSGI middleware (`api/index.py` & `vercel.json`).
- [x] **Interactive Scope & Budget Estimator**: Live JavaScript-powered spatial calculator with custom gradient range slider.
- [x] **Academic Report**: Complete 3-page report (`PROJECT_REPORT.md`).
- [x] **Demonstration Video Guide**: Script & outline included below.

---

## 🔑 Admin Login Credentials

| Role | Username | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | `/admin/login` |

---

## ⚙️ Quick Start Guide (Localhost Execution)

### Step 1: Clone or Open Project Directory
```bash
git clone https://github.com/AimanAslamLaghari/DTN-FINAL-PROJECT.git
cd DTN-FINAL-PROJECT
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Web Server
```bash
python project.py
```
Output:
```text
=========================================================
⚡ LuxeCraft Web Application Server Starting...
📍 Localhost URL: http://127.0.0.1:5000/
🔑 Admin Credentials: username='admin' | password='admin123'
=========================================================
```
Open your browser and navigate to: **`http://127.0.0.1:5000/`**

---

## 🗄️ MySQL Database Setup & Import (.sql)

### Option A: Using phpMyAdmin / XAMPP / WAMP
1. Open phpMyAdmin (`http://localhost/phpmyadmin/`).
2. Create a new database named `luxecraft_db`.
3. Click the **Import** tab.
4. Choose the `schema.sql` file located inside the project folder.
5. Click **Go** / **Import** to execute the script and seed tables.

### Option B: Using MySQL Command Line
```sql
mysql -u root -p < schema.sql
```

> **Note on Automatic SQLite Fallback:**  
> If MySQL is not running on your machine when starting `python project.py`, the system automatically creates and seeds a local SQLite database (`luxecraft.db`) with identical schema and pre-populated seed data, ensuring **100% instant zero-configuration demo execution**.

---

## 🎥 3-5 Minute Project Demonstration Video Script

When recording your 3-5 minute video, follow this structured breakdown:

1. **0:00 - 0:45 | Introduction & Business Overview**:
   - Introduce yourself and the project: LuxeCraft Interior Studio.
   - Highlight the business goal: digitalizing spatial portfolios, client inquiries, budget estimation, and admin management.
2. **0:45 - 2:00 | Public Responsive Pages Demo**:
   - Show the **Home** page (Hero showcase, stats counter, featured services, gallery preview, customer testimonials).
   - Navigate to **About Us** (heritage story, 4-step methodology, team visionaries).
   - Navigate to **Services & Pricing** (category filtering, test the **Instant Spatial Project Estimator** slider).
   - Demonstrate submitting a consultation inquiry on the **Contact Us** page.
3. **2:00 - 3:45 | Admin Panel & Full CRUD / Media Upload Demo**:
   - Log into Admin Panel using `admin` / `admin123`.
   - Show Dashboard metric counters and recent inquiries.
   - Perform CRUD: Add a new service or gallery project with an image upload / link, edit pricing, and test deletion.
   - Show the newly submitted inquiry under Client Inquiries and update its status to "In Review".
4. **3:45 - 4:30 | Database Schema & Cloud Architecture**:
   - Briefly show `schema.sql` (6 related tables) and explain the dual MySQL / SQLite architecture.
   - Highlight the live Vercel cloud deployment (`https://dtn-final-project.vercel.app`).
   - Conclude video.

---

## 📁 File Structure

```text
DTN-FINAL-PROJECT/
├── project.py              # Main Flask application, DB layer & image pipeline
├── schema.sql              # MySQL database export schema & seed data
├── requirements.txt        # Python dependencies list
├── vercel.json             # Vercel serverless deployment routing config
├── luxecraft.db            # Pre-seeded SQLite fallback database
├── PROJECT_REPORT.md       # 3-Page Academic & Professional Report
├── README.md               # Quickstart & submission guide
├── api/
│   └── index.py            # Vercel WSGI serverless entry point & middleware
├── public/                 # Edge CDN static assets
├── static/
│   ├── css/
│   │   └── style.css       # Master responsive glassmorphic stylesheet
│   ├── js/
│   │   └── main.js        # Interactive JS (mobile drawer, estimator widget)
│   └── uploads/            # High-resolution architectural photography
└── templates/
    ├── base.html           # Master layout template with inline style fallback
    ├── index.html          # Home page
    ├── about.html          # About page
    ├── services.html       # Services page & budget estimator
    ├── contact.html        # Contact & inquiry page
    ├── includes/
    │   ├── styles.html     # Pre-compiled CSS component
    │   └── scripts.html    # Pre-compiled JavaScript component
    └── admin/
        ├── login.html      # Admin login
        ├── dashboard.html  # Admin metrics dashboard
        ├── services.html   # Services CRUD & Image Upload
        ├── gallery.html    # Gallery CRUD & Image Upload
        ├── team.html       # Team CRUD & Image Upload
        └── inquiries.html  # Inquiries status management
```
