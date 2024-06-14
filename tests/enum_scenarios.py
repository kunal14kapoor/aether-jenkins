
from collections import namedtuple


Scenario = namedtuple(
    "Scenario", "name in_path out_paths error_path config_path plugins_info_path"
)


def scenario_list(fixtures_dir, in_ext=".yaml", out_ext=".xml"):
    compound_dirs = set()
    if out_ext == ".xml":
        for path in fixtures_dir.rglob("expected-output.xml"):
            dir = path.parent
            compound_dirs.add(dir)
            yield Scenario(
                name=dir.stem,
                in_path=dir,
                out_paths=[path],
                error_path=dir / "expected.error",
                # When config file is missing it will still be passed and not None,
                # so JJBConfig will prefer it over system and user configs.
                config_path=dir / "test.conf",
                plugins_info_path=dir / "test.plugins_info.yaml",
            )
    for path in fixtures_dir.rglob(f"*{in_ext}"):
        if path.name.endswith("plugins_info.yaml"):
            continue
        if any(d in path.parents for d in compound_dirs):
            continue
        out_path = path.with_suffix(out_ext)
        out_path_list = list(fixtures_dir.rglob(out_path.name))
        yield Scenario(
            name=path.stem,
            in_path=path,
            out_paths=out_path_list,
            error_path=path.with_suffix(".error"),
            # When config file is missing it will still be passed and not None,
            # so JJBConfig will prefer it over system and user configs.
            config_path=path.with_suffix(".conf"),
            plugins_info_path=path.with_suffix(".plugins_info.yaml"),
        )
