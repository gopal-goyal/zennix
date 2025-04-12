from typer import Typer, Option, secho, colors
from zennix.modules.readme import ZennixReadme
from zennix.utils import file_ops
app = Typer()

@app.command()
def readme(
    path: str = Option(".", help="Path to your project"),
    model: str = Option("llama3-8b-8192", help="Groq model to use")
):
    """Generate a README.md"""
    zr = ZennixReadme(project_path=path, model=model)
    readme_content = zr.create_readme()

    file_ops.save_file(readme_content, output_path="data/readme_files", filename="README.md") # Save the file

    secho("✅ README.md generated!", fg=colors.GREEN, bold=True)