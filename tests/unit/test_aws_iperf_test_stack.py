import json
import pytest

from aws_cdk import core
from aws-iperf-test.aws_iperf_test_stack import AwsIperfTestStack


def get_template():
    app = core.App()
    AwsIperfTestStack(app, "aws-iperf-test")
    return json.dumps(app.synth().get_stack("aws-iperf-test").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
