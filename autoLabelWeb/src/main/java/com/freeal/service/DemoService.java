package com.freeal.service;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.pojo.Task;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public interface DemoService {
    /**
     * demo版本向模型端发送请求开始标注任务(last)
     *
     * @return 请求的结果
     */
    HttpResponseEntity createTaskLast(Task task);

    // 调度llm进入Refinery模式
    HttpResponseEntity llmRefinery(Long taskId);

    // 调度slm进入Refinery模式
    HttpResponseEntity slmRefinery(Long taskId);

    /**
     * demo版本向模型端发送请求查看SLM进度
     *
     * @param taskId     任务ID
     * @param isRefinery 是否是精炼阶段
     * @return 对应模型的进度
     */
    HttpResponseEntity checkSlmProgress(Long taskId, Boolean isRefinery);

    /**
     * demo版本向模型端发送请求查看LLM进度
     *
     * @param taskId     任务ID
     * @param isRefinery 是否是精炼阶段
     * @return 对应模型标注进度
     */
    HttpResponseEntity checkLlmProgress(Long taskId, Boolean isRefinery);

    /**
     * demo版本请求llm标注详细情况接口
     *
     * @param taskId 任务的ID
     * @param page  请求第几页
     * @param size  请求一页的数据大小
     * @return 查询信息
     * @throws Exception
     */
    HttpResponseEntity checkLlmLabelFormDemo(Long taskId, int page, int size);

    /**
     * demo版调度slm筛选
     *
     * @param taskId 任务的ID
     * @return 调度结果
     */
    HttpResponseEntity startSlm(Long taskId);

    /**
     * 查看SLM筛选结果
     * @param isRefinery 是否为精炼阶段
     * @param page 页数
     * @param size 大小
     * @param sort 是否按照推荐的排序展示数据
     * @return 查看SLM筛选结果数据
     */
    HttpResponseEntity checkSlmResultForm(Boolean isRefinery, int page, int size, Boolean sort);

    // 下载标注好的文件
    ResponseEntity<InputStreamResource> requestLabelResult();

    // 请求饼图数据
    HttpResponseEntity requestPieMapDataDemo();
}
