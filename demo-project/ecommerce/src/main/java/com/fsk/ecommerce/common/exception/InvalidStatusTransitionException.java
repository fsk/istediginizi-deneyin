package com.fsk.ecommerce.common.exception;

import com.fsk.ecommerce.entity.OrderStatus;

public class InvalidStatusTransitionException extends RuntimeException {
    public InvalidStatusTransitionException(OrderStatus currentStatus, OrderStatus newStatus) {
        super("Invalid status transition from " + currentStatus + " to " + newStatus);
    }
}

