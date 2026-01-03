package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.Address;
import com.fsk.ecommerce.entity.AddressType;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface AddressRepository extends JpaRepository<Address, UUID> {
    List<Address> findByUserId(UUID userId);
    List<Address> findByUserIdAndAddressType(UUID userId, AddressType addressType);
    List<Address> findByUserIdAndIsDefaultTrue(UUID userId);

    List<Address> findByCity(String city);
}

