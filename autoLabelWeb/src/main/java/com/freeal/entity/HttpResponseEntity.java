package com.freeal.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class HttpResponseEntity {
    private Integer code;//状态码
    private String message;//状态消息
    private Object data;//返回数据
}
