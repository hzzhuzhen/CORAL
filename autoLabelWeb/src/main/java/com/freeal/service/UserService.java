package com.freeal.service;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.pojo.User;

/**
 * 员工管理
 */
public interface UserService {

    /**
     * 登录
     *
     * @param user 前端传入的登录数据
     */
    HttpResponseEntity login(User user);

    /**
     * 注册
     *
     * @param user 需要注册的数据
     */
    HttpResponseEntity register(User user);

}
