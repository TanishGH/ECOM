ECOM_V2 is a Django-based eCommerce vendor platform that allows vendors to register, manage products and categories, and perform full CRUD operations from their personalized dashboard. Admins can analyse vendors, manage listings, and view reports from the admin dashboard.

http://127.0.0.1:8000/users/verify-email/test_verification_xyz_str/
Note: This is dynamic and secure in case you initialise the smtp detail.

For email verification after registiring a vendor we can use static url to replicate the email varification link on mail for email varification.

🚀 Features
Vendor, Admin Signup & Login

Role-based Dashboard (Admin & Vendor)

Vendor Product & Category Management (CRUD)

Image Uploads for Products

Tag Support for Products

Admin Panel with:

Vendor Overview with Listings and filters

Product & Category Overview with Listings and filters

Dashboard with recent activity

Django Templating for all UI

Class-based Views

Django admin by role based login on Django templating 

Secure Authentication use (http://127.0.0.1:8000/users/verify-email/test_verification_xyz_str/) for email varification 
although you can get the link in case you initialise the smtp creadientials.


🛠️ Tech Stack
Backend: Django (Class-based views, ORM)

Frontend: Django Templates + Bootstrap

Database: SQLite / PostgreSQL (your choice)

Media Storage: Local (or can be configured for S3)

Authentication: Django's built-in auth system


⚙️ Setup Instructions

1. Clone the Repository

git clone https://github.com/TanishGH/ECOM.git
cd econ_v2


2. Create & Activate Virtual Environment

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


3. Install Requirements

pip install -r requirements.txt


4. Apply Migrations

python manage.py migrate


5. Run Development Server

python manage.py runserver


🙋‍♂️ Author
Tanish Bankey
