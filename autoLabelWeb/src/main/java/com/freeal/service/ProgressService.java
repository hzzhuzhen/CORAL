package com.freeal.service;

import com.freeal.entity.HttpResponseEntity;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Service;

@Service
public interface ProgressService {
    //Progress queryProgress(Progress progress);

    /**
     * 查询对应任务ID的任务信息接口
     * @param taskId 任务ID
     * @return 返回一个Http响应实体，成功查询到数据返回200请求码和对应的任务信息数据
     */
    HttpResponseEntity selectProgressByTaskId(@Param("taskId") Long taskId);
}
