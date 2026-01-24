package com.fsk.ecommerce.mapper;

import com.fsk.ecommerce.entity.Product;
import com.fsk.ecommerce.mapper.dto.ProductResponseDTO;
import com.fsk.ecommerce.mapper.dto.ProductSearchDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Mapper(componentModel = "spring", imports = {LocalDateTime.class})
public interface ProductMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "name", ignore = true)
    @Mapping(target = "price", ignore = true)
    @Mapping(target = "description", ignore = true)
    @Mapping(target = "category", ignore = true)
    @Mapping(target = "brand", ignore = true)
    @Mapping(target = "imageUrl", ignore = true)
    @Mapping(target = "sku", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "stockQuantity", expression = "java(product.getStockQuantity() + quantityToAdd)")
    @Mapping(target = "updatedAt", expression = "java(LocalDateTime.now())")
    void restoreStock(@MappingTarget Product product, Integer quantityToAdd);

    @Mapping(source = "id", target = "productId")
    ProductResponseDTO toProductResponseDTO(Product product);

    List<ProductResponseDTO> toProductResponseDTOList(List<Product> products);

    @Mapping(target = "name", source = "name")
    @Mapping(target = "description", source = "description")
    @Mapping(target = "minPrice", source = "minPrice")
    @Mapping(target = "maxPrice", source = "maxPrice")
    @Mapping(target = "category", source = "category")
    @Mapping(target = "brand", source = "brand")
    @Mapping(target = "minStockQuantity", source = "minStockQuantity")
    ProductSearchDTO toProductSearchDTO(String name, String description, BigDecimal minPrice, BigDecimal maxPrice, String category, String brand, Integer minStockQuantity);
}

