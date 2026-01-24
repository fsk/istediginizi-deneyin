package com.fsk.ecommerce.mapper;

import com.fsk.ecommerce.entity.Order;
import com.fsk.ecommerce.entity.OrderItem;
import com.fsk.ecommerce.entity.Product;
import com.fsk.ecommerce.mapper.dto.OrderRequestDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import java.math.BigDecimal;

@Mapper(componentModel = "spring")
public interface OrderItemMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "quantity", source = "itemRequest.quantity")
    OrderItem toEntity(OrderRequestDTO.OrderItemRequestDTO itemRequest, Order order, Product product, BigDecimal unitPrice, BigDecimal discount, BigDecimal subtotal);
}