import pytest
from unittest.mock import MagicMock
from backend.storage.models import Signal, Topic
from backend.trends.pulse_engine import TrendPulseEngine
import datetime

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_vs(monkeypatch):
    mock = MagicMock()
    mock.model.encode.return_value = [0.1] * 384
    monkeypatch.setattr("backend.trends.pulse_engine.VectorStore", lambda: mock)
    return mock

def test_trend_score_calculation(mock_db, mock_vs):
    engine = TrendPulseEngine(mock_db)
    now = datetime.datetime.utcnow()
    cluster = [
        Signal(title="Signal 1", source="blinkit", region="Indore", timestamp=now),
        Signal(title="Signal 2", source="reddit", region="Indore", timestamp=now),
        Signal(title="Signal 3", source="zepto", region="Mumbai", timestamp=now - datetime.timedelta(hours=8))
    ]
    score = engine.calculate_trend_score(cluster)
    assert score > 0
    assert score <= 100

def test_topic_naming(mock_db, mock_vs):
    engine = TrendPulseEngine(mock_db)
    cluster = [
        Signal(title="Heatwave in Indore spike demand"),
        Signal(title="Heatwave Indore towels cooling"),
        Signal(title="Indore heatwave cooling towels rise")
    ]
    name = engine.generate_topic_name(cluster)
    assert "Heatwave" in name
    assert "Indore" in name
