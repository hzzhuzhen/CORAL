package com.freeal.mapper;

import com.freeal.pojo.User;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
 * 员工管理
 */
@Mapper
public interface UserMapper {
    void insert(User user);

    // 通过用户名查询该用户
    User selectUserByName(@Param("name") String username);
}
