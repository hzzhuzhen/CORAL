package com.freeal.controller;


import com.freeal.entity.HttpResponseEntity;
import com.freeal.enums.TaskStatusEnum;
import com.freeal.modelapi.ModelProgressInfoFetcher;
import com.freeal.pojo.Llm;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.pojo.Slm;
import com.freeal.service.ModelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.annotation.*;

import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;

/**
 * 大小模型管理
 */
@RestController
public class LanguageModelController {

    @Autowired
    private ModelService modelService;

    //查询模型
    @GetMapping("/llm/list")
    public HttpResponseEntity getLlmByType(int taskType) {
        List<Llm> llms= modelService.getLlmList(taskType);
        return ResponseResultUtil.success(llms);
    }

    @GetMapping("/slm/list")
    public HttpResponseEntity getSlmByType(int taskType) {
        List<Slm> slms= modelService.getSlmList(taskType);
        return ResponseResultUtil.success(slms);
    }

    // 查询slm模型标注结果
    @CrossOrigin
    @RequestMapping(value = "/slm/result")
    public HashMap<String, Object> displayModelStatus() {
        HashMap<String, Object> data = new HashMap<>();
        data.put("code", 200);
        data.put("status", TaskStatusEnum.FINISH.getType());
        data.put("filterResult", ModelProgressInfoFetcher.requestSlmStatus());
        return data;
    }

    @CrossOrigin
    @RequestMapping(value = "/llm/getData", method = RequestMethod.POST, headers = "Accept=application/json")
    public HttpResponseEntity getData() {
        HttpResponseEntity httpResponseEntity = new HttpResponseEntity();
        try {
            ClassPathResource resource = new ClassPathResource("merged_data.csv"); // 你的CSV文件路径
            byte[] fileData = StreamUtils.copyToByteArray(resource.getInputStream());
            String res = new String(fileData, StandardCharsets.UTF_8);
            System.out.println(res.substring(0, 500));
            if (res == null) {
                httpResponseEntity.setCode(0);
                httpResponseEntity.setData(null);
                httpResponseEntity.setMessage("没有此条件对应的任务！");
            } else {
                httpResponseEntity.setCode(200);
                httpResponseEntity.setData(res);
                httpResponseEntity.setMessage("已查询到任务");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        return httpResponseEntity;
    }
}
