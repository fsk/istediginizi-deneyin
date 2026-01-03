package com.fsk.ecommerce.service;

import com.fsk.ecommerce.mapper.AddressMapper;
import com.fsk.ecommerce.mapper.dto.AddressDTO;
import com.fsk.ecommerce.repository.AddressRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AddressService {

    private final AddressRepository addressRepository;
    private final AddressMapper addressMapper;

    public List<AddressDTO> getAllAddressesFromCity(String city) {
        return addressRepository.findByCity(city).stream()
                .map(addressMapper::toDTO)
                .toList();
    }
}
