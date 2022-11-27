def EnrichInputEntity(enrich_input)->dict:
    return {
        "key": enrich_input["key"],
        "payload": enrich_input["payload"]
    }

def EnrichInputEntities(enrich_inputs)->list:
    return [EnrichInputEntity(enrich_input) for enrich_input in enrich_inputs]