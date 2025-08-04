import subprocess
import threading
import time
from typing import Union, Optional, Callable, Dict, List
from enum import Enum


class ProcessEvent(Enum):
    STARTED = "started"
    EXITED = "exited"
    ERROR = "error"
    TIMEOUT = "timeout"


class ProcessManager:

    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._hooks: Dict[ProcessEvent, List[Callable]] = {
            event: [] for event in ProcessEvent
        }
        self._is_monitoring = False

    def add_hook(self, event: ProcessEvent, callback: Callable) -> None:
        self._hooks[event].append(callback)

    def remove_hook(self, event: ProcessEvent, callback: Callable) -> bool:
        try:
            self._hooks[event].remove(callback)
            return True
        except ValueError:
            return False

    def _trigger_hooks(self, event: ProcessEvent, *args, **kwargs) -> None:
        for callback in self._hooks[event]:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"Hook callback error for {event.value}: {e}")

    def run_command(self, command: Union[str, list], wait_time: float = 1.0) -> bool:
        try:
            self.process = subprocess.Popen(command)
            time.sleep(wait_time)

            if self.process.poll() is None:
                self._trigger_hooks(ProcessEvent.STARTED, self.process)
                self._start_monitoring()
                return True
            else:
                self._trigger_hooks(ProcessEvent.EXITED, self.process.returncode)
                return False

        except Exception as e:
            self._trigger_hooks(ProcessEvent.ERROR, e)
            return False

    def _start_monitoring(self) -> None:
        if self._is_monitoring:
            return

        def monitor():
            self._is_monitoring = True
            try:
                if self.process:
                    return_code = self.process.wait()
                    self._trigger_hooks(ProcessEvent.EXITED, return_code)
            except Exception as e:
                self._trigger_hooks(ProcessEvent.ERROR, e)
            finally:
                self._is_monitoring = False

        self._monitor_thread = threading.Thread(target=monitor, daemon=True)
        self._monitor_thread.start()

    def terminate(self, timeout: float = 5.0) -> bool:
        if not self.process:
            return False

        try:
            self.process.terminate()

            try:
                self.process.wait(timeout=timeout)
                return True
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
                self._trigger_hooks(ProcessEvent.TIMEOUT)
                return True

        except Exception as e:
            self._trigger_hooks(ProcessEvent.ERROR, e)
            return False

    def wait(self, timeout: Optional[float] = None) -> Optional[int]:
        if self._monitor_thread and self._monitor_thread.is_alive():
            try:
                self._monitor_thread.join(timeout=timeout)
                if self._monitor_thread.is_alive():
                    print(f"Warning: Monitor thread still alive after {timeout}s timeout")
            except Exception as e:
                print(f"Error waiting for monitor thread: {e}")

        if self.process:
            return self.process.returncode
        return None

    def is_running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    @property
    def pid(self) -> Optional[int]:
        return self.process.pid if self.process else None

    @property
    def return_code(self) -> Optional[int]:
        return self.process.returncode if self.process else None
