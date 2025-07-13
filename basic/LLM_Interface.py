from openai import OpenAI

class KIMI:
    name = 'moonshot-v1-8k'
    key = 'sk-kCfNhTO4J8R3u7UBaHJ6bVA5FFtqRRiAttb0Y8K0zgxL05A7' 
    client = OpenAI(api_key = key, base_url = "https://api.moonshot.cn/v1")
    def get_answer(request: str):
        completion = KIMI.client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages = [
                {"role": "assistant", "content": request}
            ],
            temperature = 0.3
        )
        
        return completion.choices[0].message.content

class DeepSeek_R1:
    name = 'deepseek-chat'
    key = 'sk-26457ad2982f41cb9172891f6a41effa'
    client = OpenAI(api_key = key, base_url = "https://api.deepseek.com")
    def get_answer(request: str):
        completion = DeepSeek_R1.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "assistant", "content": request}
            ],
            temperature = 0.3,
        )
        
        return completion.choices[0].message.content

