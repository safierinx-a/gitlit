from typing import Optional, Dict, Any
import numpy as np
from .base import BasePattern


class TransitionManager:
    """Manages smooth transitions between patterns"""

    def __init__(self):
        self.current_pattern: Optional[BasePattern] = None
        self.next_pattern: Optional[BasePattern] = None
        self.transition_progress: float = 0.0
        self.transition_duration: float = 1000.0  # ms

    def preserve_state(
        self, from_pattern: BasePattern, to_pattern: BasePattern
    ) -> None:
        """Complete state preservation between patterns"""
        # Copy timing information
        to_pattern.state.time_offset = from_pattern.state.time_offset
        to_pattern.state.last_frame_time = from_pattern.state.last_frame_time
        to_pattern.state.delta_time = from_pattern.state.delta_time
        to_pattern.state.frame_count = from_pattern.state.frame_count

        # Copy shared cached data
        shared_keys = [
            "last_color",
            "last_brightness",
            "last_speed",
            "last_position",
            "last_wavelength",
            "last_size",
            "last_fade",
            "last_density",
        ]

        for key in shared_keys:
            if key in from_pattern.state.cached_data:
                to_pattern.state.cache_value(key, from_pattern.state.cached_data[key])

        # Copy performance metrics
        to_pattern.state.frame_times = from_pattern.state.frame_times.copy()
        to_pattern.state.avg_frame_time = from_pattern.state.avg_frame_time

        # Mark as transitioning
        to_pattern.state.is_transitioning = True

        # Copy parameters that should persist
        persist_params = ["brightness", "speed", "color"]
        for param in persist_params:
            if param in from_pattern.state.parameters:
                to_pattern.state.parameters[param] = from_pattern.state.parameters[
                    param
                ]
