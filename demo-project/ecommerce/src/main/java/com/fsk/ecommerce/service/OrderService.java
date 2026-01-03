package com.fsk.ecommerce.service;

import com.fsk.ecommerce.entity.Order;
import com.fsk.ecommerce.entity.OrderItem;
import com.fsk.ecommerce.entity.OrderStatus;
import com.fsk.ecommerce.entity.Product;
import com.fsk.ecommerce.entity.User;
import com.fsk.ecommerce.mapper.dto.OrderRequestDTO;
import com.fsk.ecommerce.repository.OrderItemRepository;
import com.fsk.ecommerce.repository.OrderRepository;
import com.fsk.ecommerce.repository.ProductRepository;
import com.fsk.ecommerce.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {

    private final OrderRepository orderRepository;
    private final OrderItemRepository orderItemRepository;
    private final ProductRepository productRepository;
    private final UserRepository userRepository;

    @Transactional
    public UUID createOrderSync(OrderRequestDTO request) {
        log.debug("Creating order sync for user: {}", request.getUserId());

        User user = userRepository.findById(request.getUserId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        Order order = new Order();
        order.setUser(user);
        order.setOrderDate(LocalDateTime.now());
        order.setStatus(OrderStatus.PENDING);
        order.setTotalAmount(BigDecimal.ZERO);

        order = orderRepository.save(order);

        BigDecimal totalAmount = BigDecimal.ZERO;
        List<OrderItem> orderItems = new ArrayList<>();

        for (OrderRequestDTO.OrderItemRequestDTO itemRequest : request.getItems()) {
            Product product = productRepository.findById(itemRequest.getProductId())
                    .orElseThrow(() -> new RuntimeException("Product not found: " + itemRequest.getProductId()));

            if (product.getStockQuantity() < itemRequest.getQuantity()) {
                throw new RuntimeException("Insufficient stock for product: " + product.getName());
            }

            // Simulate some processing time to make the bottleneck more apparent
            try { Thread.sleep(50); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

            product.setStockQuantity(product.getStockQuantity() - itemRequest.getQuantity());
            productRepository.save(product);

            OrderItem orderItem = new OrderItem();
            orderItem.setOrder(order);
            orderItem.setProduct(product);
            orderItem.setQuantity(itemRequest.getQuantity());
            orderItem.setUnitPrice(product.getPrice());
            orderItem.setSubtotal(product.getPrice().multiply(BigDecimal.valueOf(itemRequest.getQuantity())));
            
            orderItems.add(orderItem);
            totalAmount = totalAmount.add(orderItem.getSubtotal());
        }

        orderItemRepository.saveAll(orderItems);
        order.setTotalAmount(totalAmount);
        orderRepository.save(order);

        return order.getId();
    }
}
