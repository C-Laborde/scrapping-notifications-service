def doc_comparison(restored, document):
    if not sorted(restored.keys()) == sorted(document.keys()):
        print("RESTORED KEYS: ", restored.keys())
        print("DOCUMENT KEYS: ", document.keys())
        raise KeyError("Documents have different keys")
    for game in restored.keys():
        results_restored = [restored[game]["RESULT-LOCAL"],
                            restored[game]["RESULT-VISITANT"]]
        results_doc = [document[game]["RESULT-LOCAL"],
                       document[game]["RESULT-VISITANT"]]
        if results_restored != results_doc:
            return False
    return True
