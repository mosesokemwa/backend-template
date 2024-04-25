def exclude_by_keys(
        my_dict: dict, excluded: set[str], talk_to_me: bool = False
) -> dict:
    """Delete items from a dictionary, based on the list of the keys to exclude.

    The original dictionary remains unchanged.

    Also of interest: method dict() with 'exclude' kwargs from pydantic BaseModel.

    Args:
        my_dict: The dictionary from which to delete items.
        excluded: Set of the keys of the item to delete.
        talk_to_me: If True, display debug information to the console.

    Returns:
        The modified copy of the original dictionary, with keys excluded.
    """
    modified_dict = my_dict.copy()
    for key in list(modified_dict.keys()):
        condition_1 = key in excluded
        # Check that key starts with 1 and only 1 '_' if '_*' is excluded
        condition_2 = key[0] == "_" and key[1] != "_" and "_*" in excluded
        # Check that key starts with 2 '_' if '__' is excluded
        condition_3 = key[:2] == "__" and "__*" in excluded
        if condition_1 or condition_2 or condition_3:
            if talk_to_me:
                print(f"Excluding item with key '{key}'.")
            del modified_dict[key]
    return modified_dict
