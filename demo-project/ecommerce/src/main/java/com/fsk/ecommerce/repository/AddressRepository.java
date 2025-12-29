package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.Address;
import com.fsk.ecommerce.entity.AddressType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface AddressRepository extends JpaRepository<Address, UUID> {
    List<Address> findByUserId(UUID userId);
    List<Address> findByUserIdAndAddressType(UUID userId, AddressType addressType);
    List<Address> findByUserIdAndIsDefaultTrue(UUID userId);
}

