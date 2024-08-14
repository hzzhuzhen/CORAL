package com.freeal.modelapi;

import com.freeal.configs.LanguageModelConfig;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;

/**
 * 文件上传
 */
public class DataFileFacade {
    private static final RestTemplate restTemplate = new RestTemplate();

    /**
     * 传到算法服务器
     *
     * @param filePath
     * @throws IOException
     */
    public static void uploadInputData2ModelServer(String filePath) throws IOException {
        try {
            //String targetUrl = LanguageModelConfig.MODEL_API_HOST + "/llm"; // 目标服务器URL
            String targetUrl = "http://localhost:5000" + "/llm";
            //filePath = "data/test/test.csv"; // 本地文件路径

            uploadFile(targetUrl, filePath, String.valueOf(9));

//            Task task = new Task();
//            TaskService taskService = new TaskServiceImpl();
//            if(taskService.createTask(task)){
//                Long taskId = task.getId();
//                uploadFile(targetUrl, filePath, String.valueOf(taskId));
//            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void uploadFile(String targetUrl, String filePath, String taskId) throws IOException {
        String boundary = Long.toHexString(System.currentTimeMillis()); // 随机边界
        String CRLF = "\r\n"; // 换行符
        String postParam = "{\"taskId\": \"" + taskId + "\"}";
        URL url = new URL(targetUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setDoOutput(true);
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
        //connection.setRequestProperty("Content-Type", "application/json");

        File file = new File(filePath);
        String fileName = file.getName();

        try (
                OutputStream output = connection.getOutputStream();
                PrintWriter writer = new PrintWriter(new OutputStreamWriter(output, "UTF-8"), true);
        ) {
            // 发送 taskId 参数
            output.write(("--" + boundary + CRLF).getBytes());
            output.write(("Content-Disposition: form-data; name=\"taskId\"" + CRLF).getBytes());
            output.write(("Content-Type: text/plain; charset=UTF-8" + CRLF).getBytes());
            output.write(CRLF.getBytes());
            output.write(taskId.getBytes(StandardCharsets.UTF_8));
            output.write(CRLF.getBytes());
            // output.write((CRLF + taskId + CRLF).getBytes());

            // 发送文件数据
            output.write(("--" + boundary + CRLF).getBytes());
            output.write(("Content-Disposition: form-data; name=\"file\"; filename=\"" + fileName + "\"" + CRLF).getBytes());
            output.write(("Content-Type: " + Files.probeContentType(file.toPath()) + CRLF).getBytes());
            output.write(CRLF.getBytes());

            Files.copy(file.toPath(), output);
            output.write(CRLF.getBytes());

            output.write(("--" + boundary + "--" + CRLF).getBytes());
        }

        //try (
        //        OutputStream output = connection.getOutputStream();
        //        PrintWriter writer = new PrintWriter(new OutputStreamWriter(output, "UTF-8"), true);
        //) {
        //    // 发送文件数据
        //    File file = new File(filePath);
        //    writer.append("--" + boundary).append(CRLF);
        //    writer.append("Content-Disposition: form-data; name=\"file\"; filename=\"" + file.getName() + "\"")
        //    .append(CRLF);
        //    writer.append("Content-Type: " + URLConnection.guessContentTypeFromName(file.getName())).append(CRLF);
        //    //writer.append("Content-Type: text/csv").append(CRLF);
        //    writer.append(CRLF).flush();
        //
        //    Files.copy(file.toPath(), output);
        //    output.flush(); // 确保文件数据发送完毕
        //
        //    writer.append(CRLF).flush(); // 结束行
        //    writer.append("--" + boundary + "--").append(CRLF);
        //}

//        try (OutputStream os = connection.getOutputStream()) {
//            byte[] input = postParam.getBytes(StandardCharsets.UTF_8);
//            os.write(input, 0, input.length);
//        }
        int responseCode = connection.getResponseCode();
        System.out.println("Response Code: " + responseCode);
        connection.disconnect();
    }

    // demo版本下载标注结果文件
    public static ResponseEntity<InputStreamResource> downloadFileDemo() {
        ResponseEntity<byte[]> response = restTemplate.exchange(LanguageModelConfig.DOWNLOAD_FILE_DEMO_URI,
                HttpMethod.GET, HttpEntity.EMPTY, byte[].class);

        byte[] csvData = response.getBody();
        InputStream inputStream = new ByteArrayInputStream(csvData);
        InputStreamResource resource = new InputStreamResource(inputStream);

        HttpHeaders headers = new HttpHeaders();
        headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=label_result.csv");
        headers.add(HttpHeaders.CONTENT_TYPE, MediaType.TEXT_PLAIN_VALUE);

        return ResponseEntity.ok()
                .headers(headers)
                .contentLength(csvData.length)
                .contentType(MediaType.parseMediaType("application/octet-stream"))
                .body(resource);
    }

    public static void main(String[] args) {
        try {
            //String targetUrl = LanguageModelConfig.MODEL_API_HOST + "/llm"; // 目标服务器URL
            String targetUrl = "http://localhost:5000" + "/llm"; // 目标服务器URL
            String filePath = "data/test.csv"; // 本地文件路径
            uploadFile(targetUrl, filePath, "9");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
