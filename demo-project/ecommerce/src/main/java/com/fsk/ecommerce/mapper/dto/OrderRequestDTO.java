package com.fsk.ecommerce.mapper.dto;

import lombok.Data;
import java.util.List;
import java.util.UUID;

@Data
public class OrderRequestDTO {
    private UUID userId;
    private List<OrderItemRequestDTO> items;

    @Data
    public static class OrderItemRequestDTO {
        private UUID productId;
        private Integer quantity;
    }
}
