import click
from rich.console import Console
from rich.table import Table
from .scanner import scan_junk
from .cleaner import remove_junk
import os

console = Console()

@click.group()
def main():
    """macOS Junk Cleaner - Clean up macOS specific junk files."""
    pass

@main.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--recursive/--no-recursive', default=True, help="Scan subdirectories recursively.")
def scan(path, recursive):
    """Scan a directory for macOS junk files."""
    path = os.path.abspath(path)
    console.print(f"Scanning [bold cyan]{path}[/bold cyan]{' (recursively)' if recursive else ''}...")
    
    junk_files = scan_junk(path, recursive=recursive)
    
    if not junk_files:
        console.print("[green]No junk files found![/green]")
        return
    
    table = Table(title=f"Junk Files Found ({len(junk_files)})")
    table.add_column("Path", style="magenta")
    table.add_column("Type", style="cyan")
    
    for junk in junk_files:
        jtype = "Dir" if os.path.isdir(junk) else "File"
        table.add_row(junk, jtype)
        
    console.print(table)

@main.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--recursive/--no-recursive', default=True, help="Scan subdirectories recursively.")
@click.option('--force', is_flag=True, help="Actually delete the files.")
@click.option('--yes', '-y', is_flag=True, help="Skip confirmation prompt.")
def clean(path, recursive, force, yes):
    """Scan and remove macOS junk files."""
    path = os.path.abspath(path)
    junk_files = scan_junk(path, recursive=recursive)
    
    if not junk_files:
        console.print("[green]No junk files found to clean![/green]")
        return
    
    if not force:
        console.print(f"[yellow]Dry-run mode:[/yellow] Would remove {len(junk_files)} items.")
        for f in junk_files:
            console.print(f"  [dim]- {f}[/dim]")
        console.print("\nRun with [bold]--force[/bold] to actually delete them.")
        return

    if not yes:
        if not click.confirm(f"Are you sure you want to delete {len(junk_files)} items?"):
            console.print("[yellow]Aborted.[/yellow]")
            return

    removed, errors = remove_junk(junk_files, dry_run=False)
    
    for r in removed:
        console.print(f"[green]Removed:[/green] {r}")
        
    for path, err in errors:
        console.print(f"[red]Error removing {path}:[/red] {err}")

    console.print(f"\n[bold green]Clean up complete![/bold green] Removed {len(removed)} items.")

if __name__ == "__main__":
    main()
