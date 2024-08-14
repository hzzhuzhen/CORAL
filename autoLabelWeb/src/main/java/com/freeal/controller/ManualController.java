package com.freeal.controller;

import com.freeal.entity.HttpResponseEntity;
import com.freeal.pojo.ManualEntity;
import com.freeal.pojo.QueryEntity;
import com.freeal.pojo.SkipEntity;
import com.freeal.service.ManualService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 人工标注
 */
@RestController
public class ManualController {
    private List<ManualEntity> plist;

    public List<ManualEntity> getPlist() {
        return plist;
    }

    public void setPlist(List<ManualEntity> plist) {
        this.plist = plist;
    }

    //接口23
    @Autowired
    private ManualService manualService;

    @CrossOrigin
    @RequestMapping(value = "/manual/labeling/correcting/recommend", method = RequestMethod.POST, headers = "Accept" +
            "=application/json")
    public HttpResponseEntity getManual(@RequestBody ManualEntity manualEntity) {
        HttpResponseEntity httpResponseEntity = new HttpResponseEntity();
        try {
            List<ManualEntity> melist = manualService.queryManual(manualEntity);
            if (melist == null) {
                setPlist(melist);
                httpResponseEntity.setCode(400);
                httpResponseEntity.setData(null);
                httpResponseEntity.setMessage("没有此ID对应的任务！");
            } else {
                httpResponseEntity.setCode(200);
                httpResponseEntity.setData(melist);
                httpResponseEntity.setMessage("已查询到任务");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        return httpResponseEntity;
    }

    //    接口24
    @CrossOrigin
    @PostMapping("/manual/labeling/correcting/submit")
    public HttpResponseEntity submit(@RequestBody List<ManualEntity> melist) {
        return manualService.submit(melist);
    }

    //    接口21
    @CrossOrigin
    @RequestMapping(value = "/task/stepOver", method = RequestMethod.POST, headers = "Accept=application/json")
    public HttpResponseEntity skip(@RequestBody SkipEntity skipEntity) {
        HttpResponseEntity httpResponseEntity = new HttpResponseEntity();
        try {
            int res = manualService.skip(skipEntity);
            if (res != 0) {
                httpResponseEntity.setCode(200);
                httpResponseEntity.setData(res);
                httpResponseEntity.setMessage("跳过成功！");

            } else {
                httpResponseEntity.setCode(400);
                httpResponseEntity.setData(res);
                httpResponseEntity.setMessage("跳过失败！");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        return httpResponseEntity;
    }

    //接口25
    @CrossOrigin
    @RequestMapping(value = "/task/labeling/search", method = RequestMethod.POST, headers = "Accept=application/json")
    public HttpResponseEntity querySeq(@RequestBody QueryEntity queryEntity) {
        HttpResponseEntity httpResponseEntity = new HttpResponseEntity();
        try {
            List<ManualEntity> res = null;
            if (queryEntity.getSeq() == -1) {
                res = manualService.querySeq(queryEntity);
            } else {
                res = manualService.queryCertain(queryEntity);
            }
            if (res == null) {
                httpResponseEntity.setCode(400);
                httpResponseEntity.setData(null);
                httpResponseEntity.setMessage("没有此条件对应的任务！");
            } else {
                httpResponseEntity.setCode(200);
                httpResponseEntity.setData(res);
                httpResponseEntity.setMessage("已查询到任务");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        return httpResponseEntity;
    }
}
