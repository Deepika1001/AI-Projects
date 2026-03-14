package com.ecommerce.userservice.service;

import com.ecommerce.userservice.model.User;
import com.google.api.core.ApiFuture;
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.DocumentSnapshot;
import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.WriteResult;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final Firestore firestore;

    public UserService(Firestore firestore) {
        this.firestore = firestore;
    }

    /**
     * Retrieve a user from Firestore by numeric ID.
     */
    public User getUser(Long id) {
        try {
            DocumentReference docRef = firestore.collection("users").document(String.valueOf(id));
            ApiFuture<DocumentSnapshot> future = docRef.get();
            DocumentSnapshot document = future.get();

            if (document.exists()) {
                User user = document.toObject(User.class);
                if (user != null && user.getId() == null) {
                    user.setId(id);
                }
                return user;
            }
            throw new RuntimeException("User not found");
        } catch (Exception e) {
            throw new RuntimeException("Failed to fetch user", e);
        }
    }

    /**
     * Register or update a user record in Firestore.
     */
    public User registerUser(User user) {
        try {
            DocumentReference docRef = firestore.collection("users").document(String.valueOf(user.getId()));
            ApiFuture<WriteResult> future = docRef.set(user);
            future.get();
            return user;
        } catch (Exception e) {
            throw new RuntimeException("Failed to register user", e);
        }
    }
}