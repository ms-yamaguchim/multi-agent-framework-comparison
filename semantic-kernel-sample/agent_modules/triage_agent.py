from semantic_kernel import Kernel  
from semantic_kernel.agents import ChatCompletionAgent  
from semantic_kernel.core_plugins import TimePlugin  
from semantic_kernel.core_plugins.conversation_summary_plugin import ConversationSummaryPlugin  
from semantic_kernel.prompt_template import PromptTemplateConfig  
from semantic_kernel.functions.kernel_function_decorator import kernel_function  

import random

#エージェントに持たせる機能
class LocationPlugin:  
    @kernel_function(  
        name="get_current_location",  
        description="現在地を回答します。"  
    )  
    def get_current_location(self) -> str:  
        print("get_current_location関数を利用")

        items = ["群馬県","栃木県","茨城県","埼玉県","東京都","神奈川県","千葉県"]
        return random.choice(items)


# エージェント定義クラス
class TriageAgent:  
    def __init__(self,chat_completion_service, prompt, kernel, plugins=[]):  
        self.kernel = kernel  
        self.agent = ChatCompletionAgent(  
        service=chat_completion_service,  
        kernel=kernel,  
        name="TriageAgent",  
        instructions=prompt,  
        plugins=plugins,  
    )  


def set_triage_agent(chat_completion_service, prompt, plugin=[]):  
    kernel = Kernel()  
    kernel.add_service(chat_completion_service)  
    kernel.add_plugin(TimePlugin(), plugin_name="Time")  
    kernel.add_plugin(  
        ConversationSummaryPlugin(prompt_template_config=PromptTemplateConfig()),  
        plugin_name="SummaryPlugin"  
    ) 

    kernel.add_plugin(LocationPlugin(),plugin_name="LocationPlugin")
    agent = TriageAgent(chat_completion_service, prompt, kernel, plugin)  
    return agent
