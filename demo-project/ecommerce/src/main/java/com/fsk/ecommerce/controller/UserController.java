package com.fsk.ecommerce.controller;

import com.fsk.ecommerce.common.GenericResponse;
import com.fsk.ecommerce.common.SuccessMessage;
import com.fsk.ecommerce.mapper.dto.UserDTO;
import com.fsk.ecommerce.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.UUID;

@RequestMapping("/users")
@RestController
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/get-all-users")
    public ResponseEntity<List<UserDTO>> getAllUserDTO() {
        return ResponseEntity.ok(userService.userDTOList());
    }

    @GetMapping("/get-all-users-pagination")
    public ResponseEntity<Page<UserDTO>> getAllUserDTOPagination(@RequestParam(defaultValue = "0") int page, @RequestParam(defaultValue = "10") int size) {
        Pageable pageable = Pageable.ofSize(size).withPage(page);
        return ResponseEntity.ok(userService.findAll(pageable));
    }

    /**
     * MultipleBagFetchException tetiklemek için test endpoint'i.
     * addresses ve creditCards aynı JPQL'de JOIN FETCH edilir.
     */
    @GetMapping("/{userId}/test-multiple-bag-fetch")
    public ResponseEntity<GenericResponse<UserDTO>> testMultipleBagFetch(@PathVariable UUID userId) {
        UserDTO user = userService.loadUserWithMultipleBags(userId);
        return ResponseEntity.ok(GenericResponse.success(user, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }
}
