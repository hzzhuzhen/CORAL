package com.freeal.modelapi;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.configs.LanguageModelConfig;
import com.freeal.enums.LanguageModelEnum;
import com.freeal.commons.utils.RequestUtil;
import com.freeal.pojo.LanguageModelFetchForm;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

import java.util.ArrayList;
import java.util.List;

/**
 * 发送模型端请求过程跟踪类
 */
public class ModelProgressInfoFetcher {
    private static final List<LanguageModelFetchForm> testData = new ArrayList<>();

    static {
        testData.add(new LanguageModelFetchForm(1023L, "Our goal is the sea of stars.", "negative", "positive", 30L,
                0.7F));
        testData.add(new LanguageModelFetchForm(1022L, "Our goal is the sea of stars.", "negative", "positive", 2031L
                , 0.7F));
        testData.add(new LanguageModelFetchForm(1132L, "People in the northeast are all li", "positive", "positive",
                27L, 0.07F));
        testData.add(new LanguageModelFetchForm(1425L, "ok goal very the sea of stars.", "negative", "positive",
                2032L, 0.03F));
        testData.add(new LanguageModelFetchForm(1612L, "Our goal is iss sea of stars.", "positive", "positive", 9003L
                , 0.01F));
        testData.add(new LanguageModelFetchForm(1611L, "Our goal is iss sea of stars.", "positive", "positive", 8125L
                , 0.01F));
    }

    // 获取小模型筛选的状态信息
    public static List<LanguageModelFetchForm> requestSlmStatus() {
        // todo 模型端接口写完后这里同步改动
        String targetUrl = LanguageModelConfig.MODEL_API_HOST + "/";

        // 目前返回固定数据测试前后端联调
        return testData;
    }

    /**
     * demo版本请求模型进展情况信息接口
     *
     * @param languageModel 想要查找的对应模型枚举类
     * @param isRefinery    是否在精炼阶段
     * @return 请求结果和模型进展
     */
    public static HttpResponseEntity requestModelProgressDemo(LanguageModelEnum languageModel, Boolean isRefinery) {
        String url = languageModel == LanguageModelEnum.LLM ?
                LanguageModelConfig.REQUEST_LLM_PROGRESS_DEMO_URI : LanguageModelConfig.REQUEST_SLM_PROGRESS_DEMO_URI;
        MultiValueMap<String, String> queryParams = new LinkedMultiValueMap<>();
        queryParams.add("isRefinery", String.valueOf(isRefinery));
        return RequestUtil.getRequest(url, queryParams);
    }

    /**
     * demo版本请求llm标注详细情况接口
     *
     * @param taskId 任务的ID
     * @param page   请求第几页
     * @param size   请求一页的数据大小
     * @return 查询信息
     */
    public static HttpResponseEntity requestLlmLabelFormDemo(Long taskId, int page, int size) {
        MultiValueMap<String, String> queryParams = new LinkedMultiValueMap<>();
        queryParams.add("taskId", String.valueOf(taskId));
        queryParams.add("page", String.valueOf(page));
        queryParams.add("size", String.valueOf(size));
        return RequestUtil.getRequest(LanguageModelConfig.REQUEST_LLM_LABEL_FORM_DEMO_URI,
                queryParams);
    }

    /**
     * 发送请求查看SLM筛选结果
     *
     * @param isRefinery 是否为精炼阶段
     * @param page       页数
     * @param size       大小
     * @param sort       是否按照推荐的排序展示数据
     * @return 查看SLM筛选结果数据
     */
    public static HttpResponseEntity requestSlmResultFormDemo(Boolean isRefinery, int page, int size, Boolean sort) throws Exception {
        MultiValueMap<String, String> queryParams = new LinkedMultiValueMap<>();
        queryParams.add("isRefinery", String.valueOf(isRefinery));
        queryParams.add("page", String.valueOf(page));
        queryParams.add("size", String.valueOf(size));
        queryParams.add("sort", String.valueOf(sort));
        return RequestUtil.getRequest(LanguageModelConfig.REQUEST_SLM_RESULT_FORM_DEMO_URI,
                queryParams);
    }

    // demo版本请求饼图数据
    public static HttpResponseEntity requestPieMapDataDemo() {
        return RequestUtil.getRequest(LanguageModelConfig.PIE_MAP_DATA_DEMO_URI);
    }

    public static void main(String[] args) throws Exception {
        //System.out.println(requestLlmLabelFormDemo(1L, 1, 50));
        //System.out.println(requestPieMapDataDemo());
        System.out.println(requestModelProgressDemo(LanguageModelEnum.SLM, false));
    }
}


