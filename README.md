# Create Cloudwatch Subscription Filter


## Getting Started


### Prerequisites

What things you need to install the software and how to install them

- Python 3.x
- AWS Account
- AWS User with cli permission
- AWS CLI
- Pip command installed
- Log Group Name that you stream data to Elasticsearch

### Installing

A step by step series of examples that tell you how to get a development env running

1. Install Python 3.x with pip

2. Install and configure AWS Command Line based on your OS - See [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

### Development setup

1. Clone project from development branch
```bash
git clone -b development https://github.com/marcelo-franca/aws-cw-elastic-subscription-filter.git
cd /aws-cw-elastic-subscription-filter
```
   
2. Configure some variables that should be used by the script.
```bash
export AUTOMATION_ACCESS_KEY='<YOUR_USER_ACCESS_KEY>'
export AUTOMATION_SECRET_KEY='<YOUR_USER_SECRET_KEY>'
export AWS_ACCOUNT_ID='<1234567890>'
export AWS_REGION='<aws_region>' # Default is us-east-1
export TARGET_FUNCTION='LogsToElasticsearch_elasticsearch'
```

3. Create and active your virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install a python required modules and packages

```bash
pip install -r requirements.txt
```

5. Create a Subscription Filter at Cloudwatch
```bash
python create-subscription-filter.py '/aws/lambda/your-log-group-name'
```
## Running the tests

## Contributing

Feel free to submitting pull requests.

## License

This project is licensed under the [GNU General Public License](https://opensource.org/licenses/GPL-3.0).
