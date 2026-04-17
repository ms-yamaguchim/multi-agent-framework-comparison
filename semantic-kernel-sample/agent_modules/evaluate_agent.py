#agent_modules.evaluate_agent.py
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent

class EvaluateAgent:
    def __init__(self, chat_completion_service, prompt, kernel, plugins=[]):
        self.kernel = kernel
    
        self.agent = ChatCompletionAgent(
            service=chat_completion_service,
            kernel=kernel,
            name="EvaluateAgent",
            instructions=prompt,
            plugins=plugins,
        )


def set_evaluate_agent(chat_completion_service,prompt,plugin=[]):
    evaluate_kernel = Kernel()  
    agent = EvaluateAgent(chat_completion_service, prompt,evaluate_kernel,plugin) 
    return agent