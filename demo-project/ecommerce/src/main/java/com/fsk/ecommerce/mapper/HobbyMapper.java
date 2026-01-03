package com.fsk.ecommerce.mapper;

import com.fsk.ecommerce.entity.Hobby;
import com.fsk.ecommerce.mapper.dto.HobbyDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface HobbyMapper {
    
    @Mapping(source = "id", target = "hobbyId")
    HobbyDTO toDTO(Hobby hobby);
}

