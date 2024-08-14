package com.freeal.service.impl;

import com.freeal.mapper.PromptMapper;
import com.freeal.pojo.Prompt;
import com.freeal.service.PromptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class PromptServiceImpl implements PromptService {
    @Autowired
    private PromptMapper promptMapper;

    @Override
    public List<Prompt> getPromptList(Long taskId, Integer taskType, Integer promptType) {
        return promptMapper.getPromptList(taskId, taskType, promptType);
    }

    @Override
    public void createPrompt(List<Prompt> promptList) {
        for (Prompt prompt : promptList) {
            //当前年月日转long
//            LocalDate currentDate = LocalDate.now();
//            int year = currentDate.getYear();
//            int month = currentDate.getMonthValue();
//            int day = currentDate.getDayOfMonth();
//            long ymd = (year * 10000L + month * 100L + day); //将年月日按顺序连接成长整型数字
            long ymd =System.currentTimeMillis();

            prompt.setCreateTime(ymd);
            prompt.setUpdateTime(ymd);
            promptMapper.createPrompt(prompt);
        }
    }
}
