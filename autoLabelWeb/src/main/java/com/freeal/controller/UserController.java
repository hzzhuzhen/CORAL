package com.freeal.controller;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.enums.LanguageModelEnum;
import com.freeal.pojo.User;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

/**
 * 用户接口
 */
@RestController
@RequestMapping("/users")
public class UserController {
    @Autowired
    private UserService userService;

    //  登录接口
    @PostMapping("/login")
    public HttpResponseEntity login(@RequestBody User user) {
        return userService.login(user);
    }

    /**
     * 注册接口
     *
     * @param user 注册的数据
     * @return 注册结果
     */
    @PostMapping("/register")
    public HttpResponseEntity register(@Valid @RequestBody User user) {
        return userService.register(user);
    }
}











