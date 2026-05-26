from typing import AsyncGenerator, List, Optional
from dashscope import Generation
from app.config import settings


class LLMService:
    """百炼 LLM service for chat generation with streaming."""

    async def generate_stream(
        self,
        system_prompt: str,
        messages: List[dict],
        temperature: float = 0.3,
    ) -> AsyncGenerator[str, None]:
        full_messages = [{"role": "system", "content": system_prompt}]
        full_messages.extend(messages)

        response = Generation.call(
            model=settings.llm_model,
            messages=full_messages,
            api_key=settings.dashscope_api_key,
            stream=True,
            temperature=temperature,
            result_format="message",
        )

        for event in response:
            if event.status_code == 200:
                choice = event.output.choices[0]
                if choice.finish_reason == "stop":
                    break
                delta = choice.message.get("content", "")
                if delta:
                    yield delta
            else:
                yield f"\n[Error: {event.code} - {event.message}]"
                break

    async def summarize(self, text: str) -> str:
        response = Generation.call(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": "用一段中文简短总结以下对话内容，保留关键事实和问题。"},
                {"role": "user", "content": text},
            ],
            api_key=settings.dashscope_api_key,
            result_format="message",
        )
        if response.status_code == 200:
            return response.output.choices[0].message["content"]
        return ""


class ImageDescriber:
    """Describe charts/images using Qwen-VL multimodal model."""

    @staticmethod
    def describe_image(image_bytes: bytes) -> str:
        import base64
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/png;base64,{image_b64}"

        response = Generation.call(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": "请描述这张图片中的图表内容，包括图表类型、标题、数据趋势和关键结论。如果是表格，列出表格内容。如果只是装饰图片，回复'非图表'。"
                        },
                        {"image": image_url},
                    ],
                }
            ],
            api_key=settings.dashscope_api_key,
            result_format="message",
        )
        if response.status_code == 200:
            return response.output.choices[0].message["content"]
        return ""
