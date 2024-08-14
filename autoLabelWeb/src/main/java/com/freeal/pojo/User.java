package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.sql.Timestamp;

/**
 * 员工实体类
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private Long id; //ID
    @NotBlank(message = "Username cannot be empty")
    @Size(min = 5, max = 20, message = "Username must be between 5 and 25 in length")
    private String name; //用户名
    @NotBlank(message = "Username cannot be empty")
    @Size(min = 5, max = 20, message = "Password must be between 5 and 25 in length")
    private String password; //密码
    @NotNull(message = "Phone number cannot be empty")
    private Long phoneNumber;
    private Timestamp createTime;
    private Timestamp updateTime;
    private Short status;
}
