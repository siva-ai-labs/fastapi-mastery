from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="SIVA AI LABS - Retail Product API",
    description="Real-world FastAPI fundamentals",
    version="1.0.0"
)


# ----------------------------
# Data Models
# ----------------------------

class ProductCreate(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class Product(ProductCreate):
    id: int


class StockUpdate(BaseModel):
    stock: int = Field(ge=0)


# In-memory database for learning
products: dict[int, Product] = {
    1: Product(
        id=1,
        name="T-Shirt",
        price=199,
        stock=20
    ),
    2: Product(
        id=2,
        name="Jeans",
        price=599,
        stock=10
    ),
    3: Product(
        id=3,
        name="Jacket",
        price=999,
        stock=0
    )
}

next_product_id = 4


# ----------------------------
# Health Check
# ----------------------------

@app.get("/")
def home():
    return {
        "application": "SIVA AI LABS Retail API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "UP"}


# ----------------------------
# GET - All Products
# ----------------------------

@app.get("/products", response_model=list[Product])
def get_products(
        in_stock: bool | None = None
):
    result = list(products.values())

    if in_stock is not None:
        result = [
            product for product in result
            if (product.stock > 0) == in_stock
        ]

    return result


# ----------------------------
# GET - Product by ID
# ----------------------------

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = products.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# ----------------------------
# GET - Product Search
# ----------------------------

@app.get("/search", response_model=list[Product])
def search_products(
        name: str = Query(min_length=1)
):
    return [
        product for product in products.values()
        if name.lower() in product.name.lower()
    ]


# ----------------------------
# POST - Create Product
# ----------------------------

@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductCreate):
    global next_product_id

    new_product = Product(
        id=next_product_id,
        **product.model_dump()
    )

    products[next_product_id] = new_product
    next_product_id += 1

    return new_product


# ----------------------------
# PUT - Replace Product
# ----------------------------

@app.put(
    "/products/{product_id}",
    response_model=Product
)
def update_product(
        product_id: int,
        product: ProductCreate
):
    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    updated = Product(
        id=product_id,
        **product.model_dump()
    )

    products[product_id] = updated
    return updated


# ----------------------------
# PATCH - Update Stock
# ----------------------------

@app.patch(
    "/products/{product_id}/stock",
    response_model=Product
)
def update_stock(
        product_id: int,
        update: StockUpdate
):
    product = products.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    updated = product.model_copy(
        update={"stock": update.stock}
    )

    products[product_id] = updated
    return updated


# ----------------------------
# DELETE - Product
# ----------------------------

@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    del products[product_id]
    return None
