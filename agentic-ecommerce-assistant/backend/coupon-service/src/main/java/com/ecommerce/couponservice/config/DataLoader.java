package com.ecommerce.couponservice.config;

import com.ecommerce.couponservice.model.Coupon;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Bootstrap coupon sample data during app startup.
 */
@Configuration
public class DataLoader {

    /**
     * CommandLineRunner to populate initial coupons in Firestore (for dev/test data).
     */
    @Bean
    CommandLineRunner loadData(CouponRepository repository) {
        return args -> {

            Coupon c1 = new Coupon();
            c1.setCode("SAVE10");
            c1.setDiscount(10);
            c1.setActive(true);

            repository.save(c1);

            Coupon c2 = new Coupon();
            c2.setCode("SAVE20");
            c2.setDiscount(20);
            c2.setActive(true);

            repository.save(c2);

            Coupon c3 = new Coupon();
            c3.setCode("WELCOME");
            c3.setDiscount(15);
            c3.setActive(true);

            repository.save(c3);

        };
    }
}