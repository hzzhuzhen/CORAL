package com.freeal.commons.utils;

import com.freeal.entity.HttpResponseEntity;
import org.springframework.http.HttpStatus;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class ResponseResultUtil {
    //增删改 成功响应
    public static HttpResponseEntity success() {
        return new HttpResponseEntity(200, "success", null);
    }

    //查询 成功响应
    public static HttpResponseEntity success(Object data) {
        return new HttpResponseEntity(200, "success", data);
    }

    //失败响应
    public static HttpResponseEntity error(String msg) {
        return error(HttpStatus.BAD_REQUEST.value(), msg);
    }

    public static HttpResponseEntity error(int code, String msg) {
        return new HttpResponseEntity(code, msg, null);
    }

    /**
     * 将字符串渲染并返回客户端
     *
     * @param response 渲染对象
     * @param string   待渲染的字符串
     */
    public static void renderString(HttpServletResponse response, String string) throws IOException {
        response.setStatus(200);
        response.setContentType("application/json");
        response.setCharacterEncoding("utf-8");
        response.getWriter().print(string);
    }
}
