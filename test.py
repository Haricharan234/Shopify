from pydantic import BaseModel
import shopify

# shopify credentials
SHOP_URL = "betterbody-co-test.myshopify.com"
API_VERSION = "2024-01"
ACCESS_TOKEN = "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"


class OrdersEntity(BaseModel):
    id:int
    total_price:str


def get_order_data(obj_name):
    """get shopify attributes"""
    all_orders = []
    attribute = getattr(shopify, obj_name)
    orders = attribute.find(since_id = 0, limit = 250)
    for order in orders:
        all_orders.append(order)
    while orders.has_next_page():
        orders = order.next_page()
        for order in orders:
            all_orders.append(order)
    return all_orders

# login to shopify and activate session
session = shopify.Session(SHOP_URL, API_VERSION, ACCESS_TOKEN)
shopify.ShopifyResource.activate_session(session)

# collecting the all orders
ords = get_order_data('Order')
orders = []
for o in ords:
    orders.append(OrdersEntity.parse_obj(o.attributes))

# printing all details of order
print("order details",ords[0].attributes)

# clear the session
shopify.ShopifyResource.clear_session()
