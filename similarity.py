from sentence_transformers import SentenceTransformer, util

# 加载BGE中文向量模型
model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

# 前10条：知识库；后10条：用户问题
sentences = [
    # 知识库 0~9
    "公司年假为5天，入职满1年方可享受",
    "工作日上班时间是早上9点至下午18点，午休1小时",
    "加班可以兑换调休，调休有效期6个月",
    "每月15号发放上月工资，遇节假日提前发放",
    "出差住宿标准一线城市不超过400元/晚",
    "病假需要提供医院诊断证明，带薪病假每年3天",
    "员工内部报销提交后7个工作日内审核完成",
    "社保公积金每月按工资基数的规定比例缴纳",
    "年终奖根据年度绩效与公司营收核算，次年2月发放",
    "公司每月最后一周周五举办部门例会",
    # 用户问题 10~19
    "年假到底有几天？",
    "上下班几点？",
    "加班换来的调休多久内要用掉？",
    "每个月什么时候发工资？",
    "去上海出差一晚住宿费上限多少？",
    "带薪病假一年能休几天？",
    "报销多久能审核完？",
    "社保公积金什么时候交？",
    "年终奖一般几月份发？",
    "部门例会是什么时候？",
]

# 编码并归一化向量
emb = model.encode(sentences, normalize_embeddings=True)
# 计算20×20余弦相似度矩阵
sim = util.cos_sim(emb, emb)

# 遍历后面10个问题，匹配前面知识库
output_lines = []
for i in range(10, 20):
    scores = sim[i][:10]
    best_idx = scores.argmax()
    q = sentences[i]
    doc = sentences[best_idx]
    score = float(scores[best_idx])
    line = f"{q} → {doc} (相似度 {score:.3f})"
    print(line)
    output_lines.append(line)

# 写入笔记文件
with open("notes/w2-embedding.md", "w", encoding="utf-8") as f:
    f.write("# Embedding相似度匹配结果\n\n")
    f.write("\n".join(output_lines))
