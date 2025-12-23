"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

import os
import signal
import subprocess
from typing import List
from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

class CodeForm(FlaskForm):
    code = StringField(validators=[
        DataRequired(),
        Length(min=1, max=500, message="Code must not be empty and <=500 chars")
    ])
    timeout = IntegerField(validators=[
        DataRequired(),
        NumberRange(min=1, max=30, message="Timeout must be between 1 and 30 seconds")
    ])

def find_processes_using_port(port: int) -> List[int]:
    if not isinstance(port, int):
        raise ValueError("Port must be integer")

    command = ["lsof", "-i", f":{port}", "-t"]
    port_check_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    command_output, _ = port_check_process.communicate()

    process_ids: List[int] = []
    for line in command_output.splitlines():
        if line.isdigit():
            process_ids.append(int(line))

    return process_ids

def terminate_processes_on_port(port: int) -> None:
    process_ids = find_processes_using_port(port)
    for process_id in process_ids:
        try:
            os.kill(process_id, signal.SIGTERM)
        except ProcessLookupError:
            pass

def is_port_available(port: int) -> bool:
    return len(find_processes_using_port(port)) == 0

def execute_python_code(code: str, timeout: int) -> dict:
    command = ["prlimit", "--nproc=1:1", "python3", "-c", code]
    code_execution_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        standard_output, standard_error = code_execution_process.communicate(timeout=timeout)
        return {
            "output": standard_output,
            "error": standard_error,
            "timeout": False
        }
    except subprocess.TimeoutExpired:
        code_execution_process.kill()
        standard_output, _ = code_execution_process.communicate()
        return {
            "output": standard_output,
            "error": "Execution exceeded timeout limit",
            "timeout": True
        }

@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()

    if not form.validate_on_submit():
        return jsonify({"error": "Invalid input", "details": form.errors}), 400

    python_code = form.code.data
    timeout_seconds = form.timeout.data

    if any(symbol in python_code for symbol in [';', '&&', '||']):
        return jsonify({"error": "Unsafe code detected"}), 400

    execution_result = execute_python_code(python_code, timeout_seconds)

    if execution_result["timeout"]:
        return jsonify({
            "error": "Timeout",
            "output": execution_result["output"],
            "message": execution_result["error"]
        }), 408

    return jsonify({
        "output": execution_result["output"],
        "errors": execution_result["error"]
    })

if __name__ == '__main__':
    run_port = 5000
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        terminate_processes_on_port(run_port)
    app.run(port=run_port, debug=True, host = "0.0.0.0")
