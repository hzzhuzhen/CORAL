package com.freeal;

import com.freeal.commons.utils.DataUtil;
import lombok.extern.slf4j.Slf4j;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.EnableAsync;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;

@MapperScan({"com.freeal.mapper"})
@SpringBootApplication
@EnableAsync
@Slf4j
public class Demo1Application {
    public static void main(String[] args) {
        SpringApplication.run(Demo1Application.class, args);
    }

    // Web项目启动时检测data文件夹是否存在
    @Bean
    public CommandLineRunner checkDirectory() {
        return args -> {
            Path jarDir = Paths.get(System.getProperty("user.dir"));
            // 创建data文件夹
            File dataFolder = jarDir.resolve("data").toFile();
            DataUtil.mkFolder(dataFolder);
            // 创建data/tmp文件夹
            File tmpFolder = dataFolder.toPath().resolve("tmp").toFile();
            DataUtil.mkFolder(tmpFolder);
        };
    }
}
