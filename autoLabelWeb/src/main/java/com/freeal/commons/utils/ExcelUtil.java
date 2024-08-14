package com.freeal.commons.utils;
import com.freeal.pojo.ManualEntity;
import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;

import java.util.List;

public class ExcelUtil {
    public static Workbook exportExcel(List<ManualEntity> melist) throws Exception {
        //可选择模板是.xls格式还是.xlsx格式
        HSSFWorkbook workbook = new HSSFWorkbook();
        //创建一个sheet表，可设置多个sheet
        Sheet sheet = workbook.createSheet("sheet1");
        sheet.setColumnWidth(0, 6000);
        sheet.setColumnWidth(1, 6000);
        sheet.setColumnWidth(2, 6000);

        String[] tableHeader = new String[]{"工号", "姓名", "职位"};
        HSSFRow firstRow = (HSSFRow) sheet.createRow((short) 0);
        for (int i = 0; i < tableHeader.length; i++) {
            HSSFCell cell = firstRow.createCell((short) i);
            cell.setCellStyle(workbook.createCellStyle());
            cell.setCellValue(tableHeader[i]);
        }

        int rowNum = 1;
        for (ManualEntity me : melist) {
            HSSFRow row = (HSSFRow) sheet.createRow(rowNum++);
            for (int i = 0; i < 8; i++) {
                HSSFCell cell = row.createCell(i);
                if (i == 0)
                    cell.setCellValue(me.getId());
                else if (i == 1)
                    cell.setCellValue(me.getData());
                else if (i == 2)
                    cell.setCellValue(me.getLlmLabel());
                else if (i == 3)
                    cell.setCellValue(me.getSlmLabel());
                else if (i == 4)
                    cell.setCellValue(me.getManualLabel());
                else if (i == 5)
                    cell.setCellValue(me.getLoss());
                else if (i == 6)
                    cell.setCellValue(me.getRepresentation());
                else if (i == 7)
                    cell.setCellValue(me.getConfidence());
            }
        }

        return workbook;
    }
}
