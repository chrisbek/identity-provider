from fastapi import Query


class Validator:
    @staticmethod
    def get_str_max_len_5_optional(alias: str):
        return Query(None, max_length=5, alias=alias)

    @staticmethod
    def get_int_gt_arg_required(greater_than: int):
        return Query(..., ge=greater_than)

