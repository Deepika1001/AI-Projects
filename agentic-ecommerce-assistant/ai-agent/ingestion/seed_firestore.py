from google.cloud import firestore
from datetime import datetime, timezone

db = firestore.Client()

docs = [
    {
        "title": "Return Policy",
        "category": "policy",
        "content": (
            "Customers can return most unopened items within 30 days of delivery. "
            "Items must be unused and returned in original packaging whenever possible. "
            "Refunds are processed within 5 to 7 business days after the returned item passes inspection. "
            "Final-sale items, gift cards, and certain hygiene products are not eligible for return."
        ),
        "source_url": "/help/return-policy",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Coupon Usage Help",
        "category": "faq",
        "content": (
            "Only one coupon can be applied per order. "
            "Expired coupons cannot be reactivated. "
            "Coupons may have minimum cart value requirements and brand exclusions. "
            "Discounts are applied before shipping charges unless stated otherwise."
        ),
        "source_url": "/help/coupons",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Shipping and Delivery",
        "category": "shipping",
        "content": (
            "Standard shipping usually takes 3 to 5 business days. "
            "Express shipping usually takes 1 to 2 business days for eligible pin codes. "
            "Delivery timelines may vary during holidays, peak sale events, or severe weather conditions. "
            "Customers can see estimated delivery dates on the product page and at checkout."
        ),
        "source_url": "/help/shipping",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Order Tracking Help",
        "category": "orders",
        "content": (
            "Customers can track their order from the My Orders section after signing in. "
            "Tracking details are typically available once the order is packed and handed to the courier. "
            "A shipment tracking link is also sent by email or SMS when available."
        ),
        "source_url": "/help/order-tracking",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Payment Methods",
        "category": "payments",
        "content": (
            "We support credit cards, debit cards, UPI, net banking, and selected digital wallets. "
            "Cash on delivery is available only for eligible products and serviceable locations. "
            "Failed payment attempts are usually reversed automatically within a few business days by the payment provider."
        ),
        "source_url": "/help/payment-methods",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Refund Timeline",
        "category": "payments",
        "content": (
            "Refunds are initiated after return pickup and quality inspection are completed. "
            "Original payment method refunds usually take 5 to 7 business days. "
            "Store credit refunds may appear faster, often within 24 hours after approval."
        ),
        "source_url": "/help/refunds",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Order Cancellation",
        "category": "orders",
        "content": (
            "Customers can cancel an order before it is shipped from the warehouse. "
            "Once the order is shipped, cancellation may no longer be possible and the customer should use the return process after delivery. "
            "If cancellation is successful, the refund is started automatically."
        ),
        "source_url": "/help/order-cancellation",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Exchange Policy",
        "category": "policy",
        "content": (
            "Size and color exchanges are available for select fashion items when stock is available. "
            "Exchange requests must be placed within the eligible return window shown on the order details page. "
            "Products damaged by misuse are not eligible for exchange."
        ),
        "source_url": "/help/exchanges",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Account Registration Help",
        "category": "account",
        "content": (
            "Customers can create an account using email address or mobile number. "
            "A verification code may be required during sign-up for security purposes. "
            "Registered users can save addresses, review order history, and manage returns more easily."
        ),
        "source_url": "/help/account-registration",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Address Update Help",
        "category": "account",
        "content": (
            "Delivery addresses can usually be updated before the order is packed for shipment. "
            "Customers can manage saved addresses from the account settings page. "
            "Some restricted products may allow delivery only to selected regions."
        ),
        "source_url": "/help/address-updates",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "title": "Support Contact Options",
        "category": "support",
        "content": (
            "Customers can reach support through chat, email, or the help center contact form. "
            "For order-related issues, keeping the order ID ready helps speed up resolution. "
            "Support availability may vary by region and business hours."
        ),
        "source_url": "/help/contact-support",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    },
]

for item in docs:
    db.collection("knowledge_base").add(item)

print(f"Knowledge base seeded successfully with {len(docs)} documents.")
