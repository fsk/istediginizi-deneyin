package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.CreditCard;
import com.fsk.ecommerce.entity.CardStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CreditCardRepository extends JpaRepository<CreditCard, UUID> {
    List<CreditCard> findByUserId(UUID userId);
    List<CreditCard> findByUserIdAndStatus(UUID userId, CardStatus status);
    Optional<CreditCard> findByUserIdAndIsDefaultTrue(UUID userId);
    long countByUserId(UUID userId);
}

