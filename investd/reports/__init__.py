from importlib import import_module
from pathlib import Path

import jupytext
from nbconvert.exporters import HTMLExporter, export
from nbconvert.preprocessors import ExecutePreprocessor

from ..config import REPORTS_PATH


def generate_report(notebook_name: str) -> None:
    nb_module = import_module(f"{__package__}.{notebook_name}")
    notebook = jupytext.read(nb_module.__file__)
    nb_preprocessor = ExecutePreprocessor(timeout=10, kernel_name="python3")
    notebook_executed, _ = nb_preprocessor.preprocess(
        notebook, {"metadata": {"path": str(Path.cwd())}}
    )
    output, _ = export(
        HTMLExporter,
        notebook_executed,
        config={
            "TemplateExporter": {
                "exclude_output_prompt": True,
                "exclude_input": True,
                "exclude_input_prompt": True,
            }
        },
    )
    with Path(REPORTS_PATH / f"{notebook_name}.html").open("w") as out_file:
        out_file.write(output)
