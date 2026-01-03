package com.fsk.ecommerce.service;

import com.fsk.ecommerce.mapper.UserMapper;
import com.fsk.ecommerce.mapper.dto.UserDTO;
import com.fsk.ecommerce.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    @Transactional(readOnly = true)
    public List<UserDTO> userDTOList() {
        userRepository.findAllWithAddresses();
        userRepository.findAllWithCards();
        return userRepository.findAllWithHobbies().stream().map(userMapper::toDTO).toList();
        //return userRepository.findAllUserDetails().stream().map(userMapper::toDTO).toList();
    }

    @Transactional(readOnly = true)
    public Page<UserDTO> findAll(Pageable pageable) {
        return userRepository.findAll(pageable).map(userMapper::toDTO);
    }

}
