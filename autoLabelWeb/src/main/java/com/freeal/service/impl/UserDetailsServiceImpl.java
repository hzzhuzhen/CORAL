package com.freeal.service.impl;

import com.freeal.entity.LoginUserEntity;
import com.freeal.mapper.UserMapper;
import com.freeal.pojo.User;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
@Slf4j
public class UserDetailsServiceImpl implements UserDetailsService {
    @Autowired
    private UserMapper userMapper;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userMapper.selectUserByName(username);
        // 未找到用户抛出异常
        if (Objects.isNull(user)) {
            throw new UsernameNotFoundException("username not found");
        }
        return new LoginUserEntity(user);
    }
}
