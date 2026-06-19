# Lambda Monitor Dashboard 📊

A Python CLI tool that monitors AWS Lambda functions by extracting real-time metrics from CloudWatch — displays invocations, errors, average duration, and throttles in a formatted terminal table or as an HTML dashboard report.

---

## Demo

```
$ python3 main.py report --days 7

                                   List Functions Lambda
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Function Name       ┃ Runtime    ┃ Invocations ┃ Errors ┃ Avg Duration (ms) ┃ Throttles ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ s3-report-generator │ python3.13 │ 1           │ 0      │ 2978.13           │ 0         │
│ password-generator  │ python3.13 │ 4           │ 0      │ 5.13              │ 0         │
│ text-analyzer       │ python3.13 │ 1           │ 0      │ 2.14              │ 0         │
└─────────────────────┴────────────┴─────────────┴────────┴───────────────────┴───────────┘
```

---

## Features

- 📋 List all Lambda functions in your AWS account
- 📈 Extract real CloudWatch metrics per function — invocations, errors, duration, throttles
- 🗓️ Configurable time range (`--days`) — last 7, 14, or 30 days
- 📊 Formatted terminal table powered by `rich`
- 🌐 Export metrics as an HTML dashboard report
- 🔐 Authenticates using a named AWS CLI profile (least privilege IAM user)
- ⚡ Includes 3 deployed Lambda functions used as monitoring targets

---

## Lambda Functions

This project includes 3 Python Lambda functions deployed to AWS:

| Function | Description |
|----------|-------------|
| `password-generator` | Generates secure passwords with configurable length, uppercase, numbers, and symbols |
| `text-analyzer` | Analyzes text and returns word count, character count, sentences, paragraphs, and most frequent words |
| `s3-report-generator` | Lists objects in an S3 bucket and returns total files, total size, and breakdown by file type |

---

## Project Structure

```
LambdaMonitorDashboard/
├── lambdas/
│   ├── password_generator/
│   │   └── lambda_function.py   # Secure password generation
│   ├── text_analyzer/
│   │   └── lambda_function.py   # Text statistics analysis
│   └── s3_report_generator/
│       └── lambda_function.py   # S3 bucket report generation
├── monitor/
│   ├── __init__.py
│   ├── lambda_client.py         # List Lambda functions via boto3
│   ├── metrics.py               # Extract CloudWatch metrics per function
│   └── reporter.py              # Terminal output (rich) and HTML report
├── templates/
│   └── report.html              # HTML dashboard template
├── main.py                      # CLI entry point with subcommands
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Technology      | Description                                        |
|-----------------|----------------------------------------------------|
| Python 3.10+    | Primary language                                   |
| boto3           | AWS SDK for Python                                 |
| rich            | Terminal formatting and tables                     |
| argparse        | CLI subcommands and flag handling                  |
| string.Template | HTML report generation                             |
| AWS Lambda      | Serverless function execution                      |
| AWS CloudWatch  | Metrics extraction (invocations, errors, duration) |

---

## Prerequisites

- Python 3.10+
- AWS CLI v2 installed and configured
- An IAM user with the following permissions:
  - `lambda:ListFunctions`
  - `lambda:GetFunction`
  - `cloudwatch:GetMetricStatistics`
  - `cloudwatch:ListMetrics`

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/jcreyesDev/LambdaMonitorDashboard.git
cd LambdaMonitorDashboard
```

2. Install dependencies:

```bash
pip3 install -r requirements.txt
```

3. Configure your AWS CLI profile:

```bash
aws configure --profile your-profile-name
```

---

## Usage

```bash
# List all Lambda functions
python3 main.py list-functions

# Generate terminal report for the last 7 days (default)
python3 main.py report

# Generate report for a custom time range
python3 main.py report --days 14
python3 main.py report --days 30

# Generate terminal report + HTML dashboard
python3 main.py report --days 7 --output html

# Show help
python3 main.py --help
```

---

## IAM Policy

Minimum required permissions for the IAM user running this tool:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:ListFunctions",
        "lambda:GetFunction",
        "lambda:GetFunctionConfiguration",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "cloudwatch:GetMetricData"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## Requirements

- Python 3.10+
- AWS CLI v2
- Active AWS account with Lambda functions deployed
- IAM user with minimum required permissions

---

## Author

Developed by [@jcreyesDev](https://github.com/jcreyesDev)