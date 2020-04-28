#!/usr/bin/env python3

from aws_cdk import core
from aws_iperf_test.aws_iperf_test_stack import AwsIperfTestStack


app = core.App()

tokyo = core.Environment(account='843493563478', region='ap-northeast-1')
seoul = core.Environment(account='843493563478', region='ap-northeast-2')
singapore = core.Environment(account='843493563478', region='ap-southeast-1')
sydney = core.Environment(account='843493563478', region='ap-southeast-2')
mumbai = core.Environment(account='843493563478', region='ap-south-1')
#frankfurt = core.Environment(account='843493563478', region='eu-central-1')

# VPC 
from aws_iperf_test.vpc_stack import VPCStack

vpc_tokyo_stack = VPCStack(app, "tokyo", "10.0.0.0/16", env=tokyo)
vpc_tokyo = vpc_tokyo_stack.vpc

vpc_seoul_stack = VPCStack(app, "seoul", "10.0.0.0/16", env=seoul)
vpc_seoul = vpc_seoul_stack.vpc

vpc_singapore_stack = VPCStack(app, "singapore", "10.0.0.0/16", env=singapore)
vpc_singapore = vpc_singapore_stack.vpc

vpc_sydney_stack = VPCStack(app, "sydney", "10.0.0.0/16", env=sydney)
vpc_sydney = vpc_sydney_stack.vpc

vpc_mumbai_stack = VPCStack(app, "mumbai", "10.0.0.0/16", env=mumbai)
vpc_mumbai = vpc_mumbai_stack.vpc

#vpc_frankfurt_stack = VPCStack(app, "frankfurt", "10.0.0.0/16", env=frankfurt)
#vpc_frankfurt = vpc_frankfurt_stack.vpc

# Iperf Server
from aws_iperf_test.iperf_server_stack import IperfServer

iperf_server_tokyo = IperfServer(app, "iperf-server-tokyo", vpc_tokyo, env=tokyo)
iperf_server_singapore = IperfServer(app, "iperf-server-singapore", vpc_singapore, env=singapore)
#iperf_server_frankfurt = IperfServer(app, "iperf-server-frankfurt", vpc_frankfurt, env=frankfurt)

# Iperf Client
from aws_iperf_test.iperf_client_stack import IperfClient

iperf_client_tokyo = IperfClient(app, "iperf-client-tokyo", vpc_tokyo, env=tokyo)
iperf_client_seoul = IperfClient(app, "iperf-client-seoul", vpc_seoul, env=seoul)
iperf_client_singapore = IperfClient(app, "iperf-client-singapore", vpc_singapore, env=singapore)
iperf_client_sydney = IperfClient(app, "iperf-client-sydney", vpc_sydney, env=sydney)
iperf_client_mumbai = IperfClient(app, "iperf-client-mumbai", vpc_mumbai, env=mumbai)
#iperf_server_frankfurt = IperfServer(app, "iperf-server-frankfurt", vpc_frankfurt, env=frankfurt)

app.synth()