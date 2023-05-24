from colorama import Fore

from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.config.prompt_config import PromptConfig
from autogpt.llm import ApiManager
from autogpt.logs import logger
from autogpt.prompts.generator import PromptGenerator
from autogpt.setup import prompt_user
from autogpt.utils import clean_input

CFG = Config()

DEFAULT_TRIGGERING_PROMPT = (
    "Determine which next command to use, and respond using the format specified above:"
)


def build_default_prompt_generator() -> PromptGenerator:
    """
    This function generates a prompt string that includes various constraints,
        commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Initialize the PromptConfig object and load the file set in the main config (default: prompts_settings.yaml)
    prompt_config = PromptConfig(CFG.prompt_settings_file)

    # Add constraints to the PromptGenerator object
    for constraint in prompt_config.constraints:
        prompt_generator.add_constraint(constraint)

    # Add resources to the PromptGenerator object
    for resource in prompt_config.resources:
        prompt_generator.add_resource(resource)

    # Add performance evaluations to the PromptGenerator object
    for performance_evaluation in prompt_config.performance_evaluations:
        prompt_generator.add_performance_evaluation(performance_evaluation)

    return prompt_generator


def construct_main_ai_config() -> AIConfig:
    """Construct the prompt for the AI to respond to

    Returns:
        str: The prompt string
    """
    config = AIConfig.load(CFG.ai_settings_file)
    if CFG.skip_reprompt and config.ai_name:
        logger.typewriter_log("名称 :", Fore.GREEN, config.ai_name)
        logger.typewriter_log("职责 :", Fore.GREEN, config.ai_role)
        logger.typewriter_log("目标:", Fore.GREEN, f"{config.ai_goals}")
        logger.typewriter_log(
            "API预算:",
            Fore.GREEN,
            "无限" if config.api_budget <= 0 else f"${config.api_budget}",
        )
    elif config.ai_name:
        logger.typewriter_log(
            "欢迎回来! ",
            Fore.GREEN,
            f"你想让 {config.ai_name} 继续执行原来的任务吗?",
            speak_text=True,
        )
        should_continue = clean_input(
            f"""继续上次的这些设置?
名称:  {config.ai_name}
角色:  {config.ai_role}
目标: {config.ai_goals}
API预算: {"无限" if config.api_budget <= 0 else f"${config.api_budget}"}
继续 ({CFG.authorise_key}/{CFG.exit_key}): """
        )
        if should_continue.lower() == CFG.exit_key:
            config = AIConfig()

    if not config.ai_name:
        config = prompt_user()
        config.save(CFG.ai_settings_file)

    if CFG.restrict_to_workspace:
        logger.typewriter_log(
            "注意：此代理创建的所有文件/目录都可以在其工作区内找到：",
            Fore.YELLOW,
            f"{CFG.workspace_path}",
        )
    # set the total api budget
    api_manager = ApiManager()
    api_manager.set_total_budget(config.api_budget)

    # Agent Created, print message
    logger.typewriter_log(
        config.ai_name,
        Fore.LIGHTBLUE_EX,
        "已创建并包含以下详细信息：",
        speak_text=True,
    )

    # Print the ai config details
    # Name
    logger.typewriter_log("名称:", Fore.GREEN, config.ai_name, speak_text=False)
    # Role
    logger.typewriter_log("角色:", Fore.GREEN, config.ai_role, speak_text=False)
    # Goals
    logger.typewriter_log("目标:", Fore.GREEN, "", speak_text=False)
    for goal in config.ai_goals:
        logger.typewriter_log("-", Fore.GREEN, goal, speak_text=False)

    return config
