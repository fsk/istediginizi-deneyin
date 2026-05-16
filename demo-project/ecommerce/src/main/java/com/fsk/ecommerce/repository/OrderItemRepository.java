package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.OrderItem;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.UUID;

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


