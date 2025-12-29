package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.Hobby;
import com.fsk.ecommerce.entity.HobbyCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface HobbyRepository extends JpaRepository<Hobby, UUID> {
    Optional<Hobby> findByName(String name);
    List<Hobby> findByCategory(HobbyCategory category);
    boolean existsByName(String name);
}

