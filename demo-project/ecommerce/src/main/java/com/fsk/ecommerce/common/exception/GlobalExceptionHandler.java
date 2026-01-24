package com.fsk.ecommerce.common.exception;

import com.fsk.ecommerce.common.ErrorMessage;
import com.fsk.ecommerce.common.GenericResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<GenericResponse<Void>> handleUserNotFoundException(UserNotFoundException ex) {
        log.error("User not found: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(GenericResponse.error(ErrorMessage.USER_NOT_FOUND, HttpStatus.NOT_FOUND.value()));
    }

    @ExceptionHandler(ProductNotFoundException.class)
    public ResponseEntity<GenericResponse<Void>> handleProductNotFoundException(ProductNotFoundException ex) {
        log.error("Product not found: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(GenericResponse.error(ErrorMessage.PRODUCT_NOT_FOUND, HttpStatus.NOT_FOUND.value()));
    }

    @ExceptionHandler(AddressNotFoundException.class)
    public ResponseEntity<GenericResponse<Void>> handleAddressNotFoundException(AddressNotFoundException ex) {
        log.error("Address not found: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(GenericResponse.error(ErrorMessage.ADDRESS_NOT_FOUND, HttpStatus.NOT_FOUND.value()));
    }

    @ExceptionHandler(OrderNotFoundException.class)
    public ResponseEntity<GenericResponse<Void>> handleOrderNotFoundException(OrderNotFoundException ex) {
        log.error("Order not found: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(GenericResponse.error(ErrorMessage.ORDER_NOT_FOUND, HttpStatus.NOT_FOUND.value()));
    }

    @ExceptionHandler(OrderAlreadyCancelledException.class)
    public ResponseEntity<GenericResponse<Void>> handleOrderAlreadyCancelledException(OrderAlreadyCancelledException ex) {
        log.error("Order already cancelled: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(GenericResponse.error(ErrorMessage.ORDER_ALREADY_CANCELLED, HttpStatus.BAD_REQUEST.value()));
    }

    @ExceptionHandler(InvalidStatusTransitionException.class)
    public ResponseEntity<GenericResponse<Void>> handleInvalidStatusTransitionException(InvalidStatusTransitionException ex) {
        log.error("Invalid status transition: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(GenericResponse.error(ErrorMessage.INVALID_STATUS_TRANSITION, HttpStatus.BAD_REQUEST.value()));
    }

    @ExceptionHandler(QuantityNotAvailableException.class)
    public ResponseEntity<GenericResponse<Void>> handleQuantityNotAvailableException(QuantityNotAvailableException ex) {
        log.error("Quantity not available: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(GenericResponse.error(ErrorMessage.QUANTITY_NOT_AVAILABLE, HttpStatus.BAD_REQUEST.value()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<GenericResponse<Map<String, String>>> handleValidationExceptions(
            MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach(error -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });

        log.error("Validation error: {}", errors);
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(GenericResponse.<Map<String, String>>builder()
                        .data(errors)
                        .message(ErrorMessage.VALIDATION_ERROR.getMessage())
                        .success(false)
                        .statusCode(HttpStatus.BAD_REQUEST.value())
                        .timestamp(java.time.LocalDateTime.now())
                        .build());
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<GenericResponse<Void>> handleIllegalArgumentException(IllegalArgumentException ex) {
        log.error("Illegal argument: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(GenericResponse.error(ErrorMessage.ILLEGAL_ARGUMENT, HttpStatus.BAD_REQUEST.value()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<GenericResponse<Void>> handleGenericException(Exception ex) {
        log.error("Unexpected error occurred: ", ex);
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(GenericResponse.error(
                        ErrorMessage.INTERNAL_SERVER_ERROR,
                        HttpStatus.INTERNAL_SERVER_ERROR.value()));
    }
}