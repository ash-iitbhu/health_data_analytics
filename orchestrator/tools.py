from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import tool
from data_generator.runtime_loader import loader
from logger import get_logger

logger = get_logger(__name__)


#Initialize REPL with the dataframes injected into the global scope
repl = PythonREPL()


# expose dataset loader
repl.locals["load_dataset"] = loader.load_dataset
        
@tool
def python_repl_tool(code: str):
    """
    Executes Python code. 
    Available DataFrames can be loaded using load_dataset(table_name) function available.

        Examples:
        - load_dataset(df_lifestyle_genetics)
        - load_dataset(df_physical_activity)

    Access standard libraries: pandas, numpy, scipy, statsmodels.
    Always PRINT the final result.
    """
    code_snippet = code.replace('\n', ' ')[:100] 
    logger.info(f"Executing code in sandbox: {code_snippet}...")

    try:

        result = repl.run(code)
        logger.info("Code execution successful.")
        return f"""
            --- Executed Python Code ---
            {code}

            --- Execution Output ---
            {result}
            """
    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}")
        return f"""
            --- Executed Python Code ---
            {code}

            --- Error ---
            {str(e)}
            """