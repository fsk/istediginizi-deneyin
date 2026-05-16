package com.fsk.ecommerce.common.exception;

import java.util.UUID;

public class QuantityNotAvailableException extends RuntimeException {
    public QuantityNotAvailableException(UUID productId, Integer quantity) {
        super("Quantity " + quantity + " for product " + productId + " is not available");
    }
}
