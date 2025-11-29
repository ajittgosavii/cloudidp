"""
Message Queue Service
SQS/RabbitMQ integration for async task processing and job queues
"""

import boto3
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueueType(Enum):
    """Queue type enumeration"""
    STANDARD = "standard"
    FIFO = "fifo"
    PRIORITY = "priority"


class MessagePriority(Enum):
    """Message priority levels"""
    LOW = 1
    NORMAL = 5
    HIGH = 8
    CRITICAL = 10


class SQSQueue:
    """AWS SQS queue manager"""
    
    def __init__(self, queue_name: str, region: str = 'us-east-1'):
        """
        Initialize SQS queue
        
        Args:
            queue_name: Name of the SQS queue
            region: AWS region
        """
        self.queue_name = queue_name
        self.region = region
        
        try:
            self.sqs = boto3.client('sqs', region_name=region)
            self.queue_url = None
        except Exception as e:
            logger.error(f"Failed to initialize SQS client: {e}")
            self.sqs = None
    
    def create_queue(self, queue_type: QueueType = QueueType.STANDARD,
                    attributes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Create SQS queue
        
        Args:
            queue_type: Type of queue (standard or FIFO)
            attributes: Additional queue attributes
            
        Returns:
            Dict with queue creation status
        """
        if not self.sqs:
            return {"status": "error", "message": "SQS client not initialized"}
        
        try:
            queue_name = self.queue_name
            if queue_type == QueueType.FIFO:
                queue_name = f"{queue_name}.fifo"
            
            default_attributes = {
                'VisibilityTimeout': '300',  # 5 minutes
                'MessageRetentionPeriod': '345600',  # 4 days
                'ReceiveMessageWaitTimeSeconds': '20'  # Long polling
            }
            
            if queue_type == QueueType.FIFO:
                default_attributes['FifoQueue'] = 'true'
                default_attributes['ContentBasedDeduplication'] = 'true'
            
            if attributes:
                default_attributes.update(attributes)
            
            response = self.sqs.create_queue(
                QueueName=queue_name,
                Attributes=default_attributes
            )
            
            self.queue_url = response['QueueUrl']
            
            return {
                "status": "success",
                "queue_url": self.queue_url,
                "queue_name": queue_name
            }
            
        except Exception as e:
            logger.error(f"Failed to create queue: {e}")
            return {"status": "error", "message": str(e)}
    
    def send_message(self, message_body: Dict[str, Any],
                    message_group_id: Optional[str] = None,
                    deduplication_id: Optional[str] = None,
                    delay_seconds: int = 0) -> Dict[str, Any]:
        """
        Send message to queue
        
        Args:
            message_body: Message content
            message_group_id: Message group ID (for FIFO queues)
            deduplication_id: Deduplication ID (for FIFO queues)
            delay_seconds: Delay before message becomes visible
            
        Returns:
            Dict with send status and message ID
        """
        if not self.sqs or not self.queue_url:
            return {"status": "error", "message": "Queue not initialized"}
        
        try:
            params = {
                'QueueUrl': self.queue_url,
                'MessageBody': json.dumps(message_body),
                'DelaySeconds': delay_seconds
            }
            
            if message_group_id:
                params['MessageGroupId'] = message_group_id
            
            if deduplication_id:
                params['MessageDeduplicationId'] = deduplication_id
            
            response = self.sqs.send_message(**params)
            
            return {
                "status": "success",
                "message_id": response['MessageId'],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return {"status": "error", "message": str(e)}
    
    def send_batch(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Send multiple messages in batch
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Dict with batch send results
        """
        if not self.sqs or not self.queue_url:
            return {"status": "error", "message": "Queue not initialized"}
        
        try:
            entries = []
            for idx, msg in enumerate(messages):
                entry = {
                    'Id': str(idx),
                    'MessageBody': json.dumps(msg)
                }
                
                if msg.get('message_group_id'):
                    entry['MessageGroupId'] = msg['message_group_id']
                
                if msg.get('deduplication_id'):
                    entry['MessageDeduplicationId'] = msg['deduplication_id']
                
                entries.append(entry)
            
            response = self.sqs.send_message_batch(
                QueueUrl=self.queue_url,
                Entries=entries
            )
            
            return {
                "status": "success",
                "successful": len(response.get('Successful', [])),
                "failed": len(response.get('Failed', [])),
                "results": response
            }
            
        except Exception as e:
            logger.error(f"Failed to send batch: {e}")
            return {"status": "error", "message": str(e)}
    
    def receive_messages(self, max_messages: int = 10,
                        wait_time: int = 20) -> Dict[str, Any]:
        """
        Receive messages from queue
        
        Args:
            max_messages: Maximum number of messages to receive
            wait_time: Long polling wait time in seconds
            
        Returns:
            Dict with received messages
        """
        if not self.sqs or not self.queue_url:
            return {"status": "error", "messages": []}
        
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
                AttributeNames=['All'],
                MessageAttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            
            parsed_messages = []
            for msg in messages:
                parsed_messages.append({
                    "message_id": msg['MessageId'],
                    "receipt_handle": msg['ReceiptHandle'],
                    "body": json.loads(msg['Body']),
                    "attributes": msg.get('Attributes', {}),
                    "message_attributes": msg.get('MessageAttributes', {})
                })
            
            return {
                "status": "success",
                "count": len(parsed_messages),
                "messages": parsed_messages
            }
            
        except Exception as e:
            logger.error(f"Failed to receive messages: {e}")
            return {"status": "error", "messages": []}
    
    def delete_message(self, receipt_handle: str) -> Dict[str, Any]:
        """Delete message from queue"""
        if not self.sqs or not self.queue_url:
            return {"status": "error", "message": "Queue not initialized"}
        
        try:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            
            return {"status": "success", "message": "Message deleted"}
            
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_queue_attributes(self) -> Dict[str, Any]:
        """Get queue attributes and statistics"""
        if not self.sqs or not self.queue_url:
            return {"status": "error"}
        
        try:
            response = self.sqs.get_queue_attributes(
                QueueUrl=self.queue_url,
                AttributeNames=['All']
            )
            
            attributes = response.get('Attributes', {})
            
            return {
                "status": "success",
                "approximate_messages": int(attributes.get('ApproximateNumberOfMessages', 0)),
                "approximate_messages_not_visible": int(attributes.get('ApproximateNumberOfMessagesNotVisible', 0)),
                "approximate_messages_delayed": int(attributes.get('ApproximateNumberOfMessagesDelayed', 0)),
                "created_timestamp": attributes.get('CreatedTimestamp'),
                "last_modified_timestamp": attributes.get('LastModifiedTimestamp')
            }
            
        except Exception as e:
            logger.error(f"Failed to get queue attributes: {e}")
            return {"status": "error", "message": str(e)}


class MessageQueueManager:
    """High-level message queue manager"""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize message queue manager"""
        self.region = region
        self.queues = {}
        
        # Initialize standard queues
        self._initialize_queues()
    
    def _initialize_queues(self):
        """Initialize standard application queues"""
        queue_configs = {
            'provisioning-jobs': {'type': QueueType.STANDARD, 'priority': True},
            'terraform-execution': {'type': QueueType.FIFO, 'priority': False},
            'compliance-scans': {'type': QueueType.STANDARD, 'priority': True},
            'cost-analysis': {'type': QueueType.STANDARD, 'priority': False},
            'notifications': {'type': QueueType.STANDARD, 'priority': True},
            'audit-events': {'type': QueueType.FIFO, 'priority': False},
            'dead-letter': {'type': QueueType.STANDARD, 'priority': False}
        }
        
        for queue_name, config in queue_configs.items():
            queue = SQSQueue(queue_name, self.region)
            
            # In production, check if queue exists before creating
            self.queues[queue_name] = queue
            
            logger.info(f"Queue initialized: {queue_name}")
    
    def send_provisioning_job(self, job_data: Dict[str, Any],
                            priority: MessagePriority = MessagePriority.NORMAL) -> str:
        """Send provisioning job to queue"""
        message = {
            "job_id": str(uuid.uuid4()),
            "job_type": job_data['job_type'],
            "config": job_data['config'],
            "priority": priority.value,
            "created_at": datetime.utcnow().isoformat(),
            "created_by": job_data.get('created_by', 'system')
        }
        
        queue = self.queues.get('provisioning-jobs')
        if queue:
            result = queue.send_message(message)
            if result['status'] == 'success':
                logger.info(f"Provisioning job queued: {message['job_id']}")
                return message['job_id']
        
        return ""
    
    def send_terraform_job(self, terraform_config: Dict[str, Any]) -> str:
        """Send Terraform execution job to FIFO queue"""
        job_id = str(uuid.uuid4())
        
        message = {
            "job_id": job_id,
            "operation": terraform_config['operation'],
            "workspace": terraform_config['workspace'],
            "modules": terraform_config.get('modules', []),
            "variables": terraform_config.get('variables', {}),
            "created_at": datetime.utcnow().isoformat()
        }
        
        queue = self.queues.get('terraform-execution')
        if queue:
            result = queue.send_message(
                message,
                message_group_id=terraform_config['workspace'],
                deduplication_id=job_id
            )
            if result['status'] == 'success':
                logger.info(f"Terraform job queued: {job_id}")
                return job_id
        
        return ""
    
    def send_compliance_scan(self, scan_config: Dict[str, Any]) -> str:
        """Send compliance scan job to queue"""
        scan_id = str(uuid.uuid4())
        
        message = {
            "scan_id": scan_id,
            "account_id": scan_config['account_id'],
            "frameworks": scan_config.get('frameworks', []),
            "resources": scan_config.get('resources', []),
            "created_at": datetime.utcnow().isoformat()
        }
        
        queue = self.queues.get('compliance-scans')
        if queue:
            result = queue.send_message(message)
            if result['status'] == 'success':
                logger.info(f"Compliance scan queued: {scan_id}")
                return scan_id
        
        return ""
    
    def send_notification(self, notification: Dict[str, Any],
                         priority: MessagePriority = MessagePriority.NORMAL) -> bool:
        """Send notification message"""
        message = {
            "notification_id": str(uuid.uuid4()),
            "type": notification['type'],
            "recipient": notification['recipient'],
            "subject": notification.get('subject'),
            "body": notification['body'],
            "priority": priority.value,
            "created_at": datetime.utcnow().isoformat()
        }
        
        queue = self.queues.get('notifications')
        if queue:
            result = queue.send_message(message)
            return result['status'] == 'success'
        
        return False
    
    def send_audit_event(self, event: Dict[str, Any]) -> bool:
        """Send audit event to FIFO queue"""
        event_id = str(uuid.uuid4())
        
        message = {
            "event_id": event_id,
            "event_type": event['event_type'],
            "user_id": event['user_id'],
            "action": event['action'],
            "resource": event.get('resource'),
            "result": event.get('result', 'success'),
            "metadata": event.get('metadata', {}),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        queue = self.queues.get('audit-events')
        if queue:
            result = queue.send_message(
                message,
                message_group_id='audit',
                deduplication_id=event_id
            )
            return result['status'] == 'success'
        
        return False
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get statistics for all queues"""
        stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "queues": {}
        }
        
        for queue_name, queue in self.queues.items():
            attrs = queue.get_queue_attributes()
            if attrs['status'] == 'success':
                stats['queues'][queue_name] = {
                    "messages": attrs['approximate_messages'],
                    "in_flight": attrs['approximate_messages_not_visible'],
                    "delayed": attrs['approximate_messages_delayed']
                }
        
        return stats


# Mock message queue for demo mode
class MockMessageQueueManager:
    """Mock message queue for demo mode"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.queued_jobs = []
    
    def send_provisioning_job(self, job_data: Dict[str, Any],
                            priority: MessagePriority = MessagePriority.NORMAL) -> str:
        """Mock send provisioning job"""
        job_id = str(uuid.uuid4())
        
        self.queued_jobs.append({
            "job_id": job_id,
            "type": "provisioning",
            "priority": priority.name,
            "data": job_data,
            "created_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"[DEMO] Provisioning job queued: {job_id}")
        return job_id
    
    def send_terraform_job(self, terraform_config: Dict[str, Any]) -> str:
        """Mock send Terraform job"""
        job_id = str(uuid.uuid4())
        
        self.queued_jobs.append({
            "job_id": job_id,
            "type": "terraform",
            "data": terraform_config,
            "created_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"[DEMO] Terraform job queued: {job_id}")
        return job_id
    
    def send_compliance_scan(self, scan_config: Dict[str, Any]) -> str:
        """Mock send compliance scan"""
        scan_id = str(uuid.uuid4())
        
        self.queued_jobs.append({
            "scan_id": scan_id,
            "type": "compliance_scan",
            "data": scan_config,
            "created_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"[DEMO] Compliance scan queued: {scan_id}")
        return scan_id
    
    def send_notification(self, notification: Dict[str, Any],
                         priority: MessagePriority = MessagePriority.NORMAL) -> bool:
        """Mock send notification"""
        logger.info(f"[DEMO] Notification sent: {notification.get('subject')}")
        return True
    
    def send_audit_event(self, event: Dict[str, Any]) -> bool:
        """Mock send audit event"""
        logger.info(f"[DEMO] Audit event logged: {event.get('action')}")
        return True
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Mock queue statistics"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "mode": "demo",
            "queues": {
                "provisioning-jobs": {"messages": 5, "in_flight": 2, "delayed": 0},
                "terraform-execution": {"messages": 3, "in_flight": 1, "delayed": 0},
                "compliance-scans": {"messages": 2, "in_flight": 1, "delayed": 0},
                "notifications": {"messages": 8, "in_flight": 0, "delayed": 0},
                "audit-events": {"messages": 15, "in_flight": 0, "delayed": 0}
            },
            "total_queued_jobs": len(self.queued_jobs)
        }
