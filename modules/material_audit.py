import pytesseract
from PIL import Image
import pandas as pd
import io
from typing import Dict, Any

class MaterialAuditor:
    def __init__(self):
        # 如需本地部署OCR，需安装Tesseract
        pass

    async def process_image(self, file) -> Dict[str, Any]:
        # 读取图片
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # OCR识别
        text = pytesseract.image_to_string(image, lang="chi_sim+eng")

        # 结构化数据提取（简化模板匹配）
        structured_data = self.extract_structured_data(text)

        return {"text": text, "data": structured_data}

    def extract_structured_data(self, text: str) -> Dict:
        data = {}
        # 示例模板匹配：提取关键信息
        if "批次号" in text:
            data["batch_no"] = text.split("批次号")[-1].split("\n")[0].strip()
        if "数量" in text:
            data["quantity"] = text.split("数量")[-1].split("\n")[0].strip()
        if "日期" in text:
            data["date"] = text.split("日期")[-1].split("\n")[0].strip()
        return data