package com.ecommerce.couponservice.config;

import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.FirestoreOptions;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Spring config for creating the Firestore client bean.
 */
@Configuration
public class FirestoreConfig {

    /**
     * Firestore client for database operations.
     */
    @Bean
    public Firestore firestore() {
        return FirestoreOptions.getDefaultInstance().getService();
    }
}