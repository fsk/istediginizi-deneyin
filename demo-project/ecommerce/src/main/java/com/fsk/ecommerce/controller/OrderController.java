package com.fsk.ecommerce.controller;

import com.fsk.ecommerce.mapper.dto.OrderRequestDTO;
import com.fsk.ecommerce.service.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

@RestController
@RequestMapping("/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @PostMapping("/sync")
    public ResponseEntity<UUID> createOrderSync(@RequestBody OrderRequestDTO request) {
        return ResponseEntity.ok(orderService.createOrderSync(request));
    }
}
