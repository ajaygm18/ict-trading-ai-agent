"""
Custom Exceptions for ICT Trading AI Agent
"""

class ICTTradingError(Exception):
    """Base exception for ICT trading system"""
    pass

class DataError(ICTTradingError):
    """Data-related errors"""
    pass

class DataValidationError(DataError):
    """Data validation failed"""
    pass

class DataSourceError(DataError):
    """Data source unavailable or failed"""
    pass

class InsufficientDataError(DataError):
    """Not enough data for analysis"""
    pass

class ICTAnalysisError(ICTTradingError):
    """ICT pattern analysis errors"""
    pass

class PatternNotFoundError(ICTAnalysisError):
    """Required pattern not found"""
    pass

class InvalidPatternError(ICTAnalysisError):
    """Pattern validation failed"""
    pass

class MLError(ICTTradingError):
    """Machine learning errors"""
    pass

class ModelNotFoundError(MLError):
    """Model not found or not trained"""
    pass

class MLTrainingError(MLError):
    """Model training failed"""
    pass

class FeatureEngineeringError(MLError):
    """Feature engineering failed"""
    pass

class TradingError(ICTTradingError):
    """Trading execution errors"""
    pass

class RiskManagementError(TradingError):
    """Risk management violations"""
    pass

class ExecutionError(TradingError):
    """Trade execution failed"""
    pass

class PositionSizingError(TradingError):
    """Position sizing calculation failed"""
    pass

class BacktestError(ICTTradingError):
    """Backtesting errors"""
    pass

class PerformanceCalculationError(BacktestError):
    """Performance metric calculation failed"""
    pass

class ConfigurationError(ICTTradingError):
    """Configuration errors"""
    pass

class ValidationError(ICTTradingError):
    """General validation errors"""
    pass