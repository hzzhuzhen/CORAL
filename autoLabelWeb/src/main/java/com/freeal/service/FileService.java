package com.freeal.service;

import com.freeal.entity.HttpResponseEntity;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public interface FileService {
    // todo 待实现接口，保证前端上传的语料可以上传到模型端并带本地存储一份
    HttpResponseEntity uploadFile(MultipartFile file);

    // 下载标注好的文件
    ResponseEntity<InputStreamResource> requestLabelResult(Long taskId);
}
