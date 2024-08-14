package com.freeal.handler;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.freeal.commons.utils.JsonUtil;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.entity.HttpResponseEntity;
import com.freeal.exception.FileTypeNotSupportedException;
import org.apache.tomcat.util.http.fileupload.impl.FileSizeLimitExceededException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.HashMap;
import java.util.Map;

// 全局异常捕获处理器
@ControllerAdvice
public class GlobalExceptionHandler {
    // 参数验证失败异常处理
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<HttpResponseEntity> handleValidationExceptions(MethodArgumentNotValidException ex) throws JsonProcessingException {
        // 获取验证失败的原因
        FieldError fieldError = (FieldError) (ex.getBindingResult().getAllErrors().get(0));
        HttpResponseEntity error = ResponseResultUtil.error(fieldError.getDefaultMessage());
        return new ResponseEntity<>(error, HttpStatus.OK);
    }

    // 文件超出限制异常处理
    @ExceptionHandler(FileSizeLimitExceededException.class)
    public ResponseEntity<HttpResponseEntity> handleFileSizeExceededException() {
        HttpResponseEntity error = ResponseResultUtil.error("The field file exceeds its maximum permitted size");
        return new ResponseEntity<>(error, HttpStatus.OK);
    }

    // 不支持文件类型异常处理
    @ExceptionHandler(FileTypeNotSupportedException.class)
    public ResponseEntity<HttpResponseEntity> handleFileTypeNotSupportedException(
            FileTypeNotSupportedException ex) {
        HttpResponseEntity error = ResponseResultUtil.error(ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.OK);
    }
}
