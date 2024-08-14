package com.freeal.exception;

// 文件类型不支持异常
public class FileTypeNotSupportedException extends RuntimeException {
    public FileTypeNotSupportedException() {
        super("File type not supported");
    }

    public FileTypeNotSupportedException(String message) {
        super(message);
    }
}
