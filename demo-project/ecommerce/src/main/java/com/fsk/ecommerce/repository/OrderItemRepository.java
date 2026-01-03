package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.OrderItem;
import jakarta.persistence.QueryHint;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.QueryHints;

import java.util.List;
import java.util.UUID;
import java.util.stream.Stream;

public interface OrderItemRepository extends JpaRepository<OrderItem, UUID> {
    List<OrderItem> findByOrderId(UUID orderId);
    List<OrderItem> findByProductId(UUID productId);

//    @Query("select oi from OrderItem oi")
//    @QueryHints({
//            @QueryHint(name = org.hibernate.jpa.AvailableHints.HINT_FETCH_SIZE, value = "1000"),
//            @QueryHint(name = org.hibernate.jpa.AvailableHints.HINT_READ_ONLY, value = "true")
//    })
//    Stream<OrderItem> streamAll();
}


