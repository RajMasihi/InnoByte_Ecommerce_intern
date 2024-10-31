# InnoByte_Ecommerce_intern
This project is a Django-based e-commerce web application built using Django Rest Framework (DRF) for the backend and MySQL as the database. It provides a simple yet scalable solution for managing e-commerce activities such as user authentication, product management, cart functionality, and order processing.

Features
User registration and authentication using Django Rest Framework (DRF) and JWT.
Product management with stock tracking.
Shopping cart functionality.
Order management with various order statuses (processing, shipped, complete, canceled).
Role-based permissions for users and admin.

Prerequisites
Python 3.8+: Make sure Python is installed on your system.
Django: A high-level Python web framework.
Django Rest Framework: An API toolkit for Django.
MySQL: The database management system.
Git: For version control.

Installation Guide
Step 1: Clone the Repository

git clone https://github.com/yourusername/InnoByte_Ecommerce.git
cd InnoByte_Ecommerce

Step 2: Set Up a Virtual Environment
python -m venv myvenv

Windows:
myvenv\Scripts\activate

Step 3: Install Project Dependencies
pip install -r requirements.txt

Step 4: Configure Environment Variables
DB_NAME=innobyte_ecom_db
DB_USER=root
DB_PASSWORD=''  
DB_HOST=localhost
DB_PORT=3306

Step 5: Set Up MySQL Database
Create a MySQL database with the same name as provided in the .env file (innobyte_ecom_db).
Make sure you have the appropriate user credentials and permissions for the database.

Step 6: Apply Database Migrations
python manage.py makemigrations
python manage.py migrate

Step 7: Create a Superuser
python manage.py createsuperuser

Step 8: Start the Development Server
python manage.py runserver

step 9: after successfull execution 
enter url in your Browser: http://127.0.0.1:8000/swagger/              #this url show the all documentation of Innobyte_ecommerce project with urls  

