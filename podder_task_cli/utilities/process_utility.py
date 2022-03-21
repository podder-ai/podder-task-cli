class ProcessUtility(object):
    object_types = {
        'Dictionary': {
            "empty": "{}",
            "package": None,
        },
        'Array': {
            "empty": "[]",
            "package": None,
        },
        'Image': {
            "empty":
            "None",
            "package":
            "git+ssh://git@github.com:podder-ai/podder-task-foundation-objects-image.git",
        },
        'CSV': {
            "empty": "[]",
            "package": None,
        },
        'PDF': {
            "empty": "None",
            "package": None,
        },
    }

    @staticmethod
    def generate_input_code(name: str, object_type: str) -> [str]:
        return [
            "{} = input_payload.get(name=\"{}\", object_type=\"{}\")".format(
                name, name, object_type.lower())
        ]

    def generate_output_code(self, name: str, object_type: str) -> [str]:
        return [
            "# please set data for output",
            "{} = {}".format(name, self.object_types[object_type]["empty"]),
            "output_payload.add_{}({}, name=\"{}\")".format(
                object_type.lower(), name, name)
        ]
