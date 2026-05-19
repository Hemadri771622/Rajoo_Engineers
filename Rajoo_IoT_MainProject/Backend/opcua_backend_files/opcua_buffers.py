# app/services/opcua_buffers.py

from collections import deque

# Number of points visible on charts
MAX_POINTS = 30

# All live trends come from OPC UA and are stored here (RAM only)
opcua_trends = {
    "ibc_temp": {
        "in": deque(maxlen=MAX_POINTS),
        "out": deque(maxlen=MAX_POINTS),
    },
    "line_speed": {
        "set": deque(maxlen=MAX_POINTS),
        "actual": deque(maxlen=MAX_POINTS),
    },
    "thickness": {
        "set": deque(maxlen=MAX_POINTS),
        "actual": deque(maxlen=MAX_POINTS),
    }
}
