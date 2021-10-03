# -*- coding: utf-8 -*-


class DomainUtils:

    global_domain = "*global*"
    domain_separator = "::"

    def __init__(self, debug=False):
        pass

    def get_full_name(domain_name, user_defined_name):
        return domain_name + DomainUtils.domain_separator + user_defined_name

    def get_name(user_defined_name):
        pos = user_defined_name.find(DomainUtils.domain_separator)
        if pos > 0:
            return user_defined_name[pos + 2 :]
        else:
            return user_defined_name

    def get_domain(user_defined_name, is_user_friendly=False):
        pos = user_defined_name.find(DomainUtils.domain_separator)
        if pos > 0:
            ret_value = user_defined_name[:pos]
            if is_user_friendly and ret_value == DomainUtils.global_domain:
                return "unnamed"
            else:
                return ret_value
        else:
            if is_user_friendly and user_defined_name == DomainUtils.global_domain:
                return "unnamed"
            else:
                return user_defined_name
