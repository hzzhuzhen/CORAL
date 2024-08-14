package com.freeal.service;

import com.freeal.pojo.Llm;
import com.freeal.pojo.Slm;

import java.util.List;

public interface ModelService {
    List<Llm> getLlmList(int taskType);

    List<Slm> getSlmList(int taskType);
}
