package com.fsk.ecommerce.mapper.dto;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

@Data
public class ProductResponseDTO {
    private UUID productId;
    private String name;
    private BigDecimal price;
    private Integer stockQuantity;
    private String description;
    private String category;
    private String brand;
    private String imageUrl;
    private String sku;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}

