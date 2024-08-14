package com.freeal.service.impl;

import com.freeal.mapper.ProgressMapper;
import com.freeal.mapper.TaskMapper;
import com.freeal.pojo.Progress;
import com.freeal.pojo.Task;
import com.freeal.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class TaskServiceImpl implements TaskService {
    @Autowired
    private TaskMapper taskMapper;
    @Autowired
    private ProgressMapper progressMapper;

    @Override
    public Boolean createTask(Task task) {
        //当前年月日转long
        long now = System.currentTimeMillis();
        try {
            taskMapper.createTask(task);
            // 初始化progress表的一些数据
            Progress progress = new Progress();
            progress.setId(task.getId());
            progress.setCurrentModel(1);
            progress.setCurrentEpoch(0);
            progressMapper.insertProgress(progress);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    @Override
    public void updateTask(Task task) {

        Task task1 = new Task();
        //当前年月日转long
        LocalDate currentDate = LocalDate.now();
        int year = currentDate.getYear();
        int month = currentDate.getMonthValue();
        int day = currentDate.getDayOfMonth();

        task1.setOwnerId(task.getOwnerId());
//        task.setCreateTime(20240216L);
        task1.setOutputDataUrl(task.getOutputDataUrl());
        task1.setStatus(task.getStatus());
        taskMapper.updateTask(task1);

    }

    @Override
    public Task getTaskById(Long id) {
        return taskMapper.getTaskById(id);
    }

    @Override
    public List<Task> getTaskList(Long id, String name, Integer taskType, Integer status, Long createTime) {
        return taskMapper.getTaskList(id, name, taskType, status, createTime);
    }
}
