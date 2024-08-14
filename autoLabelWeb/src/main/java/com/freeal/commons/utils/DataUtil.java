package com.freeal.commons.utils;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.freeal.configs.DataConfig;
import com.freeal.converter.HttpResponseEntityDataConverter;
import com.freeal.enums.LanguageModelEnum;
import com.freeal.modelapi.ModelProgressInfoFetcher;
import com.freeal.pojo.LanguageModelRunningStatus;
import lombok.extern.slf4j.Slf4j;

import java.io.File;

// 数据操作工具类
@Slf4j
public class DataUtil {
    private static final ObjectMapper objectMapper = new ObjectMapper();

    // 将模型的进展数据写出
    public static Boolean writeLanguageModelProgressData(LanguageModelRunningStatus status) {
        try {
            File file = new File(DataConfig.DEMO_LLM_RUNNING_STATUS_DARA_PATH);
            objectMapper.writeValue(file, status);
            return true;
        } catch (Exception e) {
            log.error("有异常发生", e);
            return false;
        }
    }

    public static void mkFolder(File folder) {
        if (folder.exists() && folder.isDirectory()) {
            log.info("检测到目录下{}文件夹存在", folder.getAbsolutePath());
            return;
        }
        log.info("{}文件夹不存在，正在创建", folder.getAbsolutePath());
        if (folder.mkdirs()) {
            log.info("{}文件夹创建成功", folder.getAbsolutePath());
        } else {
            throw new RuntimeException(folder.getAbsolutePath() + "创建失败");
        }
    }

    public static void main(String[] args) {
        HttpResponseEntityDataConverter responseEntityDataConverter = new HttpResponseEntityDataConverter(new ObjectMapper());
        LanguageModelRunningStatus llmStatus = responseEntityDataConverter
                .convert(ModelProgressInfoFetcher.requestModelProgressDemo(LanguageModelEnum.LLM, false),
                        LanguageModelRunningStatus.class);
        writeLanguageModelProgressData(llmStatus);
    }
}
