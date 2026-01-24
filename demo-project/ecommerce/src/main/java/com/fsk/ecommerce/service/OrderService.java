package com.fsk.ecommerce.service;

import com.fsk.ecommerce.common.exception.AddressNotFoundException;
import com.fsk.ecommerce.common.exception.InvalidStatusTransitionException;
import com.fsk.ecommerce.common.exception.OrderAlreadyCancelledException;
import com.fsk.ecommerce.common.exception.OrderNotFoundException;
import com.fsk.ecommerce.common.exception.ProductNotFoundException;
import com.fsk.ecommerce.common.exception.QuantityNotAvailableException;
import com.fsk.ecommerce.common.exception.UserNotFoundException;
import com.fsk.ecommerce.entity.Address;
import com.fsk.ecommerce.entity.Order;
import com.fsk.ecommerce.entity.OrderItem;
import com.fsk.ecommerce.entity.Product;
import com.fsk.ecommerce.entity.User;
import com.fsk.ecommerce.mapper.OrderItemMapper;
import com.fsk.ecommerce.mapper.OrderMapper;
import com.fsk.ecommerce.mapper.ProductMapper;
import com.fsk.ecommerce.entity.OrderStatus;
import com.fsk.ecommerce.mapper.dto.BulkOrderRequestDTO;
import com.fsk.ecommerce.mapper.dto.OrderRequestDTO;
import com.fsk.ecommerce.mapper.dto.OrderReportDTO;
import com.fsk.ecommerce.mapper.dto.OrderResponseDTO;
import com.fsk.ecommerce.mapper.dto.OrderStatusUpdateDTO;
import com.fsk.ecommerce.mapper.dto.OrderStatsDTO;
import com.fsk.ecommerce.repository.AddressRepository;
import com.fsk.ecommerce.repository.OrderItemRepository;
import com.fsk.ecommerce.repository.OrderRepository;
import com.fsk.ecommerce.repository.ProductRepository;
import com.fsk.ecommerce.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.jspecify.annotations.NonNull;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {

    private final OrderRepository orderRepository;
    private final OrderItemRepository orderItemRepository;
    private final ProductRepository productRepository;
    private final UserRepository userRepository;
    private final AddressRepository addressRepository;
    private final OrderMapper orderMapper;
    private final OrderItemMapper orderItemMapper;
    private final ProductMapper productMapper;

    @Transactional
    public UUID createOrderSync(OrderRequestDTO request) {
        UUID userId = request.getUserId();
        User user = userRepository.findById(userId).orElseThrow(() -> new UserNotFoundException(userId));

        List<Product> products = new ArrayList<>();

        for (OrderRequestDTO.OrderItemRequestDTO item : request.getItems()) {
            Product product = productRepository.findById(item.getProductId()).orElseThrow(() -> new ProductNotFoundException(item.getProductId()));
            if (!product.checkQuantity(item.getQuantity())) {
                throw new QuantityNotAvailableException(item.getProductId(), item.getQuantity());
            }
            products.add(product);
        }

        Address[] addresses = fetchAddresses(request.getShippingAddressId(), request.getBillingAddressId());
        Address shippingAddress = addresses[0];
        Address billingAddress = addresses[1];
        
        Order order = orderMapper.toOrder(request, user, shippingAddress, billingAddress);
        order = orderRepository.save(order);

        BigDecimal totalAmount = BigDecimal.ZERO;
        List<OrderItem> orderItems = new ArrayList<>();

        for (int i = 0; i < request.getItems().size(); i++) {
            OrderRequestDTO.OrderItemRequestDTO itemRequest = request.getItems().get(i);
            Product product = products.get(i);
            BigDecimal subtotal = product.getPrice().multiply(BigDecimal.valueOf(itemRequest.getQuantity()));

            OrderItem orderItem = orderItemMapper.toEntity(itemRequest, order, product, product.getPrice(), BigDecimal.ZERO, subtotal);

            totalAmount = totalAmount.add(subtotal);
            orderItems.add(orderItem);
            product.updateProduct(itemRequest.getQuantity());
        }

        orderItemRepository.saveAll(orderItems);
        productRepository.saveAll(products);
        order.setTotalAmount(totalAmount);
        orderRepository.save(order);
        log.info("Order created successfully with ID: {}", order.getId());
        return order.getId();
    }

    @Transactional(readOnly = true)
    public OrderResponseDTO getOrderById(UUID orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
        
        return toOrderResponseDTO(order);
    }

    @Transactional(readOnly = true)
    public List<OrderResponseDTO> getAllOrders(UUID userId) {
        List<Order> orders = orderRepository.findByUserId(userId);

        return getOrderResponseDTOS(orders);
    }

    @NonNull
    private OrderResponseDTO toOrderResponseDTO(Order order) {
        OrderResponseDTO responseDTO = orderMapper.toOrderResponseDTO(order);
        
        List<OrderItem> orderItems = orderItemRepository.findByOrderId(order.getId());
        List<OrderResponseDTO.OrderItemResponseDTO> itemResponseDTOs = orderMapper.toOrderItemResponseDTOList(orderItems);
        
        responseDTO.setItems(itemResponseDTOs);
        return responseDTO;
    }

    @NonNull
    private List<OrderResponseDTO> getOrderResponseDTOS(List<Order> orders) {
        return orders.stream()
                .map(this::toOrderResponseDTO)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public List<OrderResponseDTO> getOrdersByUserIdAndStatus(UUID userId, OrderStatus status) {
        List<Order> orders = orderRepository.findByUserIdAndStatus(userId, status);

        return getOrderResponseDTOS(orders);
    }

    @Transactional(readOnly = true)
    public Page<OrderResponseDTO> getAllOrdersWithPagination(OrderStatus status, Pageable pageable) {
        Page<Order> orders;
        
        if (status != null) {
            orders = orderRepository.findByStatus(status, pageable);
        } else {
            orders = orderRepository.findAll(pageable);
        }
        
        return orders.map(this::toOrderResponseDTO);
    }

    @Transactional
    public OrderResponseDTO updateOrderStatus(UUID orderId, OrderStatusUpdateDTO statusUpdateDTO) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
        
        OrderStatus currentStatus = order.getStatus();
        OrderStatus newStatus = statusUpdateDTO.getStatus();
        
        // Status geçiş validasyonu
        if (!currentStatus.canTransitionTo(newStatus)) {
            throw new InvalidStatusTransitionException(currentStatus, newStatus);
        }
        
        order.setStatus(newStatus);
        order = orderRepository.save(order);
        
        log.info("Order {} status updated from {} to {}", orderId, currentStatus, newStatus);
        
        return toOrderResponseDTO(order);
    }

    @Transactional
    public OrderResponseDTO cancelOrder(UUID orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
        
        if (order.getStatus() == OrderStatus.CANCELLED) {
            throw new OrderAlreadyCancelledException(orderId);
        }
        
        // Sadece belirli status'lardan cancel edilebilir
        if (order.getStatus() == OrderStatus.DELIVERED || order.getStatus() == OrderStatus.REFUNDED) {
            throw new InvalidStatusTransitionException(order.getStatus(), OrderStatus.CANCELLED);
        }
        
        // Stokları geri ekle
        List<OrderItem> orderItems = orderItemRepository.findByOrderId(order.getId());
        for (OrderItem item : orderItems) {
            Product product = item.getProduct();
            productMapper.restoreStock(product, item.getQuantity());
            productRepository.save(product);
        }
        
        order.setStatus(OrderStatus.CANCELLED);
        order = orderRepository.save(order);
        
        log.info("Order {} cancelled, stock quantities restored", orderId);
        
        return toOrderResponseDTO(order);
    }

    @Transactional(readOnly = true)
    public List<OrderResponseDTO.OrderItemResponseDTO> getOrderItems(UUID orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
        
        List<OrderItem> orderItems = orderItemRepository.findByOrderId(order.getId());
        return orderMapper.toOrderItemResponseDTOList(orderItems);
    }

    @Transactional(readOnly = true)
    public OrderStatsDTO getOrderStats() {
        long totalOrders = orderRepository.count();
        long totalUsers = userRepository.count();
        
        Map<String, Long> ordersByStatus = new HashMap<>();
        for (OrderStatus status : OrderStatus.values()) {
            long count = orderRepository.countByStatus(status);
            ordersByStatus.put(status.name(), count);
        }
        
        return orderMapper.toOrderStatsDTO(totalOrders, ordersByStatus, totalUsers);
    }

    @Transactional(readOnly = true)
    public OrderReportDTO getOrderReport(LocalDateTime startDate, LocalDateTime endDate) {
        List<Order> orders = orderRepository.findByOrderDateBetween(startDate, endDate);
        long totalOrders = orders.size();
        
        BigDecimal totalRevenue = orderRepository.calculateTotalRevenueBetween(startDate, endDate);
        if (totalRevenue == null) {
            totalRevenue = BigDecimal.ZERO;
        }
        
        List<Object[]> userSummariesRaw = orderRepository.findUserOrderSummariesBetween(startDate, endDate);
        List<OrderReportDTO.UserOrderSummaryDTO> userSummaries = userSummariesRaw.stream()
                .map(orderMapper::toUserOrderSummaryDTO)
                .collect(Collectors.toList());
        
        return orderMapper.toOrderReportDTO(totalOrders, totalRevenue, startDate, endDate, userSummaries);
    }

    @Transactional
    public List<UUID> createBulkOrders(BulkOrderRequestDTO bulkRequest) {
        UUID userId = bulkRequest.getUserId();
        User user = userRepository.findById(userId).orElseThrow(() -> new UserNotFoundException(userId));
        
        Address[] addresses = fetchAddresses(bulkRequest.getShippingAddressId(), bulkRequest.getBillingAddressId());
        Address shippingAddress = addresses[0];
        Address billingAddress = addresses[1];
        
        List<UUID> createdOrderIds = new ArrayList<>();
        
        for (BulkOrderRequestDTO.BulkOrderItemDTO item : bulkRequest.getItems()) {
            Product product = productRepository.findById(item.getProductId())
                    .orElseThrow(() -> new ProductNotFoundException(item.getProductId()));
            
            if (!product.checkQuantity(item.getQuantity())) {
                throw new QuantityNotAvailableException(item.getProductId(), item.getQuantity());
            }
            
            // Tek item'lı order request oluştur
            OrderRequestDTO orderRequest = orderMapper.bulkOrderItemToOrderRequest(userId, item, bulkRequest);
            
            // Order oluştur
            Order order = orderMapper.toOrder(orderRequest, user, shippingAddress, billingAddress);
            order = orderRepository.save(order);
            
            // OrderItem oluştur
            BigDecimal subtotal = product.getPrice().multiply(BigDecimal.valueOf(item.getQuantity()));
            OrderItem orderItem = orderItemMapper.toEntity(orderRequest.getItems().getFirst(), order, product, product.getPrice(), BigDecimal.ZERO, subtotal);
            orderItemRepository.save(orderItem);
            
            // Stok güncelle
            product.updateProduct(item.getQuantity());
            productRepository.save(product);
            
            // Order total amount güncelle
            order.setTotalAmount(subtotal);
            orderRepository.save(order);
            
            createdOrderIds.add(order.getId());
        }
        
        log.info("Bulk order created successfully: {} orders", createdOrderIds.size());
        return createdOrderIds;
    }

    private Address[] fetchAddresses(UUID shippingAddressId, UUID billingAddressId) {
        Address shippingAddress = null;
        Address billingAddress = null;
        
        if (shippingAddressId != null) {
            shippingAddress = addressRepository.findById(shippingAddressId)
                    .orElseThrow(() -> new AddressNotFoundException(shippingAddressId));
        }
        
        if (billingAddressId != null) {
            billingAddress = addressRepository.findById(billingAddressId)
                    .orElseThrow(() -> new AddressNotFoundException(billingAddressId));
        }
        
        return new Address[]{shippingAddress, billingAddress};
    }

}
