# W2 Prompt 实验记录
> 核心原则：固定测试用例不变，单次实验只修改1个变量，避免玄学调优。
> 固定用例：QA(3条)、信息抽取(3条)、意图分类(3条)
> 变量可选：Prompt文本 / temperature / JSON输出方式（手法1：prompt约束；手法2：response_format强制json）

## 基础信息
- 仓库commit版本：
- 实验时间：
- 改动说明：

### ✅ QA任务 PROMPT_QA
参数：temperature 默认
固定Case：
1. case1
context="公司年假每年5天，入职满1年方可享受"
question="入职半年可以休年假吗？"

2. case2
context="报销提交截止每月25号"
question="报销最晚什么时候提交"

3. case3
context="公司办公区在A栋3层"
question="公司班车路线有几条？"

| Case | 模型输出 | 评价（✅正常 / ❌幻觉/格式错误） | 备注 |
| ---- | ---- | ---- | ---- |
| case1 |  |  |  |
| case2 |  |  |  |
| case3 |  |  |  |

---

### ✅ 信息抽取 PROMPT_EXTRACT
参数：temperature=0.1
固定Case：
1. case1 text="2025年10月12日，甲公司付款12000元"
2. case2 text="乙公司合同金额50万，签订日期2025-03-01"
3. case3 text="今天和丙企业开会，暂未确定金额"

> 手法1：仅Prompt文字约束JSON
| Case | 模型输出JSON | 能否loads解析 | 评价 |
| ---- | ---- | ---- | ---- |
| case1 |  |  |  |
| case2 |  |  |  |
| case3 |  |  |  |

> 手法2：开启 response_format={"type":"json_object"}
| Case | 模型输出JSON | 能否loads解析 | 评价 |
| ---- | ---- | ---- | ---- |
| case1 |  |  |  |
| case2 |  |  |  |  |
| case3 |  |  |  |

---

### ✅ 意图分类 PROMPT_CLASSIFY
参数：temperature 默认
固定Case：
1. case1 text="请问怎么申请VPN权限"
2. case2 text="系统卡顿经常闪退，无法登录"
3. case3 text="客服回复太慢，服务体验很差"

> 手法1：仅Prompt文字约束JSON
| Case | 模型输出JSON | 能否loads解析 | 评价 |
| ---- | ---- | ---- | ---- |
| case1 |  |  |  |
| case2 |  |  |  |
| case3 |  |  |  |

> 手法2：开启 response_format={"type":"json_object"}
| Case | 模型输出JSON | 能否loads解析 | 评价 |
| ---- | ---- | ---- | ---- |
| case1 |  |  |  |
| case2 |  |  |  |
| case3 |  |  |  |

## 本次实验总结
- 两种JSON方案对比：
- Prompt存在问题：
- 后续优化方向：
