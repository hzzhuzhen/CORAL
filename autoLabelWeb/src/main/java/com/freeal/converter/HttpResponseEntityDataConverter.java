package com.freeal.converter;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.freeal.entity.HttpResponseEntity;
import lombok.AllArgsConstructor;
import org.springframework.core.convert.converter.Converter;
import org.springframework.stereotype.Component;

import java.util.LinkedHashMap;

/**
 * 专门给HttpResponseEntity中的data属性使用的转换类
 */
@Component
@AllArgsConstructor
public class HttpResponseEntityDataConverter implements Converter<HttpResponseEntity, Object> {
    private final ObjectMapper objectMapper;

    @Override
    public Object convert(HttpResponseEntity source) {
        throw new UnsupportedOperationException("此转换器需要指定目标类进行转换");
    }

    /**
     * 输入HttpResponseEntity类和需要转换的类型(如xxx.class)，
     * 会将其输入HttpResponseEntity中的data转换成对应的类型
     * 使用样例如下：
     * HttpResponseEntity source = new HttpResponseEntity();
     * LanguageModelRunningStatus status = HttpResponseEntityDataConverter.convert(source, LanguageModelRunningStatus.class)
     * @param source HttpResponseEntity类
     * @param targetType 想要转换成的实体类
     * @return HttpResponseEntity中data数据转换后的实体类
     */
    public <T> T convert(HttpResponseEntity source, Class<T> targetType) {
        if (source.getData() instanceof LinkedHashMap) {
            return objectMapper.convertValue(source.getData(), targetType);
        } else {
            throw new IllegalArgumentException("无效的数据类型");
        }
    }
}
