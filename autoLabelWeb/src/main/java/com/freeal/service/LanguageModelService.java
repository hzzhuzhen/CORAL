package com.freeal.service;

import org.springframework.stereotype.Service;

@Service
public interface LanguageModelService {
    void startLlm(Long taskId, Boolean isRefinery);
}
