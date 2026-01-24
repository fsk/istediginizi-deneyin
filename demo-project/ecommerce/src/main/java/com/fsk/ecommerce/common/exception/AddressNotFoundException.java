package com.fsk.ecommerce.common.exception;

import java.util.UUID;

public class AddressNotFoundException extends RuntimeException {
    public AddressNotFoundException(UUID addressId) {
        super("Address with ID " + addressId + " not found");
    }
}

