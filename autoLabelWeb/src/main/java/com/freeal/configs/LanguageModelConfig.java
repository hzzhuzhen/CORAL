package com.freeal.configs;

import org.springframework.core.io.ClassPathResource;
import org.springframework.util.xml.DomUtils;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;

// 模型端的配置类
public class LanguageModelConfig {
    // 目标服务器URL
    public static final String MODEL_API_HOST = "http://47.115.210.129:15001";
    //public static final String MODEL_API_HOST = "http://localhost:5000";
    public static final String USER_UPLOAD_DATA_TEMP_SAVE_DIR = "data/tmp";
    // demo版本请求调用slm第一次训练接口地址
    public static final String TRAIN_SLM_URI = LanguageModelConfig.MODEL_API_HOST + "/demo/slm";
    // demo版本请求slm开始Refinery接口地址
    public static final String SLM_REFINERY_URI = LanguageModelConfig.MODEL_API_HOST + "/demo/slm/refinery";
    // demo版本请求调用llm初始化标注接口地址
    public static final String INITIAL_LABEL_WITH_LLM_URI = LanguageModelConfig.MODEL_API_HOST + "/demo/llm";
    // demo版本请求llm开始Refinery接口地址
    public static final String LLM_REFINERY_DEMO_URI = LanguageModelConfig.MODEL_API_HOST + "/demo/llm/refinery";
    // demo版本请求llm进展情况信息接口地址
    public static final String REQUEST_LLM_PROGRESS_DEMO_URI = MODEL_API_HOST + "/demo/llm/check";
    // demo版本请求slm进展情况信息接口地址
    public static final String REQUEST_SLM_PROGRESS_DEMO_URI = MODEL_API_HOST + "/demo/slm/check";
    // demo版本请求llm标注详细情况接口地址
    public static final String REQUEST_LLM_LABEL_FORM_DEMO_URI = MODEL_API_HOST + "/demo/progress/llm/check/form";
    // demo版本请求slm筛选结果接口地址
    public static final String REQUEST_SLM_RESULT_FORM_DEMO_URI = MODEL_API_HOST + "/demo/progress/slm/check/form";
    // 存储用户的标注数据，防止标注丢失
    public static final String MANUAL_LABEL_SAVE_DEMO_URI = MODEL_API_HOST + "/demo/manual/label/save";
    // demo版本更新用户标注数据
    public static final String MANUAL_LABEL_UPDATE_DEMO_URI = MODEL_API_HOST + "/demo/manual/label/submit";
    // demo版本下载标注数据文件URI地址
    public static final String DOWNLOAD_FILE_DEMO_URI = MODEL_API_HOST + "/demo/down/result";
    // demo版本请求饼图数据
    public static final String PIE_MAP_DATA_DEMO_URI = MODEL_API_HOST + "/demo/map/pie";
    // id转大模型类别映射
    private static final HashMap<Long, String> idToLlmMap = new HashMap<>();
    // 大模型类别转id映射
    private static final HashMap<String, Long> llmToIdMap = new HashMap<>();
    // id转大模型类别映射
    private static final HashMap<Long, String> idToSlmMap = new HashMap<>();
    // 小模型类别转id映射
    private static final HashMap<String, Long> slmToIdMap = new HashMap<>();

    public static String getLlmById(Long id) {
        return idToLlmMap.get(id);
    }

    public static String getSlmById(Long id) {
        return idToSlmMap.get(id);
    }

    public static Long getIdByLlm(String id) {
        return llmToIdMap.get(id);
    }

    public static Long getIdBySlm(String id) {
        return slmToIdMap.get(id);
    }

    static {
        try {
            // 加载模型映射配置文件
            ClassPathResource resource = new ClassPathResource("language-model-map.xml");
            InputStream inputStream = resource.getInputStream();

            // 解析XML文件
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(inputStream);

            // 获取根元素
            Element root = doc.getDocumentElement();
            List<Element> modelElements = DomUtils.getChildElementsByTagName(root, "model");

            // 获取所有的llm和slm元素
            List<Element> llmElements = DomUtils.getChildElementsByTagName(root, "llm");
            List<Element> slmElements = DomUtils.getChildElementsByTagName(root, "slm");

            for (Element llmElement : llmElements) {
                Long id = null;
                String name = null;

                // 获取子元素
                List<Element> childElements = DomUtils.getChildElements(llmElement);
                for (Element childElement : childElements) {
                    String tagName = childElement.getTagName();
                    String value = childElement.getTextContent();

                    if (tagName.equals("id")) {
                        id = Long.parseLong(value);
                    } else if (tagName.equals("name")) {
                        name = value;
                    }

                    // 当获取到id和name时，存入对应的映射
                    if (id != null && name != null) {
                        idToLlmMap.put(id, name);
                        llmToIdMap.put(name, id);
                    }
                }
            }

            // 处理slm元素
            for (Element slmElement : slmElements) {
                Long id = null;
                String name = null;

                // 获取子元素
                List<Element> childElements = DomUtils.getChildElements(slmElement);
                for (Element childElement : childElements) {
                    String tagName = childElement.getTagName();
                    String value = childElement.getTextContent();

                    if (tagName.equals("id")) {
                        id = Long.parseLong(value);
                    } else if (tagName.equals("name")) {
                        name = value;
                    }

                    // 当获取到id和name时，存入对应的映射
                    if (id != null && name != null) {
                        idToSlmMap.put(id, name);
                        slmToIdMap.put(name, id);
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
