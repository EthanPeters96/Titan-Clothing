# Entity Relationship Diagram (ERD) for Titan-Clothing

```mermaid
erDiagram
    User ||--o{ Order : places
    User ||--|| UserProfile : has
    User {
        id int PK
        username string
        email string
        password string
        is_active boolean
        date_joined datetime
    }

    UserProfile ||--o{ Order : has
    UserProfile {
        id int PK
        user_id int FK
        phone_number string
        address_line1 string
        address_line2 string
        city string
        postcode string
        country string
    }

    Order ||--|{ OrderLineItem : contains
    Order {
        id int PK
        user_profile_id int FK
        order_number string
        date datetime
        total_amount decimal
        delivery_cost decimal
        grand_total decimal
        status string
    }

    OrderLineItem {
        id int PK
        order_id int FK
        product_id int FK
        quantity int
        lineitem_total decimal
    }

    Category ||--o{ Product : contains
    Category {
        id int PK
        name string
        friendly_name string
    }

    Product {
        id int PK
        category_id int FK
        name string
        description text
        price decimal
        image string
        has_sizes boolean
        rating decimal
        created_at datetime
        updated_at datetime
    }
```

## Entity Descriptions

### User

-   Represents the user account in the system
-   Contains basic authentication information
-   One-to-one relationship with UserProfile

### UserProfile

-   Extended user information
-   Contains delivery details
-   One-to-many relationship with Orders

### Order

-   Represents a purchase order
-   Contains order details and totals
-   One-to-many relationship with OrderLineItems

### OrderLineItem

-   Represents individual items in an order
-   Contains quantity and line item total
-   Many-to-one relationship with Product

### Category

-   Represents product categories
-   Contains category name and friendly name
-   One-to-many relationship with Products

### Product

-   Represents clothing items
-   Contains product details and pricing
-   Many-to-one relationship with Category

## Relationships

1. User → UserProfile: One-to-One
2. UserProfile → Order: One-to-Many
3. Order → OrderLineItem: One-to-Many
4. OrderLineItem → Product: Many-to-One
5. Category → Product: One-to-Many
