import platform
import subprocess
from typing import Optional


class PlatformUtility(object):
    class Platform(object):
        MacOS = "macos"
        RedHat = "redhat"
        Debian = "debian"
        Windows = "windows"
        Unknown = "unknown"

    def get_platform(self) -> Optional[str]:
        platform_name = platform.system().lower()
        if platform_name == "darwin":
            return self.Platform.MacOS
        if platform_name == "linux":
            if self.detect_command("yum"):
                return self.Platform.RedHat
            if self.detect_command("apt"):
                return self.Platform.Debian
        if platform_name == "windows":
            return self.Platform.Windows

        return self.Platform.Unknown

    @staticmethod
    def detect_command(command: str) -> bool:
        result = subprocess.run(["which", command], capture_output=True)
        return result.stdout != ""
