package com.fsk.ecommerce.mapper;

import com.fsk.ecommerce.entity.User;
import com.fsk.ecommerce.mapper.dto.UserDTO;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface UserMapper {

    UserDTO userDto(User user);

}
