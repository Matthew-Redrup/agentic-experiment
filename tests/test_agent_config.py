import pytest
from agentic_edu.agents.agent_config import (
    create_func_map,
    build_function_map_run_sql,
    function_map_write_file,
    function_map_write_json_file,
    function_map_write_yaml_file,
)
from agentic_edu.modules.db import PostgresManager


def test_create_func_map():
    # Dummy function for testing
    def dummy_func():
        pass

    func_name = "dummy_func"
    func_map = create_func_map(func_name, dummy_func)

    assert isinstance(func_map, dict)
    assert func_name in func_map
    assert func_map[func_name] == dummy_func


def test_build_function_map_run_sql():
    db = PostgresManager()
    func_map = build_function_map_run_sql(db)

    assert isinstance(func_map, dict)
    assert "run_sql" in func_map
    assert callable(func_map["run_sql"])


def test_function_map_write_file():
    assert isinstance(function_map_write_file, dict)
    assert "write_file" in function_map_write_file
    assert callable(function_map_write_file["write_file"])


def test_function_map_write_json_file():
    assert isinstance(function_map_write_json_file, dict)
    assert "write_json_file" in function_map_write_json_file
    assert callable(function_map_write_json_file["write_json_file"])


def test_function_map_write_yaml_file():
    assert isinstance(function_map_write_yaml_file, dict)
    assert "write_yaml_file" in function_map_write_yaml_file
    assert callable(function_map_write_yaml_file["write_yaml_file"])
