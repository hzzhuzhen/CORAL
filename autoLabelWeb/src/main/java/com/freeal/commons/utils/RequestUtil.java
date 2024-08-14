package com.freeal.commons.utils;

import com.freeal.entity.HttpResponseEntity;
import org.springframework.http.ResponseEntity;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;

public class RequestUtil {
    private final static RestTemplate restTemplate = new RestTemplate();

    /**
     * 发送GET请求
     *
     * @param url         目标接口url
     * @param queryParams 携带的参数
     * @return
     */
    public static HttpResponseEntity getRequest(String url, MultiValueMap<String, String> queryParams) {
        URI uri = UriComponentsBuilder.fromHttpUrl(url)
                .queryParams(queryParams)
                .build()
                .toUri();
        ResponseEntity<HttpResponseEntity> response = restTemplate.getForEntity(uri, HttpResponseEntity.class);
        return response.getBody();
    }


    public static HttpResponseEntity getRequest(String url) {
        return getRequest(url, null);
    }

    /**
     * 发送POST请求
     *
     * @param url         目标接口url
     * @param requestBody 请求体
     * @return 请求结果
     */
    public static HttpResponseEntity postRequest(String url, Object requestBody) {
        URI uri = UriComponentsBuilder.fromHttpUrl(url)
                .build()
                .toUri();
        ResponseEntity<HttpResponseEntity> response = restTemplate.postForEntity(uri,
                requestBody, HttpResponseEntity.class);
        return response.getBody();
    }
}
