package com.freeal.controller;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.pojo.InitLabel;
import com.freeal.commons.utils.ResponseResultUtil;
import com.freeal.service.LabelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 初始化标注
 */
@RestController
public class LabelController {

    @Autowired
    private LabelService labelService;

    //保存人工初始化标注
    @PostMapping("/manual/labeling/init/save")
    public HttpResponseEntity createLabel(@RequestBody List<InitLabel> initLabelList){
        labelService.createLabel(initLabelList);
        return ResponseResultUtil.success("true");
    }
}
