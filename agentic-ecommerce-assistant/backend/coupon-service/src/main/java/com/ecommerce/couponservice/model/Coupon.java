package com.ecommerce.couponservice.model;

/**
 * Represents a coupon and discount metadata.
 */
public class Coupon {

    private String code;
    private Integer discount;
    private boolean active;

    public Coupon() {}

    /** Coupon code. */
    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    /** Percentage or fixed discount value. */
    public Integer getDiscount() {
        return discount;
    }

    public void setDiscount(Integer discount) {
        this.discount = discount;
    }

    /** Active status. */
    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }
}