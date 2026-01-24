package com.fsk.ecommerce.common;

public enum ErrorMessage {
    USER_NOT_FOUND("User not found"),
    VALIDATION_ERROR("Validation failed"),
    ILLEGAL_ARGUMENT("Invalid argument"),
    INTERNAL_SERVER_ERROR("An unexpected error occurred"),
    RESOURCE_NOT_FOUND("Resource not found"),
    UNAUTHORIZED("Unauthorized access"),
    FORBIDDEN("Access forbidden"),
    BAD_REQUEST("Bad request"),
    PRODUCT_NOT_FOUND("Product not found"),
    QUANTITY_NOT_AVAILABLE("Quantity not available"),
    ADDRESS_NOT_FOUND("Address not found"),
    ORDER_NOT_FOUND("Order not found"),
    ORDER_ALREADY_CANCELLED("Order is already cancelled"),
    INVALID_STATUS_TRANSITION("Invalid status transition");

    private final String message;

    ErrorMessage(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}


