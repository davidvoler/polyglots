def get_int_scale(minval: int, maxval: int, scale_size):
    j = (maxval-minval)/(scale_size - 1)
    return [minval + round(i*j) for i in range(scale_size)]


def get_float_scale(minval: float, maxval: float, scale_size: int, round_num: int = 3):
    j = (maxval-minval)/(scale_size - 1)
    return [round(minval + i*j, round_num) for i in range(scale_size)]


def get_param_value(val: float):
    i_scale = get_int_scale(3, 34, 10)
    print(i_scale)
    f_scale = get_float_scale(-1, 1, 10)
    print(f_scale)
    for i in range(len(i_scale)):
        if val <= f_scale[i]:
            return i_scale[i]
    return i_scale[-1]


# print(get_param_value(-2))


def scale(input_val: float,
          min_input: float,
          max_input: float,
          min_output: float,
          max_output: float, 
          scale_size: int=20) -> float:
    if scale_size < 5:
        #raise ValueError("scale_size must be greater than 1")
        #minimum scale_size is 5
        scale_size = 5
    input_scale = get_float_scale(min_input, max_input, scale_size)
    # print(input_scale)
    output_scale = get_float_scale(min_output, max_output, scale_size)
    # print(output_scale)
    for i in range(len(input_scale)):
        if input_val <= input_scale[i]:
            return output_scale[i]
    return output_scale[-1]


if  __name__ == "__main__":
    results = scale(input_val=0.6, 
                    min_input=-1, 
                    max_input=1,
                    min_output=2,
                    max_output=10)
    # print(results, round(results))
    results = scale(input_val=-0.6, 
                    min_input=-1, 
                    max_input=1,
                    min_output=2,
                    max_output=10)
    print(results, round(results))
    results = scale(input_val=-1, 
                    min_input=-1, 
                    max_input=1,
                    min_output=2,
                    max_output=10)
    print(results, round(results))

    results = scale(input_val=1,
                    min_input=-1,
                    max_input=1,
                    min_output=2,
                    max_output=10)
    print(results, round(results))