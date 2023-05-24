"""Set up the AI and its goals"""
import re

from colorama import Fore, Style
from jinja2 import Template

from autogpt import utils
from autogpt.config import Config
from autogpt.config.ai_config import AIConfig
from autogpt.llm import create_chat_completion
from autogpt.logs import logger
from autogpt.prompts.default_prompts import (
    DEFAULT_SYSTEM_PROMPT_AICONFIG_AUTOMATIC,
    DEFAULT_TASK_PROMPT_AICONFIG_AUTOMATIC,
    DEFAULT_USER_DESIRE_PROMPT,
)

CFG = Config()


def prompt_user() -> AIConfig:
    """Prompt the user for input

    Returns:
        AIConfig: The AIConfig object tailored to the user's input
    """
    ai_name = ""
    ai_config = None

    # Construct the prompt
    logger.typewriter_log(
        "欢迎来到 Auto-GPT! ",
        Fore.GREEN,
        "运行 '--help' 了解更多信息.",
        speak_text=True,
    )

    # Get user desire
    logger.typewriter_log(
        "创建一个 AI 助手:",
        Fore.GREEN,
        "输入 '--manual' 进入手动模式.",
        speak_text=True,
    )

    user_desire = utils.clean_input(
        f"{Fore.LIGHTBLUE_EX}我希望Auto-GPT{Style.RESET_ALL}: "
    )
    logger.typewriter_log(
        "收到您指派的任务:",
        Fore.GREEN,
        f"{user_desire}",
        speak_text=True,
    )
    if user_desire == "":
        user_desire = DEFAULT_USER_DESIRE_PROMPT  # Default prompt

    # If user desire contains "--manual"
    if "--manual" in user_desire:
        logger.typewriter_log(
            "选择手动模式",
            Fore.GREEN,
            speak_text=True,
        )
        return generate_aiconfig_manual()

    else:
        try:
            return generate_aiconfig_automatic(user_desire)
        except Exception as e:
            logger.typewriter_log(
                "无法根据用户需求自动生成AI Config.",
                Fore.RED,
                "回退到手动模式.",
                speak_text=True,
            )

            return generate_aiconfig_manual()


def generate_aiconfig_manual() -> AIConfig:
    """
    Interactively create an AI configuration by prompting the user to provide the name, role, and goals of the AI.

    This function guides the user through a series of prompts to collect the necessary information to create
    an AIConfig object. The user will be asked to provide a name and role for the AI, as well as up to five
    goals. If the user does not provide a value for any of the fields, default values will be used.

    Returns:
        AIConfig: An AIConfig object containing the user-defined or default AI name, role, and goals.
    """

    # Manual Setup Intro
    logger.typewriter_log(
        "创建一个 AI 助手:",
        Fore.GREEN,
        "不输入内容将加载默认助手.",
        speak_text=True,
    )

    # Get AI Name from User
    logger.typewriter_log(
        "为您的 AI 命名：",Fore.GREEN,"例如, 'Entrepreneur-GPT'"
    )
    ai_name = utils.clean_input("AI 机器人名称: ")
    if ai_name == "":
        ai_name = "Entrepreneur-GPT"

    logger.typewriter_log(
        f"{ai_name} 在这里!", Fore.LIGHTBLUE_EX, "我随时为您服务。", speak_text=True
    )

    # Get AI Role from User
    logger.typewriter_log(
        "描述您的 AI 的角色：",
        Fore.GREEN,
        "例如，'一种旨在自主开发和经营业务的人工智能，其唯一目标是增加你的净资产。"
    )
    ai_role = utils.clean_input(f"{ai_name} 的职责: ")
    if ai_role == "":
        ai_role = "一个旨在自主开发和经营企业以唯一目标增加你净值的人工智能"

    # Enter up to 5 goals for the AI
    logger.typewriter_log(
        "提示:输入最多5个要帮你实现的功能/目标 ",
        Fore.GREEN,
         "例如：\n增加公众号关注者、市场调研、自主开发网站等等")
    logger.info("输入空白以加载默认值，完成时不要输入任何内容.")
    ai_goals = []
    for i in range(5):
        ai_goal = utils.clean_input(f"{Fore.LIGHTBLUE_EX}Goal{Style.RESET_ALL} {i+1}: ")
        if ai_goal == "":
            break
        ai_goals.append(ai_goal)
    if not ai_goals:
        ai_goals = [
            "增加网络价值",
            "增加 Twitter 账户的关注者",
            "自主开发和管理多个业务",
        ]

    # Get API Budget from User
    logger.typewriter_log(
        "输入您的 API 调用预算：",
        Fore.GREEN,
        "例如：: $1.50（1.50 美元）",
    )
    logger.info("不输入任何内容让 AI 在没有金额限制的情况下运行")
    api_budget_input = utils.clean_input(
        f"{Fore.LIGHTBLUE_EX}预算{Style.RESET_ALL}: $"
    )
    if api_budget_input == "":
        api_budget = 0.0
    else:
        try:
            api_budget = float(api_budget_input.replace("$", ""))
        except ValueError:
            logger.typewriter_log(
                 "输入的预算无效。 将预算设置为无限制.", Fore.RED
            )
            api_budget = 0.0

    return AIConfig(ai_name, ai_role, ai_goals, api_budget)


def generate_aiconfig_automatic(user_prompt) -> AIConfig:
    """Generates an AIConfig object from the given string.

    Returns:
    AIConfig: The AIConfig object tailored to the user's input
    """

    system_prompt = DEFAULT_SYSTEM_PROMPT_AICONFIG_AUTOMATIC
    prompt_ai_config_automatic = Template(
        DEFAULT_TASK_PROMPT_AICONFIG_AUTOMATIC
    ).render(user_prompt=user_prompt)
    # Call LLM with the string as user input
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": prompt_ai_config_automatic,
        },
    ]
    output = create_chat_completion(messages, CFG.fast_llm_model)

    # Debug LLM Output
    logger.debug(f"AI Config Generator 原始输出: {output}")

    # Parse the output
    ai_name = re.search(r"Name(?:\s*):(?:\s*)(.*)", output, re.IGNORECASE).group(1)
    ai_role = (
        re.search(
            r"Description(?:\s*):(?:\s*)(.*?)(?:(?:\n)|Goals)",
            output,
            re.IGNORECASE | re.DOTALL,
        )
        .group(1)
        .strip()
    )
    ai_goals = re.findall(r"(?<=\n)-\s*(.*)", output)
    api_budget = 0.0  # TODO: parse api budget using a regular expression

    return AIConfig(ai_name, ai_role, ai_goals, api_budget)
