package com.freeal.configs;

import com.freeal.handler.CustomAuthenticationEntryPoint;
import com.freeal.security.filter.UserTokenAuthenticationFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.savedrequest.NullRequestCache;

// Spring Security配置类
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Autowired
    private CustomAuthenticationEntryPoint customAuthenticationEntryPoint;
    @Autowired
    private UserTokenAuthenticationFilter userTokenAuthenticationFilter;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        // 前后端分离删除一些过滤器：表单登录/登出、session管理、csrf防护等
        http
                .formLogin(AbstractHttpConfigurer::disable)
                .httpBasic(AbstractHttpConfigurer::disable)
                .logout(AbstractHttpConfigurer::disable)
                .sessionManagement(AbstractHttpConfigurer::disable)
                .csrf(AbstractHttpConfigurer::disable)
                .requestCache(cache -> cache.requestCache(new NullRequestCache()))
                .authorizeRequests(auth -> auth
                        .antMatchers("/demo/**").permitAll() // demo版本接口放行
                        // 登录和注册接口使用匿名访问
                        .antMatchers("/users/register", "/users/login").anonymous()
                        .antMatchers("/swagger-ui.html", "/webjars/**", "/v2/**", "/swagger-resources/**").permitAll()
                        .anyRequest().authenticated()
                );

        // 添加检测请求头是否带有token过滤器
        http.addFilterBefore(userTokenAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);
        // 异常处理器配置
        http.exceptionHandling()
                .authenticationEntryPoint(customAuthenticationEntryPoint); // 认证失败异常处理
        // 允许跨域
        http.cors();
        return http.build();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration) throws Exception {
        return authenticationConfiguration.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }


}
