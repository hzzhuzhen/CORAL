package com.freeal.service.impl;

import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.entity.HttpResponseEntity;
import com.freeal.configs.LanguageModelConfig;
import com.freeal.exception.FileTypeNotSupportedException;
import com.freeal.service.FileService;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Service
public class FileServiceImpl implements FileService {
    @Override
    public HttpResponseEntity uploadFile(MultipartFile file) {
        try {
            // 检测文件格式是否合法
            String contentType = file.getContentType();
            if (!"text/plain".equals(contentType) && !"text/csv".equals(contentType)) {
                throw new FileTypeNotSupportedException();
            }

            // 获取 UUID
            String uuid = UUID.randomUUID().toString();
            // 获取当前时间戳
            String timeStampStr = String.valueOf(System.currentTimeMillis());
            // 将时间戳插入到文件名和扩展名之间
            String newFileName = uuid + "_" + timeStampStr + ".csv";
            // 保存文件到指定位置
            Path filePath = Paths.get(LanguageModelConfig.USER_UPLOAD_DATA_TEMP_SAVE_DIR, newFileName);
            // 使用 try-with-resources 语句确保文件流在完成后被正确关闭
            try (InputStream inputStream = file.getInputStream()) {
                Files.copy(inputStream, filePath, StandardCopyOption.REPLACE_EXISTING);
            }

            // 同步到算法服务器
            //DataFileFacade.uploadInputData2ModelServer(savedFilePath);
            return ResponseResultUtil.success(new HashMap<>().put("fileName", newFileName));
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseResultUtil.error("Failed to upload file.");
        }
    }

    @Override
    public ResponseEntity<InputStreamResource> requestLabelResult(Long taskId) {
        return null;
    }
}
