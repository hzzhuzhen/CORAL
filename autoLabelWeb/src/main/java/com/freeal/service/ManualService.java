package com.freeal.service;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.pojo.QueryEntity;
import com.freeal.pojo.SkipEntity;
import com.freeal.pojo.ManualEntity;
import com.freeal.pojo.ManualLabel;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface ManualService {
    List<ManualEntity> queryManual(ManualEntity manualEntity);

    /**
     * 接收到人工修改的数据并保存到数据库
     *
     * @param melist 修改过的所有数据(可以没有修改)
     * @return 保存结果的Http请求实体类
     */
    HttpResponseEntity submit(List<ManualEntity> melist);

    int skip(SkipEntity skipEntity);

    List<ManualEntity> queryCertain(QueryEntity queryEntity);

    List<ManualEntity> querySeq(QueryEntity queryEntity);

    /**
     * 将接收到的人工标注发送到模型端
     * @param manualLabel 收到的人工标注请求
     * @return 是否发送成功
     */
    HttpResponseEntity saveManualLabel(ManualLabel manualLabel);

    HttpResponseEntity updateManualLabel();
}
