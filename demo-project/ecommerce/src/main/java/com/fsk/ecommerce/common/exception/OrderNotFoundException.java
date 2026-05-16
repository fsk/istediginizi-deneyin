package com.fsk.ecommerce.common.exception;

import java.util.UUID;

public class OrderNotFoundException extends RuntimeException {
    public OrderNotFoundException(UUID orderId) {
        super("Order with ID " + orderId + " not found");
    }
}

