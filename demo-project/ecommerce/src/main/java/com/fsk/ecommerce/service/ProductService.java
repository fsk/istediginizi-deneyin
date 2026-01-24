package com.fsk.ecommerce.service;

import com.fsk.ecommerce.entity.Product;
import com.fsk.ecommerce.mapper.ProductMapper;
import com.fsk.ecommerce.mapper.dto.ProductResponseDTO;
import com.fsk.ecommerce.mapper.dto.ProductSearchDTO;
import com.fsk.ecommerce.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class ProductService {

    private final ProductRepository productRepository;
    private final ProductMapper productMapper;

    @Transactional(readOnly = true)
    public List<ProductResponseDTO> searchProducts(ProductSearchDTO searchDTO) {
        List<Product> products = productRepository.searchProducts(
                searchDTO.getName(),
                searchDTO.getDescription(),
                searchDTO.getMinPrice(),
                searchDTO.getMaxPrice(),
                searchDTO.getCategory(),
                searchDTO.getBrand(),
                searchDTO.getMinStockQuantity()
        );
        
        return productMapper.toProductResponseDTOList(products);
    }
}

