package com.fsk.ecommerce.controller;

import com.fsk.ecommerce.common.ErrorMessage;
import com.fsk.ecommerce.common.GenericResponse;
import com.fsk.ecommerce.common.SuccessMessage;
import com.fsk.ecommerce.mapper.ProductMapper;
import com.fsk.ecommerce.mapper.dto.ProductResponseDTO;
import com.fsk.ecommerce.service.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;
    private final ProductMapper productMapper;

    @GetMapping("/search")
    public ResponseEntity<GenericResponse<List<ProductResponseDTO>>> searchProducts(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String description,
            @RequestParam(required = false) BigDecimal minPrice,
            @RequestParam(required = false) BigDecimal maxPrice,
            @RequestParam(required = false) String category,
            @RequestParam(required = false) String brand,
            @RequestParam(required = false) Integer minStockQuantity) {
        
        var searchDTO = productMapper.toProductSearchDTO(name, description, minPrice, maxPrice, category, brand, minStockQuantity);
        List<ProductResponseDTO> products = productService.searchProducts(searchDTO);
        return ResponseEntity.ok(GenericResponse.success(products, HttpStatus.OK.value(), SuccessMessage.RETRIEVED));
    }

    /**
     * StaleStateException'ı tetiklemek için test endpoint'i.
     * Aynı product'ı iki farklı thread'de eşzamanlı güncellemeye çalışır.
     * 
     * @param productId Product ID
     * @param quantity1 İlk thread'in azaltacağı miktar
     * @param quantity2 İkinci thread'in azaltacağı miktar
     */
    @PostMapping("/{productId}/test-concurrent-update")
    public ResponseEntity<GenericResponse<String>> testConcurrentUpdate(@PathVariable UUID productId, @RequestParam(defaultValue = "10") Integer quantity1, @RequestParam(defaultValue = "5") Integer quantity2) {
        productService.updateProductConcurrently(productId, quantity1, quantity2);
        return ResponseEntity.ok(GenericResponse.success("Concurrent update completed successfully", HttpStatus.OK.value(), SuccessMessage.SUCCESS));
    }


}

