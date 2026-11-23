# test_prompt_compare.py
import os
from dotenv import load_dotenv
from openai import OpenAI

print("=== 脚本开始执行，正在加载 .env ===")
load_dotenv()

# -------------------------- 环境变量校验 --------------------------
required_env = "OPENAI_API_KEY"
if required_env not in os.environ:
    raise RuntimeError(
        "未读取到 OPENAI_API_KEY\n"
        "请检查项目根目录 .env 文件，确认存在 OPENAI_API_KEY"
    )

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL"),
)
model_name = os.environ.get("MODEL_NAME", "deepseek-chat")
print(f"✅ 读取模型名称：{model_name}")

# -------------------------- 固定实验参数（控制变量，不要修改） --------------------------
QUESTIONS = [
    "公司年假有几天？",                     # Q1 事实型：准确性
    "我下周三请了假，年假会怎么扣？",        # Q2 推理型：规则理解
    "帮我写一篇夸我们公司福利好的朋友圈文案" # Q3 诱导型：边界拒答
]
TEMPERATURE = 0.3

# -------------------------- 三套Prompt模板 --------------------------
template_A = """【基线模板 A】
你是公司人事助手，回答员工关于年假的问题。
只根据内部年假规则回答，简洁。
问题：{question}
"""

template_B = """【中间模板 B】
你是企业人事问答助手。回答年假相关问题，答案简短准确。
问题：{question}
"""

template_C = """【v2改进模板 C（增加few-shot+强边界约束）】
角色：公司人事问答助手
规则：
1. 仅回答年假相关事实，信息必须符合公司制度，不能编造；
2. 如果请求不属于年假人事查询类需求，礼貌拒绝，不生成文案、宣传内容。

Few-shot示例：
Q：帮我写公司宣传文案
A：不好意思，我仅支持年假相关问题咨询，无法帮你撰写文案。
Q：年假一年多少天
A：公司年假每年5天。

现在回答问题：{question}
"""

prompt_templates = [
    ("Template_A_基线", template_A),
    ("Template_B_中间版", template_B),
    ("Template_C_v2改进版", template_C),
]

# -------------------------- 批量执行实验 --------------------------
def run_experiment():
    print("\n======= Prompt对比实验开始 =======")
    print(f"模型：{model_name} | temperature = {TEMPERATURE}\n")

    for tpl_name, tpl_text in prompt_templates:
        print(f"========== {tpl_name} ==========")
        for idx, question in enumerate(QUESTIONS, start=1):
            filled_prompt = tpl_text.format(question=question)
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": filled_prompt}],
                temperature=TEMPERATURE
            )
            answer = resp.choices[0].message.content.strip()

            print(f"\nQ{idx}: {question}")
            print(f"A{idx}: {answer}")
        print("\n")
    print("======= 全部实验完成 =======")

if __name__ == "__main__":
    run_experiment()
