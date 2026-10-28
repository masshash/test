# module_utils/timing.py
from datetime import datetime, timezone
import time
from typing import Any, NoReturn, Optional

from ansible.module_utils.basic import AnsibleModule


def _utc_iso(dt: datetime) -> str:
    return dt.isoformat(timespec="microseconds")


class ProcessTimer:
    """処理の開始時刻・終了時刻・経過秒数を計測し、結果に付与して返すクラス"""

    def __init__(self) -> None:
        self.process_started_at: datetime = datetime.now(timezone.utc)
        self._t0: float = time.monotonic()
        self._module: Optional[AnsibleModule] = None

    def set_module(self, module: AnsibleModule) -> None:
        self._module = module

    def _timing(self) -> dict[str, Any]:
        elapsed = time.monotonic() - self._t0
        finished_at = datetime.now(timezone.utc)
        return dict(
            process_started_at=_utc_iso(self.process_started_at),
            process_finished_at=_utc_iso(finished_at),
            process_elapsed_seconds=round(elapsed, 6),
        )

    def _require_module(self) -> AnsibleModule:
        if self._module is None:
            raise RuntimeError("module is not set. Call set_module() first.")
        return self._module

    def exit_json(self, **kwargs: Any) -> NoReturn:
        module = self._require_module()
        kwargs.update(self._timing())
        module.exit_json(**kwargs)

    def fail_json(self, msg: str, **kwargs: Any) -> NoReturn:
        module = self._require_module()
        kwargs.update(self._timing())
        module.fail_json(msg=msg, **kwargs)
