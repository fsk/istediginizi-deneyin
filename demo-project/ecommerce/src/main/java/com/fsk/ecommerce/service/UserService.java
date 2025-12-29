package com.fsk.ecommerce.service;

import com.fsk.ecommerce.mapper.UserMapper;
import com.fsk.ecommerce.mapper.dto.UserDTO;
import com.fsk.ecommerce.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    @GetMapping("/users/get-all-users")
    public List<UserDTO> userDTOList() {
        return userRepository.findAll().stream().map(userMapper::userDto).toList();
    }

}
