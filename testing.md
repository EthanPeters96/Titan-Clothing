# Testing Documentation

## Automated Testing

I have written automated tests for key functionality using Django's testing framework, including:

-   User authentication
-   Product management
-   Shopping cart functionality
-   Checkout process
-   Order management

## Manual Testing

| Feature                  | Action                             | Expected Result                               | Tested | Passed | Comments |
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

## Known Bugs

-   Minor styling issues on some mobile devices (resolved)
-   Checkout form validation error messages sometimes unclear (in progress)

## Browser Compatibility

The website has been tested and is fully functional on the following browsers:

-   Google Chrome (latest version)
-   Mozilla Firefox (latest version)
-   Microsoft Edge (latest version)
-   Safari (latest version)
-   Mobile browsers (iOS Safari, Android Chrome)

## Code Validation

The following tools were used to validate the code:

### HTML Validation

-   W3C HTML Validator
-   All pages pass validation with no errors

### CSS Validation

-   W3C CSS Validator
-   All stylesheets pass validation with no errors

### JavaScript Validation

-   JSHint
-   All JavaScript files pass validation with no errors

### Python Validation

-   PEP8
-   All Python files follow PEP8 guidelines

## Testing Process

### Unit Testing

-   Tests cover all major functionality including:
    -   User authentication
    -   Product management
    -   Shopping cart operations
    -   Checkout process
    -   Order management
    -   Form validation
    -   API endpoints

### Integration Testing

-   Tests verify the interaction between different components:
    -   User registration and login flow
    -   Product search and filtering
    -   Shopping cart to checkout process
    -   Payment processing with Stripe
    -   AWS S3 file uploads

### End-to-End Testing

-   Manual testing of complete user journeys:
    -   User registration to first purchase
    -   Product browsing to checkout
    -   Profile management
    -   Admin product management
