# Titan-Clothing

Welcome to Titan-Clothing, the ultimate clothing store. Discover amazing clothing for men and women. From quick weeknight outfits to impressive outfits for special occasions, Titan-Clothing has something for everyone. Join our community and start your clothing adventure today!

### Link to live site : [Titan-Clothing](https://titan-clothing-d681a47fade4.herokuapp.com)

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

I used the site [coolors](https://coolors.co/palette/ccd5ae-e9edc9-fefae0-faedcd-d4a373) for the color scheme, I think these colors complement the purpose of the site well.

![Color Scheme](#)

### Stock Images

I used [Unsplash](https://unsplash.com/) to find my stock images.

### Favicon

I used [Favicon](https://favicon.io/) to create my favicon.

### Wireframes

I used [Balsamiq](https://balsamiq.com/) for my wireframes.

![Titan-Clothing Wireframes](#)

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

## Deployment & Local Development

### Deployment

The site is deployed using Heroku - [Titan-Clothing](https://titan-clothing-d681a47fade4.herokuapp.com)

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

#### How to Fork

To fork the repository:

1. Log in (or sign up) to Github.
2. Go to the repository for this project, [Titan-Clothing](https://github.com/EthanPeters96/Titan-Clothing)
3. Click the Fork button in the top right corner.

#### How to Clone

To clone the repository:

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, [Titan-Clothing](https://github.com/EthanPeters96/Titan-Clothing)
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.

## Testing

### Automated Testing

I have written automated tests for key functionality using Django's testing framework.

### Manual Testing

| Feature                  | Action                             | Expected result                               | Tested | Passed | Comments |
| ------------------------ | ---------------------------------- | --------------------------------------------- | ------ | ------ | -------- |
| User Registration        | Complete signup form               | Account created and verification email sent   | Yes    | Yes    | -        |
| User Login               | Enter credentials and submit       | User logged in and redirected to home page    | Yes    | Yes    | -        |
| Product Filtering        | Select category from navigation    | Only products from that category displayed    | Yes    | Yes    | -        |
| Product Search           | Enter search term in search bar    | Relevant products displayed                   | Yes    | Yes    | -        |
| Add to Bag               | Click "Add to Bag" on product      | Product added to bag and notification shown   | Yes    | Yes    | -        |
| Update Quantity          | Change quantity in shopping bag    | Quantity updated and totals recalculated      | Yes    | Yes    | -        |
| Remove from Bag          | Click "Remove" in shopping bag     | Item removed from bag and totals recalculated | Yes    | Yes    | -        |
| Checkout                 | Complete checkout form and payment | Order created and confirmation shown          | Yes    | Yes    | -        |
| View Profile             | Navigate to profile page           | User's order history and saved info displayed | Yes    | Yes    | -        |
| Update Profile           | Edit delivery information          | Information updated for future orders         | Yes    | Yes    | -        |
| Admin Product Management | Add/edit/delete products as admin  | Products successfully managed in database     | Yes    | Yes    | -        |

The site was also tested using dev tools on Google Chrome for responsiveness across different device sizes.

### Known Bugs

-   Minor styling issues on some mobile devices (resolved)
-   Checkout form validation error messages sometimes unclear (in progress)

### Lighthouse

I have tested my website using lighthouse.

#### Home Page

![Home Page](/assets/screenshots/home-lighthouse.png)

#### Products Page

![Products](/assets/screenshots/recipe-lighthouse.png)

#### Profile Page

![Profile](/assets/screenshots/profile-lighthouse.png)

### Compatibility

Tested on Google Chrome, Firefox, Safari, and Microsoft Edge for functionality, appearance, and responsiveness. All features passed.

### Validator Testing

I have used W3C HTML Validator, W3C CSS Validator, and JSHint to validate my code.

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

### Content

-   Product descriptions were written by me
-   Images were sourced from Unsplash with appropriate licensing

### Acknowledgments

I'd like to give thanks to my mentor Graeme Taylor for the support he has given me throughout my project. Here is a [link](https://github.com/G-Taylor) to his GitHub.

I'd also like to thank my tutor Jonathan from Nescot for his guidance and feedback.
