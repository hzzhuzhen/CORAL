package com.freeal.mapper;

import com.freeal.pojo.Llm;
import com.freeal.pojo.Slm;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface ModelMapper {

    //根据任务类型查询大小模型
    @Select("SELECT * FROM TB_YXM_LLM " +
            "WHERE task_type = #{taskType} ")
    List<Llm> getLlmList(int taskType);

    @Select("SELECT * FROM TB_YXM_SLM " +
            "WHERE task_type = #{taskType} ")
    List<Slm> getSlmList(int taskType);

}
