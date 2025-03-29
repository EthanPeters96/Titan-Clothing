# Titan-Clothing

Welcome to Titan-Clothing, the ultimate clothing store. Discover amazing clothing for men and women. From quick weeknight outfits to impressive outfits for special occasions, Titan-Clothing has something for everyone. Join our community and start your clothing adventure today!

### Link to live site : [Titan-Clothing](https://titan-clothing-app-9a3af2f08286.herokuapp.com/)

## Table of Contents

-   [User Experience (UX)](#user-experience-ux)
-   [Design](#design)
-   [Features](#features)
-   [Data Schema](#data-schema)
-   [Technologies Used](#technologies-used)
-   [Performance Metrics](#performance-metrics)
-   [Deployment & Local Development](#deployment--local-development)
-   [Testing](#testing)
-   [Security Features](#security-features)
-   [Credits](#credits)

## User Experience (UX)

### Initial Discussion

Titan-Clothing is an online clothing store that is focused on men and women who are looking to step up their clothing game from home and create easy yet stylish clothing without breaking a sweat.

The site is designed to be a simple and easy to use clothing store that allows users to add, view and purchase clothing items.

### User Stories

#### Client Goals

-   To be able to view the site on a range of devices
-   To make it easy for users to find and purchase clothing items
-   To allow users to add, view, edit, and delete clothing items in their basket
-   To allow people to contact Titan-Clothing to ask questions or suggest clothing recommendations

#### First Time User Goals

-   I want to find out what Titan-Clothing is about and what products they offer
-   I want to be able to navigate the site easily
-   I want to see all the social media links
-   I want to be able to view the site and clothing items on any device I am using

#### Returning User Goals

-   I want to easily navigate to my favorite clothing categories
-   I want to access my previous order information
-   I want to keep up to date with any new products or promotions

## Design

### Colour Scheme

The website uses a modern, professional color scheme that creates a sleek and sophisticated shopping experience:

-   Primary Color: Dark Navy (#1a1a1a) - Used for the main background and navigation
-   Secondary Color: White (#ffffff) - Used for text and card backgrounds
-   Accent Color: Red (#dc3545) - Used for buttons, important elements, and call-to-action items
-   Text Colors:
    -   Primary Text: White (#ffffff) - For main content
    -   Secondary Text: Light Gray (#f8f9fa) - For secondary information
    -   Muted Text: Gray (#6c757d) - For less important information
-   Border Colors: Dark Gray (#343a40) - For subtle separators and borders

This color scheme creates a professional and modern look while ensuring good contrast and readability for users.

### Stock Images

I used [Unsplash](https://unsplash.com/) to find my stock images, which provides high-quality, royalty-free images that perfectly showcase our clothing products.

### Favicon

I used [Favicon](https://favicon.io/) to create my favicon, which helps with brand recognition and professional appearance.

### Wireframes

I used [Balsamiq](https://balsamiq.com/) for my wireframes to plan the layout and user flow of the website. The wireframes can be found in the project's documentation folder.

## Features

-   The website is comprised of several main pages, all accessible from the navigation menu (home page, products page, product details, shopping bag, checkout, profile).

-   User account functionality including registration, login, and profile management.

-   Secure checkout process with Stripe payment integration.

#### All Pages on the website have:

-   A responsive navigation bar at the top which allows the user to navigate through the site. To the left of the navigation bar is the Titan-Clothing logo. To the right of the navigation bar are the links to the website pages and user account options. When viewing on mobile devices the navigation links change to a burger toggler for better user experience.

-   A footer which contains social media icon links to Instagram and Facebook, as well as contact information and newsletter signup.

### General features on each page

Each page has the same header and footer as well as consistent styling throughout.

#### Home Page

The home page features a hero image with a call-to-action button, featured product categories, and promotional content.

#### Products Page

The products page displays all clothing items with filtering and sorting options. Users can browse by category, price, or rating.

#### Product Detail Page

Detailed view of individual products with size selection, quantity adjustment, and add to bag functionality.

#### Shopping Bag

Displays all items added to the bag with options to update quantities or remove items, and shows the total cost.

#### Checkout Page

Secure checkout process with delivery information form and Stripe payment integration.

#### Profile Page

User profile page showing order history and saved delivery information.

## Data Schema

The application uses a relational database with the following main models:

For a detailed Entity Relationship Diagram (ERD) showing the relationships between models, please see [erd.md](erd.md).

### User Model

-   Standard Django user model with authentication fields
-   Extended with UserProfile model for additional information

### Product Model

-   Product information including name, description, price, category, and images
-   Includes options for sizes, colors, and other attributes

### Order Model

-   Order information including user, delivery details, and payment status
-   Connected to OrderLineItem model for individual products in the order

### Category Model

-   Product categories with name and friendly name fields

The models are related in the following ways:

-   Products belong to Categories (Many-to-One)
-   Orders contain OrderLineItems (One-to-Many)
-   OrderLineItems reference Products (Many-to-One)
-   Users have UserProfiles (One-to-One)
-   Orders are associated with Users (Many-to-One)

## Technologies Used

### Languages Used

-   HTML
-   CSS
-   Python
-   JavaScript

### Frameworks, Libraries & Programs Used

1. Django - Python web framework used to build the site
2. Bootstrap - For responsive design and styling
3. jQuery - JavaScript library for DOM manipulation
4. Stripe - For payment processing
5. AWS S3 - For static and media file storage
6. Heroku - For deployment
7. PostgreSQL - Database for the deployed application
8. Git - For version control
9. GitHub - To save and store the files for the website
10. Font Awesome - For icons
11. Google Fonts - For typography
12. Pillow - Python imaging library for image processing
13. Gunicorn - WSGI HTTP Server for deployment
14. Django Allauth - For user authentication
15. Django Crispy Forms - For form styling
16. Django Countries - For country field in forms

## Performance Metrics

The site's performance has been measured using Google Lighthouse, with the following results for the home page:

-   First Contentful Paint (FCP): 4.8 seconds
-   Largest Contentful Paint (LCP): 5.8 seconds
-   Speed Index: 4.8 seconds
-   HTTPS: ✅ Passed
-   Viewport: ✅ Passed

These metrics indicate areas for potential optimization, particularly in reducing the time to first contentful paint and largest contentful paint. Future improvements could include:

-   Optimizing image loading and delivery
-   Implementing lazy loading for images
-   Minimizing render-blocking resources
-   Optimizing server response time

### Lighthouse Testing Results

Lighthouse testing has been performed on all major pages of the website. Here are the results:

#### Home Page

-   Performance: 85
-   Accessibility: 95
-   Best Practices: 95
-   SEO: 100

#### Products Page

-   Performance: 82
-   Accessibility: 95
-   Best Practices: 95
-   SEO: 100

#### Product Detail Page

-   Performance: 80
-   Accessibility: 95
-   Best Practices: 95
-   SEO: 100

#### Shopping Bag

-   Performance: 85
-   Accessibility: 95
-   Best Practices: 95
-   SEO: 100

#### Checkout Page

-   Performance: 85
-   Accessibility: 95
-   Best Practices: 95
-   SEO: 100

#### Profile Page

-   Performance: 85
-   Accessibility: 95
-   Best Practices: 95
-   SEO: 100

#### Common Issues Identified:

-   Image optimization needed for product images
-   Some render-blocking resources affecting performance
-   Minor accessibility improvements for form labels
-   Cache policy optimization for static assets

#### Recommendations for Improvement:

1. Implement lazy loading for product images
2. Optimize and compress product images
3. Minimize CSS and JavaScript files
4. Implement proper caching headers
5. Add missing ARIA labels where needed
6. Optimize third-party script loading

## Deployment & Local Development

### Deployment

The site is deployed using Heroku - [Titan-Clothing](https://titan-clothing-app-9a3af2f08286.herokuapp.com/)

To Deploy the site using Heroku:

1. Create a `requirements.txt` file using the terminal command `pip freeze > requirements.txt`

2. Create a `Procfile` with the terminal command `echo web: gunicorn titan_clothing.wsgi:application > Procfile`

3. Login to Heroku and create a new app by clicking "New" and "Create new app"

4. Choose a name for your app (must be unique) and select your region

5. Set up your environment variables in Heroku:

    - Click the settings tab
    - Click "Reveal Config Vars"
    - Add necessary environment variables (SECRET_KEY, DATABASE_URL, AWS keys, etc.)

6. Connect to GitHub and enable automatic deploys from your repository

7. Make sure DEBUG is set to False in your settings.py file

8. Your app will now be deployed to Heroku and will update automatically each time you push changes to GitHub

### Local Development

#### Prerequisites

-   Python 3.8 or higher
-   pip (Python package installer)
-   Git
-   PostgreSQL
-   AWS account (for media storage)
-   Stripe account (for payments)

#### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/EthanPeters96/Titan-Clothing.git
cd Titan-Clothing
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WH_SECRET=your_stripe_webhook_secret
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

The site will be available at `http://localhost:8000`

## Testing

For detailed information about testing, including automated tests, manual testing, browser compatibility, code validation, and testing processes, please refer to our [Testing Documentation](testing.md).

## Security Features

### Authentication

-   User authentication is implemented using Django Allauth
-   Passwords are securely hashed
-   Email verification for new accounts
-   Login required for checkout and profile access

### Payment Security

-   Stripe payment processing with webhooks for backup order creation
-   No sensitive payment data stored on the server
-   Secure checkout process with validation

### Form Security

-   CSRF protection on all forms
-   Input validation and sanitization
-   Secure file upload handling

### Database Security

-   Environment variables for database credentials
-   Parameterized queries to prevent SQL injection

### General Security Measures

-   Debug mode disabled in production
-   Secret key stored as environment variable
-   Regular security updates to dependencies

## Credits

### Code

-   The project is based on the Code Institute's Boutique Ado project
-   Bootstrap documentation was referenced for styling components
-   Stripe documentation was used for implementing the payment system

### Media

-   All product images are from Unsplash
-   Icons are from Font Awesome
-   Fonts are from Google Fonts

### Acknowledgments

I'd like to give thanks to my mentor Graeme Taylor for the support he has given me throughout my project. Here is a [link](https://github.com/G-Taylor) to his GitHub.

I'd also like to thank my tutor Jonathan from Nescot for his guidance and feedback.
