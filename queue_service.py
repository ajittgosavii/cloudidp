"""
CloudIDP Backend Infrastructure - Queue Service
Handles SQS message queuing for asynchronous processing
"""

import boto3
import json
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import uuid
from backend_config import BackendConfig, SQS_QUEUES
from backend_models import QueueMessage, ProvisioningMessage, DeploymentMessage
import logging
from collections import deque
import time

logger = logging.getLogger(__name__)


class QueueService:
    """
    SQS Queue Service for asynchronous message processing
    Supports demo mode for testing without AWS infrastructure
    """
    
    def __init__(self, config: BackendConfig):
        self.config = config
        self.demo_mode = config.demo_mode
        
        if not self.demo_mode:
            self.sqs_client = boto3.client('sqs', region_name=config.region)
            self.queue_urls: Dict[str, str] = {}
            self._init_queues()
        else:
            # Demo mode: use in-memory queues
            self._demo_queues: Dict[str, deque] = {
                queue_name: deque() for queue_name in SQS_QUEUES.keys()
            }
            self._demo_dlq: deque = deque()
            self._message_handlers: Dict[str, Callable] = {}
    
    # ==================== Queue Initialization ====================
    
    def _init_queues(self):
        """Initialize SQS queues if they don't exist"""
        try:
            for queue_name, config in SQS_QUEUES.items():
                full_queue_name = self.config.get_queue_name(queue_name)
                
                try:
                    response = self.sqs_client.get_queue_url(QueueName=full_queue_name)
                    self.queue_urls[queue_name] = response['QueueUrl']
                    logger.info(f"Queue {full_queue_name} already exists")
                except self.sqs_client.exceptions.QueueDoesNotExist:
                    self._create_queue(queue_name, config)
        except Exception as e:
            logger.error(f"Error initializing queues: {e}")
    
    def _create_queue(self, queue_name: str, config: Dict):
        """Create an SQS queue"""
        try:
            full_queue_name = self.config.get_queue_name(queue_name)
            
            attributes = {
                'VisibilityTimeout': str(self.config.sqs_visibility_timeout),
                'MessageRetentionPeriod': str(self.config.sqs_message_retention),
                'ReceiveMessageWaitTimeSeconds': '20'  # Long polling
            }
            
            # Add DLQ configuration for non-DLQ queues
            if queue_name != 'dlq':
                dlq_name = self.config.get_queue_name('dlq')
                try:
                    dlq_response = self.sqs_client.get_queue_url(QueueName=dlq_name)
                    dlq_arn = self.sqs_client.get_queue_attributes(
                        QueueUrl=dlq_response['QueueUrl'],
                        AttributeNames=['QueueArn']
                    )['Attributes']['QueueArn']
                    
                    attributes['RedrivePolicy'] = json.dumps({
                        'deadLetterTargetArn': dlq_arn,
                        'maxReceiveCount': self.config.sqs_max_receive_count
                    })
                except:
                    pass  # DLQ not yet created
            
            if config.get('fifo', False):
                attributes['FifoQueue'] = 'true'
                attributes['ContentBasedDeduplication'] = 'true'
                full_queue_name += '.fifo'
            
            response = self.sqs_client.create_queue(
                QueueName=full_queue_name,
                Attributes=attributes
            )
            
            self.queue_urls[queue_name] = response['QueueUrl']
            logger.info(f"Created queue {full_queue_name}")
            
        except Exception as e:
            logger.error(f"Error creating queue {queue_name}: {e}")
    
    # ==================== Message Sending ====================
    
    def send_message(self, queue_name: str, message: QueueMessage) -> bool:
        """
        Send a message to a queue
        
        Args:
            queue_name: Name of the queue
            message: QueueMessage to send
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.demo_mode:
                self._demo_queues[queue_name].append(message.dict())
                logger.info(f"Demo: Sent message to {queue_name}: {message.message_id}")
                return True
            
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                logger.error(f"Queue {queue_name} not found")
                return False
            
            message_body = json.dumps(message.dict(), default=str)
            
            response = self.sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=message_body,
                MessageAttributes={
                    'MessageType': {
                        'StringValue': message.message_type,
                        'DataType': 'String'
                    },
                    'Priority': {
                        'StringValue': str(message.priority),
                        'DataType': 'Number'
                    }
                }
            )
            
            logger.info(f"Sent message to {queue_name}: {response['MessageId']}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message to {queue_name}: {e}")
            return False
    
    def send_batch(self, queue_name: str, messages: List[QueueMessage]) -> Dict[str, Any]:
        """
        Send multiple messages to a queue (batch operation)
        
        Args:
            queue_name: Name of the queue
            messages: List of QueueMessages to send
            
        Returns:
            Dictionary with success/failure counts
        """
        if self.demo_mode:
            for message in messages:
                self._demo_queues[queue_name].append(message.dict())
            return {"successful": len(messages), "failed": 0}
        
        queue_url = self.queue_urls.get(queue_name)
        if not queue_url:
            logger.error(f"Queue {queue_name} not found")
            return {"successful": 0, "failed": len(messages)}
        
        # SQS batch size limit is 10
        batch_size = 10
        total_successful = 0
        total_failed = 0
        
        for i in range(0, len(messages), batch_size):
            batch = messages[i:i+batch_size]
            entries = [
                {
                    'Id': str(j),
                    'MessageBody': json.dumps(msg.dict(), default=str),
                    'MessageAttributes': {
                        'MessageType': {
                            'StringValue': msg.message_type,
                            'DataType': 'String'
                        }
                    }
                }
                for j, msg in enumerate(batch)
            ]
            
            try:
                response = self.sqs_client.send_message_batch(
                    QueueUrl=queue_url,
                    Entries=entries
                )
                total_successful += len(response.get('Successful', []))
                total_failed += len(response.get('Failed', []))
            except Exception as e:
                logger.error(f"Error sending batch to {queue_name}: {e}")
                total_failed += len(batch)
        
        return {"successful": total_successful, "failed": total_failed}
    
    # ==================== Message Receiving ====================
    
    def receive_messages(self, queue_name: str, max_messages: int = 10, 
                        wait_time: int = 20) -> List[Dict[str, Any]]:
        """
        Receive messages from a queue
        
        Args:
            queue_name: Name of the queue
            max_messages: Maximum number of messages to receive (1-10)
            wait_time: Long polling wait time in seconds
            
        Returns:
            List of messages
        """
        try:
            if self.demo_mode:
                messages = []
                for _ in range(min(max_messages, len(self._demo_queues[queue_name]))):
                    if self._demo_queues[queue_name]:
                        msg = self._demo_queues[queue_name].popleft()
                        msg['ReceiptHandle'] = str(uuid.uuid4())
                        messages.append(msg)
                return messages
            
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                logger.error(f"Queue {queue_name} not found")
                return []
            
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=min(max_messages, 10),
                WaitTimeSeconds=wait_time,
                MessageAttributeNames=['All'],
                AttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            logger.info(f"Received {len(messages)} messages from {queue_name}")
            return messages
            
        except Exception as e:
            logger.error(f"Error receiving messages from {queue_name}: {e}")
            return []
    
    def delete_message(self, queue_name: str, receipt_handle: str) -> bool:
        """
        Delete a message from the queue after processing
        
        Args:
            queue_name: Name of the queue
            receipt_handle: Receipt handle from received message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.demo_mode:
                logger.info(f"Demo: Deleted message from {queue_name}")
                return True
            
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                return False
            
            self.sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            return True
            
        except Exception as e:
            logger.error(f"Error deleting message from {queue_name}: {e}")
            return False
    
    # ==================== Message Processing ====================
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a message handler function"""
        self._message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type}")
    
    def process_messages(self, queue_name: str, max_messages: int = 10) -> int:
        """
        Process messages from a queue using registered handlers
        
        Args:
            queue_name: Name of the queue
            max_messages: Maximum number of messages to process
            
        Returns:
            Number of messages processed
        """
        messages = self.receive_messages(queue_name, max_messages)
        processed_count = 0
        
        for message in messages:
            try:
                if self.demo_mode:
                    message_body = message
                    receipt_handle = message.get('ReceiptHandle')
                else:
                    message_body = json.loads(message['Body'])
                    receipt_handle = message['ReceiptHandle']
                
                message_type = message_body.get('message_type')
                handler = self._message_handlers.get(message_type)
                
                if handler:
                    # Process message
                    result = handler(message_body)
                    if result:
                        # Delete message after successful processing
                        self.delete_message(queue_name, receipt_handle)
                        processed_count += 1
                    else:
                        logger.warning(f"Handler returned False for message {message_type}")
                else:
                    logger.warning(f"No handler registered for message type: {message_type}")
                    # Move to DLQ
                    self.send_to_dlq(message_body)
                    self.delete_message(queue_name, receipt_handle)
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # Message will be retried or moved to DLQ by SQS
        
        return processed_count
    
    def send_to_dlq(self, message: Dict[str, Any]):
        """Send message to Dead Letter Queue"""
        dlq_message = QueueMessage(
            message_type="dlq_message",
            payload=message,
            timestamp=datetime.utcnow()
        )
        self.send_message('dlq', dlq_message)
    
    # ==================== Queue Management ====================
    
    def get_queue_attributes(self, queue_name: str) -> Dict[str, Any]:
        """Get queue attributes (size, age, etc.)"""
        if self.demo_mode:
            return {
                "ApproximateNumberOfMessages": len(self._demo_queues[queue_name]),
                "ApproximateNumberOfMessagesNotVisible": 0,
                "ApproximateNumberOfMessagesDelayed": 0
            }
        
        queue_url = self.queue_urls.get(queue_name)
        if not queue_url:
            return {}
        
        try:
            response = self.sqs_client.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['All']
            )
            return response.get('Attributes', {})
        except Exception as e:
            logger.error(f"Error getting queue attributes: {e}")
            return {}
    
    def purge_queue(self, queue_name: str) -> bool:
        """Purge all messages from a queue"""
        if self.demo_mode:
            self._demo_queues[queue_name].clear()
            logger.info(f"Demo: Purged queue {queue_name}")
            return True
        
        queue_url = self.queue_urls.get(queue_name)
        if not queue_url:
            return False
        
        try:
            self.sqs_client.purge_queue(QueueUrl=queue_url)
            logger.info(f"Purged queue {queue_name}")
            return True
        except Exception as e:
            logger.error(f"Error purging queue {queue_name}: {e}")
            return False
    
    # ==================== Specialized Message Sending ====================
    
    def send_provisioning_request(self, message: ProvisioningMessage) -> bool:
        """Send account provisioning request"""
        queue_message = QueueMessage(
            message_type="provisioning_request",
            payload=message.dict(),
            priority=8  # High priority
        )
        return self.send_message("provisioning", queue_message)
    
    def send_deployment_request(self, message: DeploymentMessage) -> bool:
        """Send deployment request"""
        queue_message = QueueMessage(
            message_type="deployment_request",
            payload=message.dict(),
            priority=7
        )
        return self.send_message("provisioning", queue_message)
    
    def send_monitoring_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Send monitoring alert"""
        queue_message = QueueMessage(
            message_type="monitoring_alert",
            payload=alert_data,
            priority=9  # Very high priority
        )
        return self.send_message("monitoring", queue_message)
    
    def send_cost_analysis_task(self, task_data: Dict[str, Any]) -> bool:
        """Send cost analysis task"""
        queue_message = QueueMessage(
            message_type="cost_analysis",
            payload=task_data,
            priority=5  # Normal priority
        )
        return self.send_message("cost_analysis", queue_message)
    
    def send_compliance_check(self, check_data: Dict[str, Any]) -> bool:
        """Send compliance check task"""
        queue_message = QueueMessage(
            message_type="compliance_check",
            payload=check_data,
            priority=6
        )
        return self.send_message("compliance_checks", queue_message)
    
    # ==================== Message Processing Loop ====================
    
    def start_worker(self, queue_name: str, poll_interval: int = 5):
        """
        Start a worker to continuously process messages (for demo/testing)
        In production, use Lambda triggers or ECS tasks
        """
        logger.info(f"Starting worker for queue: {queue_name}")
        
        while True:
            try:
                processed = self.process_messages(queue_name)
                if processed == 0:
                    time.sleep(poll_interval)
            except KeyboardInterrupt:
                logger.info("Worker stopped")
                break
            except Exception as e:
                logger.error(f"Worker error: {e}")
                time.sleep(poll_interval)
