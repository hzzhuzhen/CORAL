package com.freeal.controller;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.service.FileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;


@RestController
public class FileController {
    @Autowired
    private FileService fileService;

    @PostMapping("/inputFile/upload")
    public HttpResponseEntity handleFileUpload(@RequestParam("file") MultipartFile file) {
        return fileService.uploadFile(file);
    }
}
