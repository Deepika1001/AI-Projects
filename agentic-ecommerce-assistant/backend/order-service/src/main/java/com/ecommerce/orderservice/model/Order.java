package com.ecommerce.orderservice.model;

/**
 * Order domain object for order service.
 */
public class Order {

    private String id;

    private String userId;
    private String status;
    private String address;

    public Order() {}

    /** Unique order identifier. */
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    /** User ID who placed the order. */
    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }

    /** Order status (pending/shipped/delivered). */
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    /** Shipping address. */
    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }

}