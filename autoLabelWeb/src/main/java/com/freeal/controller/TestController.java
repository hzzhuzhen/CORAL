package com.freeal.controller;

import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.entity.HttpResponseEntity;
import com.freeal.service.DemoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.HashMap;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;

/**
 * hello world测试接口
 */


@RestController()
@RequestMapping("/test")
public class TestController {
    @Autowired
    private DemoService demoService;

    @GetMapping ("/hello")
    public HttpResponseEntity helloSpringboot(){
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        Long uid = (Long) authentication.getPrincipal();
        HashMap<String, Long> data = new HashMap<>();
        data.put("uid", uid);
        return ResponseResultUtil.success(data);
    }

    //@RequestMapping("/llm")
    //public String testLLM() {
    //    demoService.createTask()
    //}
}
