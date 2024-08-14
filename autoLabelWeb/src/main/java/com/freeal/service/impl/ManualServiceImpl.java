package com.freeal.service.impl;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.mapper.ManualEntityMapper;
import com.freeal.modelapi.ManualOperationSender;
import com.freeal.pojo.ManualEntity;
import com.freeal.pojo.QueryEntity;
import com.freeal.pojo.SkipEntity;
import com.freeal.pojo.ManualLabel;
import com.freeal.service.ManualService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ManualServiceImpl implements ManualService {
    @Autowired
    private ManualEntityMapper manualEntityMapper;

    public List<ManualEntity> queryManual(ManualEntity manualEntity) {
        List<ManualEntity> res = manualEntityMapper.queryManual(manualEntity);
        return res;
    }

    public HttpResponseEntity submit(List<ManualEntity> melist) {
        HttpResponseEntity httpResponseEntity = new HttpResponseEntity();
        try {
            System.out.println("接口/manual/labeling/correcting/submit：接收到请求");
            for (ManualEntity manualEntity : melist) {
                if (manualEntity.getInputDataUrl() == null) {
                    manualEntity.setInputDataUrl("");
                }
                if (manualEntity.getOutputDataUrl() == null) {
                    manualEntity.setOutputDataUrl("");
                }
                System.out.println(manualEntity);
            }
            httpResponseEntity.setCode(200);
            httpResponseEntity.setMessage("提交成功");
            //for (ManualEntity manualEntity : melist) {
            //    int tmp = manualEntityMapper.submit(manualEntity);
            //    if (tmp == 0) {
            //        httpResponseEntity.setCode("200");
            //        httpResponseEntity.setMessage("提交成功");
            //    } else {
            //        httpResponseEntity.setCode("405");
            //        httpResponseEntity.setMessage("提交失败");
            //    }
            //}
        } catch (Exception e) {
            httpResponseEntity.setCode(400);
            httpResponseEntity.setMessage("提交失败");
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        return httpResponseEntity;
    }

    public int skip(SkipEntity skipEntity) {
        int res = manualEntityMapper.skip(skipEntity);
        return res;
    }

    public List<ManualEntity> queryCertain(QueryEntity queryEntity) {
        List<ManualEntity> res = manualEntityMapper.queryCertain(queryEntity);
        return res;
    }

    public List<ManualEntity> querySeq(QueryEntity queryEntity) {
        List<ManualEntity> res = manualEntityMapper.querySeq(queryEntity);
        return res;
    }

    @Override
    public HttpResponseEntity saveManualLabel(ManualLabel manualLabel) {
        return ManualOperationSender.sendManualCorrectingLabel(manualLabel);
    }

    @Override
    public HttpResponseEntity updateManualLabel() {
        try {
            return ManualOperationSender.updateManualCorrectingLabel();
        } catch (Exception e) {
            return ResponseResultUtil.error("Manual Label update err");
        }
    }
}
