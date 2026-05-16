package com.fsk.ecommerce.mapper.dto;

import lombok.Data;
import java.util.List;
import java.util.UUID;

@Data
public class BulkOrderRequestDTO {
    private UUID userId;
    private UUID shippingAddressId;
    private UUID billingAddressId;
    private String notes;
    private List<BulkOrderItemDTO> items;

    @Data
    public static class BulkOrderItemDTO {
        private UUID productId;
        private Integer quantity;
    }
}

