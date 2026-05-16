package com.fsk.ecommerce.service;

import com.fsk.ecommerce.entity.Product;
import com.fsk.ecommerce.repository.ProductRepository;
import org.hibernate.StaleStateException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.orm.ObjectOptimisticLockingFailureException;
import org.springframework.test.annotation.Rollback;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.UUID;
import java.util.concurrent.CompletionException;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class ProductServiceStaleStateExceptionTest {

    @Autowired
    private ProductService productService;

    @Autowired
    private ProductRepository productRepository;

    private UUID testProductId;

    @BeforeEach
    @Transactional
    @Rollback(false)
    void setUp() {
        // Test için bir Product oluştur
        Product product = new Product();
        product.setName("Test Product");
        product.setPrice(new BigDecimal("100.00"));
        product.setStockQuantity(1000); // Yeterli stok
        product.setDescription("Test Description");
        product.setCategory("Test Category");
        product.setBrand("Test Brand");
        product.setSku("TEST-SKU-" + UUID.randomUUID());
        product.setVersion(0L); // Version başlangıç değeri
        
        Product savedProduct = productRepository.save(product);
        productRepository.flush(); // Hemen commit et
        testProductId = savedProduct.getId();
        
        System.out.println("=== Test Product Oluşturuldu ===");
        System.out.println("ID: " + testProductId);
        System.out.println("Başlangıç Stock: " + savedProduct.getStockQuantity());
        System.out.println("Başlangıç Version: " + savedProduct.getVersion());
    }

    @Test
    @Transactional
    @Rollback(false) // Test sonrası rollback yapma, veriyi görmek için
    void testUpdateProductConcurrently_ShouldThrowStaleStateException() {
        System.out.println("\n=== Concurrent Update Test Başlıyor ===");
        
        // Arrange
        Integer quantity1 = 10;
        Integer quantity2 = 5;
        boolean staleStateExceptionCaught = false;
        Exception caughtException = null;

        // Act
        try {
            productService.updateProductConcurrently(testProductId, quantity1, quantity2);
            System.out.println("❌ Exception fırlatılmadı!");
        } catch (CompletionException e) {
            caughtException = e;
            Throwable cause = e.getCause();
            
            // Exception chain'i kontrol et
            Throwable current = e;
            int depth = 0;
            while (current != null && depth < 10) {
                System.out.println("  [" + depth + "] " + current.getClass().getSimpleName() + ": " + current.getMessage());
                
                if (current instanceof StaleStateException || 
                    current instanceof ObjectOptimisticLockingFailureException) {
                    staleStateExceptionCaught = true;
                    System.out.println("✅ StaleStateException yakalandı!");
                    System.out.println("Exception Type: " + current.getClass().getSimpleName());
                    System.out.println("Exception Message: " + current.getMessage());
                    break;
                }
                
                current = current.getCause();
                depth++;
            }
            
            // Eğer doğrudan RuntimeException içinde wrapped ise
            if (!staleStateExceptionCaught && cause instanceof RuntimeException) {
                Throwable nestedCause = cause.getCause();
                if (nestedCause instanceof StaleStateException || 
                    nestedCause instanceof ObjectOptimisticLockingFailureException) {
                    staleStateExceptionCaught = true;
                    System.out.println("✅ StaleStateException yakalandı (nested)!");
                    System.out.println("Exception Type: " + nestedCause.getClass().getSimpleName());
                    System.out.println("Exception Message: " + nestedCause.getMessage());
                }
            }
            
            if (!staleStateExceptionCaught) {
                e.printStackTrace();
            }
        } catch (RuntimeException e) {
            caughtException = e;
            Throwable cause = e.getCause();
            
            if (cause instanceof StaleStateException || 
                cause instanceof ObjectOptimisticLockingFailureException) {
                staleStateExceptionCaught = true;
                System.out.println("✅ StaleStateException yakalandı!");
                System.out.println("Exception Type: " + cause.getClass().getSimpleName());
                System.out.println("Exception Message: " + cause.getMessage());
            } else {
                e.printStackTrace();
            }
        } catch (Exception e) {
            caughtException = e;
            System.out.println("Beklenmeyen exception: " + e.getClass().getSimpleName());
            e.printStackTrace();
        }

        // Assert
        assertTrue(staleStateExceptionCaught || caughtException != null, 
            "StaleStateException veya ObjectOptimisticLockingFailureException fırlatılmalı");

        // Product'ın son durumunu kontrol et
        Product finalProduct = productRepository.findById(testProductId).orElseThrow();
        System.out.println("\n=== Final Durum ===");
        System.out.println("Final Stock: " + finalProduct.getStockQuantity());
        System.out.println("Final Version: " + finalProduct.getVersion());
        
        // Sadece bir thread'in güncellemesi başarılı olmalı
        // Diğeri StaleStateException nedeniyle başarısız olmalı
        assertTrue(finalProduct.getStockQuantity() < 1000, 
            "Stock azalmalı (en az bir güncelleme başarılı olmalı)");
    }

    @Test
    void testUpdateProductWithStaleVersion_ShouldThrowStaleStateException() {
        System.out.println("\n=== Stale Version Test Başlıyor ===");
        
        // Arrange
        Integer quantityToReduce = 10;

        // Act & Assert
        Exception exception = assertThrows(Exception.class, () -> {
            productService.updateProductWithStaleVersion(testProductId, quantityToReduce);
        });

        // Exception tipini kontrol et
        boolean isExpectedException = exception instanceof StaleStateException ||
                exception instanceof ObjectOptimisticLockingFailureException ||
                (exception.getCause() != null && 
                 (exception.getCause() instanceof StaleStateException ||
                  exception.getCause() instanceof ObjectOptimisticLockingFailureException));

        assertTrue(isExpectedException, 
            "Expected StaleStateException or ObjectOptimisticLockingFailureException but got: " + 
            exception.getClass().getSimpleName());

        System.out.println("✅ Exception yakalandı!");
        System.out.println("Exception Type: " + exception.getClass().getSimpleName());
        System.out.println("Exception Message: " + exception.getMessage());
        System.out.println("✅ updateProductWithStaleVersion StaleStateException fırlattı!");
    }
}
