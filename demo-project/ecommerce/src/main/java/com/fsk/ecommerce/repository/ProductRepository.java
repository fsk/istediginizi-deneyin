package com.fsk.ecommerce.repository;

import com.fsk.ecommerce.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface ProductRepository extends JpaRepository<Product, UUID> {
    Optional<Product> findBySku(String sku);
    List<Product> findByCategory(String category);
    List<Product> findByBrand(String brand);
    List<Product> findByStockQuantityGreaterThan(Integer quantity);
    boolean existsBySku(String sku);

    
    @Query("""
        SELECT p FROM Product p WHERE 
        (:name IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%', :name, '%'))) AND 
        (:description IS NULL OR LOWER(p.description) LIKE LOWER(CONCAT('%', :description, '%'))) AND 
        (:minPrice IS NULL OR p.price >= :minPrice) AND 
        (:maxPrice IS NULL OR p.price <= :maxPrice) AND 
        (:category IS NULL OR p.category = :category) AND 
        (:brand IS NULL OR p.brand = :brand) AND 
        (:minStockQuantity IS NULL OR p.stockQuantity >= :minStockQuantity)
        """)
    List<Product> searchProducts(
            @Param("name") String name,
            @Param("description") String description,
            @Param("minPrice") BigDecimal minPrice,
            @Param("maxPrice") BigDecimal maxPrice,
            @Param("category") String category,
            @Param("brand") String brand,
            @Param("minStockQuantity") Integer minStockQuantity
    );
}


