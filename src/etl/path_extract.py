import json

def extract_paths(obj, prefix=""):
    """
    Recursively extract all JSON paths.
    """
    paths = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            paths.append(new_prefix)
            paths.extend(extract_paths(v, new_prefix))

    elif isinstance(obj, list):
        if not obj:
            return paths
        # ambil 1 item saja untuk schema
        new_prefix = f"{prefix}[0]"
        paths.append(new_prefix)
        paths.extend(extract_paths(obj[0], new_prefix))

    return paths


def main():
    with open("../../freelancers.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # pastikan ambil OBJECT freelancer, bukan wrapper
    if isinstance(data, dict) and "items" in data:
        freelancers = data["items"]
    elif isinstance(data, list):
        freelancers = data
    else:
        raise RuntimeError("Unsupported JSON structure")

    first = freelancers[0]

    print("\n=== ALL JSON PATHS (SCHEMA) ===\n")
    for p in sorted(set(extract_paths(first))):
        print(p)


if __name__ == "__main__":
    main()
