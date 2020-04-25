#!/usr/bin/env python3

from aws_cdk import core

from aws_iperf_test.aws_iperf_test_stack import AwsIperfTestStack


app = core.App()
AwsIperfTestStack(app, "aws-iperf-test", env={'region': 'us-west-2'})

app.synth()
