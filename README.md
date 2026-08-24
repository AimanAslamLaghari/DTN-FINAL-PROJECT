# LuxeCraft Interior Studio - Full-Stack Web Application & Admin Panel
> **Assessment Plan A - Final Project Deliverable Package**

A modern, responsive full-stack website and secure Admin Management Panel built for **LuxeCraft Interior Studio** (a real local business model) using Python (Flask), MySQL, HTML5, CSS3, and JavaScript.

---

## 📢 Assessment Plan A Deliverables Checklist

- [x] **Responsive 4-5 Page Website**: Home, About Us, Services & Pricing, Contact Us.
- [x] **Secure Admin Panel**: Session-based login with hashed password protection.
- [x] **Full CRUD Functionality**: Add, Edit, and Delete Services, Gallery Items, Team Members, and Inquiries.
- [x] **Image Upload Pipeline**: Image validation and storage in `static/uploads/`.
- [x] **MySQL Database (.sql export)**: `schema.sql` file containing 6 related tables with seed data.
- [x] **Automatic SQLite Fallback**: Zero-config instant local execution if MySQL server is offline.
- [x] **Academic Report**: Complete 3-page report (`PROJECT_REPORT.md`).
- [x] **Demonstration Video Guide**: Script & outline included below.

---

## 🔑 Quick Admin Login Credentials

| Role | Username | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | `http://127.0.0.1:5000/admin/login` |

---

## ⚙️ Quick Start Guide (Localhost Execution)

### Step 1: Clone or Open Project Directory
Navigate to the project root in terminal / command prompt:
```bash
cd "c:\Users\Aiman Aslam\Desktop\ML Project\DtnFinalProject"
```

### Step 2: Install Python Dependencies
Install required packages using pip:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Web Server
Execute the main application file:
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
4. Choose the `schema.sql` file located inside the `DtnFinalProject` folder.
5. Click **Go** / **Import** to execute script and seed tables.

### Option B: Using MySQL Command Line
```sql
mysql -u root -p < schema.sql
```

> **Note on Automatic SQLite Fallback:**  
> If MySQL is not running on your machine when running `python project.py`, the system will automatically initialize a local SQLite database (`luxecraft.db`) with identical schema and pre-populated seed data so you can test the application instantly without errors!

---

## 🎥 3-5 Minute Project Demonstration Video Script

When recording your 3-5 minute video, follow this structured breakdown:

1. **0:00 - 0:45 | Introduction & Business Problem**:
   - Introduce yourself and the project: LuxeCraft Interior Studio.
   - Mention the business goal: digitalizing spatial portfolios, client inquiries, and admin management.
2. **0:45 - 2:00 | Public Responsive Pages Demo**:
   - Show Home page (Hero, Stats, Featured Services, Testimonials).
   - Navigate to About Us, Services & Pricing (demonstrate category filtering).
   - Demonstrate submitting a contact inquiry on the Contact Us page.
3. **2:00 - 3:45 | Admin Panel & CRUD / Image Upload Demo**:
   - Log into Admin Panel using `admin` / `admin123`.
   - Show Dashboard analytics counters.
   - Perform CRUD: Add a new service with image upload, edit its price, and verify deletion.
   - Show the newly submitted inquiry under Client Inquiries and update status to "In Review".
4. **3:45 - 4:30 | Database Schema & Code Structure**:
   - Briefly show `schema.sql` (6 related tables) and `PROJECT_REPORT.md`.
   - Conclude video.

---

## 🚀 GitHub Upload Instructions

1. Initialize git in directory:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Final Project Assessment Plan A"
   ```
2. Link to your GitHub Repository:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/LuxeCraft-Final-Project.git
   git branch -M main
   git push -u origin main
   ```

---

## 📁 File Structure

```text
DtnFinalProject/
├── project.py              # Main Flask application & DB layer
├── schema.sql              # MySQL database export schema & seed data
├── requirements.txt        # Dependencies list
├── PROJECT_REPORT.md       # 3-Page Academic & Professional Report
├── README.md               # Quickstart & submission guide
├── static/
│   ├── css/
│   │   └── style.css       # Master responsive CSS
│   ├── js/
│   │   └── main.js        # Client-side JavaScript
│   └── uploads/            # Dynamic image upload storage
└── templates/
    ├── base.html           # Master layout template
    ├── index.html          # Home page
    ├── about.html          # About page
    ├── services.html       # Services page
    ├── contact.html        # Contact page
    └── admin/
        ├── login.html      # Admin login
        ├── dashboard.html  # Admin dashboard
        ├── services.html   # Services CRUD & Image Upload
        ├── gallery.html    # Gallery CRUD & Image Upload
        ├── team.html       # Team CRUD & Image Upload
        └── inquiries.html  # Inquiries status management
```
