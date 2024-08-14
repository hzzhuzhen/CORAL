package com.freeal.controller;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.service.ProgressService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 过程跟踪
 */
//接口18
@RestController
public class TaskProgressController {
    @Autowired
    private ProgressService progressService;

    /**
     * 接受前端轮询查看任务进度
     * @param taskId 任务id
     * @return 返回任务信息
     */
    @CrossOrigin
    @GetMapping("/task/progress/check")
    public HttpResponseEntity getProgress(@RequestParam Long taskId) {
        return progressService.selectProgressByTaskId(taskId);
    }


    /**
     * 开启训练
     * @param progressEntity
     * @return
     */
    /**
     * LLM标注
     * @param progressEntity
     * @return
     */

    /**
     * SLM标注
     * @param progressEntity
     * @return
     */

    /**
     * 模型状态检查
     * @param progressEntity
     * @return
     */
}
