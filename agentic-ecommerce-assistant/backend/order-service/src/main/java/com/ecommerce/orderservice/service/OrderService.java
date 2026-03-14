package com.ecommerce.orderservice.service;

import com.ecommerce.orderservice.model.Order;
import com.google.api.core.ApiFuture;
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.DocumentSnapshot;
import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.WriteResult;
import org.springframework.stereotype.Service;

@Service
public class OrderService {

    private final Firestore firestore;

    public OrderService(Firestore firestore) {
        this.firestore = firestore;
    }

    /**
     * Retrieve order details by ID from Firestore.
     */
    public Order getOrder(String id) {
        try {
            DocumentReference docRef = firestore.collection("orders").document(String.valueOf(id));
            ApiFuture<DocumentSnapshot> future = docRef.get();
            DocumentSnapshot document = future.get();

            if (document.exists()) {
                Order order = document.toObject(Order.class);
                if (order != null && order.getId() == null) {
                    order.setId(id);
                }
                return order;
            }
            throw new RuntimeException("Order not found");
        } catch (Exception e) {
            throw new RuntimeException("Failed to fetch order", e);
        }
    }

    /**
     * Get the status text for an order.
     */
    public String getOrderStatus(String id) {
        return getOrder(id).getStatus();
    }

    /**
     * Update shipping address on an order and return updated order.
     */
    public Order updateAddress(String id, String address) {
        try {
            DocumentReference docRef = firestore.collection("orders").document(String.valueOf(id));
            ApiFuture<WriteResult> future = docRef.update("address", address);
            future.get();
            return getOrder(id);
        } catch (Exception e) {
            throw new RuntimeException("Failed to update order address", e);
        }
    }
}