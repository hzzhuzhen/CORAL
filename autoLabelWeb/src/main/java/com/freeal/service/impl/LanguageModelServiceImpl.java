package com.freeal.service.impl;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.converter.HttpResponseEntityDataConverter;
import com.freeal.enums.LanguageModelEnum;
import com.freeal.enums.TaskStatusEnum;
import com.freeal.commons.utils.DataUtil;
import com.freeal.commons.utils.LanguageModelUtil;
import com.freeal.mapper.ProgressMapper;
import com.freeal.mapper.TaskMapper;
import com.freeal.modelapi.ModelProgressInfoFetcher;
import com.freeal.modelapi.ModelScheduler;
import com.freeal.pojo.LanguageModelRunningStatus;
import com.freeal.service.LanguageModelService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
@Slf4j
public class LanguageModelServiceImpl implements LanguageModelService {
    @Autowired
    private HttpResponseEntityDataConverter responseEntityDataConverter;
    @Autowired
    private TaskMapper taskMapper;
    @Autowired
    private ProgressMapper progressMapper;

    // todo 暂时废弃，待修改
    @Override
    @Async
    @Deprecated
    public void startLlm(Long taskId, Boolean isRefinery) {
        try {
            HttpResponseEntity modelResponse = ModelScheduler.invokeLlm(isRefinery);
            Integer taskStatus = TaskStatusEnum.IN_PROCESSING.getType();
            if (modelResponse.getCode() != 200) { // 远程请求LLM失败
                log.warn(String.format("(taskId=%d)llm调度失败llm端返回调度失败信息: %s",
                        taskId, modelResponse.getMessage()));
                // todo 数据库状态更改
                taskStatus = TaskStatusEnum.EXCEPTION_OCCUR.getType();
            }
            // 数据库状态更新
            taskMapper.updateStatusById(taskId, taskStatus, System.currentTimeMillis());
            // 开启LLM监控
            if (Objects.equals(taskStatus, TaskStatusEnum.IN_PROCESSING.getType())) {
                monitorLlmProgress(taskId, isRefinery);
            }
        } catch (Exception e) {
            //DataUtil.writeLanguageModelProgressData(new LanguageModelRunningStatus(-1, -1,
            //        LanguageModelUtil.ERROR_STATUS));
            log.error("发生异常", e);
        }
    }

    @Deprecated
    private void monitorLlmProgress(Long taskId, Boolean isRefinery) {
        try {
            String status = "";
            int errorTime = 0, maxErrorTime = 3;
            while (!LanguageModelUtil.isFinishStatus(status) && errorTime < maxErrorTime) {
                try {
                    // 减少请求的时间
                    Thread.sleep(3000);
                    // 请求查询大模型运行的状态
                    LanguageModelRunningStatus llmStatus = responseEntityDataConverter
                            .convert(ModelProgressInfoFetcher.requestModelProgressDemo(LanguageModelEnum.LLM, isRefinery),
                                    LanguageModelRunningStatus.class);
                    double rate = llmStatus.getCurrent() / llmStatus.getTotal().doubleValue() * 100;
                    log.info(String.format("taskId=%d请求到LLM状态完成%.2f%%(目前标注: %d条 总共：%d条)",
                            taskId, rate, llmStatus.getCurrent(), llmStatus.getTotal()));
                    status = llmStatus.getStatus();
                    // 往本地写运行状态数据
                    DataUtil.writeLanguageModelProgressData(llmStatus);
                    errorTime = 0;
                } catch (Exception e) {
                    errorTime++;
                    log.error("有异常发生: ", e);
                }
            }
            // 检测完提交数据到数据库
            long endTime = System.currentTimeMillis();
            progressMapper.updateEndTimeById(taskId, endTime, endTime);
            log.info(String.format("taskId=%d监测结束", taskId));
            taskMapper.updateStatusById(taskId, TaskStatusEnum.FINISH.getType(), System.currentTimeMillis());
        } catch (Exception e) {
            taskMapper.updateStatusById(taskId, TaskStatusEnum.EXCEPTION_OCCUR.getType(), System.currentTimeMillis());
            log.error(String.format("taskId=%d监测到异常", taskId), e);
        }
    }
}
