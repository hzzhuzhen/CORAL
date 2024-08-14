package com.freeal.mapper;

import com.freeal.pojo.Prompt;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface PromptMapper {
    @Select("SELECT * FROM TB_YXM_TASK_PROMPT " +
            "WHERE task_id = #{taskId} " +
            "AND task_type = #{taskType} " +
            "AND prompt_type = #{promptType}")
    List<Prompt> getPromptList(Long taskId, Integer taskType, Integer promptType);

    //保存大模型提示设置
    @Insert("INSERT INTO TB_YXM_TASK_PROMPT " +
            "(name, task_id, task_type, prompt_type, " +
            "content, create_time, update_time) " +
            "VALUES (#{name}, #{taskId}, #{taskType}, #{promptType}, " +
            "#{content}, #{createTime}, #{updateTime})")
    void createPrompt(Prompt prompt);
}
