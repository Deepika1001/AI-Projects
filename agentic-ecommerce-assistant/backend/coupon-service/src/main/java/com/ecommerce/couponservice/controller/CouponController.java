package com.ecommerce.couponservice.controller;

import com.ecommerce.couponservice.model.Coupon;
import com.ecommerce.couponservice.service.CouponService;
import org.springframework.web.bind.annotation.*;

/**
 * REST controller for coupon lookup in the ecommerce assistant environment.
 */
@RestController
@RequestMapping("/coupons")
public class CouponController {

    private final CouponService service;

    public CouponController(CouponService service) {
        this.service = service;
    }

    /**
     * Lookup a coupon by code.
     *
     * @param code the coupon code
     * @return Coupon details, or error response when not found
     */
    @GetMapping("/{code}")
    public Coupon getCoupon(@PathVariable String code) {
        return service.getCoupon(code);
    }
}