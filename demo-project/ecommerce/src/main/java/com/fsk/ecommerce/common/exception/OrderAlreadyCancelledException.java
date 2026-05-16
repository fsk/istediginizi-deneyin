package com.fsk.ecommerce.common.exception;

import java.util.UUID;

public class OrderAlreadyCancelledException extends RuntimeException {
    public OrderAlreadyCancelledException(UUID orderId) {
        super("Order with ID " + orderId + " is already cancelled");
    }
}

