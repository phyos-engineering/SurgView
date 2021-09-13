from dataclasses import dataclass, field
import dataclasses
import json
import platform
import utils


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclass
class SessionLog:
    date: str
    serial_number: str = utils.get_serial_number()
    application_version: str = "0.01"

    # OS Info
    system_name: str = platform.system()
    system_release: str = platform.release()
    system_version: str = platform.version()

    # Python Info
    python_version: str = platform.python_version()

    mapped_interfaces: list = field(default_factory=lambda: [])
    luis_ai_responses: list = field(default_factory=lambda: [])
    mapped_workflows: list = field(default_factory=lambda: [])


@dataclass
class LuisResponse:
    luis_id: int
    time: str
    content: json
    # response_time: str


@dataclass
class MappedWorkflow:
    workflow_id: int
    luis_id: str
    interface_id: str
    time: str
    workflow: list
    # execution_time: str


@dataclass
class MappedInterface:
    interface_id: int
    time: str
    mapping: dict
    # execution_time: str
