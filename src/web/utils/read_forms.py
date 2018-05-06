def read_int_from_form(form, id, default_value="50"):
    intv_str = form.get(id, default_value)
    if (intv_str):
        intv_str = intv_str.strip()
    else:
        intv_str = default_value
    if intv_str:
        intv = int(intv_str) if intv_str.isdigit() else default_value
        return intv
    else:
        return None