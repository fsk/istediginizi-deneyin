package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface UserRepository extends JpaRepository<User, UUID> {

    @EntityGraph(attributePaths = {"addresses", "creditCards", "hobbies"})
    Page<User> findAll(Pageable pageable);

    @Query("select u from User u left join fetch u.addresses")
    List<User> findAllWithAddresses();

    @Query("select u from User u left join fetch u.creditCards")
    List<User> findAllWithCards();

    @Query("select u from User u left join fetch u.hobbies")
    List<User> findAllWithHobbies();

//     @Query("""
//                select u from User u
//                left join fetch u.addresses
//                left join fetch u.creditCards
//                left join fetch u.hobbies
//            """)
//    List<User> findAllUserDetails();

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);
}


