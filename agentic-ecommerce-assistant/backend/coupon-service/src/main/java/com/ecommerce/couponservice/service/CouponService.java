package com.ecommerce.couponservice.service;

import com.ecommerce.couponservice.model.Coupon;
import com.google.api.core.ApiFuture;
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.DocumentSnapshot;
import com.google.cloud.firestore.Firestore;
import org.springframework.stereotype.Service;

@Service
public class CouponService {

    private final Firestore firestore;

    public CouponService(Firestore firestore) {
        this.firestore = firestore;
    }

    /**
     * Retrieve coupon data from Firestore by code.
     *
     * @param code coupon identifier
     * @return Coupon object
     */
    public Coupon getCoupon(String code) {
        try {
            DocumentReference docRef = firestore.collection("coupons").document(code);
            ApiFuture<DocumentSnapshot> future = docRef.get();
            DocumentSnapshot document = future.get();

            if (document.exists()) {
                Coupon coupon = document.toObject(Coupon.class);
                if (coupon != null && coupon.getCode() == null) {
                    coupon.setCode(code);
                }
                return coupon;
            }
            throw new RuntimeException("Coupon not found");
        } catch (Exception e) {
            throw new RuntimeException("Failed to fetch coupon", e);
        }
    }
}