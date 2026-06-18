from rich.console import Console
from rich.table import Table
from string import Template
from datetime import datetime

def print_functions_table(functions: list[dict], metrics: dict):
    console = Console()
    table = Table(title='List Functions Lambda')

    table.add_column('Function Name', style='cyan', no_wrap=True)
    table.add_column('Runtime', style='cyan')
    table.add_column('Invocations', style='cyan')
    table.add_column('Errors', style='cyan')
    table.add_column('Avg Duration (ms)', style='cyan')
    table.add_column('Throttles', style='cyan')

    for func in functions:
        name = func['FunctionName']
        runtime = func['Runtime']
        m = metrics.get(name, {})

        table.add_row(
            name,
            runtime,
            str(m.get('invocations', 0)),
            str(m.get('errors', 0)),
            str(m.get('duration', 0)),
            str(m.get('throttles', 0))
        )
    
    console.print(table)

def generate_html_report(functions: list[dict], metrics: dict, days: int = 7):
    with open('templates/report.html', 'r') as f:
        template = Template(f.read())
    
    rows = ""

    for func in functions:
        name = func['FunctionName']
        runtime = func['Runtime']
        m = metrics.get(name, {})
        
        rows += f"""
        <tr>
            <td>{name}</td>
            <td>{runtime}</td>
            <td>{m.get('invocations', 0)}</td>
            <td class="errors">{m.get('errors', 0)}</td>
            <td>{m.get('duration', 0)}</td>
            <td>{m.get('throttles', 0)}</td>
        </tr>
        """

    generated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    html = template.substitute(
        generated_at=generated_at,
        days=days,
        rows=rows
    )

    with open('report.html', 'w') as f:
        f.write(html)