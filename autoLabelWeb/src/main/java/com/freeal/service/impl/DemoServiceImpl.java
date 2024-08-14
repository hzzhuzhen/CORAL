package com.freeal.service.impl;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.converter.HttpResponseEntityDataConverter;
import com.freeal.enums.LanguageModelEnum;
import com.freeal.mapper.ProgressMapper;
import com.freeal.mapper.TaskMapper;
import com.freeal.modelapi.DataFileFacade;
import com.freeal.modelapi.ModelScheduler;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.modelapi.ModelProgressInfoFetcher;
import com.freeal.pojo.LanguageModelRunningStatus;
import com.freeal.pojo.Progress;
import com.freeal.pojo.Task;
import com.freeal.service.DemoService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.net.ConnectException;
import java.util.HashMap;

@Service
@Slf4j
public class DemoServiceImpl implements DemoService {
    @Autowired
    private TaskMapper taskMapper;
    @Autowired
    private ProgressMapper progressMapper;
    @Autowired
    private HttpResponseEntityDataConverter responseEntityDataConverter;

    @Override
    public HttpResponseEntity createTaskLast(Task task) {
        try {
            log.info(String.format("(taskId=%d)调度llm开始初始化标注", task.getId()));
            HttpResponseEntity modelResponse = ModelScheduler.invokeLlm(false);
            if (modelResponse.getCode() != 200) {
                log.warn(String.format("(taskId=%d)llm调度失败llm端返回调度失败信息: %s",
                        task.getId(), modelResponse.getMessage()));
                return modelResponse;
            }
            // 提交task表
            taskMapper.createTask(task);
            // 初始化progress表的一些数据
            Progress progress = new Progress();
            progress.setId(task.getId());
            progress.setCurrentModel(1);
            progress.setCurrentEpoch(0);
            progressMapper.insertProgress(progress);
            HashMap<String, Long> data = new HashMap<>();
            data.put("taskId", task.getId());
            log.info(String.format("(taskId=%d)调度llm成功,开始初始化标注", task.getId()));
            return ResponseResultUtil.success(data);
        }  catch (Exception e) {
            log.error("发生异常", e);
            return ResponseResultUtil.error("llm start error");
        }
    }

    @Override
    public HttpResponseEntity llmRefinery(Long taskId) {
        try {
            log.info("调度llm开始Refinery阶段");
            return ModelScheduler.invokeLlm(true);
        } catch (Exception e) {
            log.error("发生异常", e);
            return ResponseResultUtil.error("llm start error");
        }
    }

    @Override
    public HttpResponseEntity slmRefinery(Long taskId) {
        try {
            log.info("调度slm开始Refinery阶段");
            return ModelScheduler.invokeSlm(true);
        } catch (Exception e) {
            log.error("发生异常", e);
            return ResponseResultUtil.error("error");
        }
    }

    @Override
    public HttpResponseEntity checkSlmProgress(Long taskId, Boolean isRefinery) {
        try {
            return ModelProgressInfoFetcher.requestModelProgressDemo(LanguageModelEnum.SLM, isRefinery);
        } catch (Exception e) {
            log.error("发生异常", e);
            return ResponseResultUtil.error("llm status get error");
        }
    }

    @Override
    public HttpResponseEntity checkLlmProgress(Long taskId, Boolean isRefinery) {
        try {
            return ModelProgressInfoFetcher.requestModelProgressDemo(LanguageModelEnum.LLM, isRefinery);
        } catch (Exception e) {
            log.error("发生异常", e);
            return ResponseResultUtil.error("llm status get error");
        }
    }

    @Override
    public HttpResponseEntity checkLlmLabelFormDemo(Long taskId, int page, int size) {
        return ModelProgressInfoFetcher.requestLlmLabelFormDemo(taskId, page, size);
    }

    @Override
    public HttpResponseEntity startSlm(Long taskId) {
        try {
            // 请求查询大模型运行的状态
            LanguageModelRunningStatus llmStatus = responseEntityDataConverter
                    .convert(ModelProgressInfoFetcher.requestModelProgressDemo(LanguageModelEnum.LLM, false),
                            LanguageModelRunningStatus.class);
            if (!"finish".equals(llmStatus.getStatus())) {
                log.warn(String.format("taskId=%d llm未结束，不进行调度slm", taskId));
                return ResponseResultUtil.error("llm not finish");
            }
            // 调度小模型
            HttpResponseEntity invokeResponse = ModelScheduler.invokeSlm(false);
            if (invokeResponse.getCode() == 400) {
                log.warn(String.format("taskId=%d slm调度失败，失败原因: %s", taskId, invokeResponse.getMessage()));
            }
            return invokeResponse;
        } catch (Exception e) {
            log.error("发生异常", e);
            return ResponseResultUtil.error("error");
        }
    }

    @Override
    public HttpResponseEntity checkSlmResultForm(Boolean isRefinery, int page, int size, Boolean sort) {
        try {
            return ModelProgressInfoFetcher.requestSlmResultFormDemo(isRefinery, page, size, sort);
        } catch (ConnectException e) {
            log.error("发生异常", e);
            return ResponseResultUtil.error("connect to llm platform");
        } catch (Exception e) {
            log.error("发生异常", e);
            return ResponseResultUtil.error("error");
        }
    }

    @Override
    public ResponseEntity<InputStreamResource> requestLabelResult() {
        return DataFileFacade.downloadFileDemo();
    }

    @Override
    public HttpResponseEntity requestPieMapDataDemo() {
        return ModelProgressInfoFetcher.requestPieMapDataDemo();
    }
}