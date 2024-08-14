package com.freeal.service.impl;

import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.entity.HttpResponseEntity;
import com.freeal.commons.utils.JsonUtil;
import com.freeal.commons.utils.JwtUtil;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.entity.HttpResponseEntity;
import com.freeal.entity.LoginUserEntity;
import com.freeal.mapper.UserMapper;
import com.freeal.pojo.User;
import com.freeal.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.Objects;

@Service
@Slf4j
public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private AuthenticationManager authenticationManager;
    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public HttpResponseEntity login(User user) {
        Authentication authentication = new UsernamePasswordAuthenticationToken(user.getName(),
                user.getPassword());
        // 认证用户信息
        Authentication authenticate = authenticationManager.authenticate(authentication);
        // 认证成功
        LoginUserEntity loginUser = (LoginUserEntity) authenticate.getPrincipal();
        // 在这里生成并返回JWT生成的token给后续用户带上
        String token = JwtUtil.generateToken(String.valueOf(loginUser.getUser().getId()));
        HashMap<String, String> data = new HashMap<>();
        data.put("CORAL_token", token);
        return ResponseResultUtil.success(data);
    }

    @Override
    public HttpResponseEntity register(User user) {
        try {
            if (Objects.nonNull(userMapper.selectUserByName(user.getName()))) {
                return ResponseResultUtil.error(401, "该用户已存在");
            }

            // 加密密码
            user.setPassword(passwordEncoder.encode(user.getPassword()));
            userMapper.insert(user);
            return ResponseResultUtil.success();
        } catch (Exception e) {
            log.error("注册过程中发生异常", e);
            // 返回错误响应
            return ResponseResultUtil.error("注册失败");
        }

    }
}
