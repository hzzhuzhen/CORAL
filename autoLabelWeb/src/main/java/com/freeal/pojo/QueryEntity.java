package com.freeal.pojo;

public class QueryEntity {
    private int taskId;
    private String inputDataUrl;
    private String outputDataUrl;
    private int seq = -1;
    private int lseq = -1;
    private int rseq = -1;

    public int getTaskId() {
        return taskId;
    }

    public void setTaskId(int taskId) {
        this.taskId = taskId;
    }

    public String getInputDataUrl() {
        return inputDataUrl;
    }

    public void setInputDataUrl(String inputDataUrl) {
        this.inputDataUrl = inputDataUrl;
    }

    public String getOutputDataUrl() {
        return outputDataUrl;
    }

    public void setOutputDataUrl(String outputDataUrl) {
        this.outputDataUrl = outputDataUrl;
    }

    public int getSeq() {
        return seq;
    }

    public void setSeq(int seq) {
        this.seq = seq;
    }

    public int getLseq() {
        return lseq;
    }

    public void setLseq(int lseq) {
        this.lseq = lseq;
    }

    public int getRseq() {
        return rseq;
    }

    public void setRseq(int rseq) {
        this.rseq = rseq;
    }

}
