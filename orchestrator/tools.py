from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import tool
from data_generator.data_loader import data_manager
from logger import get_logger

logger = get_logger(__name__)

# Initialize REPL with the dataframes injected into the global scope
repl = PythonREPL()
repl.locals["df_health"] = data_manager.df_health
repl.locals["df_activity"] = data_manager.df_activity

@tool
def python_repl_tool(code: str):
    """
    Executes Python code. 
    Use this to analyze `df_health` and `df_activity`.
    Access standard libraries: pandas, numpy, scipy, statsmodels.
    Always PRINT the final result.
    """
    code_snippet = code.replace('\n', ' ')[:100] 
    logger.info(f"Executing Python REPL: {code_snippet}...")

    try:
        result = repl.run(code)
        logger.info("Code execution successful.")
        return result
    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}")
        return f"Error executing code: {str(e)}"