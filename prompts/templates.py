# prompts/templates.py
PROMPT_QA = """你是企业知识库问答助手。只根据「参考资料」回答，资料里没有就说「资料中未提及」。先给结论，再给一句理由，不超过 200 字。
参考资料：{context}
问题：{question}
回答："""

PROMPT_EXTRACT = """你是信息抽取助手。只输出 JSON，不要任何其他文字。
输出格式：{"company": "公司名", "amount": "金额", "date": "日期"}
文本：{text}
JSON："""

PROMPT_CLASSIFY = """把句子分类到「咨询/投诉/工单报障」三类之一，输出 {"category": "..."}。
咨询：询问信息；投诉：表达不满；工单报障：报告故障。
句子：{text}
分类："""
