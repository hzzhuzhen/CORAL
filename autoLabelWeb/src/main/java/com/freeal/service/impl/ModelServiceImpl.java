package com.freeal.service.impl;

import com.freeal.mapper.ModelMapper;
import com.freeal.pojo.Llm;
import com.freeal.pojo.Slm;
import com.freeal.service.ModelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ModelServiceImpl implements ModelService {

    @Autowired
    private ModelMapper modelMapper;
    @Override
    public List<Llm> getLlmList(int taskType) {
        return modelMapper.getLlmList(taskType);
    }

    @Override
    public List<Slm> getSlmList(int taskType) {
        return modelMapper.getSlmList(taskType);
    }
}
