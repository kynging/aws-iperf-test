from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class VPCStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, cidr: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ## create vpc
        subnets = [{'cidrMask': 24, 'name': 'Public', 'subnetType': ec2.SubnetType.PUBLIC}]
        
        # class aws_cdk.aws_ec2.Vpc(scope, id, *, cidr=None, default_instance_tenancy=None, enable_dns_hostnames=None, enable_dns_support=None, gateway_endpoints=None, max_azs=None, nat_gateways=None, nat_gateway_subnets=None, subnet_configuration=None, vpn_connections=None, vpn_gateway=None, vpn_gateway_asn=None, vpn_route_propagation=None)
        self.vpc = ec2.Vpc(self, 'vpc', 
                           cidr=cidr, 
                           max_azs=1, 
                           subnet_configuration=subnets, 
                           nat_gateways=0)