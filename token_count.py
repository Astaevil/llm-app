import tiktoken

def count_token(text: str, model="gpt-3.5-turbo") -> int:
    """统计文本token数量，等价网页tokenizer"""
    enc = tiktoken.encoding_for_model(model)
    token_list = enc.encode(text)
    return len(token_list), token_list


if __name__ == "__main__":
    # 示例文本，可以替换成你的prompt模板、问题
    test_text = """请你扮演助手，当需要查询天气时调用天气工具，需要计算时调用计算器。
用户问题：上海和北京哪个热"""

    cnt, tokens = count_token(test_text)
    print(f"文本：\n{test_text}")
    print(f"\ntoken总数：{cnt}")
    print(f"token id列表（对应网页上拆分的token）：{tokens[:20]}……")
