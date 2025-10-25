from teeny.value import Env, Number, String, Table, Error, ValError, BuiltinClosure, \
                        makeTable, makeObject, Value, Nil
import math
from pathlib import Path
import json
import os
import shutil

srcPath = Path(__file__).parent.parent.parent / "example"

Math = Table({
    String(value = "pi"): Number(value = math.pi), String(value = "e"): Number(value = math.e)
})
Err = Table({
    String(value = "_call_"): BuiltinClosure(fn = lambda typ, message: ValError(typ = typ, value = message)),
    String(value = "panic"): BuiltinClosure(fn = lambda err: Error({}, err.typ, err.value)),
    String(value = "raise"): BuiltinClosure(fn = lambda typ, message: Error({}, typ, message))
})

def read(path: String, isJson = False, lines = False) -> String | Table:
    pth: str = srcPath / path.value
    res: str = ""
    print(pth, path.value)
    try:
        res = open(pth, "r").read()
        if isJson:
            res = json.loads(res)
    except Exception as e:
        print(e)
        return Error({}, "IOError", "Error when reading from file")
    if not isJson:
        if not lines:
            return String(res)
        else:
            rs = Table({})
            for item in res.splitlines():
                rs.append(String(value = item))
            return rs
    else:
        return makeTable(res)
def write(path: String, content: Value, isJson = False, lines = False, append = Number(0)) -> Value:
    pth: str = srcPath / path.value
    cont: str = (content.value if not lines else '\n'.join(content.toList())) if not isJson else json.dumps(makeObject(content))
    num: bool = bool(append.value)
    try:
        open(pth, ("w" if not num else "a")).write(cont)
    except:
        return Error({}, "IOError", "Error when writing to file")
    return content
def exists(path: String) -> Number:
    pth: str = srcPath / path.value
    return Number(value = int(os.path.exists(pth)))
def listDir(path: String) -> Table:
    pth: str = srcPath / path.value
    lis = os.listdir(pth)
    res = Table({})
    for item in lis:
        res.append(String(value = item))
    return res
def isFile(path: String) -> Number:
    pth: str = srcPath / path.value
    res = os.path.isfile(pth)
    return Number(value = int(res))
def isDir(path: String) -> Number:
    pth: str = srcPath / path.value
    res = os.path.isdir(pth)
    return Number(value = int(res))
def copy(src: String, dst: String) -> Nil:
    pthSrc: str = srcPath / src
    pthDst: str = srcPath / dst
    shutil.copy2(pthSrc, pthDst)
    return Nil()
def move(src: String, dst: String) -> Nil:
    pthSrc: str = srcPath / src
    pthDst: str = srcPath / dst
    shutil.move(pthSrc, pthDst)
    return Nil()
def join(table: Table) -> String:
    tab = table.toList()
    return String(value = os.path.join(tab))
def findFiles(path: String, check: Value) -> Table:
    pth: str = srcPath / path
    lis = os.listdir(pth)
    lis = filter(check, lis)
    res = Table({})
    for item in lis:
        res.append(String(value = item))
    return res
Fs = Table({
    String(value = "readText"): BuiltinClosure(fn = lambda path: read(path, False)),
    String(value = "writeText"): BuiltinClosure(fn = lambda path, content, append = Number(0): write(path, content, False, append = append)),
    String(value = "readJson"): BuiltinClosure(fn = lambda path: read(path, True)),
    String(value = "writeJson"): BuiltinClosure(fn = lambda path, content, append = Number(0): write(path, content, True, append = append)),
    String(value = "readLines"): BuiltinClosure(fn = lambda path: read(path, False, True)),
    String(value = "writeLines"): BuiltinClosure(fn = lambda path, content, append = Number(0): write(path, content, False, True, append = append)),
    String(value = "exists"): BuiltinClosure(fn = exists),
    String(value = "listDir"): BuiltinClosure(fn = listDir),
    String(value = "isFile"): BuiltinClosure(fn = isFile),
    String(value = "isDir"): BuiltinClosure(fn = isDir),
    String(value = "copy"): BuiltinClosure(fn = copy),
    String(value = "move"): BuiltinClosure(fn = move),
    String(value = "join"): BuiltinClosure(fn = join),
    String(value = "mkdir"): BuiltinClosure(fn = lambda path: (os.mkdir(srcPath / path.value), Nil())[-1]),
    String(value = "rmdir"): BuiltinClosure(fn = lambda path: (os.rmdir(srcPath / path.value), Nil())[-1]),
    String(value = "fileSize"): BuiltinClosure(fn = lambda path: (os.path.getsize(srcPath / path.value, Nil()))[-1]),
    String(value = "findFiles"): BuiltinClosure(fn = findFiles)
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