"""
CloudIDP - AWS Compute & Network Integration Module
EC2, VPC, and network infrastructure management
"""

import streamlit as st
import boto3
from typing import Dict, List, Optional, Any
from botocore.exceptions import ClientError


class ComputeNetworkIntegration:
    """AWS EC2 and VPC integration for CloudIDP"""
    
    def __init__(self, demo_mode: bool = True, region: str = 'us-east-1'):
        self.demo_mode = demo_mode
        self.region = region
        
        if not demo_mode:
            try:
                # Try to read from Streamlit secrets first
                if hasattr(st, 'secrets') and 'aws' in st.secrets:
                    self.ec2_client = boto3.client(
                        'ec2',
                        aws_access_key_id=st.secrets["aws"]["access_key"],
                        aws_secret_access_key=st.secrets["aws"]["secret_access_key"],
                        region_name=st.secrets["aws"].get("region", region)
                    )
                    self.ec2_resource = boto3.resource(
                        'ec2',
                        aws_access_key_id=st.secrets["aws"]["access_key"],
                        aws_secret_access_key=st.secrets["aws"]["secret_access_key"],
                        region_name=st.secrets["aws"].get("region", region)
                    )
                else:
                    # Fallback to default credentials (IAM role, env vars, etc.)
                    self.ec2_client = boto3.client('ec2', region_name=region)
                    self.ec2_resource = boto3.resource('ec2', region_name=region)
            except Exception as e:
                print(f"Warning: {e}")
                self.demo_mode = True
    
    # ============= VPC OPERATIONS =============
    
    def create_vpc(self, cidr_block: str, name: str,
                   enable_dns: bool = True) -> Dict[str, Any]:
        """Create a VPC"""
        if self.demo_mode:
            return {
                'success': True,
                'vpc_id': f'vpc-{str(hash(name))[-12:]}',
                'cidr_block': cidr_block,
                'name': name,
                'demo_mode': True
            }
        
        try:
            response = self.ec2_client.create_vpc(
                CidrBlock=cidr_block,
                AmazonProvidedIpv6CidrBlock=False
            )
            vpc_id = response['Vpc']['VpcId']
            
            # Tag VPC
            self.ec2_client.create_tags(
                Resources=[vpc_id],
                Tags=[{'Key': 'Name', 'Value': name}]
            )
            
            # Enable DNS
            if enable_dns:
                self.ec2_client.modify_vpc_attribute(
                    VpcId=vpc_id,
                    EnableDnsHostnames={'Value': True}
                )
                self.ec2_client.modify_vpc_attribute(
                    VpcId=vpc_id,
                    EnableDnsSupport={'Value': True}
                )
            
            return {
                'success': True,
                'vpc_id': vpc_id,
                'cidr_block': cidr_block
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def create_subnet(self, vpc_id: str, cidr_block: str, 
                     availability_zone: str, name: str) -> Dict[str, Any]:
        """Create a subnet"""
        if self.demo_mode:
            return {
                'success': True,
                'subnet_id': f'subnet-{str(hash(name))[-12:]}',
                'cidr_block': cidr_block,
                'demo_mode': True
            }
        
        try:
            response = self.ec2_client.create_subnet(
                VpcId=vpc_id,
                CidrBlock=cidr_block,
                AvailabilityZone=availability_zone
            )
            subnet_id = response['Subnet']['SubnetId']
            
            # Tag subnet
            self.ec2_client.create_tags(
                Resources=[subnet_id],
                Tags=[{'Key': 'Name', 'Value': name}]
            )
            
            return {
                'success': True,
                'subnet_id': subnet_id,
                'cidr_block': cidr_block
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def list_vpcs(self) -> Dict[str, Any]:
        """List all VPCs"""
        if self.demo_mode:
            return {
                'success': True,
                'count': 2,
                'vpcs': [
                    {
                        'VpcId': 'vpc-prod001',
                        'CidrBlock': '10.0.0.0/16',
                        'State': 'available',
                        'Tags': [{'Key': 'Name', 'Value': 'Production VPC'}]
                    },
                    {
                        'VpcId': 'vpc-dev001',
                        'CidrBlock': '10.1.0.0/16',
                        'State': 'available',
                        'Tags': [{'Key': 'Name', 'Value': 'Development VPC'}]
                    }
                ],
                'demo_mode': True
            }
        
        try:
            response = self.ec2_client.describe_vpcs()
            return {
                'success': True,
                'count': len(response['Vpcs']),
                'vpcs': response['Vpcs']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    # ============= EC2 OPERATIONS =============
    
    def launch_instance(self, ami_id: str, instance_type: str,
                       subnet_id: str, key_name: str,
                       security_group_ids: List[str],
                       name: str) -> Dict[str, Any]:
        """Launch an EC2 instance"""
        if self.demo_mode:
            return {
                'success': True,
                'instance_id': f'i-{str(hash(name))[-12:]}',
                'instance_type': instance_type,
                'state': 'pending',
                'demo_mode': True
            }
        
        try:
            response = self.ec2_resource.create_instances(
                ImageId=ami_id,
                InstanceType=instance_type,
                MinCount=1,
                MaxCount=1,
                KeyName=key_name,
                NetworkInterfaces=[{
                    'SubnetId': subnet_id,
                    'DeviceIndex': 0,
                    'AssociatePublicIpAddress': True,
                    'Groups': security_group_ids
                }],
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': name}]
                }]
            )
            
            instance = response[0]
            return {
                'success': True,
                'instance_id': instance.id,
                'instance_type': instance_type
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def list_instances(self, filters: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """List EC2 instances"""
        if self.demo_mode:
            return {
                'success': True,
                'count': 4,
                'instances': [
                    {
                        'InstanceId': 'i-prod001',
                        'InstanceType': 't3.large',
                        'State': {'Name': 'running'},
                        'Tags': [{'Key': 'Name', 'Value': 'Web Server 1'}]
                    },
                    {
                        'InstanceId': 'i-prod002',
                        'InstanceType': 't3.large',
                        'State': {'Name': 'running'},
                        'Tags': [{'Key': 'Name', 'Value': 'Web Server 2'}]
                    },
                    {
                        'InstanceId': 'i-dev001',
                        'InstanceType': 't3.medium',
                        'State': {'Name': 'stopped'},
                        'Tags': [{'Key': 'Name', 'Value': 'Dev Server'}]
                    },
                    {
                        'InstanceId': 'i-db001',
                        'InstanceType': 'r5.xlarge',
                        'State': {'Name': 'running'},
                        'Tags': [{'Key': 'Name', 'Value': 'Database Server'}]
                    }
                ],
                'demo_mode': True
            }
        
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            response = self.ec2_client.describe_instances(**params)
            instances = []
            for reservation in response['Reservations']:
                instances.extend(reservation['Instances'])
            
            return {
                'success': True,
                'count': len(instances),
                'instances': instances
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def stop_instance(self, instance_id: str) -> Dict[str, Any]:
        """Stop an EC2 instance"""
        if self.demo_mode:
            return {
                'success': True,
                'instance_id': instance_id,
                'state': 'stopping',
                'demo_mode': True
            }
        
        try:
            response = self.ec2_client.stop_instances(
                InstanceIds=[instance_id]
            )
            return {
                'success': True,
                'instance_id': instance_id,
                'state': response['StoppingInstances'][0]['CurrentState']['Name']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def terminate_instance(self, instance_id: str) -> Dict[str, Any]:
        """Terminate an EC2 instance"""
        if self.demo_mode:
            return {
                'success': True,
                'instance_id': instance_id,
                'state': 'terminating',
                'demo_mode': True
            }
        
        try:
            response = self.ec2_client.terminate_instances(
                InstanceIds=[instance_id]
            )
            return {
                'success': True,
                'instance_id': instance_id,
                'state': response['TerminatingInstances'][0]['CurrentState']['Name']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    # ============= SECURITY GROUP OPERATIONS =============
    
    def create_security_group(self, vpc_id: str, name: str,
                             description: str) -> Dict[str, Any]:
        """Create a security group"""
        if self.demo_mode:
            return {
                'success': True,
                'security_group_id': f'sg-{str(hash(name))[-12:]}',
                'demo_mode': True
            }
        
        try:
            response = self.ec2_client.create_security_group(
                GroupName=name,
                Description=description,
                VpcId=vpc_id
            )
            return {
                'success': True,
                'security_group_id': response['GroupId']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    print("Compute & Network Integration Demo")
    cn = ComputeNetworkIntegration(demo_mode=True)
    
    # Test VPC creation
    vpc = cn.create_vpc('10.0.0.0/16', 'Test VPC')
    print(f"VPC Created: {vpc['vpc_id']}")
    
    # Test instance listing
    instances = cn.list_instances()
    print(f"\nTotal Instances: {instances['count']}")
    for inst in instances['instances'][:2]:
        print(f"  - {inst['InstanceId']} ({inst['InstanceType']}): {inst['State']['Name']}")
    
    print("\n✅ Demo completed!")
