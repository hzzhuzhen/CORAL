package com.freeal.controller;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.pojo.ManualLabel;
import com.freeal.pojo.Task;
import com.freeal.service.DemoService;
import com.freeal.service.ManualService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * demo演示版本流程接口
 */
@RestController
@RequestMapping("/demo")
@Slf4j
@CrossOrigin
public class DemoController {
    @Autowired
    private DemoService demoService;
    @Autowired
    private ManualService manualService;

    // 提交任务请求
    @GetMapping("/task/upset")
    public HttpResponseEntity startLlm() {
        // -------------设置Demo版本基础任务表(固定)-------------
        Task task = new Task();
        task.setName("mr");
        task.setOwnerId(0L);
        task.setEpoch(25);
        task.setInputDataUrl("default");
        task.setOutputDataUrl("default");
        task.setLlmId(1L);
        task.setSlmId(2L);
        task.setRemark("This is a demo task");
        task.setThreshold(10L);
        task.setStatus(1);
        // ---------------------------------------------------
        log.info("/task/upset接口响应请求创建Demo版本llm任务");
        return demoService.createTaskLast(task);
        //return demoService.createTask(task);
    }

    // 查看LLM进度请求
    @GetMapping("/progress/llm/check")
    public HttpResponseEntity checkLlmProgress(@RequestParam Long taskId,
                                               @RequestParam(defaultValue = "false") Boolean isRefinery) {
        log.info(String.format("/progress/llm/check接口响应请求查询LLM的进度(taskId=%d)", taskId));
        if (taskId == null || taskId <= 0) {
            log.warn("/progress/llm/check/form接口taskId异常");
            return ResponseResultUtil.error("taskId cannot be null");
        }
        return demoService.checkLlmProgress(taskId, isRefinery);
    }

    // 查看LLM标注情况请求
    @GetMapping("/progress/llm/check/form")
    public HttpResponseEntity checkLlmLabelForm(@RequestParam Long taskId,
                                                @RequestParam(defaultValue = "1") int page,
                                                @RequestParam(defaultValue = "10") int size) {
        if (taskId == null || taskId <= 0) {
            log.warn("/demo/progress/llm/check/form接口taskId异常");
            return ResponseResultUtil.error("taskId error");
        }
        log.info(String.format("/demo/progress/llm/check/form接口响应请求查询LLM标注结果(taskId=%d,page=%d,size=%d)", taskId, page, size));
        return demoService.checkLlmLabelFormDemo(taskId, page, size);
    }

    // 进行LLM精炼请求
    @GetMapping("/llm/refinery")
    public HttpResponseEntity llmRefineryDemo(@RequestParam Long taskId) {
        log.info(String.format("/demo/llm/refinery接口响应请求查询LLM精炼阶段(taskId=%d)", taskId));
        if (taskId == null || taskId <= 0) {
            log.warn("/demo/llm/refinery接口taskId异常");
            return ResponseResultUtil.error("taskId cannot be null");
        }
        return demoService.llmRefinery(taskId);
    }

    // 启动SLM筛选请求
    @GetMapping("/slm")
    public HttpResponseEntity startSlm(@RequestParam Long taskId) {
        log.info(String.format("/demo/slm接口响应请求启动SLM筛选(taskId=%d)", taskId));
        if (taskId == null || taskId <= 0) {
            log.warn("/demo/slm接口taskId异常");
            return ResponseResultUtil.error("taskId cannot be null");
        }
        return demoService.startSlm(taskId);
    }

    // 启动SLM筛选精炼阶段请求
    @GetMapping("/slm/refinery")
    public HttpResponseEntity slmRefineryDemo(@RequestParam Long taskId) {
        log.info(String.format("/demo/slm/refinery接口响应请求查询LLM精炼阶段(taskId=%d)", taskId));
        if (taskId == null || taskId <= 0) {
            log.warn("/demo/slm/refinery接口taskId异常");
            return ResponseResultUtil.error("taskId cannot be null");
        }
        return demoService.slmRefinery(taskId);
    }

    // 查看SLM进度请求
    @GetMapping("/progress/slm/check")
    public HttpResponseEntity checkSlmProgress(@RequestParam Long taskId,
                                               @RequestParam(defaultValue = "false") Boolean isRefinery) {
        log.info(String.format("/demo/progress/slm/check接口响应请求查询SLM进度(taskId=%d)", taskId));
        if (taskId == null || taskId <= 0) {
            log.warn("/progress/slm/check接口taskId异常");
            return ResponseResultUtil.error("taskId cannot be null");
        }
        return demoService.checkSlmProgress(taskId, isRefinery);
    }

    // 检测SLM筛选结果请求
    @GetMapping("/progress/slm/check/form")
    public HttpResponseEntity checkSlmResultForm(@RequestParam Long taskId,
                                                 @RequestParam(defaultValue = "false") Boolean isRefinery,
                                                 @RequestParam(defaultValue = "1") int page,
                                                 @RequestParam(defaultValue = "10") int size,
                                                 @RequestParam(defaultValue = "false") Boolean sort) {
        if (taskId == null || taskId <= 0) {
            log.warn("/demo/progress/slm/check/form接口taskId异常");
            return ResponseResultUtil.error("taskId cannot be null");
        }
        if (isRefinery) {
            log.info(String.format("/demo/progress/slm/check/form接口响应请求查询查询SLM精炼结果(taskId=%d,page=%d,size=%d)", taskId, page, size));
        } else {
            log.info(String.format("/demo/progress/slm/check/form接口响应请求查询查询SLM首次训练结果(taskId=%d,page=%d,size=%d)", taskId, page, size));
        }
        return demoService.checkSlmResultForm(isRefinery, page, size, sort);
    }

    // 存储用户的标注数据
    @PostMapping("/manual/label/save")
    public HttpResponseEntity saveManualLabel(@RequestBody ManualLabel manualLabel) {
        log.info("/demo/manual/label/correct接口收到人工标注数据: " + manualLabel.toString());
        return manualService.saveManualLabel(manualLabel);
    }

    // 更新用户的标注数据
    @GetMapping("/manual/label/update")
    public HttpResponseEntity updateManualLabel() {
        log.info("/demo/manual/label/update接口收到请求更新模型端的人工标注数据");
        return manualService.updateManualLabel();
    }

    // 下载模型标注的数据
    @GetMapping("/down/result")
    public ResponseEntity<InputStreamResource> downLabelResult() {
        return demoService.requestLabelResult();
    }

    @GetMapping("/map/pie")
    public HttpResponseEntity getPieMapData() {
        log.info("/demo/map/pie接口收到请求获取饼图数据");
        return demoService.requestPieMapDataDemo();
    }
}
