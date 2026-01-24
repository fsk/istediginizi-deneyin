package com.fsk.ecommerce.common;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class GenericResponse<T> {
    private T data;
    private String message;
    private boolean success;
    private Integer statusCode;
    private LocalDateTime timestamp;


    public static <T> GenericResponse<T> success(T data, Integer statusCode, SuccessMessage successMessage) {
        return GenericResponse.<T>builder()
                .data(data)
                .success(true)
                .message(successMessage.getMessage())
                .statusCode(statusCode)
                .timestamp(LocalDateTime.now())
                .build();
    }

    public static <T> GenericResponse<T> error(ErrorMessage errorMessage, Integer statusCode) {
        return GenericResponse.<T>builder()
                .message(errorMessage.getMessage())
                .statusCode(statusCode)
                .success(false)
                .timestamp(LocalDateTime.now())
                .build();
    }
}