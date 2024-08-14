package com.freeal.service.impl;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.configs.LanguageModelConfig;
import com.freeal.mapper.TaskInfoMapper;
import com.freeal.pojo.TaskInfo;
import com.freeal.mapper.TaskMapper;
import com.freeal.pojo.Task;
import com.freeal.service.InfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;

@Service
public class InfoServiceImpl implements InfoService {
    @Autowired
    private TaskInfoMapper taskInfoMapper;
    @Autowired
    private TaskMapper taskMapper;

    @Override
    public TaskInfo queryInfo(TaskInfo taskInfo) {
        return taskInfoMapper.queryInfo(taskInfo);
    }

    @Override
    public HttpResponseEntity getBasicTaskInformationById(Long id) {
        HttpResponseEntity httpResponseEntity = new HttpResponseEntity();
        try {
            Task task = taskMapper.getTaskById(id);
            if (task == null) {
                httpResponseEntity.setCode(404);
                httpResponseEntity.setMessage("未找到任务");
                return httpResponseEntity;
            }
            HashMap<String, String> info = new HashMap<>();
            info.put("taskName", task.getName());
            info.put("llmModel", LanguageModelConfig.getLlmById(task.getLlmId()));
            info.put("slmModel", LanguageModelConfig.getSlmById(task.getSlmId()));
            httpResponseEntity.setData(info);
        } catch (Exception e) {
            e.printStackTrace();
            httpResponseEntity.setCode(400);
            httpResponseEntity.setMessage("请求查询错误");
            return httpResponseEntity;
        }
        httpResponseEntity.setCode(200);
        httpResponseEntity.setMessage("找到对应的任务信息");
        return httpResponseEntity;
    }
}
