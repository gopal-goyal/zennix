from typer import Typer, Option, secho, colors
from zennix.modules.readme import ZennixReadme
app = Typer()

@app.command()
def readme(
    path: str = Option(".", help="Path to your project"),
    model: str = Option("llama3-8b-8192", help="Groq model to use")
):
    """Generate a README.md"""
    zr = ZennixReadme(project_path=path, model=model)
    zr.create_readme()
    secho("✅ README.md generated!", fg=colors.GREEN, bold=True)