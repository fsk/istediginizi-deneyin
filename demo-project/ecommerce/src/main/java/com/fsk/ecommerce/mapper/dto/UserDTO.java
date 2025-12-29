package com.fsk.ecommerce.mapper.dto;

import lombok.Data;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
public class UserDTO {

    UUID userId;
    String name;
    String email;
    LocalDateTime createdAt;

}
