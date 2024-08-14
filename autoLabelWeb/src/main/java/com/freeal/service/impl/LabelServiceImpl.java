package com.freeal.service.impl;

import com.freeal.mapper.LabelMapper;
import com.freeal.pojo.InitLabel;
import com.freeal.service.LabelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Service
public class LabelServiceImpl implements LabelService {
    @Autowired
    private LabelMapper labelMapper;

    @Override
    @Transactional
    public void createLabel(List<InitLabel> initLabelList) {

        for (InitLabel initLabel : initLabelList) {

            //当前年月日转long
            LocalDate currentDate = LocalDate.now();
            int year = currentDate.getYear();
            int month = currentDate.getMonthValue();
            int day = currentDate.getDayOfMonth();
            long ymd = (year * 10000L + month * 100L + day); //将年月日按顺序连接成长整型数字

            initLabel.setCreateTime(ymd);
            initLabel.setUpdateTime(ymd);
            initLabel.setInputDataUrl("C:/Users/19115/Desktop/upload");
            labelMapper.createLabel(initLabel);
        }


    }
}
