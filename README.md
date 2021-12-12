# COMP3019J - Product Ranking Website - Group10

This is the project of COMP3019J_2021 Group10, 
which is titled as "**Product Ranking Website**".

## About Our Group
*Group Members:*

Name|UCD student number|GitLab Username
:---:|:---:|:---:
LiuZhe|19206218|@Thor
GengTianyi|19206222|@19206222


## Basic Logic of our Product Ranking Website
There are three kinds of user role in total - **Customer**, Retailer, Administrator.   
Customers are able to search, view, rate, comment, favorite, and buy the products that
the retailer users uploaded.


## Intended Functionalities
1. login, logout, registration
1. For anonymous users, they can only view the category slides, and a limited number of the highest rated products.
2. After logging in, users are able to browse all the products.
2. Users with 'retailer' role are able to upload their products with pictures.
1. Users with 'retailer' role are able to edit or manage the products they have uploaded.   
3. Users are able to check their own profiles and the profiles of the retailer of each product.  
3. User are able to edit their profiles.
3. Users who have logged in are able to filter the products by different constrains.
3. Users who have logged in are able to search for specific products.
3. Users who have logged in are able to sort the products in the page with different sorting ways.
1. All the users are able to view the details about each specific product.
1. In the details page of a product, users who have logged in are able to rating the product by giving stars (1 - 5) or 
just view the rating feedback they have done.
1. In the details page of a product, anonymous users are able to view 5 latest released comments.
1. In the details page of a product, users who have logged in can view all the comments, details of those comments,
and the replies of it.
1. In the details page of a product, users who have logged in are able to comment the product.
1. In the details page of a product, users who have logged in are able to reply to each comment.
1. Users with a role of 'Customer' have a favorites, they can add or remove products from their favorites.
1. Users with a role of 'Customer' have a cart, they can add or remove products from their cart. 
   Further, they are able to select products in their cart to purchase.
1. Users with a role of 'administrator' are able to view all the products, comments and replies. Further, they are
able to delete or ban the illegal and improper things in our website.


## Functions implemented in milestone 1
1. login, logout, registration
1. For anonymous users, they can only view the category slides, and a limited number of the highest rated products.
2. After logging in, users are able to browse all the products.
2. Users with 'retailer' role are able to upload their products with pictures.
3. Users are able to check their own profiles and the profiles of the retailer of each product (no frontend yet).  
1. Clicking on the picture slides on the index page, user can view all the products under the corresponding category. 
1. All the users are able to view the details about each specific product.
1. In the details page of a product, users who have logged in are able to rating the product by giving stars (1 - 5) or 
just view the rating feedback they have done.
1. Some initial product data are made up (just for show) and 
   there are also the mechanism of auto inserting these data into our database.

## Functions implemented in milestone 2
1. Users can view products in different categories, by the pulldown bar in the nav. bar(under "categories").
2. Users can check their own profiles and  the profiles of the retailer of each product (with frontend).
3. Users can edit their profiles, includes change avatar.
4. Users can view the shopping cart by the pulldown bar in the nav. bar(under "Profile").
5. Users can add products to the cart in the detail page of a product.
6. Users can remove products in the cart.
7. Users can purchase products in the cart, with the total cost.
8. Users can see their avatar on the nav. bar, which is also the button to profile page.
9. Users can view the shopping history by the pulldown bar in the nav. bar(under ).
10. Users can change the theme(in dark or light), by the pulldown bar on the nav. bar(under "Theme").
11. Users can comment a bought product in the shopping history page.
12. Users can view comments in the product detail page.
13. A log file has been created.
14. Administrator can delete all the products in the website.
15. Administrator can delete one product of a retailer.

