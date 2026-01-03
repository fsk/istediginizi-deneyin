package com.fsk.ecommerce.mapper;

import com.fsk.ecommerce.entity.Address;
import com.fsk.ecommerce.mapper.dto.AddressDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface AddressMapper {
    
    @Mapping(source = "id", target = "addressId")
    AddressDTO toDTO(Address address);
}

