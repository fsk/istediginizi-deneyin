package com.fsk.ecommerce.mapper.dto;

import lombok.Data;
import java.util.Map;

@Data
public class OrderStatsDTO {
    private Long totalOrders;
    private Map<String, Long> ordersByStatus;
    private Long totalUsers;
}

