package com.fsk.ecommerce.controller;

import com.fsk.ecommerce.entity.Address;
import com.fsk.ecommerce.mapper.dto.AddressDTO;
import com.fsk.ecommerce.service.AddressService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RequestMapping("/address")
@RestController
@RequiredArgsConstructor
public class AddressController {

    private final AddressService addressService;

    @GetMapping("/by-city")
    public List<AddressDTO> getAllAddresses(@RequestParam String city) {
        long startTime = System.currentTimeMillis();
        List<AddressDTO> addresses = addressService.getAllAddressesFromCity(city);
        long endTime = System.currentTimeMillis();
        System.out.println("Retrieved addresses in " + (endTime - startTime) + "ms");
        return addresses;
    }

}
