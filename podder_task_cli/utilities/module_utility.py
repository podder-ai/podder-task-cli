import sys
from importlib import import_module
from importlib.abc import MetaPathFinder
from importlib.util import spec_from_file_location
from pathlib import Path
from typing import Optional


class ModuleUtility(object):
    @staticmethod
    def import_module_from_file_location(path: Path,
                                         name: Optional[str] = None
                                         ) -> Optional[object]:
        # Ref: https://qiita.com/kzm4269/items/e7e67ab6c1dd278c3d16
        if name is None or name == "":
            name = path.stem

        class DynamicFinder(MetaPathFinder):
            @staticmethod
            def find_spec(fullname, *_):
                if fullname == name:
                    return spec_from_file_location(name, str(path))

        finder = DynamicFinder()
        sys.meta_path.insert(0, finder)
        try:
            return import_module(name)
        finally:
            sys.meta_path.remove(finder)

    def import_class_from_file_location(self, path: Path,
                                        class_name: str) -> Optional[object]:
        module = self.import_module_from_file_location(path)
        if hasattr(module, class_name):
            return getattr(module, class_name)

        return None
