from pathlib import Path

import jupytext
from nbconvert.exporters import HTMLExporter, export
from nbconvert.preprocessors import ExecutePreprocessor

from ..config import REPORTS_PATH


def generate_report(report_path: Path) -> None:
    notebook = jupytext.read(report_path)
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
    output_path = Path(REPORTS_PATH / report_path.with_suffix(".html").name)
    with output_path.open("w") as out_file:
        out_file.write(output)
