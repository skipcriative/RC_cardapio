Here’s the updated `README.md` to include the AWS S3 integration and other recent changes:

---

# RC Cardapio Backend

A backend application for managing restaurant menus with Flask, SQLAlchemy, MySQL, and AWS S3. The application provides CRUD (Create, Read, Update, Delete) operations for `Product`, `Category`, and `Order` models, with organized endpoints in separate controllers. Products can include images stored in an AWS S3 bucket.

---

## Features

- Full CRUD operations for `Product`, `Category`, and `Order`.
- Database initialization with sample data.
- Swagger API documentation for easy testing.
- Modular structure with separate controllers for endpoints.
- Environment variable configuration for sensitive data.
- AWS S3 integration for managing product images.

---

## Project Structure

```
project-root/
├── app_factory.py              # Factory function to create and configure the Flask app
├── rc_cardapio.py              # Main entry point to start the application
├── models.py                   # SQLAlchemy models for Product, Category, and Order
├── controllers/                # Folder to hold endpoint files for modularity
│   ├── product_controller.py   # Controller for Product-related endpoints
│   ├── category_controller.py  # Controller for Category-related endpoints
│   ├── order_controller.py     # Controller for Order-related endpoints
├── initialize_db.py            # Script to initialize the database with sample data
├── s3_handler.py               # AWS S3 utility class for handling file uploads
├── .env                        # Environment variables for database and AWS credentials
├── requirements.txt            # List of project dependencies
└── migrations/                 # Directory for database migration files (if using Flask-Migrate)
```

---

## Requirements

- Python 3.x
- MySQL
- AWS S3 bucket
- `pip` (Python package manager)

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/rc-cardapio-backend.git
   cd rc-cardapio-backend
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate     # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory with the following variables:

   ```plaintext
   # Database Configuration
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_NAME=your_db_name
   DB_PORT=3306
   DATABASE_URI=mysql+mysqlconnector://your_db_user:your_db_password@your_db_host:3306/your_db_name

   # AWS S3 Configuration
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_BUCKET_NAME=your_bucket_name
   AWS_REGION=your_bucket_region
   ```

5. **Initialize the Database**

   Run the `initialize_db.py` script to create tables and insert sample data:

   ```bash
   python initialize_db.py
   ```

6. **Run Database Migrations (Optional)**

   If using Flask-Migrate, initialize and apply migrations:

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

---

## Running the Application

To start the Flask application, run:

```bash
python rc_cardapio.py
```

The application will be available at `http://localhost:5000`.

---

## API Documentation

Swagger documentation is available at `http://localhost:5000/apidocs`. It provides a UI to test all the endpoints and see the expected request and response formats.

---

## Endpoints

### Product Endpoints

- **Create Product**: `POST /products`
  - Accepts optional image file uploads, stores the image in AWS S3, and saves the public URL.
- **Get All Products**: `GET /products`
  - Includes the public image URL in the response.
- **Get Product by ID**: `GET /products/<id>`
  - Includes the public image URL in the response.
- **Update Product**: `PUT /products/<id>`
  - Allows updating the product image.
- **Delete Product**: `DELETE /products/<id>`

### Category Endpoints

- **Create Category**: `POST /categories`
- **Get All Categories**: `GET /categories`
- **Get Category by ID**: `GET /categories/<id>`
- **Update Category**: `PUT /categories/<id>`
- **Delete Category**: `DELETE /categories/<id>`

### Order Endpoints

- **Create Order**: `POST /orders`
- **Get All Orders**: `GET /orders`
- **Get Order by ID**: `GET /orders/<id>`
- **Update Order**: `PUT /orders/<id>`
- **Delete Order**: `DELETE /orders/<id>`

---

## AWS S3 Integration

- **S3Handler**: Handles file uploads to AWS S3.
- **File Storage**:
  - Uploaded product images are stored in the `products/` folder in the S3 bucket.
  - The public S3 URL is saved in the `image_link` field of the `Product` model.

---

## Troubleshooting

- **Database Issues**:
  - Ensure that the database credentials in the `.env` file are correct.
  - Verify that MySQL is running and accessible.

- **AWS S3 Issues**:
  - Ensure that the AWS credentials in the `.env` file are valid.
  - Check the bucket permissions (public read access must be enabled).

- **Dependencies**:
  - Run `pip install -r requirements.txt` to ensure all dependencies are installed.

---

## License

This project is licensed under the MIT License.

---

### Summary of Updates

- Added **AWS S3 Integration** details.
- Updated **Project Structure** with `s3_handler.py`.
- Expanded **Endpoints** section with image upload details for products.
- Added **Troubleshooting** for AWS S3.

Let me know if you'd like further refinements!