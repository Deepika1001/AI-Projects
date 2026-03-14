package com.ecommerce.userservice.model;

/**
 * User domain object for user profile operations.
 */
public class User {

    private Long id;
    private String name;
    private String email;

    public User() {}

    /** Numeric user ID. */
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    /** User display name. */
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    /** User e-mail address. */
    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}