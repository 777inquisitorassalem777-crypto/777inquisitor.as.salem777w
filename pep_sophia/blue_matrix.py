"""
Голубая Матрица — абстрактный интерфейс к физическим / виртуальным сенсорам.
Преобразует сырые сенсорные данные в сигналы, понятные SophiaEngine.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import random
from .state import SophiaState


@dataclass
class SensorReading:
    sensor_id: str
    modality: str          # vision, audio, proprioception, environment, ethical_field
    value: float           # нормализованное [-1 .. 1] или [0 .. 1]
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    raw_note: str = ""


class BlueMatrix:
    """
    Интерфейс «Голубая Матрица».
    В реальной системе здесь были бы драйверы камер, лидаров, микрофонов и т.д.
    Здесь — симуляция + нормализация сигналов для ядра.
    """

    def __init__(self, state: SophiaState):
        self.state = state
        self.sensor_history: List[SensorReading] = []
        self.active_sensors = {
            "vision_front": 0.8,
            "audio_ambient": 0.6,
            "proprioception": 0.9,
            "environment_temp": 0.7,
            "ethical_field": 0.75,      # мета-сенсор «поля добра/зла»
            "human_presence": 0.5,
        }

    def read_all(self) -> List[SensorReading]:
        """Считывает все активные сенсоры (симуляция)."""
        readings = []
        for sid, base_conf in self.active_sensors.items():
            modality = sid.split("_")[0]
            # Симуляция значений с небольшим шумом
            value = random.uniform(-0.4, 0.7) * (0.6 + self.state.pneuma * 0.4)
            conf = min(1.0, base_conf + random.uniform(-0.1, 0.1))
            reading = SensorReading(
                sensor_id=sid,
                modality=modality,
                value=round(value, 3),
                confidence=round(conf, 3),
                raw_note=f"sim-{modality}"
            )
            readings.append(reading)
            self.sensor_history.append(reading)

        if len(self.sensor_history) > 300:
            self.sensor_history = self.sensor_history[-300:]
        return readings

    def to_signals(self, readings: Optional[List[SensorReading]] = None) -> Dict[str, float]:
        """
        Преобразует сенсорные данные в сигналы для evolve().
        Возвращает:
            - aggregate_signal
            - risk_estimate
            - ethical_field_signal
        """
        if readings is None:
            readings = self.read_all()

        if not readings:
            return {"aggregate_signal": 0.0, "risk_estimate": 0.3, "ethical_field_signal": 0.0}

        # Агрегация
        values = [r.value * r.confidence for r in readings]
        aggregate = sum(values) / len(values)

        # Оценка риска (высокая неопределённость или негативный ethical_field)
        ethical_vals = [r.value for r in readings if r.sensor_id == "ethical_field"]
        ethical_signal = ethical_vals[0] if ethical_vals else 0.0

        risk = 0.2
        if self.state.uncertainty > 0.6:
            risk += 0.25
        if ethical_signal < -0.2:
            risk += 0.3
        risk = min(1.0, risk)

        return {
            "aggregate_signal": round(max(-1.0, min(1.0, aggregate)), 3),
            "risk_estimate": round(risk, 3),
            "ethical_field_signal": round(ethical_signal, 3),
            "num_sensors": len(readings)
        }

    def inject_real_reading(self, sensor_id: str, value: float, confidence: float = 0.9, note: str = ""):
        """Позволяет подать реальные данные извне (для будущей интеграции)."""
        modality = sensor_id.split("_")[0] if "_" in sensor_id else "custom"
        reading = SensorReading(
            sensor_id=sensor_id,
            modality=modality,
            value=max(-1.0, min(1.0, value)),
            confidence=max(0.0, min(1.0, confidence)),
            raw_note=note or "external"
        )
        self.sensor_history.append(reading)
        return reading

    def status(self) -> Dict[str, Any]:
        return {
            "active_sensors": list(self.active_sensors.keys()),
            "history_length": len(self.sensor_history),
            "last_readings": [
                {"id": r.sensor_id, "value": r.value, "conf": r.confidence}
                for r in self.sensor_history[-5:]
            ]
        }
