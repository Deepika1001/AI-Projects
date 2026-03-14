from google.cloud import firestore
from datetime import datetime, timezone

db = firestore.Client()

docs = [
    {
        "title": "Return Policy",
        "category": "policy",
        "content": (
            "Customers can return unopened items within 10 days of delivery. "
            "Refunds are processed within 5 business days after inspection."
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
            "Expired coupons cannot be reactivated."
        ),
        "source_url": "/help/coupons",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    }
]

for item in docs:
    db.collection("knowledge_base").add(item)

print("Knowledge base seeded successfully.")