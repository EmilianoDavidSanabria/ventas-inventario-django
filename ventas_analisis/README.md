# Project Title: Sales and Inventory Management System
**Video Demo:** https://youtu.be/kgVbnv2BlkA?si=rEwSNO0xlybiyTWX

## Description:
This project is a Sales and Inventory Management System built using Django (a Python web framework) and HTML for the frontend. The system is designed to help businesses manage their products, track sales, generate reports, and visualize data through interactive charts. It includes user authentication, data filtering, pagination, caching, and export functionality.
 
---

## Key Features:

### 1. Product Management:
- Add new products with details such as name, price, and description.
- View a list of all products in the inventory.

### 2. Sales Management:
- Record sales transactions, including the product sold, quantity, and total price.
- Automatically calculate the total price based on the product's price and quantity sold.
- View a paginated list of all sales transactions.

### 3. Data Visualization:
- Generate static charts using Matplotlib to visualize total sales over time.
- Create interactive charts using Plotly to display sales trends and product performance.
- Display monthly and quarterly sales statistics using Django's aggregation functions.

### 4. Advanced Statistics:
- Analyze sales data by grouping transactions by month or quarter.
- Identify the top-selling products based on the quantity sold.

### 5. Data Filtering:
- Filter sales data by product, date range, price range, and transaction status.
- View the total sales amount for filtered results.

### 6. User Authentication:
- Users can register, log in, and log out securely.
- Certain features (e.g., adding products or sales) are restricted to authenticated users.

### 7. Caching:
- Implemented caching to improve performance for frequently accessed data, such as the list of sales.

### 8. Export Data:
- Export sales data to an Excel file using the openpyxl library for further analysis.

### 9. Pagination:
- The list of sales transactions is paginated to improve usability and performance.

---

## Technologies Used:
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS
- **Data Visualization:** Matplotlib, Plotly
- **Data Manipulation:** Pandas
- **Authentication:** Django's built-in authentication system
- **Caching:** Django's caching framework
- **Excel Export:** openpyxl
- **Database:** SQLite (default Django database)

---

## How It Works:

### 1. Adding Products:
- Authenticated users can add products using a form. The product details are saved to the database.

### 2. Recording Sales:
- Users can record sales transactions by selecting a product, entering the quantity, and specifying the date. The total price is calculated automatically.

### 3. Viewing Data:
- Users can view lists of products and sales transactions. The sales list is paginated for better usability.

### 4. Generating Reports:
- Users can generate static and interactive charts to visualize sales trends.
- Advanced statistics provide insights into monthly and quarterly sales performance.

### 5. Filtering Data:
- Users can filter sales data based on various criteria, such as product, date range, and price range.

### 6. Exporting Data:
- Sales data can be exported to an Excel file for offline analysis.

### 7. User Authentication:
- Users must log in to access certain features. New users can register for an account.
