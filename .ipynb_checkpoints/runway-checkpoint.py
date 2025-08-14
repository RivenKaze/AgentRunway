import requests
import json
from models.qwen import QwenVLModel

model_path = "/root/autodl-tmp/Qwen/Qwen2.5-VL-7B-Instruct"
vl_model = QwenVLModel(model_path)

system_prompt_1 = """你是一位专注于走秀模特脸部描述生成的专家，能够从正向和负向两个角度，根据用户输入精准输出详细且专业的模特脸部描述，以助力走秀模特脸部图像生成。当用户给出最初输入后，深入分析输入信息，从模特的脸部特征（如脸型、五官特点、发型、发色等）、气质风格（优雅、酷帅、甜美等）等多维度生成正向且专业的模特脸部描述。确保描述具有足够的细节，能够清晰地勾勒出令人赞赏的模特脸部形象，便于后续图像生成。同样基于用户输入，从上述相同的多维度角度，生成负向且专业的模特脸部描述。描述需包含具体不足细节，清晰呈现出有缺陷的模特脸部形象，以满足不同需求的图像生成。只围绕生成走秀模特的正向和负向脸部描述进行输出，拒绝回答与走秀模特脸部描述无关的话题。描述内容需全面且有条理，涵盖上述提到的多维度信息。输出语言需简洁明了，避免过于复杂的表述。如需获取外部信息，使用搜索引擎工具搜索相关内容，确保信息准确，并在输出中用 Markdown 的 ^^ 形式说明引用来源。 """

system_prompt_2 = """你是一位专业的视觉脚本扩展师，专注于时装走秀相关场景的图生视频提示词创作。你擅长将用于图像生成的提示词，特别是涉及模特和走秀的静态提示词，扩展为具有镜头运动、丰富动作变化、精确节奏控制的图生视频提示词。你能够精确的把握静态图像提示词中关于模特的核心元素，并将其巧妙的转化为栩栩如生的视频画面描述，让生成的视频具有自然时间感、丰富且细腻的动作过程、精妙的镜头语言与细节动态。接受用户输入的包含模特的静态图像提示词（中文）。为生成的视频画面描述添加时间/天气信息，如阳光明媚的早晨、彩霞满天的黄昏、细雨蒙蒙的下雨天等。融入细致的镜头语言，例如“镜头从右侧以极慢的速度缓缓推进，聚焦在模特身上”，“画面从背后轻柔的跟拍那位模特，捕捉她每一个细微的动作”等。详细设计模特的持续性动作，比如“模特迈着悠闲的步伐，左摇右摆的走向舞台的前方”，“模特两手叉腰，抬起头自信的微笑向观众致意，随后转身退场”等。细腻体现环境动态变化，像“闪耀的灯光洒落在舞台上”。精心营造氛围节奏感，例如营造出人声鼎沸的走秀现场、优雅的现场气氛。全文需不少于5段提示词，每段描述一幅连续画面，构成完整的走秀现场片段。将以上元素整合统一为不少于5段自然语言风格的视频画面描述句，适合AI视频生成系统直接使用，不添加标签、编号解释或选项，保持描述细腻、真实、生动，有强烈的画面节奏感。输出内容必须严格按照上述要求生成，确保包含所有规定元素，尤其是对模特动作的详细描写。描述要保持自然语言风格，符合正常表达习惯。生成的视频画面描述需要符合逻辑并且具有连贯性，特别需要保持模特动作的连贯性与合理性。"""

system_prompt_3 = """你是一位专业的走秀时尚顾问，精通走秀服装的设计理念与潮流趋势，擅长依据用户给出的提示词精心设计走秀服装。能够从专业时尚视角出发，为用户生成契合要求的衣服设计方案，并针对设计给出积极的肯定以及具有建设性的改进建议。当用户输入提示词时，精准剖析提示词中的关键元素，如风格、颜色、材质等具体要求。 凭借对时尚和走秀服装的深厚专业理解，生成一套完备的衣服设计方案，涵盖款式、版型、色彩搭配、材质选用等详尽描述。描述时仅聚焦衣服本身，不涉及模特相关内容。针对生成的衣服设计，从时尚感、创新性、舞台表现力、受众吸引力等多个专业维度，给出至少三条正面提示，清晰阐述该设计的优势与亮点。同样从专业时尚领域出发，综合考虑走秀场景、市场接受度、制作难度等方面因素，对生成的衣服设计提出至少两条负面提示，准确指出可能存在的缺陷或有待改进之处。只围绕根据提示词生成走秀衣服设计以及给出相关提示展开交流，拒绝回应与走秀衣服设计无关的话题。所输出的内容必须条理清晰，分别明确阐述衣服设计方案、正面提示和负面提示，不能偏离框架要求。 """

print("用户输入:")
user_input = input()

response_1 = vl_model.generate_response(system_prompt_1, user_input)
print("人像提示词返回:\n")
print(response_1)
print('\n')

response_2 = vl_model.generate_response(system_prompt_2, user_input)
print("分镜提示词返回:\n")
parts = response_2.split('\n\n')
print(parts)
print('\n')

response_3 = vl_model.generate_response(system_prompt_3, user_input)
print("服装提示词返回:\n")
print(response_3)
print('\n')

# API URL
url = 'https://api.coze.cn/v1/workflow/run'
 
# Headers
headers = {
    'Authorization': 'Bearer pat_bdVgMIeib37gvbyxHzlKzloZj4ooqWZL9Z62SFy0JMZJziWVpweXsy1A4OeEM5kM',  # 替换为真实的token
    'Content-Type': 'application/json'
}
 
# 请求数据
data = {
    "workflow_id": "7537982459381350400",  # 替换为实际的workflow_id
    "parameters": {   # 你的工作流的输入
        "input": response_1
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data))
data = response.json()['data']
data_ = json.loads(data)
print("人像生成结果:\n")
print(data_['output'])
print('\n')

data = {
    "workflow_id": "7538294241539047478",  # 替换为实际的workflow_id
    "parameters": {   # 你的工作流的输入
        "input": response_3
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data))
cloth = response.json()['data']
cloth_ = json.loads(cloth)
print("服装生成结果:\n")
print(cloth_['output'])
print('\n')

cnt = 1 
links = []
for text in parts :
    data = {
        "workflow_id": "7529767104511361065",  # 替换为实际的workflow_id
        "parameters": {   # 你的工作流的输入
            "input": text,
            "model_image":data_['output'],
            "cloth_image":cloth_['output']
        }
    }
    print("第{}分镜提示词:{}\n生成结果:".format(cnt,text))
    response = requests.post(url, headers=headers, data=json.dumps(data))
    part = response.json()['data']
    part_ = json.loads(part)
    print(part_['data'])
    links.append(part_['data'])
    print('\n')
    cnt = cnt + 1

for i in range(len(links)-1):
    data = {
        "workflow_id": "7538288140738838563",  # 替换为实际的workflow_id
        "parameters": {   # 你的工作流的输入
            "input": parts[i],
            "image_1":links[i],
            "image_2":links[i+1]
        }
    }
    print("第{}分镜生成结果:".format(i+1))
    response = requests.post(url, headers=headers, data=json.dumps(data))
    part = response.json()['data']
    part_ = json.loads(part)
    print(part_['output'])
    print('\n')
    