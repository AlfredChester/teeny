from teeny.value import Env, Number, String, Table, Error, ValError, BuiltinClosure, \
                        makeTable, makeObject, Value
import math
from pathlib import Path
import json

srcPath = Path(__file__).parent.parent.parent / "example"

Math = Table({
    String(value = "pi"): Number(value = math.pi), String(value = "e"): Number(value = math.e)
})
Err = Table({
    String(value = "_call_"): BuiltinClosure(fn = lambda typ, message: ValError(typ = typ, value = message)),
    String(value = "panic"): BuiltinClosure(fn = lambda err: Error({}, err.typ, err.value)),
    String(value = "raise"): BuiltinClosure(fn = lambda typ, message: Error({}, typ, message))
})

def read(path: String, isJson = False) -> String | Table:
    pth: str = srcPath / path.value
    res: str = ""
    try:
        res = open(pth, "r").read()
        if isJson:
            res = json.loads(res)
    except:
        return Error({}, "IOError", "Error when reading from file")
    if not isJson:
        return String(res)
    else:
        return makeTable(res)
def write(path: String, content: Value, isJson = False):
    pth: str = srcPath / path.value
    cont: str = content.value if not isJson else json.dumps(makeObject(content))
    try:
        open(pth, "w").write(cont)
    except:
        return Error({}, "IOError", "Error when writing to file")
    return content
Fs = Table({
    String(value = "readText"): BuiltinClosure(fn = lambda path: read(path, False)),
    String(value = "writeText"): BuiltinClosure(fn = lambda path, content: write(path, content, False)),
    String(value = "readJson"): BuiltinClosure(fn = lambda path: read(path, True)),
    String(value = "writeJson"): BuiltinClosure(fn = lambda path, content: write(path, content, True))
})

def Import(name: String) -> Table:
    code = open(srcPath / name.value).read()
    from teeny.runner import run
    res = run(code)
    return res.get("export")

def Mix(table: Table, env: Env):
    for key in table.value.keys():
        if isinstance(key, String):
            env.define(key.value, table.get(key))

def makeGlobal() -> Env:
    gEnv = Env()
    gEnv.update({
        "math": Math,
        "print": BuiltinClosure(fn = lambda *x: print(*x, sep = '', end = '')),
        "input": BuiltinClosure(fn = lambda: input("")),
        "export": Table(value = {}),
        "import": BuiltinClosure(fn = Import),
        "mix": BuiltinClosure(fn = Mix, hasEnv = True),
        "include": BuiltinClosure(fn = lambda name, env: Mix(Import(name), env), hasEnv = True),
        "error": Err,
        "fs": Fs
    })
    return gEnv