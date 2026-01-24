package com.fsk.ecommerce.common;

public enum SuccessMessage {
    SUCCESS("Operation completed successfully"),
    CREATED("Resource created successfully"),
    UPDATED("Resource updated successfully"),
    DELETED("Resource deleted successfully"),
    RETRIEVED("Resource retrieved successfully");

    private final String message;

    SuccessMessage(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}


