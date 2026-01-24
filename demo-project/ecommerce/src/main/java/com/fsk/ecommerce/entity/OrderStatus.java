package com.fsk.ecommerce.entity;

public enum OrderStatus {
    PENDING,
    CONFIRMED,
    PROCESSING,
    SHIPPED,
    DELIVERED,
    CANCELLED,
    REFUNDED;

    public boolean canTransitionTo(OrderStatus newStatus) {
        // Aynı status'a geçiş her zaman geçerlidir
        if (this == newStatus) {
            return true;
        }

        // Basit bir status geçiş validasyonu
        // Daha karmaşık kurallar eklenebilir
        return switch (this) {
            case PENDING -> newStatus == CONFIRMED || newStatus == CANCELLED;
            case CONFIRMED -> newStatus == PROCESSING || newStatus == CANCELLED;
            case PROCESSING -> newStatus == SHIPPED || newStatus == CANCELLED;
            case SHIPPED -> newStatus == DELIVERED || newStatus == CANCELLED;
            case DELIVERED -> newStatus == REFUNDED;
            case CANCELLED, REFUNDED -> false; // Bu status'lardan geçiş yapılamaz
        };
    }
}

