from ..state.schema import AgentState, WorkingMemoryItem
from ..utils.time import current_timestamp
from ..memory import store
from . import nlp


def ingest_message(text: str, state: AgentState) -> dict:
    intent = nlp.detect_intent(text)
    emotion = nlp.detect_emotion(text)
    timestamp = current_timestamp()
    event = {"content": text, "intent": intent, "emotion": emotion, "timestamp": timestamp}
    store.write_event(event)
    state.working_memory.append(WorkingMemoryItem(content=text, timestamp=timestamp))
    return event
