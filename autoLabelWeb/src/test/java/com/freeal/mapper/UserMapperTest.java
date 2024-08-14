package com.freeal.mapper;

import com.freeal.pojo.User;
import org.junit.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.transaction.annotation.Transactional;

@ExtendWith(SpringExtension.class)
@TestPropertySource(locations = "classpath:application.yml")
@Transactional
@SpringBootTest
@RunWith(JUnit4.class)
public class UserMapperTest {
    @Autowired
    private UserMapper userMapper;
//    @Autowired
//    private TaskMapper taskMapper;

    @Test
    public void selectUserByNameTest() {
        System.out.println("666");
        User user = userMapper.selectUserByName("test");
        System.out.println("1"+user);
    }
}
