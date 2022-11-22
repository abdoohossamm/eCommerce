## Store application: API V1

Products API:
  * /api/v1/products/
      * Any users can send a GET request that will return the products list.
      * Only authenticated users with is_seller, or is_staff can send a POST request with form data like the following:
  
      {

      "title": "required text",

      "slug": "required text",

      "description": "optional text",

      "price": "required float",

      "in_stock": "optional boolean",

      "is_active": "optional boolean",

      "thumbnail": "optional file(image)",

      "created_at": "auto generated",

      "modified_at": "auto generated",

      "category": "required int"

    }
  * /api/v1/products/<product-slug>/
    * Any user can send a GET request that will return the product details.
    * Only product's seller or staff user can send a PATH and PUT request to update the product.
    * Only product's seller or staff user can send a DELETE request to delete the product.
  * /api/v1/products/mine/
    * Only authenticated user can send a GET request to see the products owned by them.
  