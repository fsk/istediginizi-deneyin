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
    INVALID_STATUS_TRANSITION("Invalid status transition"),
    OPTIMISTIC_LOCKING_FAILED("The entity has been modified by another transaction. Please refresh and try again."),
    MULTIPLE_BAG_FETCH("Cannot fetch multiple bag collections in a single query. Use separate queries or Set instead of List.");

    private final String message;

    ErrorMessage(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}


