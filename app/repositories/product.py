from app.models import Product


class ProductRepository:
    def __init__(self, session):
        self.session = session

    def _apply_sort(self, query, sort: str | None):
        sort_options = {
            "price_asc": Product.price.asc(),
            "price_desc": Product.price.desc(),
            "stock_asc": Product.stock.asc(),
            "stock_desc": Product.stock.desc(),
            "title_asc": Product.title.asc(),
            "title_desc": Product.title.desc(),
            "newest": Product.created_at.desc(),
            "oldest": Product.created_at.asc(),
        }

        if sort in sort_options:
            query = query.order_by(sort_options[sort])

        return query

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
        category_ids: list[int] | None = None,
        page: int = 1,
        page_size: int = 20,
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
            query = query.filter(Product.category_id.in_(category_ids))

        query = self._apply_sort(query, sort)

        offset = (page - 1) * page_size

        query = query.offset(offset).limit(page_size)

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
