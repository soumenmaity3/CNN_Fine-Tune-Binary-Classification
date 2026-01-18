import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration manager for the CNN fine-tuning project."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration from YAML file.
        
        Args:
            config_path: Path to config YAML file. Defaults to configs/default.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "configs" / "default.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def __getitem__(self, key):
        """Access config values using dictionary syntax."""
        return self.config[key]
    
    def __repr__(self):
        """String representation of configuration."""
        return f"Config({self.config_path})"
