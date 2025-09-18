"""
Production Configuration for ICT Trading AI Agent
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
from pydantic import BaseSettings, validator
import logging

class Config(BaseSettings):
    """Main configuration with validation"""
    
    # Trading parameters
    INITIAL_CAPITAL: float = 100000.0
    MAX_DAILY_LOSS_PCT: float = 2.0
    MAX_POSITION_RISK_PCT: float = 1.0
    MAX_PORTFOLIO_RISK_PCT: float = 5.0
    MAX_CONCURRENT_TRADES: int = 5
    MIN_RISK_REWARD_RATIO: float = 1.5
    
    # ICT parameters
    SWING_LOOKBACK: int = 5
    LIQUIDITY_THRESHOLD_PCT: float = 0.1
    MIN_CONFLUENCE_SCORE: float = 0.6
    FVG_MIN_SIZE_PCT: float = 0.3
    OB_MIN_IMPULSE_PCT: float = 2.0
    
    # ML parameters
    FEATURE_SELECTION_K: int = 50
    MODEL_RETRAIN_DAYS: int = 30
    MIN_TRAINING_SAMPLES: int = 5000
    VALIDATION_SPLIT: float = 0.2
    LSTM_SEQUENCE_LENGTH: int = 60
    
    # Data parameters
    DATA_CACHE_TTL: int = 300
    MAX_DATA_AGE_HOURS: int = 24
    REQUIRED_DATA_POINTS: int = 200
    DEFAULT_LOOKBACK_DAYS: int = 30
    
    # API keys
    ALPACA_API_KEY: str = os.getenv("ALPACA_API_KEY", "")
    ALPACA_SECRET_KEY: str = os.getenv("ALPACA_SECRET_KEY", "")
    ALPACA_BASE_URL: str = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
    POLYGON_API_KEY: str = os.getenv("POLYGON_API_KEY", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///ict_trading.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # System
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    TIMEZONE: str = "America/New_York"
    MAX_WORKERS: int = 4
    ENABLE_PAPER_TRADING: bool = True
    
    @validator('INITIAL_CAPITAL')
    def validate_capital(cls, v):
        if v <= 0:
            raise ValueError("Initial capital must be positive")
        return v
    
    @validator('MAX_DAILY_LOSS_PCT')
    def validate_daily_loss(cls, v):
        if not 0 < v <= 10:
            raise ValueError("Daily loss % must be between 0 and 10")
        return v
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@dataclass
class TradingSession:
    """Trading session definitions"""
    name: str
    start_time: str  # "HH:MM" format
    end_time: str
    timezone: str = "America/New_York"
    active: bool = True

# Trading sessions for US markets
TRADING_SESSIONS = {
    "premarket": TradingSession("premarket", "04:00", "09:30"),
    "market_open": TradingSession("market_open", "09:30", "10:30"),
    "morning": TradingSession("morning", "09:30", "12:00"),
    "lunch": TradingSession("lunch", "12:00", "13:30"),
    "afternoon": TradingSession("afternoon", "13:30", "15:00"),
    "power_hour": TradingSession("power_hour", "15:00", "16:00"),
    "afterhours": TradingSession("afterhours", "16:00", "20:00")
}

# ICT Strategy configurations
STRATEGY_CONFIGS = {
    "silver_bullet": {
        "window_start": "09:45",
        "window_end": "10:00",
        "min_displacement_pct": 1.5,
        "fvg_mitigation_pct": 50.0
    },
    "turtle_soup": {
        "lookback_days": 20,
        "min_breakout_pct": 0.5,
        "max_reversal_hours": 4
    },
    "power_of_3": {
        "accumulation_volume_threshold": 1.2,
        "manipulation_volatility_threshold": 0.03,
        "distribution_volume_threshold": 1.5
    },
    "smt_divergence": {
        "correlation_window": 20,
        "divergence_threshold": 0.02,
        "min_correlation": 0.7
    }
}

# Symbol universe for different strategies
SYMBOL_UNIVERSE = {
    "large_cap": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "JNJ", "V"],
    "etfs": ["SPY", "QQQ", "IWM", "DIA", "VTI", "XLF", "XLK", "XLV", "XLE", "XLI"],
    "forex_majors": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD"],
    "crypto": ["BTC-USD", "ETH-USD", "ADA-USD", "DOT-USD", "SOL-USD"]
}

# Global configuration instance
config = Config()

def get_logger(name: str) -> logging.Logger:
    """Get configured logger"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, config.LOG_LEVEL))
    return logger