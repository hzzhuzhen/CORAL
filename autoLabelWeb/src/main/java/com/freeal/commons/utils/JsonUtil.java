package com.freeal.commons.utils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonUtil {
    private final static ObjectMapper objectMapper = new ObjectMapper();

    /**
     * 类序列化为字符串
     *
     * @param obj 传入的类
     * @return 序列化后的字符串
     */
    public static String ObjectToJson(Object obj) throws JsonProcessingException {
        return objectMapper.writeValueAsString(obj);
    }
}
