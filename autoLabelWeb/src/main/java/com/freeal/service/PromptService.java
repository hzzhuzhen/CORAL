package com.freeal.service;

import com.freeal.pojo.Prompt;

import java.util.List;

public interface PromptService {
    List<Prompt> getPromptList(Long taskId, Integer taskType, Integer promptType);

    void createPrompt(List<Prompt> prompt);

}
