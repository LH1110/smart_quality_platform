from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from modules.knowledge_base import KnowledgeBase
from modules.material_audit import MaterialAuditor
from modules.dify_agent import DifyAgent
from modules.report_generator import ReportGenerator

app = FastAPI(title="智能生产质量管理与知识协作平台")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 初始化模块
kb = KnowledgeBase()
auditor = MaterialAuditor()
agent = DifyAgent()
reporter = ReportGenerator()

@app.get("/")
async def root():
    return FileResponse("static/index.html")

# 知识库接口
@app.post("/kb/add")
async def add_knowledge(file: UploadFile = File(...)):
    return await kb.add_document(file)

@app.get("/kb/query")
async def query_knowledge(q: str):
    return {"answer": kb.query(q)}

# AI材料审核（OCR+结构化）
@app.post("/audit/material")
async def audit_material(file: UploadFile = File(...)):
    result = await auditor.process_image(file)
    return {"ocr_text": result["text"], "structured_data": result["data"]}

# 智能体流程编排
@app.post("/agent/run")
async def run_agent(workflow: str = Form(...)):
    return {"result": agent.run_workflow(workflow)}

# AI智能报告生成
@app.post("/report/generate")
async def generate_report(data: str = Form(...)):
    report_path = reporter.generate(data)
    return {"report_path": report_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)