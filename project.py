"""
=====================================================================
LuxeCraft Interior Studio - Full-Stack Local Business Web App
Assessment Plan A - Final Project Submission
Language: Python 3.9+ / Framework: Flask
Database Engine: MySQL (Primary) with SQLite (Automatic Fallback)
=====================================================================
"""

import os
import sqlite3
import time
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, 
    flash, session, jsonify, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Try importing pymysql for MySQL support
try:
    import pymysql
    import pymysql.cursors
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

# Base directory for absolute path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IS_SERVERLESS = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or '/var/task' in os.path.abspath(__file__))

# Initialize Flask App with explicit folder paths
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static'),
    static_url_path='/static'
)
app.secret_key = os.environ.get('SECRET_KEY', 'luxecraft_secret_key_2026_super_secure')

# Explicit static file route handler for serverless environments
@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static'), filename)

# Upload Config
UPLOAD_FOLDER = '/tmp/uploads' if IS_SERVERLESS else os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max limit

# Ensure upload directory exists safely
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception:
    pass

# MySQL Config (Override via environment variables if desired)
MYSQL_HOST = os.environ.get('DB_HOST', 'localhost')
MYSQL_USER = os.environ.get('DB_USER', 'root')
MYSQL_PASSWORD = os.environ.get('DB_PASSWORD', '')
MYSQL_DB = os.environ.get('DB_NAME', 'luxecraft_db')
MYSQL_PORT = int(os.environ.get('DB_PORT', 3306))

# Helper: Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper: Upload file helper
def save_uploaded_file(file_obj, default_path):
    if file_obj and file_obj.filename != '' and allowed_file(file_obj.filename):
        filename = secure_filename(file_obj.filename)
        timestamp = int(time.time())
        unique_filename = f"{timestamp}_{filename}"
        try:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file_obj.save(filepath)
            return f"/static/uploads/{unique_filename}"
        except Exception:
            return default_path
    return default_path

# Database Abstraction Wrapper
class Database:
    def __init__(self):
        self.use_sqlite = False
        self.sqlite_db = os.path.join(BASE_DIR, 'luxecraft.db')
        
        # Serverless / Vercel compatibility: fallback to writable /tmp directory if read-only
        if IS_SERVERLESS or not os.access(BASE_DIR, os.W_OK):
            tmp_db = '/tmp/luxecraft.db'
            if not os.path.exists(tmp_db) and os.path.exists(self.sqlite_db):
                try:
                    import shutil
                    shutil.copy2(self.sqlite_db, tmp_db)
                except Exception:
                    pass
            self.sqlite_db = tmp_db
            # If DB_HOST is not explicitly configured in serverless env, default to SQLite immediately
            if not os.environ.get('DB_HOST'):
                self.use_sqlite = True
            
        self._init_db()

    def get_connection(self):
        if not self.use_sqlite and MYSQL_AVAILABLE:
            try:
                conn = pymysql.connect(
                    host=MYSQL_HOST,
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    database=MYSQL_DB,
                    port=MYSQL_PORT,
                    autocommit=True,
                    connect_timeout=3,
                    cursorclass=pymysql.cursors.DictCursor
                )
                return conn, 'mysql'
            except Exception as e:
                # Fallback to SQLite if MySQL connection fails
                self.use_sqlite = True

        # SQLite Connection
        conn = sqlite3.connect(self.sqlite_db, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn, 'sqlite'

    def _init_db(self):
        """Ensure database tables & default seed data exist."""
        conn, engine = self.get_connection()
        if engine == 'sqlite':
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'admin',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    slug TEXT UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Services table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    title TEXT NOT NULL,
                    short_desc TEXT NOT NULL,
                    full_desc TEXT NOT NULL,
                    price REAL DEFAULT 0.0,
                    price_unit TEXT DEFAULT 'per project',
                    image_url TEXT DEFAULT '/static/uploads/service_default.jpg',
                    is_featured INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
                )
            ''')

            # Gallery table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gallery (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    title TEXT NOT NULL,
                    location TEXT DEFAULT 'Local Studio',
                    image_url TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
                )
            ''')

            # Team members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    bio TEXT,
                    email TEXT,
                    phone TEXT,
                    image_url TEXT DEFAULT '/static/uploads/team_default.jpg',
                    display_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Inquiries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inquiries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_id INTEGER,
                    client_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    subject TEXT DEFAULT 'General Inquiry',
                    message TEXT NOT NULL,
                    status TEXT DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE SET NULL
                )
            ''')
            conn.commit()

            # Seed default admin if missing
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                admin_pass = generate_password_hash('admin123')
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                    ('admin', 'admin@luxecraft.com', admin_pass, 'admin')
                )
                conn.commit()

            # Seed default categories if empty
            cursor.execute("SELECT COUNT(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                categories = [
                    (1, 'Residential Interior', 'residential-interior', 'Bespoke home, luxury apartment, and villa interior design.'),
                    (2, 'Commercial Design', 'commercial-design', 'High-end office spaces, retail boutiques, and corporate suites.'),
                    (3, 'Architectural Planning', 'architectural-planning', 'Structural blueprints, 3D modeling, and renovation execution.'),
                    (4, 'Custom Furniture', 'custom-furniture', 'Handcrafted bespoke furniture and tailored spatial decor.')
                ]
                cursor.executemany("INSERT INTO categories VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)", categories)
                conn.commit()

            # Seed default services if empty
            cursor.execute("SELECT COUNT(*) FROM services")
            if cursor.fetchone()[0] == 0:
                services = [
                    (1, 1, 'Luxury Villa Redesign', 'Complete interior transformation for high-end villas and luxury penthouses.', 'Our signature luxury villa design package includes 3D spatial mapping, custom material sourcing, lighting design, and end-to-end execution managed by certified architects.', 2500.0, 'per project', '/static/uploads/service1.jpg', 1),
                    (2, 2, 'Modern Corporate Office Workspace', 'Ergonomic, scalable workplace layouts designed to elevate productivity.', 'We design smart, collaboration-focused corporate environments equipped with acoustic paneling, glass partitions, and executive lounge suites.', 1800.0, 'per floor', '/static/uploads/service2.jpg', 1),
                    (3, 3, '3D Architectural Rendering & Blueprinting', 'Ultra-realistic 4K walkthroughs and structural schematics.', 'Transform raw concepts into photorealistic 3D virtual walkthroughs before physical construction begins. Includes structural assessment and compliance checks.', 950.0, 'per design concept', '/static/uploads/service3.jpg', 1),
                    (4, 4, 'Bespoke Custom Furniture Crafting', 'Custom handcrafted timber, marble, and velvet interior decor pieces.', 'Tailor-made furniture designed specifically for your space dimensions. Crafted using sustainable teak wood, brushed brass details, and luxury upholstery.', 1200.0, 'per package', '/static/uploads/service4.jpg', 0)
                ]
                cursor.executemany("INSERT INTO services VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", services)
                conn.commit()

            # Seed default gallery items if empty
            cursor.execute("SELECT COUNT(*) FROM gallery")
            if cursor.fetchone()[0] == 0:
                gallery = [
                    (1, 1, 'The Emerald Penthouse Suite', 'Downtown Skyline', '/static/uploads/gallery1.jpg', 'Modern minimalist living room featuring floor-to-ceiling glass windows and custom marble hearth.'),
                    (2, 2, 'Horizon Tech Innovation Hub', 'Tech City Block', '/static/uploads/gallery2.jpg', 'Open-concept co-working ecosystem featuring bio-centric green walls and custom acoustic pods.'),
                    (3, 1, 'Nordic Minimalist Villa', 'Suburban Estates', '/static/uploads/gallery3.jpg', 'Warm neutral color palettes, natural oak flooring, and custom ambient cove lighting.'),
                    (4, 3, 'Skyline Glass Pavilion Architecture', 'Coastal Heights', '/static/uploads/gallery4.jpg', 'Futuristic architectural extension integrating passive solar cooling and smart home automation.')
                ]
                cursor.executemany("INSERT INTO gallery VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", gallery)
                conn.commit()

            # Seed default team members if empty
            cursor.execute("SELECT COUNT(*) FROM team_members")
            if cursor.fetchone()[0] == 0:
                team = [
                    (1, 'Eleanor Vance', 'Principal Architectural Director', 'Over 12 years of experience leading international luxury interior and spatial planning projects.', 'eleanor@luxecraft.com', '+1 (555) 234-5678', '/static/uploads/team1.jpg', 1),
                    (2, 'Marcus Thorne', 'Senior Commercial Space Designer', 'Specializes in ergonomic corporate office design, sustainable acoustic materials, and spatial flow.', 'marcus@luxecraft.com', '+1 (555) 345-6789', '/static/uploads/team2.jpg', 2),
                    (3, 'Sophia Al-Mansoor', '3D Visualizer & Color Theorist', 'Award-winning CG artist delivering photorealistic 3D architectural renders and lighting concepts.', 'sophia@luxecraft.com', '+1 (555) 456-7890', '/static/uploads/team3.jpg', 3)
                ]
                cursor.executemany("INSERT INTO team_members VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", team)
                conn.commit()

            # Seed default inquiries if empty
            cursor.execute("SELECT COUNT(*) FROM inquiries")
            if cursor.fetchone()[0] == 0:
                inquiries = [
                    (1, 1, 'David Miller', 'david.m@example.com', '+1 (555) 987-6543', 'Villa Renovation Consultation', 'Hi, I would like to schedule an in-person site audit for a 4500 sq ft residential villa renovation next month.', 'In Review'),
                    (2, 2, 'Sarah Jenkins', 's.jenkins@innovatetech.io', '+1 (555) 876-5432', 'Office Floor Redesign Quote', 'Looking for an initial quote and 3D concept layout for our new headquarters office floor.', 'Pending')
                ]
                cursor.executemany("INSERT INTO inquiries VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", inquiries)
                conn.commit()

            conn.close()

    def query(self, sql, params=(), one=False):
        conn, engine = self.get_connection()
        try:
            if engine == 'mysql':
                with conn.cursor() as cursor:
                    # Adapt SQLite ? placeholders to MySQL %s
                    formatted_sql = sql.replace('?', '%s')
                    cursor.execute(formatted_sql, params)
                    result = cursor.fetchone() if one else cursor.fetchall()
                    conn.close()
                    return result
            else:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
                conn.close()
                if one:
                    return result[0] if result else None
                return result
        except Exception as e:
            if conn:
                conn.close()
            raise e

    def execute(self, sql, params=()):
        conn, engine = self.get_connection()
        try:
            if engine == 'mysql':
                with conn.cursor() as cursor:
                    formatted_sql = sql.replace('?', '%s')
                    cursor.execute(formatted_sql, params)
                    last_id = cursor.lastrowid
                    conn.close()
                    return last_id
            else:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit()
                last_id = cursor.lastrowid
                conn.close()
                return last_id
        except Exception as e:
            if conn:
                conn.close()
            raise e

# Instantiate Database Manager
db = Database()

# Authentication Decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access the Admin Panel.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# =====================================================================
# PUBLIC ROUTES
# =====================================================================

@app.route('/')
@app.route('/api/index')
@app.route('/api/index.py')
def home():
    """Home Page: Hero slider, stats counter, featured services, gallery preview, testimonials."""
    featured_services = db.query(
        "SELECT s.*, c.name as category_name FROM services s LEFT JOIN categories c ON s.category_id = c.id WHERE s.is_featured = 1 LIMIT 3"
    )
    gallery_items = db.query(
        "SELECT g.*, c.name as category_name FROM gallery g LEFT JOIN categories c ON g.category_id = c.id ORDER BY g.id DESC LIMIT 4"
    )
    stats = {
        'projects_completed': 140,
        'happy_clients': 125,
        'design_awards': 18,
        'years_experience': 10
    }
    return render_template('index.html', featured_services=featured_services, gallery_items=gallery_items, stats=stats)


@app.route('/about')
def about():
    """About Page: Business story, mission/vision, team showcase."""
    team_members = db.query("SELECT * FROM team_members ORDER BY display_order ASC")
    return render_template('about.html', team_members=team_members)


@app.route('/services')
def services():
    """Services & Products Page: Category filtering, detailed pricing cards."""
    category_id = request.args.get('category', type=int)
    categories = db.query("SELECT * FROM categories ORDER BY name ASC")
    
    if category_id:
        services_list = db.query(
            "SELECT s.*, c.name as category_name FROM services s LEFT JOIN categories c ON s.category_id = c.id WHERE s.category_id = ? ORDER BY s.id DESC",
            (category_id,)
        )
    else:
        services_list = db.query(
            "SELECT s.*, c.name as category_name FROM services s LEFT JOIN categories c ON s.category_id = c.id ORDER BY s.id DESC"
        )
        
    return render_template('services.html', services=services_list, categories=categories, selected_category=category_id)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact Page: Contact form submission with DB persistence."""
    services_list = db.query("SELECT id, title FROM services ORDER BY title ASC")
    
    if request.method == 'POST':
        client_name = request.form.get('client_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        service_id = request.form.get('service_id', type=int)
        subject = request.form.get('subject', 'General Inquiry').strip()
        message = request.form.get('message', '').strip()

        if not client_name or not email or not message:
            flash('Please complete all required fields.', 'danger')
            return redirect(url_for('contact'))

        db.execute(
            '''INSERT INTO inquiries (service_id, client_name, email, phone, subject, message, status)
               VALUES (?, ?, ?, ?, ?, ?, 'Pending')''',
            (service_id if service_id else None, client_name, email, phone, subject, message)
        )
        flash('Thank you! Your inquiry has been submitted successfully. Our design team will contact you within 24 hours.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', services=services_list)


# =====================================================================
# ADMIN PANEL & AUTHENTICATION ROUTES
# =====================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin Login Page."""
    if 'user_id' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = db.query("SELECT * FROM users WHERE username = ?", (username,), one=True)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Welcome back, {user['username']}! Logged in successfully.", 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    """Logout action."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin Dashboard overview with analytics counters."""
    services_count = db.query("SELECT COUNT(*) as cnt FROM services", one=True)['cnt']
    gallery_count = db.query("SELECT COUNT(*) as cnt FROM gallery", one=True)['cnt']
    team_count = db.query("SELECT COUNT(*) as cnt FROM team_members", one=True)['cnt']
    inquiries_count = db.query("SELECT COUNT(*) as cnt FROM inquiries", one=True)['cnt']
    pending_inquiries = db.query("SELECT COUNT(*) as cnt FROM inquiries WHERE status = 'Pending'", one=True)['cnt']

    recent_inquiries = db.query(
        "SELECT i.*, s.title as service_title FROM inquiries i LEFT JOIN services s ON i.service_id = s.id ORDER BY i.id DESC LIMIT 5"
    )

    return render_template(
        'admin/dashboard.html',
        services_count=services_count,
        gallery_count=gallery_count,
        team_count=team_count,
        inquiries_count=inquiries_count,
        pending_inquiries=pending_inquiries,
        recent_inquiries=recent_inquiries
    )


# --- ADMIN CRUD: SERVICES ---

@app.route('/admin/services')
@admin_required
def admin_services():
    """Manage Services List."""
    services_list = db.query(
        "SELECT s.*, c.name as category_name FROM services s LEFT JOIN categories c ON s.category_id = c.id ORDER BY s.id DESC"
    )
    categories = db.query("SELECT * FROM categories ORDER BY name ASC")
    return render_template('admin/services.html', services=services_list, categories=categories)


@app.route('/admin/services/add', methods=['POST'])
@admin_required
def admin_service_add():
    """Create new Service with Image Upload."""
    title = request.form.get('title', '').strip()
    category_id = request.form.get('category_id', type=int)
    short_desc = request.form.get('short_desc', '').strip()
    full_desc = request.form.get('full_desc', '').strip()
    price = request.form.get('price', type=float, default=0.0)
    price_unit = request.form.get('price_unit', 'per project').strip()
    is_featured = 1 if request.form.get('is_featured') else 0

    # Image upload handling
    image_file = request.files.get('image')
    image_url = save_uploaded_file(image_file, '/static/uploads/service_default.jpg')

    db.execute(
        '''INSERT INTO services (category_id, title, short_desc, full_desc, price, price_unit, image_url, is_featured)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (category_id, title, short_desc, full_desc, price, price_unit, image_url, is_featured)
    )
    flash('New service added successfully!', 'success')
    return redirect(url_for('admin_services'))


@app.route('/admin/services/edit/<int:service_id>', methods=['POST'])
@admin_required
def admin_service_edit(service_id):
    """Update existing Service with optional Image Upload."""
    service = db.query("SELECT * FROM services WHERE id = ?", (service_id,), one=True)
    if not service:
        flash('Service not found.', 'danger')
        return redirect(url_for('admin_services'))

    title = request.form.get('title', '').strip()
    category_id = request.form.get('category_id', type=int)
    short_desc = request.form.get('short_desc', '').strip()
    full_desc = request.form.get('full_desc', '').strip()
    price = request.form.get('price', type=float, default=0.0)
    price_unit = request.form.get('price_unit', 'per project').strip()
    is_featured = 1 if request.form.get('is_featured') else 0

    # Retain existing image if no new file provided
    image_file = request.files.get('image')
    image_url = save_uploaded_file(image_file, service['image_url'])

    db.execute(
        '''UPDATE services 
           SET category_id = ?, title = ?, short_desc = ?, full_desc = ?, price = ?, price_unit = ?, image_url = ?, is_featured = ?
           WHERE id = ?''',
        (category_id, title, short_desc, full_desc, price, price_unit, image_url, is_featured, service_id)
    )
    flash('Service updated successfully!', 'success')
    return redirect(url_for('admin_services'))


@app.route('/admin/services/delete/<int:service_id>', methods=['POST'])
@admin_required
def admin_service_delete(service_id):
    """Delete Service."""
    db.execute("DELETE FROM services WHERE id = ?", (service_id,))
    flash('Service deleted successfully.', 'success')
    return redirect(url_for('admin_services'))


# --- ADMIN CRUD: GALLERY / PORTFOLIO ---

@app.route('/admin/gallery')
@admin_required
def admin_gallery():
    """Manage Gallery Items."""
    gallery_items = db.query(
        "SELECT g.*, c.name as category_name FROM gallery g LEFT JOIN categories c ON g.category_id = c.id ORDER BY g.id DESC"
    )
    categories = db.query("SELECT * FROM categories ORDER BY name ASC")
    return render_template('admin/gallery.html', gallery=gallery_items, categories=categories)


@app.route('/admin/gallery/add', methods=['POST'])
@admin_required
def admin_gallery_add():
    """Add Portfolio Item with mandatory Image Upload."""
    title = request.form.get('title', '').strip()
    category_id = request.form.get('category_id', type=int)
    location = request.form.get('location', 'Local Studio').strip()
    description = request.form.get('description', '').strip()

    image_file = request.files.get('image')
    image_url = save_uploaded_file(image_file, '/static/uploads/gallery_default.jpg')

    db.execute(
        '''INSERT INTO gallery (category_id, title, location, image_url, description)
           VALUES (?, ?, ?, ?, ?)''',
        (category_id, title, location, image_url, description)
    )
    flash('Gallery project added successfully!', 'success')
    return redirect(url_for('admin_gallery'))


@app.route('/admin/gallery/delete/<int:item_id>', methods=['POST'])
@admin_required
def admin_gallery_delete(item_id):
    """Delete Portfolio Item."""
    db.execute("DELETE FROM gallery WHERE id = ?", (item_id,))
    flash('Gallery item removed.', 'success')
    return redirect(url_for('admin_gallery'))


# --- ADMIN CRUD: TEAM MEMBERS ---

@app.route('/admin/team')
@admin_required
def admin_team():
    """Manage Studio Team Members."""
    team_members = db.query("SELECT * FROM team_members ORDER BY display_order ASC")
    return render_template('admin/team.html', team=team_members)


@app.route('/admin/team/add', methods=['POST'])
@admin_required
def admin_team_add():
    """Add Team Member with Profile Image Upload."""
    name = request.form.get('name', '').strip()
    role = request.form.get('role', '').strip()
    bio = request.form.get('bio', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    display_order = request.form.get('display_order', type=int, default=0)

    image_file = request.files.get('image')
    image_url = save_uploaded_file(image_file, '/static/uploads/team_default.jpg')

    db.execute(
        '''INSERT INTO team_members (name, role, bio, email, phone, image_url, display_order)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (name, role, bio, email, phone, image_url, display_order)
    )
    flash('Team member added successfully!', 'success')
    return redirect(url_for('admin_team'))


@app.route('/admin/team/edit/<int:member_id>', methods=['POST'])
@admin_required
def admin_team_edit(member_id):
    """Edit Team Member."""
    member = db.query("SELECT * FROM team_members WHERE id = ?", (member_id,), one=True)
    if not member:
        flash('Member not found.', 'danger')
        return redirect(url_for('admin_team'))

    name = request.form.get('name', '').strip()
    role = request.form.get('role', '').strip()
    bio = request.form.get('bio', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    display_order = request.form.get('display_order', type=int, default=0)

    image_file = request.files.get('image')
    image_url = save_uploaded_file(image_file, member['image_url'])

    db.execute(
        '''UPDATE team_members 
           SET name = ?, role = ?, bio = ?, email = ?, phone = ?, image_url = ?, display_order = ?
           WHERE id = ?''',
        (name, role, bio, email, phone, image_url, display_order, member_id)
    )
    flash('Team member profile updated!', 'success')
    return redirect(url_for('admin_team'))


@app.route('/admin/team/delete/<int:member_id>', methods=['POST'])
@admin_required
def admin_team_delete(member_id):
    """Delete Team Member."""
    db.execute("DELETE FROM team_members WHERE id = ?", (member_id,))
    flash('Team member deleted.', 'success')
    return redirect(url_for('admin_team'))


# --- ADMIN INQUIRIES MANAGEMENT ---

@app.route('/admin/inquiries')
@admin_required
def admin_inquiries():
    """View and manage client inquiries."""
    inquiries_list = db.query(
        "SELECT i.*, s.title as service_title FROM inquiries i LEFT JOIN services s ON i.service_id = s.id ORDER BY i.id DESC"
    )
    return render_template('admin/inquiries.html', inquiries=inquiries_list)


@app.route('/admin/inquiries/status/<int:inquiry_id>', methods=['POST'])
@admin_required
def admin_inquiry_status(inquiry_id):
    """Update Inquiry Status."""
    new_status = request.form.get('status', 'Pending')
    db.execute("UPDATE inquiries SET status = ? WHERE id = ?", (new_status, inquiry_id))
    flash('Inquiry status updated.', 'success')
    return redirect(url_for('admin_inquiries'))


@app.route('/admin/inquiries/delete/<int:inquiry_id>', methods=['POST'])
@admin_required
def admin_inquiry_delete(inquiry_id):
    """Delete Inquiry record."""
    db.execute("DELETE FROM inquiries WHERE id = ?", (inquiry_id,))
    flash('Inquiry record deleted.', 'success')
    return redirect(url_for('admin_inquiries'))


# Helper Route: Generate high quality placeholders if static uploads don't exist yet
@app.before_request
def create_sample_images_if_missing():
    # Only execute once if sample images are missing
    if not hasattr(app, '_sample_images_created'):
        try:
            sample_files = [
                'service_default.jpg', 'team_default.jpg', 'gallery_default.jpg',
                'service1.jpg', 'service2.jpg', 'service3.jpg', 'service4.jpg',
                'gallery1.jpg', 'gallery2.jpg', 'gallery3.jpg', 'gallery4.jpg',
                'team1.jpg', 'team2.jpg', 'team3.jpg'
            ]
            
            for img_name in sample_files:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
                if not os.path.exists(file_path):
                    try:
                        from PIL import Image, ImageDraw
                        img = Image.new('RGB', (600, 400), color=(30, 41, 59))
                        draw = ImageDraw.Draw(img)
                        draw.rectangle([10, 10, 590, 390], outline=(99, 102, 241), width=4)
                        draw.text((200, 190), f"LuxeCraft: {img_name}", fill=(248, 250, 252))
                        img.save(file_path, 'JPEG')
                    except Exception:
                        with open(file_path, 'wb') as f:
                            f.write(b'\xFF\xD8\xFF\xE0\x00\x10JFIF')
        except Exception:
            pass
        app._sample_images_created = True


if __name__ == '__main__':
    print("=========================================================")
    print("[*] LuxeCraft Web Application Server Starting...")
    print("[-] Localhost URL: http://127.0.0.1:5000/")
    print("[-] Admin Credentials: username='admin' | password='admin123'")
    print("=========================================================")
    app.run(debug=True, host='127.0.0.1', port=5000)
