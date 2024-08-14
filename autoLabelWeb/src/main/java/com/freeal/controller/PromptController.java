package com.freeal.controller;


import com.freeal.entity.HttpResponseEntity;
import com.freeal.commons.utils.MockDataOpt;
import com.freeal.pojo.Prompt;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.service.PromptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 提示词管理
 */
@RestController
public class PromptController {

    @Autowired
    private PromptService promptService;

    //查询大模型提示模版
    @GetMapping("/prompt/list")
    public HttpResponseEntity getPromptsByParams(Long taskId, Integer taskType, Integer promptType) {
        List<Prompt> prompts = promptService.getPromptList(taskId, taskType, promptType);
        return ResponseResultUtil.success(prompts);
    }
    //新增大模型提示模版
    @PostMapping("/prompt/list/save")
    public HttpResponseEntity createPrompt(@RequestBody List<Prompt>  promptList){
        promptList=MockDataOpt.createPrompt(promptList);
        promptService.createPrompt(promptList);
        return ResponseResultUtil.success("true");
    }


}
