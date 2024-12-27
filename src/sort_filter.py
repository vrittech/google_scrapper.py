from src.utils import kebab_case, unicode_to_ascii


def sort_dict_by_keys(dictionary, keys):
    new_dict = {}
    
    try:
        for key in keys:
            new_dict[key] = dictionary[key]
    except:
        raise Exception("Failed to sort dict by keys")
    return new_dict


def filter_places(ls, filter_data):
    def fn(i):
        web_site = i.get("website")
        has_website = filter_data.get("has_website")
        if has_website is not None:
            if (has_website is False and web_site is not None):
                return False

            if (has_website is True and web_site is None):
                return False
        min_reviews = filter_data.get("min_reviews")
        reviews = i.get('reviews')

        if min_reviews is not None and (reviews == '' or reviews is None or reviews < min_reviews):
            return False

        return True

    return list(filter(fn, ls))


def sort_place(places:list, sort):
     
    def sorting_key(item):
        key = sort[0]
        value = item.get(key)

        # Handle None separately
        if value is None:
            return (0,)  # A tuple with a single element to ensure type consistency

        # Return a tuple with type indicator and value
        return (1, value) if isinstance(value, int) else (2, value)

    def sorting_bool_true(item):
        sorting_by = sort[0]
        result = item.get(sorting_by, 0)

        if result is True  or result is not None:
            return 1

        return 0

    def sorting_bool_false(item):
        sorting_by = sort[0]
        result = item.get(sorting_by, 0)

        if result is False  or result is None:
            return 1

        return 0

    sorting_order = sort[1]

    if isinstance(sorting_order, bool):
        if sorting_order:
            sorted_data = sorted(places, key=sorting_bool_false)
        else: 
            sorted_data = sorted(places, key=sorting_bool_true)
    else:
        sorted_data = sorted(places, key=sorting_key,
                         reverse=(sorting_order == "desc"))

    return sorted_data

def sort_places(places:list, sorts):
    for sort in sorts:
            places = sort_place(places, sort)

    return places


def list_contains_string(string_list, target_string):
    target_string_lower = kebab_case(unicode_to_ascii(target_string)).lower()  # Convert target string to lowercase
    for item in string_list:
        if target_string_lower == kebab_case(unicode_to_ascii(item)).lower():  # Compare in a case-insensitive manner
            return True
    return False





