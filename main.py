import argparse
from monitor.lambda_client import get_functions
from monitor.metrics import get_function_metrics
from monitor.reporter import print_functions_table, generate_html_report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lambda Monitor Dashboard')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list-functions', help='List all Lambda functions')

    report_parser = subparsers.add_parser('report', help='Generate Lambda metrics report')
    report_parser.add_argument('--days', type=int, default=7, help='Number of days to look back')
    report_parser.add_argument('--output', choices=['html'], help='Export format')

    args = parser.parse_args()

    if args.command == 'list-functions':
        functions = get_functions()

        print_functions_table(functions=functions, metrics={})
    elif args.command == 'report':
        functions = get_functions()

        metrics = {}

        for func in functions:
            name = func['FunctionName']
            metrics[name] = get_function_metrics(name, days=args.days)
        
        print_functions_table(functions=functions, metrics=metrics)
        
        if args.output == 'html':
            generate_html_report(functions=functions, metrics=metrics, days=args.days)
    elif args.command is None:
        parser.print_help()