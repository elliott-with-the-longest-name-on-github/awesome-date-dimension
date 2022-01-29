from enum import Enum, auto


class Language(Enum):
    TSQL = auto()


class ScriptGeneratorFactory():
    def __init__(self, language: Language):
        self.script_generators = {
            Language.TSQL: ''
        }

        generator = self.script_generators.get(language)
        if generator is None:
            raise NotImplementedError(
                'The provided language does not have an implemented ScriptGenerator.')
