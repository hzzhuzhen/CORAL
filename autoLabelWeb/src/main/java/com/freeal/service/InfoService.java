package com.freeal.service;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.pojo.TaskInfo;

public interface InfoService {
    TaskInfo queryInfo(TaskInfo taskInfo);

    /**
     * 通过任务ID返回用户填写的任务的基本信息接口
     *
     * @param id 任务ID
     * @return http请求实体类，如果查询成功返回成功的请求码和该任务对应的基本信息
     */
    HttpResponseEntity getBasicTaskInformationById(Long id);
}
