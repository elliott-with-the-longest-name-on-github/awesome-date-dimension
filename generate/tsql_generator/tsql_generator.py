from script_generatior import ScriptGenerator, ScriptGeneratorConfig


class TSQLGenerator(ScriptGenerator):
    def __init__(self, config: ScriptGeneratorConfig):
        self._config = config

    def generate_scripts(self) -> None:
        self._generate_setup_scripts()
        self._generate_build_scripts()
        self._generate_refresh_procs()
        self._generate_table_constraints()

    def _generate_setup_scripts(self) -> None:
        raise NotImplementedError()

    def _generate_build_scripts(self) -> None:
        raise NotImplementedError()

    def _generate_refresh_procs(self) -> None:
        raise NotImplementedError()

    def _generate_table_constraints(self) -> None:
        raise NotImplementedError()
