package com.fsk.ecommerce.mapper.dto;

import com.fsk.ecommerce.entity.OrderStatus;
import lombok.Data;

@Data
public class OrderStatusUpdateDTO {
    private OrderStatus status;
}

