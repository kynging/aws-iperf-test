from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core
)


class IperfServer(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        instance_type = ec2.InstanceType('m5.large')
        machine_image = ec2.AmazonLinuxImage(edition=ec2.AmazonLinuxEdition.STANDARD,
                                             generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2)
        key_name = 'kyn-key'
        allow_all_outbound = True
        user_data = ec2.UserData.for_linux()
        user_data.add_commands('sudo yum -y update', 
                               'sudo yum install -y iperf3',
                               'iperf3 -s -i 1 -D')
        
        ## create security group
        # class aws_cdk.aws_ec2.SecurityGroup(scope, id, *, vpc, allow_all_outbound=None, description=None, security_group_name=None)
        cidr = vpc.vpc_cidr_block
        self.iperf_server_sg = ec2.SecurityGroup(self, 'iperf-server-sg', 
                                                       vpc=vpc, 
                                                       allow_all_outbound=True,
                                                       security_group_name='iperf-server-sg')
        self.iperf_server_sg.add_ingress_rule(peer=ec2.Peer.ipv4('0.0.0.0/0'), 
                                                    connection=ec2.Port.tcp(22), 
                                                    description='Allow Inbound SSH Connection')
        self.iperf_server_sg.add_ingress_rule(peer=ec2.Peer.ipv4('0.0.0.0/0'), 
                                                    connection=ec2.Port.tcp(5201), 
                                                    description='Allow Inbound iperf TCP Connection')
        self.iperf_server_sg.add_ingress_rule(peer=ec2.Peer.ipv4('0.0.0.0/0'), 
                                                    connection=ec2.Port.udp(5201), 
                                                    description='Allow Inbound iperf UDP Connection')
        self.iperf_server_sg.add_ingress_rule(peer=ec2.Peer.ipv4(cidr), 
                                                    connection=ec2.Port.all_traffic(), 
                                                    description='Allow Inbound Connection from VPC')
        security_group = self.iperf_server_sg
        
        ## create iam role for ec2
        # class aws_cdk.aws_iam.Role(scope, id, *, assumed_by, external_id=None, external_ids=None, inline_policies=None, managed_policies=None, max_session_duration=None, path=None, permissions_boundary=None, role_name=None)
        managed_policies = []
        policy = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore')
        managed_policies.append(policy)
        role = iam.Role(self, 'iperf-server-role', 
                        assumed_by=iam.ServicePrincipal('ec2'),
                        managed_policies=managed_policies,
                        role_name=None)
        
        ## create iperf server instance
        # class aws_cdk.aws_ec2.Instance(scope, id, *, instance_type, machine_image, vpc, allow_all_outbound=None, availability_zone=None, instance_name=None, key_name=None, resource_signal_timeout=None, role=None, security_group=None, user_data=None, vpc_subnets=None)
        self.iperf_server = ec2.Instance(self, 'ec2', 
                                         instance_type=instance_type,
                                         machine_image=machine_image,
                                         vpc=vpc,
                                         allow_all_outbound=allow_all_outbound,
                                         key_name=key_name,
                                         security_group=security_group,
                                         user_data=user_data,
                                         role=role,
                                         vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
                                         )