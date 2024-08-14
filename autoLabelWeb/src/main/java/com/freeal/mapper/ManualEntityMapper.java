package com.freeal.mapper;

import com.freeal.pojo.ManualEntity;
import com.freeal.pojo.QueryEntity;
import com.freeal.pojo.SkipEntity;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
@Component
@Mapper
public interface ManualEntityMapper {
    List<ManualEntity> queryManual(ManualEntity manualEntity);

    int submit(ManualEntity manualEntity);

    int skip(SkipEntity skipEntity);

    List<ManualEntity> queryCertain(QueryEntity queryEntity);

    List<ManualEntity> querySeq(QueryEntity queryEntity);
}
