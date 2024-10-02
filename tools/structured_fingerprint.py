from specimen_utils import sha256hex


def of_event_descriptor(descr):
    kind = descr["kind"]
    match kind:
        case "green-flag" | "clicked" | "start-as-clone":
            return f"{kind}:-"
        case "key-pressed":
            suffix = sha256hex(descr["keyName"])
            return f"{kind}:{suffix}"
        case "message-received":
            suffix = sha256hex(descr["message"])
            return f"{kind}:{suffix}"
    raise RuntimeError(f"unknown kind {kind}")


def of_event_handler(handler):
    event_print = of_event_descriptor(handler["event"])
    code_hash = sha256hex(handler["pythonCode"])
    return f"{event_print}:{code_hash}"


def of_actor(actor):
    handlers_prints = ",".join(
        of_event_handler(h) for h in actor["handlers"]
    )
    kind = actor["kind"]
    name = actor["name"]
    hash_input = f"{kind}:{name}[{handlers_prints}]"
    return sha256hex(hash_input)
