package com.fsk.ecommerce.mapper;

import com.fsk.ecommerce.entity.Address;
import com.fsk.ecommerce.entity.Order;
import com.fsk.ecommerce.entity.OrderItem;
import com.fsk.ecommerce.entity.OrderStatus;
import com.fsk.ecommerce.entity.User;
import com.fsk.ecommerce.mapper.dto.BulkOrderRequestDTO;
import com.fsk.ecommerce.mapper.dto.OrderRequestDTO;
import com.fsk.ecommerce.mapper.dto.OrderReportDTO;
import com.fsk.ecommerce.mapper.dto.OrderResponseDTO;
import com.fsk.ecommerce.mapper.dto.OrderStatsDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Mapper(componentModel = "spring", uses = {AddressMapper.class}, imports = {LocalDateTime.class, OrderStatus.class})
public interface OrderMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "user", source = "user")
    @Mapping(target = "orderDate", expression = "java(LocalDateTime.now())")
    @Mapping(target = "status", expression = "java(OrderStatus.PENDING)")
    @Mapping(target = "totalAmount", ignore = true)
    @Mapping(target = "shippingAddress", source = "shippingAddress")
    @Mapping(target = "billingAddress", source = "billingAddress")
    @Mapping(target = "notes", source = "orderRequestDTO.notes")
    Order toOrder(OrderRequestDTO orderRequestDTO, User user, Address shippingAddress, Address billingAddress);

    @Mapping(source = "id", target = "orderId")
    @Mapping(source = "user.id", target = "userId")
    @Mapping(source = "user.username", target = "username")
    @Mapping(target = "items", ignore = true)  // Service'de set edilecek
    OrderResponseDTO toOrderResponseDTO(Order order);

    @Mapping(source = "id", target = "itemId")
    @Mapping(source = "product.id", target = "productId")
    @Mapping(source = "product.name", target = "productName")
    OrderResponseDTO.OrderItemResponseDTO toOrderItemResponseDTO(OrderItem orderItem);

    List<OrderResponseDTO.OrderItemResponseDTO> toOrderItemResponseDTOList(List<OrderItem> orderItems);

    @Mapping(target = "totalOrders", source = "totalOrders")
    @Mapping(target = "ordersByStatus", source = "ordersByStatus")
    @Mapping(target = "totalUsers", source = "totalUsers")
    OrderStatsDTO toOrderStatsDTO(Long totalOrders, java.util.Map<String, Long> ordersByStatus, Long totalUsers);

    @Mapping(target = "totalOrders", source = "totalOrders")
    @Mapping(target = "totalRevenue", source = "totalRevenue")
    @Mapping(target = "reportStartDate", source = "startDate")
    @Mapping(target = "reportEndDate", source = "endDate")
    @Mapping(target = "userSummaries", source = "userSummaries")
    OrderReportDTO toOrderReportDTO(Long totalOrders, java.math.BigDecimal totalRevenue, LocalDateTime startDate, LocalDateTime endDate, List<OrderReportDTO.UserOrderSummaryDTO> userSummaries);

    default OrderReportDTO.UserOrderSummaryDTO toUserOrderSummaryDTO(Object[] row) {
        UUID userId = (UUID) row[0];
        String username = (String) row[1];
        Long orderCount = ((Number) row[2]).longValue();
        java.math.BigDecimal totalRevenue = (java.math.BigDecimal) row[3];
        
        OrderReportDTO.UserOrderSummaryDTO dto = new OrderReportDTO.UserOrderSummaryDTO();
        dto.setUserId(userId);
        dto.setUsername(username);
        dto.setOrderCount(orderCount);
        dto.setTotalRevenue(totalRevenue);
        return dto;
    }

    default OrderRequestDTO bulkOrderItemToOrderRequest(UUID userId, BulkOrderRequestDTO.BulkOrderItemDTO bulkItem, BulkOrderRequestDTO bulkRequest) {
        OrderRequestDTO orderRequest = new OrderRequestDTO();
        orderRequest.setUserId(userId);
        orderRequest.setShippingAddressId(bulkRequest.getShippingAddressId());
        orderRequest.setBillingAddressId(bulkRequest.getBillingAddressId());
        orderRequest.setNotes(bulkRequest.getNotes());
        
        OrderRequestDTO.OrderItemRequestDTO orderItemRequest = bulkOrderItemToOrderItemRequest(bulkItem);
        orderRequest.setItems(java.util.List.of(orderItemRequest));
        
        return orderRequest;
    }

    @Mapping(target = "productId", source = "productId")
    @Mapping(target = "quantity", source = "quantity")
    OrderRequestDTO.OrderItemRequestDTO bulkOrderItemToOrderItemRequest(BulkOrderRequestDTO.BulkOrderItemDTO bulkItem);
}
