package com.freeal.mapper;

import com.freeal.pojo.InitLabel;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface LabelMapper {

    @Insert("INSERT INTO TB_YXM_MANUAL_INIT_LABELING_RECOMMEND " +
            "(task_id, input_data_url, seq, data, " +
            "labeling, status, create_time, update_time) " +
            "VALUES (#{taskId}, #{inputDataUrl}, #{seq}, #{data}, " +
            "#{labeling}, #{status}, #{createTime}, #{updateTime})")
    void createLabel(InitLabel initLabel);
}
