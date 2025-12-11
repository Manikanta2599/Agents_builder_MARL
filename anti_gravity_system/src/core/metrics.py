from typing import Dict, Any, List
import time
from dataclasses import dataclass, field
from anti_gravity_system.src.utils.logger import logger

@dataclass
class MetricRecord:
    metric_name: str
    value: float
    unit: str
    tags: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

class MetricsTracker:
    def __init__(self):
        self.records: List[MetricRecord] = []
        self.start_times: Dict[str, float] = {}
        logger.info("MetricsTracker initialized")

    def start_timer(self, operation_id: str):
        self.start_times[operation_id] = time.time()

    def stop_timer(self, operation_id: str, metric_name: str = "latency", tags: Dict[str, str] = None):
        if operation_id in self.start_times:
            duration = time.time() - self.start_times.pop(operation_id)
            self.record_metric(metric_name, duration, "seconds", tags)

    def record_metric(self, name: str, value: float, unit: str, tags: Dict[str, str] = None):
        record = MetricRecord(name, value, unit, tags or {})
        self.records.append(record)
        # Log critical metrics
        if name in ["error_count", "cost"]:
            logger.info(f"Metric: {name}={value}{unit} {tags}")

    def get_summary(self) -> Dict[str, Any]:
        summary = {
            "total_latency": 0.0,
            "total_cost": 0.0,
            "total_errors": 0,
            "tasks_completed": 0
        }
        
        for r in self.records:
            if r.metric_name == "latency":
                summary["total_latency"] += r.value
            elif r.metric_name == "cost":
                summary["total_cost"] += r.value
            elif r.metric_name == "error_count":
                summary["total_errors"] += int(r.value)
            elif r.metric_name == "task_completion":
                summary["tasks_completed"] += int(r.value)
                
        return summary
