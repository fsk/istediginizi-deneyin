package com.fsk.ecommerce.service;

import com.fsk.ecommerce.entity.User;
import com.fsk.ecommerce.repository.UserRepository;
import org.hibernate.loader.MultipleBagFetchException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class UserServiceMultipleBagFetchExceptionTest {

    @Autowired
    private UserService userService;

    @Autowired
    private UserRepository userRepository;

    private UUID testUserId;

    @BeforeEach
    @Transactional
    @Rollback(false)
    void setUp() {
        User user = userRepository.findAll().stream().findFirst().orElseThrow();
        testUserId = user.getId();
    }

    @Test
    void loadUserWithMultipleBags_ShouldThrowMultipleBagFetchException() {
        Exception exception = assertThrows(Exception.class,
                () -> userService.loadUserWithMultipleBags(testUserId));

        assertTrue(containsMultipleBagFetchException(exception),
                "Expected MultipleBagFetchException but got: " + exception.getClass().getName());
    }

    private boolean containsMultipleBagFetchException(Throwable throwable) {
        Throwable current = throwable;
        while (current != null) {
            if (current instanceof MultipleBagFetchException) {
                return true;
            }
            current = current.getCause();
        }
        return false;
    }
}
