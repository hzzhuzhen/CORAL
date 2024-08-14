package com.freeal.controller;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.commons.utils.MockDataOpt;
import com.freeal.pojo.TaskInfo;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.pojo.Task;
import com.freeal.service.InfoService;
import com.freeal.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 任务管理
 */
@RestController
@RequestMapping("/task")
public class TaskController {
    @Autowired
    private TaskService taskService;
    @Autowired
    private InfoService infoService;
    //    接口5

    // 新增任务
    @PostMapping("/upset")
    public HttpResponseEntity createTask(@RequestBody Task task) {
        try {
            // 添加一些错误判断逻辑
            if (task == null) {
                return ResponseResultUtil.error("Task cannot be null.");
            }

            task = MockDataOpt.mockTaskConfigurationData(task);
            // 调用服务创建任务

            taskService.createTask(task);
            System.out.println("打印：" + task);
            System.out.println("打印：" + task);
            return ResponseResultUtil.success(task.getId());
        } catch (Exception e) {
            // 捕获异常，处理错误情况
            e.printStackTrace();
            return ResponseResultUtil.error("An unexpected error occurred.");
        }
    }

    /**
     * 通过前端的任务ID返回任务对应的基本信息
     *
     * @param taskId 任务id
     * @return 返回对应的基本信息
     */
    @GetMapping("/basicInfo")
    @CrossOrigin
    public HttpResponseEntity getBasicInfoById(@RequestParam Long taskId) {
        return infoService.getBasicTaskInformationById(taskId);
    }

    //更新任务 荒废
    @PutMapping("/upset")
    public HttpResponseEntity updateTask(@RequestBody Task task) {
        taskService.updateTask(task);
        return ResponseResultUtil.success("true");
    }

    @GetMapping("/list")
    public HttpResponseEntity getTaskList(@RequestParam(required = false) Long id,
                              @RequestParam(required = false) String name,
                              @RequestParam(required = false) Integer taskType,
                              @RequestParam(required = false) Integer status,
                              @RequestParam(required = false) Long createTime
    ) {
        // 调用 Service 层进行任务列表查询
        List<Task> tasks = taskService.getTaskList(id, name, taskType, status, createTime);
        return ResponseResultUtil.success(tasks);
    }


    @CrossOrigin
    @RequestMapping(value = "/info", method = RequestMethod.POST, headers = "Accept=application/json")
    public HttpResponseEntity trackingPanel(@RequestBody TaskInfo taskInfo) {
        HttpResponseEntity httpResponseEntity = new HttpResponseEntity();
        try {
            TaskInfo ie = infoService.queryInfo(taskInfo);
            if (ie == null) {
                httpResponseEntity.setCode(0);
                httpResponseEntity.setData(null);
                httpResponseEntity.setMessage("没有此ID对应的任务！");
            } else {
                httpResponseEntity.setCode(200);
                httpResponseEntity.setData(ie);
                httpResponseEntity.setMessage("已查询到任务");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        return httpResponseEntity;
    }
}
