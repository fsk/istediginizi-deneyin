package com.fsk.ecommerce.service;

import com.fsk.ecommerce.common.exception.ProductNotFoundException;
import com.fsk.ecommerce.entity.Product;
import com.fsk.ecommerce.mapper.ProductMapper;
import com.fsk.ecommerce.mapper.dto.ProductResponseDTO;
import com.fsk.ecommerce.mapper.dto.ProductSearchDTO;
import com.fsk.ecommerce.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Service
@RequiredArgsConstructor
@Slf4j
public class ProductService {

    private final ProductRepository productRepository;
    private final ProductMapper productMapper;
    private final ExecutorService executorService = Executors.newFixedThreadPool(10);
    private final ApplicationContext applicationContext;

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

    /**
     * StaleStateException'ı tetiklemek için tasarlanmış metod.
     * Aynı product'ı iki farklı thread'de eşzamanlı olarak güncellemeye çalışır.
     * Bu, optimistic locking (@Version) nedeniyle StaleStateException fırlatır.
     * <p>
     * NOT: Her thread kendi transaction'ında çalışır, bu yüzden @Transactional annotation'ı kaldırıldı.
     */
    public void updateProductConcurrently(UUID productId, Integer quantityToReduce1, Integer quantityToReduce2) {
        ProductService productService = ((ProductService) applicationContext.getBean("productService"));
        // İlk thread: Product'ı oku ve güncelle
        CompletableFuture<Void> future1 = CompletableFuture.runAsync(() -> productService.updateProductInTransaction(productId, quantityToReduce1, 1), executorService);

        // İkinci thread: Aynı product'ı oku ve güncelle (StaleStateException tetiklenecek)
        CompletableFuture<Void> future2 = CompletableFuture.runAsync(() -> productService.updateProductInTransaction(productId, quantityToReduce2, 2), executorService);

        // Her iki thread'in tamamlanmasını bekle
        CompletableFuture.allOf(future1, future2).join();
    }

    @Transactional
    public void updateProductInTransaction(UUID productId, Integer quantityToReduce, int threadNumber) {
        Product product = productRepository.findById(productId).orElseThrow(() -> new ProductNotFoundException(productId));
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        product.updateProduct(quantityToReduce);
        productRepository.save(product);
        log.info("Thread {}: Product {} updated, quantity reduced by {}", threadNumber, productId, quantityToReduce);
    }

}

