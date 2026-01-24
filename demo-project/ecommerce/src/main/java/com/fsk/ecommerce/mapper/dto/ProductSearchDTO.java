package com.fsk.ecommerce.mapper.dto;

import lombok.Data;
import java.math.BigDecimal;

@Data
public class ProductSearchDTO {
    private String name;
    private String description;
    private BigDecimal minPrice;
    private BigDecimal maxPrice;
    private String category;
    private String brand;
    private Integer minStockQuantity;
}

