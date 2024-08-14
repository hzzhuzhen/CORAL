package com.freeal.service.impl;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.mapper.ProgressMapper;
import com.freeal.pojo.Epoch;
import com.freeal.service.ProgressService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ProgressServiceImpl implements ProgressService {
    @Autowired
    private ProgressMapper progressMapper;

    //public Progress queryProgress(Progress progress) {
    //    Progress res = progressMapper.queryProgress(progress);
    //    Progress res2 = progressMapper.queryProgress2(progress);
    //    res.setStatus(res2.getStatus());
    //    res.setEpoch(res2.getEpoch());
    //    return res;
    //}

    @Override
    public HttpResponseEntity selectProgressByTaskId(Long taskId) {
        HttpResponseEntity httpResponseEntity = new HttpResponseEntity();
        try {
            Epoch epoch = progressMapper.selectProgressByTaskId(taskId);
            if (epoch == null) {
                httpResponseEntity.setCode(400);
                httpResponseEntity.setMessage("未找到任务");
                return httpResponseEntity;
            }
            httpResponseEntity.setData(epoch);
        } catch (Exception e) {
            e.printStackTrace();
            httpResponseEntity.setCode(400);
            httpResponseEntity.setMessage("请求查询错误");
            return httpResponseEntity;
        }
        httpResponseEntity.setCode(200);
        httpResponseEntity.setMessage("找到对应的任务信息");
        // 模拟模型训练epoch增加
        progressMapper.updateCurrentEpoch(taskId);
        return httpResponseEntity;
    }
}
