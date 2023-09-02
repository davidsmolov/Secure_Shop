# Secure Shop API

Secure Shop API is a secure and feature-rich API for a basic online shop. It prioritizes security aspects in API development and provides a reference implementation for anyone looking to build a secure e-commerce API. The API allows users to view products, add products to their carts, and make payments using the free tier PayPal API.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [User Schemes](#user-schemes)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Api Challenge](#Api-Challenge)
- [License](#license)

## Introduction

Online shopping APIs are plentiful, but many lack a strong emphasis on security. Secure Shop API is designed to fill this gap by providing a secure and well-structured API for online shops. It not only protects the integrity of the code but also enforces business logic to ensure a safe and reliable shopping experience.

## Features

- Unauthenticated users can view products.
- Authenticated users can view products and create their own carts.
- Seller users have the ability to edit products and create their own carts.
- Supervisor users can edit user permissions and create their own carts.
- Superusers have full access and control over all aspects of the application.
- Carts are impervious to meddling by other users in the app.
- The price to pay can not be manipulated.
- A user cant add to his cart more of a product than exists is stock.
- items are only removed from stock once the purchase is complete.

## User Schemes

- **Unauthenticated User**: Can only view products.
- **Authenticated User**: Can view products and create their own cart.
- **Seller User**: Can edit products and create their own cart.
- **Supervisor User**: Can edit user permissions and create their own cart.
- **Superuser**: Has complete access to all features and functionalities of the app.

## Getting Started

### Prerequisites

Before setting up Secure Shop API, ensure you have the following prerequisites:

1. **Email Configuration**:
   - You will need an `email_host_user` and `email_host_password` to enable the email service of the app. For more information, refer to [Gmail SMTP Settings](https://www.saleshandy.com/smtp/gmail-smtp-settings/).

2. **PayPal API Credentials**:
   - Obtain the `paypal_client_id` and `paypal_secret_key` from PayPal. You can find more details on obtaining these credentials in the [PayPal Developer Dashboard](https://developer.paypal.com/tools/sandbox/).

3. **Python 3**:
   - Ensure that the latest version of Python 3 is installed on your machine.

### Installation

To install and run Secure Shop API on your local machine, follow these steps:

1. **Create a Virtual Environment**:
   - Activate a virtual environment on your local machine. You can use tools like `virtualenv` or `venv` to create and activate a virtual environment.

2. **Install Dependencies**:
   - Inside the virtual environment, navigate to the project directory and run the following command to install the required dependencies from the `requirements.txt` file:

     ```
     pip install -r requirements.txt
     ```

3. **Run the Development Server**:
   - Navigate to the `shop` folder within the project directory, where the Django application is located.
   - Run the following command to start the development server:

     ```
     python manage.py runserver
     ```

   - The API should now be accessible locally at `http://localhost:8000/`.

## Usage

To understand how to use Secure Shop API and explore its endpoints, you can use the following Postman API collection:

- [Secure Shop API Postman Collection](https://github.com/davidsmolov/Secure_Shop/blob/main/Secure_Shop_Documentation.json)

The base URL in the Postman collection is currently set to my own running API for reference. You can use the provided user credentials for testing:

- Email: test@test.com
- Password: Pentest1!

Once you have explored the collection and read the documentation within it, feel free to change the base URL to `http://localhost:8000/` and run the API locally with any changes you have added.



## API Documentation

documentation for the file is included in the postman collection's comments. 
- [Secure Shop API Postman Collection](https://github.com/davidsmolov/Secure_Shop/blob/main/Secure_Shop_Documentation.json)



## Api Challenge

To provide a small challenge to how security apis work. I left one vulnerability regarding a way to bypass the stock limitation so a user can purchase more of an item than exists in the stock.
Feel free to attempt to find it, and even more, to patch it.
If assistance is requiered feel free to consult me on my linkdIn at: https://www.linkedin.com/in/david-smolovich/.

## License

This project is licensed under the [MIT License](LICENSE), allowing free use and modification while maintaining the emphasis on security and integrity.
