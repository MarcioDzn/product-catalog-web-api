from app.models import Product


class ProductRepository:
    def __init__(self, session):
        self.session = session

    def create(self, product_data, commit=True):
        product_db = Product(
            category_id=product_data.category_id,
            title=product_data.title,
            description=product_data.description,
            price=product_data.price,
            is_visible=product_data.is_visible,
            stock=product_data.stock,
        )

        self.session.add(product_db)

        if commit:
            self.session.commit()
            self.session.refresh(product_db)
        else:
            self.session.flush()

        return product_db

    def get_all(
        self,
        title: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_stock: int | None = None,
        max_stock: int | None = None,
        sort: str | None = None,
        category_ids: int | None = None
    ):
        query = self.session.query(Product)

        if title:
            query = query.filter(Product.title.ilike(f"%{title}%"))

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if min_stock is not None:
            query = query.filter(Product.stock >= min_stock)

        if max_stock is not None:
            query = query.filter(Product.stock <= max_stock)

        if category_ids:
            query = query.filter(
                Product.category_id.in_(category_ids)
            )

        if sort == "price_asc":
            query = query.order_by(Product.price.asc())

        elif sort == "price_desc":
            query = query.order_by(Product.price.desc())

        elif sort == "stock_asc":
            query = query.order_by(Product.stock.asc())

        elif sort == "stock_desc":
            query = query.order_by(Product.stock.desc())

        elif sort == "title_asc":
            query = query.order_by(Product.title.asc())

        elif sort == "title_desc":
            query = query.order_by(Product.title.desc())

        elif sort == "newest":
            query = query.order_by(Product.created_at.desc())

        elif sort == "oldest":
            query = query.order_by(Product.created_at.asc())

        return query.all()

    def get_by_id(self, id):
        return self.session.query(Product).filter(Product.id == id).first()

    def update(self, product, product_data):
        updated_data = {}

        for key, value in product_data.model_dump(exclude_unset=True).items():
            if value is not None:
                updated_data[key] = value

        db_fields = {column.name for column in product.__table__.columns}

        for key, value in updated_data.items():
            if key in db_fields:
                setattr(product, key, value)

        self.session.commit()
        self.session.refresh(product)

        return product

    def delete(self, product):
        self.session.delete(product)
        self.session.commit()
