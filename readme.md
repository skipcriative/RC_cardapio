
# RC Cardapio Backend

A backend application for managing restaurant menus with Flask, SQLAlchemy, and MySQL. The application provides CRUD (Create, Read, Update, Delete) operations for `Product` and `Category` models, with organized endpoints in separate controllers.

## Features

- Full CRUD operations for `Product` and `Category`.
- Database initialization with sample data.
- Swagger API documentation.
- Modular structure with separate controllers for `Product` and `Category` endpoints.
- Environment variable configuration for sensitive data.

## Project Structure


```
project-root/
├── app_factory.py            # Factory function to create and configure the Flask app
├── rc_cardapio.py            # Main entry point to start the application
├── models.py                 # SQLAlchemy models for Product and Category
├── controllers/              # Folder to hold endpoint files for modularity
│   ├── product_controller.py # Controller for Product-related endpoints
│   └── category_controller.py # Controller for Category-related endpoints
├── initialize_db.py          # Script to initialize the database with sample data
├── .env                      # Environment variables for database credentials and configuration
├── requirements.txt          # List of project dependencies
└── migrations/               # Directory for database migration files (optional if using Flask-Migrate)

```

## Requirements

- Python 3.x
- MySQL
- `pip` (Python package manager)

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
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_NAME=your_db_name
   DB_PORT=3306
   DATABASE_URI=mysql+mysqlconnector://your_db_user:your_db_password@your_db_host:3306/your_db_name
   ```

5. **Initialize the Database**

   Run the `initialize_db.py` script to create tables and insert sample data:

   ```bash
   python initialize_db.py
   ```

## Running the Application

To start the Flask application, run:

```bash
python rc_cardapio.py
```

The application will be available at `http://localhost:5000`.

## API Documentation

Swagger documentation is available at `http://localhost:5000/apidocs`. It provides a UI to test all the endpoints and see the expected request and response formats.

## Endpoints

### Product Endpoints

- **Create Product**: `POST /products`
- **Get All Products**: `GET /products`
- **Get Product by ID**: `GET /products/<id>`
- **Update Product**: `PUT /products/<id>`
- **Delete Product**: `DELETE /products/<id>`

### Category Endpoints

- **Create Category**: `POST /categories`
- **Get All Categories**: `GET /categories`
- **Get Category by ID**: `GET /categories/<id>`
- **Update Category**: `PUT /categories/<id>`
- **Delete Category**: `DELETE /categories/<id>`

## Project Details

- **Modular Structure**: Routes are separated into `product_controller.py` and `category_controller.py` files inside the `controllers` directory.
- **Database Models**: Defined in `models.py` using SQLAlchemy.
- **App Factory**: `app_factory.py` contains a factory function to create the Flask app, configure it, and register blueprints.

## Troubleshooting

If you encounter database connection issues:
- Ensure that the database credentials in the `.env` file are correct.
- Make sure MySQL is running and accessible on the specified `DB_HOST` and `DB_PORT`.

## License

This project is licensed under the MIT License.

---

### Explanation

- **Overview**: Describes what the project is and its main features.
- **Installation**: Detailed steps on setting up the project, including environment setup.
- **API Documentation**: Instructions to access Swagger UI.
- **Endpoints**: Lists available endpoints with HTTP methods.
- **Troubleshooting**: Tips for common issues.
- **License**: Basic licensing information (customize if needed).

