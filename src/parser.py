import re

def parse_header(filepath: str) -> list:
    with open(filepath, "r") as f:
        content = f.read()
    
    functions = []
    func_pattern = re.compile(
        r"(\w[\w\s\*]+?)\s+(\w+)\s*\(([^)]*)\)\s*;"
    )

    for match in func_pattern.finditer(content):
        return_val, func_name, func_param = match.groups()
        return_val = return_val.strip()
        func_param = [p.strip() for p in func_param.split(",") if p.strip()]
        
        i = 0
        for param in func_param:
            func_param[i] = param.split(" ")[0]
            i += 1

        if return_val.split()[-1] in ("typedef", "struct", "enum"):
            continue
        
        functions.append((func_name, func_param, return_val))

    return functions

if __name__ == "__main__":
    result = parse_header("include/trie.h")
    print(result)
