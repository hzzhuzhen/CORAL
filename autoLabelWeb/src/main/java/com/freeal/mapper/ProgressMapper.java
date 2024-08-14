package com.freeal.mapper;

import com.freeal.pojo.Epoch;
import com.freeal.pojo.Progress;
import com.freeal.pojo.Task;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

@Repository
@Component
@Mapper
public interface ProgressMapper {
    // 根据任务ID查询当前训练的Epoch和总的Epoch
    Epoch selectProgressByTaskId(@Param("taskId") Long taskId);

    // 测试使用，模拟后端模型训练Epoch
    void updateCurrentEpoch(@Param("taskId") Long taskId);

    // 任务提交后插入初始的数据到跟踪表中
    void insertProgress(Progress progress);

    // 通过TaskId查询当前跟踪表中对应的信息
    Progress selectProgressInfoByTaskId(@Param("taskId") Long taskId);

    void updateProgress(Progress progress);

    // 通过taskId修改endTime
    void updateEndTimeById(@Param("taskId") Long taskId, @Param("endTime") Long endTime,
                           @Param("updateTime") Long updateTime);

}
