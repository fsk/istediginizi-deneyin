package com.fsk.ecommerce.mapper.dto;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Data
public class OrderReportDTO {
    private Long totalOrders;
    private BigDecimal totalRevenue;
    private LocalDateTime reportStartDate;
    private LocalDateTime reportEndDate;
    private List<UserOrderSummaryDTO> userSummaries;

    @Data
    public static class UserOrderSummaryDTO {
        private UUID userId;
        private String username;
        private Long orderCount;
        private BigDecimal totalRevenue;
    }
}

