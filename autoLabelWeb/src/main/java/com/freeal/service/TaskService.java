package com.freeal.service;

import com.freeal.pojo.Task;

import java.util.List;

public interface TaskService {
    Boolean createTask(Task task);

    void updateTask(Task task);

    Task getTaskById(Long id);

    List<Task> getTaskList(Long id, String name, Integer taskType, Integer status, Long createTime);
}

