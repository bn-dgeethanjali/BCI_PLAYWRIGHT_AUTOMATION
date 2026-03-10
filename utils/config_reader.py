import yaml
import os

def load_config(config_path=None):
    """
    Loads YAML config from the given path or from default location.
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), '../resources/playwright.config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
