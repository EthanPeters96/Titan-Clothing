readme

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
-   To allow users to add, view, edit, and delete clothing items in there basket
-   To allow people to contact Titan-Clothing to ask questions or suggest clothing recommendations

#### First Time User Goals

-   I want to find out what Titan-Clothing is about and what I can do.
-   I want to be able to navigate the site easily.
-   I want to see all the social media links.
-   I want to be able to view the site and clothing items on any device I am using.

#### Returning User Goals

-   I want to easily navigate to my favorite clothing items.
-   I want to keep up to date with any new social media they post.

## Design

### Colour Scheme

I used the site [coolors](https://coolors.co/palette/ccd5ae-e9edc9-fefae0-faedcd-d4a373) for the color scheme, I think these colors complement the purpose of the site well.

![Color Scheme](/assets/screenshots/coolors.png)

### Stock Images

I used [Unsplash](https://unsplash.com/) to find my stock images.

### Favicon

I used [Favicon](https://favicon.io/) to create my favicon.

### Wireframes

I used [Balsamiq](https://balsamiq.com/) for my wireframes.

![FlavorVault Wireframes](/assets/screenshots/wireframes.png)

## Features

-   The website is comprised of five main pages, all are accessible from the navigation menu (home page, recipes page, categories page, login page & signup page).

-   secondary pages are profile page and add recipe page.

-   Lastly one extra page. (404 page)

#### All Pages on the website have:

-   A responsive navigation bar at the top which allows the user to navigate through the site. To the left of the navigation bar is the text Titan-Clothing. To the right of the navigation bar are the links to the website pages (home page, recipes page, categories page, login page & signup page). When viewing on mobile devices the navigation links change to a burger toggler. This was implemented to give the site a clean look and to promote a good user experience, as users are used to seeing the burger icon when navigating a site on a mobile device.

-   A footer which contains social media icons links to Instagram and Facebook. Icons were used to keep the footer clean and because they are universally recognizable.

### General features on each page

Each page has the same header and footer as well as theme to complete.

#### Home Page

![FlavorVault Home page](/assets/screenshots/home.png)

#### Recipes Page

![FlavorVault Recipes page](/assets/screenshots/recipe.png)

#### Categories Page

![FlavorVault Categories page](/assets/screenshots/categories.png)

#### Login Page

![FlavorVault Login page](/assets/screenshots/login.png)

#### Signup Page

![FlavorVault Signup page](/assets/screenshots/signup.png)

#### Profile Page

![FlavorVault Profile page](/assets/screenshots/profile.png)

## Data Schema

The application uses MongoDB as its database, with the following collections and field structures:

### Users Collection

{

"\_id": ObjectId,

"username": String,

"password": String (hashed),

"email": String

}

### Recipes Collection

{

"\_id": ObjectId,

"recipe_name": String,

"category_name": String,

"recipe_description": String,

"ingredients": Array,

"instructions": Array,

"created_by": String,

"date_added": Date

}

### Categories Collection

{

"\_id": ObjectId,

"category_name": String,

"category_description": String,

"created_by": String

}

The collections are related in the following ways:

-   Recipes reference categories through the `category_name` field
-   Recipes and categories reference users through the `created_by` field which matches the user's `username`
-   Each recipe and category document stores the username of its creator

### Entity Relationship Diagram (ERD)

![Entity Relationship Diagram](/assets/screenshots/erd.png)

This diagram illustrates:

-   One user can create many recipes (1:Many)
-   One user can create many categories (1:Many)
-   One category can contain many recipes (1:Many)

## Technologies Used

### Languages Used

-   HTML
-   CSS
-   Python
-   JavaScript

### Frameworks, Libraries & Programs Used

1. Balsamiq - Used to create wireframes
2. Flask - Used to create the backend for the website
3. Flask-WTF - Used to create the forms for the website
4. Flask-Login - Used to create the login system for the website
5. Jinja - Used to create the dynamic pages for the website
6. Heroku - Used to deploy the website
7. MongoDB - Used to store the data for the website
8. dnspython - Used to connect to the database
9. jQuery - Used to make the site more interactive
10. Pylint - To check for errors in the code
11. Black - To format the code app.py
12. prettier - To format all the other files
13. Font Awesome - For icons
14. pymongo - Used to interact with the database
15. Git - For version control
16. Github - To save and store the files for the website
17. Bootstrap - Used to create the navigation bar, cards and form
18. Google Dev Tools - To troubleshoot and test features and solve issues with responsiveness and styling
19. Stripe - To process payments
20. Bulma - To style the site
21. Google Fonts - To style the site

## Deployment & Local Development

### Deployment

The site is deployed using Heroku - [FlavorVault](https://flavorvault-d681a47fade4.herokuapp.com)

To Deploy the site using Heroku:

1. Create a `requirements.txt` file using the terminal command `pip freeze > requirements.txt`

2. Create a `Procfile` with the terminal command `echo web: python app.py > Procfile`

3. Login to Heroku and create a new app by clicking "New" and "Create new app"

4. Choose a name for your app (must be unique) and select your region

5. From the deploy tab on Heroku:

    - Select "Connect to GitHub" as the deployment method
    - Search for your repository name and click "Connect"
    - Scroll to the bottom of the deploy page and select "Enable Automatic Deploys"

6. Set up your environment variables in Heroku:

    - Click the settings tab
    - Click "Reveal Config Vars"
    - Add any necessary environment variables (e.g., SECRET_KEY, DATABASE_URL)

7. Push these changes to your GitHub repository: `bash
git add . 
git commit -m "Deployment: Add requirements.txt and Procfile"
git push   `

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

### Jest Testing

I have written a testing script using jest, all tests passed.

![Jest](/assets/screenshots/jest.png)

### Pylint Testing

I have used pylint to check for errors in the code. and black to format the code.

app.py is pep8 compliant and passes pylint with no errors.

![Pylint](/assets/screenshots/pylint.png)

### Manual Testing

| Feature         | Action                                | Expected result                                   | Tested | Passed | Comments |
| --------------- | ------------------------------------- | ------------------------------------------------- | ------ | ------ | -------- |
| Home            | Click on the "Home" link              | The user is redirected to the main page           | Yes    | Yes    | -        |
| New Recipes     | Click on the "New Recipes" link       | The user is redirected to the recipes page        | Yes    | Yes    | -        |
| Login           | Click on the "Login" link             | The user is redirected to the login page          | Yes    | Yes    | -        |
| Register        | Click on the "Register" link          | The user is redirected to the register page       | Yes    | Yes    | -        |
| Logout          | Click on the "Logout" link            | The user is redirected to the logout page         | Yes    | Yes    | -        |
| Profile         | Click on the "Profile" link           | The user is redirected to the profile page        | Yes    | Yes    | -        |
| Add Recipe      | Click on the "Add Recipe" button      | The user is redirected to the add recipe page     | Yes    | Yes    | -        |
| Edit Recipe     | Click on the "Edit Recipe" button     | The user is redirected to the edit recipe page    | Yes    | Yes    | -        |
| Delete Recipe   | Click on the "Delete" button          | Modal appears asking for confirmation             | Yes    | Yes    | -        |
| Delete Recipe   | Click "Cancel" in delete modal        | Modal closes, recipe is not deleted               | Yes    | Yes    | -        |
| Delete Recipe   | Click "Delete" in delete modal        | Recipe is deleted and user sees success message   | Yes    | Yes    | -        |
| Add Category    | Click on the "Add Category" button    | The user is redirected to the add category page   | Yes    | Yes    | -        |
| View Category   | Click on the "View Category" button   | The user is redirected to the view category page  | Yes    | Yes    | -        |
| Edit Category   | Click on the "Edit Category" button   | The user is redirected to the edit category page  | Yes    | Yes    | -        |
| Delete Category | Click on the "Delete Category" button | Modal appears asking for confirmation             | Yes    | Yes    | -        |
| Delete Category | Click "Cancel" in delete modal        | Modal closes, category is not deleted             | Yes    | Yes    | -        |
| Delete Category | Click "Delete" in delete modal        | Category is deleted and user sees success message | Yes    | Yes    | -        |
| 404 Error       | Click on a non-existent link          | The user is redirected to the 404 page            | Yes    | Yes    | -        |

The site was also tested using dev tools on Google Chrome for responsiveness.

### Known Bugs

-   Add category button icon display issue on mobile devices (unresolved)
-   New recipe form not displaying correctly on mobile devices (resolved)
-   Edit recipe form not displaying correctly on mobile devices (resolved)

### LightHouse

I have tested my website using lighthouse.

#### Home Page

![Home Page](/assets/screenshots/home-lighthouse.png)

#### Recipes Page

![Recipes](/assets/screenshots/recipe-lighthouse.png)

#### Profile Page

![Profile](/assets/screenshots/profile-lighthouse.png)

#### Categories Page

![Categories](/assets/screenshots/categories-lighthouse.png)

#### Login Page

![Login](/assets/screenshots/login-lighthouse.png)

#### Register Page

![Register](/assets/screenshots/register-lighthouse.png)

### Compatibility

Tested on [Google Chrome](https://www.google.co.uk/) for functionality, appearance, and responsiveness. All features passed.

### Validator

I have used [W3C](https://www.w3.org/) & [JSHint](https://jshint.com/) to validate my code.

### HTML

![HTML](/assets/screenshots/html-val.png)

Tested on all pages.

### CSS

![CSS](/assets/screenshots/css-val.png)

### JS

![JS](/assets/screenshots/js-hint.png)

## Security Features

### Authentication

-   User authentication is implemented using Flask-Login
-   Passwords are hashed using Werkzeug's security features before storage
-   Login is required for creating, editing, and deleting recipes/categories
-   Users can only modify their own content

### Form Security

-   CSRF (Cross-Site Request Forgery) protection is implemented using Flask-WTF
-   Input validation and sanitization is performed on all form submissions
-   File upload validation restricts file types and sizes

### Database Security

-   MongoDB connection string is stored as an environment variable
-   Database credentials are never exposed in the code
-   Queries are parameterized to prevent injection attacks

### Session Security

-   Session cookies are HTTP-only
-   Secure flag is set on cookies in production
-   Sessions expire after period of inactivity
-   Session data is stored server-side

### General Security Measures

-   Debug mode is disabled in production
-   Environment variables are used for sensitive configuration
-   Error messages don't reveal sensitive information
-   Regular security updates are applied to all dependencies

### Rate Limiting

-   API endpoints are rate-limited to prevent abuse
-   Failed login attempts are tracked and temporary lockouts are enforced

## Credits

I have used previous projects to help with this project.

I used AI assistant for my script.js file. and my app.py file.

[Boutique ADO](https://github.com/Code-Institute-Solutions/boutique_ado_v1)

[Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/)

I also referred to [Bootstrap](https://getbootstrap.com/) docs to learn new ways to style my page.

I followed some guidance from my mentor [Graeme Taylor](https://github.com/G-Taylor).

### Acknowledgments

I'd like to give thanks to Graeme my mentor for the support he has given me throughout my project here is a [link](https://github.com/G-Taylor) to his github.

I'd also like to thank my tutor Jonathan from Nescot.
