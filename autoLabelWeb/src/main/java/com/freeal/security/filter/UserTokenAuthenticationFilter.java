package com.freeal.security.filter;

import com.freeal.commons.utils.JwtUtil;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

// 检测请求是否带有用户token信息过滤器
@Component
public class UserTokenAuthenticationFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        String token = request.getHeader("CORAL_token");
        // 请求头没带token
        if (!StringUtils.hasText(token)) {
            // 没有token放行 此时的SecurityContextHolder没有用户信息 会被后面的过滤器拦截
            // 不直接拦截是因为可能请求是登录请求需要到后面的过滤器中认证
            logger.warn("未检测到携带token");
            filterChain.doFilter(request, response);
            return;
        }
        Long uid;
        // 解析token
        try {
            uid = Long.parseLong(JwtUtil.extractUsername(token));
        } catch (Exception e) {
            // token非法
            throw new RuntimeException("Invalidate Token");
        }
        // token检测正常给权限
        UsernamePasswordAuthenticationToken authentication  =
                new UsernamePasswordAuthenticationToken(uid, null, null);
        SecurityContextHolder.getContext().setAuthentication(authentication);
        // 放行
        filterChain.doFilter(request, response);
    }
}
