package com.freeal.mapper;

import com.freeal.pojo.Task;
import org.apache.ibatis.annotations.*;

import java.util.List;


@Mapper
public interface TaskMapper {
    void createTask(Task task);

    // 通过taskId更新表数据
    @Update("UPDATE TB_YXM_TASK SET " +
            "name = #{name}, " +
            "epoch = #{epoch}, " +
            "input_data_url = #{inputDataUrl}, " +
            "output_data_url = #{outputDataUrl}, " +
            "llm_id = #{llmId}, " +
            "slm_id = #{slmId}, " +
            "remark = #{remark}, " +
            "threshold = #{threshold}, " +
            "status = #{status}, " +
            "update_time = #{updateTime} " +
            "WHERE id = #{id}")
    void updateTask(Task task);

    Task getTaskById(@Param("taskId") Long id);

    List<Task> getTaskList(
            @Param("id") Long id,
            @Param("name") String name,
            @Param("taskType") Integer taskType,
            @Param("status") Integer status,
            @Param("createTime") Long createTime
    );

    void updateStatusById(@Param("taskId") Long taskId, @Param("status") Integer status,
                          @Param("updateTime") Long updateTime);
}
