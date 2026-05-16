package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface UserRepository extends JpaRepository<User, UUID> {

    @EntityGraph(attributePaths = {"addresses", "hobbies"})
    Page<User> findAll(Pageable pageable);

    @Query("select u from User u left join fetch u.addresses")
    List<User> findAllWithAddresses();

    @Query("select u from User u left join fetch u.creditCards")
    List<User> findAllWithCards();

    @Query("select u from User u left join fetch u.hobbies")
    List<User> findAllWithHobbies();

    /**
     * İki List (bag) koleksiyonunu aynı sorguda fetch eder → MultipleBagFetchException tetiklenir.
     */
    @Query("""
            SELECT DISTINCT u FROM User u
            LEFT JOIN FETCH u.addresses
            LEFT JOIN FETCH u.creditCards
            WHERE u.id = :id
            """)
    Optional<User> findByIdWithMultipleBags(@Param("id") UUID id);

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);
}


