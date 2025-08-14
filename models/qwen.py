from modelscope import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch

class QwenVLModel:
    def __init__(self, model_path, use_flash_attention=False, min_pixels=None, max_pixels=None):
        """
        初始化Qwen2.5-VL模型
        
        Args:
            model_path (str): 模型路径
            use_flash_attention (bool): 是否使用flash attention加速
            min_pixels (int): 最小像素数
            max_pixels (int): 最大像素数
        """
        self.model_path = model_path
        self.use_flash_attention = use_flash_attention
        self.min_pixels = min_pixels
        self.max_pixels = max_pixels
        
        # 初始化模型和处理器
        self._initialize_model()
        self._initialize_processor()
    
    def _initialize_model(self):
        """初始化模型"""
        if self.use_flash_attention:
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.model_path,
                torch_dtype=torch.bfloat16,
                attn_implementation="flash_attention_2",
                device_map="auto"
            )
        else:
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.model_path,
                torch_dtype="auto",
                device_map="auto"
            )
    
    def _initialize_processor(self):
        """初始化处理器"""
        if self.min_pixels is not None and self.max_pixels is not None:
            self.processor = AutoProcessor.from_pretrained(
                self.model_path,
                min_pixels=self.min_pixels,
                max_pixels=self.max_pixels
            )
        else:
            self.processor = AutoProcessor.from_pretrained(self.model_path)
    
    def generate_response(self, system_prompt, user_input, max_new_tokens=1024):
        """
        生成模型响应
        
        Args:
            system_prompt (str): 系统提示词
            user_input (str): 用户输入
            max_new_tokens (int): 最大生成token数
            
        Returns:
            str: 模型生成的响应文本
        """
        # 构造消息
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": system_prompt}],
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": user_input}],
            }
        ]
        
        # 准备输入
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")
        
        # 生成响应
        generated_ids = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=False
        )
        
        return output_text[0] if output_text else ""


# 使用示例
if __name__ == "__main__":
    # 初始化模型
    model_path = "/root/autodl-tmp/Qwen/Qwen2.5-VL-7B-Instruct"
    vl_model = QwenVLModel(model_path)
    
    # 系统提示词
    system_prompt = """你是一位专注于走秀模特脸部描述生成的专家，能够从正向和负向两个角度，根据用户输入精准输出详细且专业的模特脸部描述，以助力走秀模特脸部图像生成。
                        当用户给出最初输入后，深入分析输入信息，从模特的脸部特征（如脸型、五官特点、发型、发色等）、气质风格（优雅、酷帅、甜美等）等多维度生成正向且专业的模特脸部描述。
                        确保描述具有足够的细节，能够清晰地勾勒出令人赞赏的模特脸部形象，便于后续图像生成。
                        同样基于用户输入，从上述相同的多维度角度，生成负向且专业的模特脸部描述。
                        描述需包含具体不足细节，清晰呈现出有缺陷的模特脸部形象，以满足不同需求的图像生成。
                        只围绕生成走秀模特的正向和负向脸部描述进行输出，拒绝回答与走秀模特脸部描述无关的话题。
                        描述内容需全面且有条理，涵盖上述提到的多维度信息。
                        输出语言需简洁明了，避免过于复杂的表述。
                        如需获取外部信息，使用搜索引擎工具搜索相关内容，确保信息准确，并在输出中用 Markdown 的 ^^ 形式说明引用来源。 """  # 这里放入完整的系统提示
    
    # 用户输入
    user_input = "一位金发欧洲女模特在巴黎时装秀上走秀"
    
    # 生成响应
    response = vl_model.generate_response(system_prompt, user_input)
    print(response)