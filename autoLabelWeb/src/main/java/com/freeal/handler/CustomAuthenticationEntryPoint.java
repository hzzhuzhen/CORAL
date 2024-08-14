package com.freeal.handler;

import com.freeal.commons.utils.JsonUtil;
import com.freeal.commons.utils.ResponseResultUtil;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

// Spring Security认证异常处理器
@Component
public class CustomAuthenticationEntryPoint implements AuthenticationEntryPoint {
    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response,
                         AuthenticationException authException) throws IOException {
        String responseContent = JsonUtil.ObjectToJson(ResponseResultUtil.error(HttpStatus.UNAUTHORIZED.value(),
                "Authentication Failed"));
        ResponseResultUtil.renderString(response, responseContent);
    }
}
