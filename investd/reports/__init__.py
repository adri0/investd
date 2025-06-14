import os
from datetime import datetime
from pathlib import Path

os.environ["JUPYTER_PLATFORM_DIRS"] = "1"

import jupytext
from nbconvert.exporters import HTMLExporter, export
from nbconvert.preprocessors import ExecutePreprocessor

from investd import config
from investd.exceptions import NoTransactionsError
from investd.transaction import load_transactions


def generate_report(notebook_name: str) -> Path:
    path_notebook = Path(__file__).parent / f"{notebook_name}.py"
    _assert_transactions()
    notebook = jupytext.read(path_notebook)
    preprocessor = ExecutePreprocessor(timeout=10, kernel_name="python3")
    nb_executed, _ = preprocessor.preprocess(
        notebook, {"metadata": {"path": str(Path.cwd())}}
    )
    output, _ = export(
        HTMLExporter,
        nb_executed,
        config={
            "TemplateExporter": {
                "exclude_output_prompt": True,
                "exclude_input": True,
                "exclude_input_prompt": True,
            }
        },
    )
    report_path = _save_report(name=notebook_name, content=output)
    return report_path


def _save_report(name: str, content: str) -> Path:
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"{name}_{today}_{config.INVESTD_REF_CURRENCY}.html"
    report_path = config.INVESTD_REPORTS / filename
    report_path.parent.mkdir(exist_ok=True, parents=True)
    with report_path.open("w") as out_file:
        out_file.write(content)
    return report_path


def _assert_transactions() -> None:
    df_tx = load_transactions()
    if df_tx.empty:
        raise NoTransactionsError()
