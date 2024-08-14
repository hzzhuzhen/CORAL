package com.freeal.mapper;

import com.freeal.pojo.TaskInfo;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;
import org.apache.ibatis.annotations.Mapper;
@Repository
@Component
@Mapper
public interface TaskInfoMapper {
    TaskInfo queryInfo(TaskInfo taskInfo);
}
