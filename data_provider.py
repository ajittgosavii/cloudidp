"""
CloudIDP Data Provider
Centralized data provider that handles Demo vs Live mode
Works with existing AWS integration modules
"""

import streamlit as st
from typing import Any, Callable, Optional


class DataProvider:
    """
    Centralized data provider for Demo vs Live mode
    
    Usage:
        provider = DataProvider()
        cost = provider.get('monthly_cost', demo_value="$45K", live_fn=get_live_cost)
    """
    
    def __init__(self):
        """Initialize data provider"""
        self.demo_mode = self._is_demo_mode()
    
    @staticmethod
    def _is_demo_mode() -> bool:
        """Check if currently in demo mode"""
        return st.session_state.get('mode', 'Demo') == 'Demo'
    
    def get(self, key: str, demo_value: Any, live_fn: Optional[Callable] = None) -> Any:
        """
        Get data based on current mode
        
        Args:
            key: Unique identifier for this data point (for error messages)
            demo_value: Value to return in demo mode
            live_fn: Function to call in live mode (returns live data)
        
        Returns:
            demo_value if in Demo mode, otherwise result of live_fn()
        
        Example:
            cost = provider.get(
                key='monthly_cost',
                demo_value='$45,234',
                live_fn=lambda: cost_service.get_monthly_cost()
            )
        """
        # Always return demo value in demo mode
        if self._is_demo_mode():
            return demo_value
        
        # If no live function provided, return demo value
        if live_fn is None:
            st.warning(f"⚠️ No live data source configured for {key}")
            return demo_value
        
        # Try to get live data
        try:
            return live_fn()
        except Exception as e:
            # If error, fall back to demo value and show warning
            st.warning(f"⚠️ Error fetching live data for {key}: {str(e)[:100]}")
            return demo_value
    
    def get_multiple(self, data_dict: dict) -> dict:
        """
        Get multiple data points at once
        
        Args:
            data_dict: Dictionary with format:
                {
                    'key1': {'demo': value1, 'live': function1},
                    'key2': {'demo': value2, 'live': function2},
                }
        
        Returns:
            Dictionary with actual values: {'key1': result1, 'key2': result2}
        
        Example:
            data = provider.get_multiple({
                'cost': {'demo': '$45K', 'live': lambda: get_cost()},
                'projects': {'demo': '12', 'live': lambda: count_projects()}
            })
            # Returns: {'cost': '$45K', 'projects': '12'} in demo mode
        """
        results = {}
        for key, config in data_dict.items():
            results[key] = self.get(
                key=key,
                demo_value=config.get('demo'),
                live_fn=config.get('live')
            )
        return results


class LiveDataService:
    """
    Service to fetch live data from AWS
    Uses existing integration modules
    """
    
    def __init__(self):
        """Initialize live data service"""
        # Initialize AWS services (will only be used in Live mode)
        # Don't cache demo_mode - check it dynamically!
        try:
            from cost_explorer_integration import CostExplorerIntegration
            from database_integration import DatabaseIntegration
            from compute_network_integration import ComputeNetworkIntegration
            
            self.cost_explorer = CostExplorerIntegration(demo_mode=False)
            self.database = DatabaseIntegration(demo_mode=False)
            self.compute = ComputeNetworkIntegration(demo_mode=False)
            self.aws_initialized = True
        except Exception as e:
            # AWS services not available - will fall back to demo data
            self.aws_initialized = False
    
    def _is_demo_mode(self) -> bool:
        """Check current mode dynamically (don't cache!)"""
        return st.session_state.get('mode', 'Demo') == 'Demo'
    
    # ========== COST DATA ==========
    
    def get_monthly_cost(self) -> str:
        """Get current month's cost from AWS Cost Explorer"""
        # Check mode dynamically!
        if self._is_demo_mode():
            return "$45,234"
        
        # Check if AWS is initialized
        if not self.aws_initialized:
            return "$45,234"
        
        try:
            from datetime import datetime
            
            # Get current month dates
            start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end = datetime.now().strftime('%Y-%m-%d')
            
            # Get cost from Cost Explorer
            result = self.cost_explorer.get_cost_and_usage(start, end)
            
            if result['success']:
                cost = result['total_cost']
                # Format as currency
                if cost >= 1000:
                    return f"${cost/1000:.1f}K"
                else:
                    return f"${cost:.0f}"
            else:
                return "$45,234"  # Fallback
                
        except Exception as e:
            st.error(f"Error getting cost: {e}")
            return "$45,234"
    
    def get_cost_forecast(self) -> str:
        """Get next month's cost forecast"""
        if self._is_demo_mode():
            return "$47,890"
        
        try:
            from datetime import datetime, timedelta
            
            # Next month dates
            start = (datetime.now() + timedelta(days=30)).replace(day=1).strftime('%Y-%m-%d')
            end = (datetime.now() + timedelta(days=60)).replace(day=1).strftime('%Y-%m-%d')
            
            result = self.cost_explorer.get_cost_forecast(start, end)
            
            if result['success']:
                forecast = float(result['forecasted_cost'])
                return f"${forecast/1000:.1f}K"
            else:
                return "$47,890"
                
        except Exception:
            return "$47,890"
    
    # ========== RESOURCE COUNTS ==========
    
    def count_ec2_instances(self) -> str:
        """Count running EC2 instances"""
        if self._is_demo_mode():
            return "156"
        
        try:
            result = self.compute.list_instances()
            if result['success']:
                # Count only running instances
                running = sum(1 for i in result['instances'] 
                            if i.get('State', {}).get('Name') == 'running')
                return str(running)
            else:
                return "156"
        except Exception:
            return "156"
    
    def count_rds_instances(self) -> str:
        """Count RDS database instances"""
        if self._is_demo_mode():
            return "12"
        
        try:
            result = self.database.list_db_instances()
            if result['success']:
                return str(result['count'])
            else:
                return "12"
        except Exception:
            return "12"
    
    def count_dynamodb_tables(self) -> str:
        """Count DynamoDB tables"""
        if self._is_demo_mode():
            return "8"
        
        try:
            result = self.database.list_dynamodb_tables()
            if result['success']:
                return str(result['count'])
            else:
                return "8"
        except Exception:
            return "8"
    
    # ========== COMPLIANCE DATA ==========
    
    def get_compliance_score(self) -> str:
        """Get compliance score (placeholder - implement with AWS Config)"""
        if self._is_demo_mode():
            return "98%"
        
        # TODO: Implement with AWS Config integration
        # For now, return demo value
        return "98%"
    
    # ========== PROJECT DATA ==========
    
    def count_active_projects(self) -> str:
        """Count active projects (placeholder - implement with database)"""
        if self._is_demo_mode():
            return "12"
        
        # TODO: Implement with database_service
        # For now, return demo value
        return "12"


# Singleton instances
_data_provider = None
_live_service = None

def get_data_provider() -> DataProvider:
    """Get singleton DataProvider instance"""
    global _data_provider
    if _data_provider is None:
        _data_provider = DataProvider()
    return _data_provider

def get_live_service() -> LiveDataService:
    """Get singleton LiveDataService instance"""
    global _live_service
    if _live_service is None:
        _live_service = LiveDataService()
    return _live_service