package com.freeal.modelapi;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.configs.LanguageModelConfig;
import com.freeal.commons.utils.RequestUtil;

/**
 * 模型端任务调度接口类
 */
public class ModelScheduler {
    /**
     * 远程调用llm执行任务函数
     *
     * @param isRefinery 是否是Refinery阶段
     * @return 请求的结果
     */
    public static HttpResponseEntity invokeLlm(Boolean isRefinery) {
        String url = isRefinery ?
                LanguageModelConfig.LLM_REFINERY_DEMO_URI : LanguageModelConfig.INITIAL_LABEL_WITH_LLM_URI;
        return RequestUtil.getRequest(url);
    }

    /**
     * 远程调用SLM执行任务函数
     *
     * @param isRefinery 是否是Refinery阶段
     * @return 请求的结果
     */
    public static HttpResponseEntity invokeSlm(Boolean isRefinery) {
        String url = isRefinery ?
                LanguageModelConfig.SLM_REFINERY_URI : LanguageModelConfig.TRAIN_SLM_URI;
        return RequestUtil.getRequest(url);
    }
}
