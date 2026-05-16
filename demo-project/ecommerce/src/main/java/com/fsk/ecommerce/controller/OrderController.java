package com.fsk.ecommerce.controller;

import com.fsk.ecommerce.common.GenericResponse;
import com.fsk.ecommerce.common.SuccessMessage;
import com.fsk.ecommerce.entity.OrderStatus;
import com.fsk.ecommerce.mapper.dto.BulkOrderRequestDTO;
import com.fsk.ecommerce.mapper.dto.OrderRequestDTO;
import com.fsk.ecommerce.mapper.dto.OrderReportDTO;
import com.fsk.ecommerce.mapper.dto.OrderResponseDTO;
import com.fsk.ecommerce.mapper.dto.OrderStatusUpdateDTO;
import com.fsk.ecommerce.mapper.dto.OrderStatsDTO;
import com.fsk.ecommerce.service.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @PostMapping("/create-order")
    public ResponseEntity<GenericResponse<UUID>> createOrderSync(@RequestBody OrderRequestDTO request) {
        UUID orderId = orderService.createOrderSync(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(GenericResponse.success(orderId, HttpStatus.CREATED.value(), SuccessMessage.CREATED));
    }

    @GetMapping("/{orderId}")
    public ResponseEntity<GenericResponse<OrderResponseDTO>> getOrderById(@PathVariable UUID orderId) {
        OrderResponseDTO order = orderService.getOrderById(orderId);
        return ResponseEntity.ok(GenericResponse.success(order, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<GenericResponse<List<OrderResponseDTO>>> getAllOrdersByUserId(@PathVariable UUID userId) {
        List<OrderResponseDTO> orders = orderService.getAllOrders(userId);
        return ResponseEntity.ok(GenericResponse.success(orders, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }

    @GetMapping("/user/{userId}/status/{status}")
    public ResponseEntity<GenericResponse<List<OrderResponseDTO>>> getOrdersByUserIdAndStatus(@PathVariable UUID userId,@PathVariable OrderStatus status) {
        List<OrderResponseDTO> orders = orderService.getOrdersByUserIdAndStatus(userId, status);
        return ResponseEntity.ok(GenericResponse.success(orders, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }

    @GetMapping
    public ResponseEntity<GenericResponse<Page<OrderResponseDTO>>> getAllOrdersWithPagination(
            @RequestParam(required = false) OrderStatus status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "orderDate") String sortBy,
            @RequestParam(defaultValue = "DESC") Sort.Direction direction) {
        Sort sort = Sort.by(direction, sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);
        Page<OrderResponseDTO> orders = orderService.getAllOrdersWithPagination(status, pageable);
        return ResponseEntity.ok(GenericResponse.success(orders, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }

    @PatchMapping("/{orderId}/status")
    public ResponseEntity<GenericResponse<OrderResponseDTO>> updateOrderStatus(@PathVariable UUID orderId, @RequestBody OrderStatusUpdateDTO statusUpdateDTO) {
        OrderResponseDTO order = orderService.updateOrderStatus(orderId, statusUpdateDTO);
        return ResponseEntity.ok(GenericResponse.success(order, HttpStatus.OK.value(), SuccessMessage.UPDATED));
    }

    @PutMapping("/{orderId}/cancel")
    public ResponseEntity<GenericResponse<OrderResponseDTO>> cancelOrder(@PathVariable UUID orderId) {
        OrderResponseDTO order = orderService.cancelOrder(orderId);
        return ResponseEntity.ok(GenericResponse.success(order, HttpStatus.OK.value(), SuccessMessage.UPDATED));
    }

    @GetMapping("/{orderId}/items")
    public ResponseEntity<GenericResponse<List<OrderResponseDTO.OrderItemResponseDTO>>> getOrderItems(@PathVariable UUID orderId) {
        List<OrderResponseDTO.OrderItemResponseDTO> items = orderService.getOrderItems(orderId);
        return ResponseEntity.ok(GenericResponse.success(items, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }

    @GetMapping("/stats")
    public ResponseEntity<GenericResponse<OrderStatsDTO>> getOrderStats() {
        OrderStatsDTO stats = orderService.getOrderStats();
        return ResponseEntity.ok(GenericResponse.success(stats, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }

    @GetMapping("/report")
    public ResponseEntity<GenericResponse<OrderReportDTO>> getOrderReport(
            @RequestParam(required = false) LocalDateTime startDate,
            @RequestParam(required = false) LocalDateTime endDate) {
        
        // Eğer tarih verilmemişse, son 30 günü al
        if (startDate == null) {
            startDate = LocalDateTime.now().minusDays(30);
        }
        if (endDate == null) {
            endDate = LocalDateTime.now();
        }
        
        OrderReportDTO report = orderService.getOrderReport(startDate, endDate);
        return ResponseEntity.ok(GenericResponse.success(report, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }

    @PostMapping("/bulk")
    public ResponseEntity<GenericResponse<List<UUID>>> createBulkOrders(@RequestBody BulkOrderRequestDTO bulkRequest) {
        List<UUID> orderIds = orderService.createBulkOrders(bulkRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(GenericResponse.success(orderIds, HttpStatus.CREATED.value(), SuccessMessage.CREATED));
    }
}
