package com.ecommerce.couponservice.controller;

import com.ecommerce.couponservice.model.Coupon;
import com.ecommerce.couponservice.service.CouponService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/coupons")
public class CouponController {

    private final CouponService service;

    public CouponController(CouponService service) {
        this.service = service;
    }

    @GetMapping("/{code}")
    public Coupon getCoupon(@PathVariable String code) {
        return service.getCoupon(code);
    }
}