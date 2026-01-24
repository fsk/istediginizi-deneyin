package com.fsk.ecommerce.mapper.dto;

import com.fsk.ecommerce.entity.OrderStatus;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Data
public class OrderResponseDTO {

    private UUID orderId;
    private UUID userId;
    private String username;
    private LocalDateTime orderDate;
    private BigDecimal totalAmount;
    private OrderStatus status;
    private String notes;

    private AddressDTO shippingAddress;
    private AddressDTO billingAddress;

    private List<OrderItemResponseDTO> items;

    @Data
    public static class OrderItemResponseDTO {
        private UUID itemId;
        private UUID productId;
        private String productName;
        private Integer quantity;
        private BigDecimal unitPrice;
        private BigDecimal discount;
        private BigDecimal subtotal;
    }
}