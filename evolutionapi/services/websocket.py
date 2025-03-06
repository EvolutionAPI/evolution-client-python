import socketio
from typing import Callable, Dict, Any
import logging
import time
from typing import Optional
from ..models.websocket import WebSocketConfig, WebSocketInfo

class WebSocketService:
    def __init__(self, client):
        self.client = client

    def set_websocket(self, instance_id: str, config: WebSocketConfig, instance_token: str):
        """
        Configure WebSocket settings for an instance
        
        Args:
            instance_id (str): The instance ID
            config (WebSocketConfig): The WebSocket configuration
            instance_token (str): The instance token
            
        Returns:
            dict: The response from the API
        """
        return self.client.post(
            f'websocket/set/{instance_id}',
            data=config.__dict__,
            instance_token=instance_token
        )

    def find_websocket(self, instance_id: str, instance_token: str) -> WebSocketInfo:
        """
        Get WebSocket settings for an instance
        
        Args:
            instance_id (str): The instance ID
            instance_token (str): The instance token
            
        Returns:
            WebSocketInfo: The WebSocket information
        """
        response = self.client.get(
            f'websocket/find/{instance_id}',
            instance_token=instance_token
        )
        return WebSocketInfo(**response)

class WebSocketManager:
    def __init__(self, base_url: str, instance_id: str, api_token: str, max_retries: int = 5, retry_delay: float = 1.0):
        """
        Initialize the WebSocket manager
        
        Args:
            base_url (str): Base URL of the API
            instance_id (str): Instance ID
            api_token (str): API authentication token
            max_retries (int): Maximum number of reconnection attempts
            retry_delay (float): Initial delay between attempts in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.instance_id = instance_id
        self.api_token = api_token
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_count = 0
        self.should_reconnect = True
        
        # Socket.IO configuration
        self.sio = socketio.Client(
            ssl_verify=False,  # For local development
            logger=False,
            engineio_logger=False,
            request_timeout=30
        )
        
        # Configure class logger to INFO
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Dictionary to store registered handlers
        self._handlers = {}
        
        # Configure event handlers
        self.sio.on('connect', self._on_connect)
        self.sio.on('disconnect', self._on_disconnect)
        self.sio.on('error', self._on_error)
        
        # Register global handler in instance-specific namespace
        self.sio.on('*', self._handle_event, namespace=f'/{self.instance_id}')
    
    def _on_connect(self):
        """Handler for connection event"""
        self.logger.info("Socket.IO connected")
        self.retry_count = 0  # Reset retry counter after successful connection
    
    def _on_disconnect(self):
        """Handler for disconnection event"""
        self.logger.warning(f"Socket.IO disconnected. Attempt {self.retry_count + 1}/{self.max_retries}")
        if self.should_reconnect and self.retry_count < self.max_retries:
            self._attempt_reconnect()
        else:
            self.logger.error("Maximum number of reconnection attempts reached")
    
    def _on_error(self, error):
        """Handler for error events"""
        self.logger.error(f"Socket.IO error: {str(error)}", exc_info=True)
    
    def _attempt_reconnect(self):
        """Attempt to reconnect with exponential backoff"""
        try:
            delay = self.retry_delay * (2 ** self.retry_count)  # Exponential backoff
            self.logger.info(f"Attempting to reconnect in {delay:.2f} seconds...")
            time.sleep(delay)
            self.connect()
            self.retry_count += 1
        except Exception as e:
            self.logger.error(f"Error during reconnection attempt: {str(e)}", exc_info=True)
            if self.retry_count < self.max_retries:
                self._attempt_reconnect()
            else:
                self.logger.error("All reconnection attempts failed")
    
    def _handle_event(self, event, *args):
        """Global handler for all events"""
        # Only process registered events
        if event in self._handlers:
            self.logger.debug(f"Event received in namespace /{self.instance_id}: {event}")
            self.logger.debug(f"Event data: {args}")
            
            try:
                # Extract event data
                raw_data = args[0] if args else {}
                
                # Ensure we're passing the correct object to the callback
                if isinstance(raw_data, dict):
                    self.logger.debug(f"Calling handler for {event} with data: {raw_data}")
                    self._handlers[event](raw_data)
                else:
                    self.logger.error(f"Invalid data received for event {event}: {raw_data}")
            except Exception as e:
                self.logger.error(f"Error processing event {event}: {str(e)}", exc_info=True)
    
    def connect(self):
        """Connect to Socket.IO server"""
        try:
            # Connect only to instance namespace with authentication header
            self.sio.connect(
                f"{self.base_url}?apikey={self.api_token}",
                transports=['websocket'],
                namespaces=[f'/{self.instance_id}'],
                wait_timeout=30
            )
            
            # Join instance-specific room
            self.sio.emit('subscribe', {'instance': self.instance_id}, namespace=f'/{self.instance_id}')
            
        except Exception as e:
            self.logger.error(f"Error connecting to Socket.IO: {str(e)}", exc_info=True)
            raise
    
    def disconnect(self):
        """Disconnect from Socket.IO server"""
        self.should_reconnect = False  # Prevent reconnection attempts
        if self.sio.connected:
            self.sio.disconnect()
    
    def on(self, event: str, callback: Callable):
        """
        Register a callback for a specific event
        
        Args:
            event (str): Event name
            callback (Callable): Function to be called when the event occurs
        """
        self._handlers[event] = callback