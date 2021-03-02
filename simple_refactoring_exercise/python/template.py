def template(source_template, req_id):
    # refactoring: use const
    split_pattern1 = "%CODE%"
    split_pattern2 = "%ALTCODE%"
    template = str(source_template)

    #refactoring: validations
    if len(req_id) != 10:
        print('invalid input')
        return None
    if split_pattern1 not in source_template or split_pattern2 not in source_template:
        print('invalid input')
        return None
    # Substitute for %CODE%
    # refactoring: use const instead of fixed value
    template_split_begin = template.index(split_pattern1)
    # refactoring: use len() instead of fixed value
    #template_split_end = template_split_begin + 6
    template_split_end = template_split_begin + len(split_pattern1)

    template_part_one = str(template[0:(template_split_begin)])
    template_part_two = str(template[template_split_end:len(template)])
    code = str(req_id)
    template = str(template_part_one + code + template_part_two)

    # Substitute for %ALTCODE%
    # refactoring: use const instead of fixed value
    #template_split_begin = template.index("%ALTCODE%")
    template_split_begin = template.index(split_pattern2)
    # refactoring: use len() instead of fixed value
    #template_split_end = template_split_begin + 9
    template_split_end = template_split_begin + len(template_part_two)
    template_part_one = str(template[0:(template_split_begin)])
    template_part_two = str(template[template_split_end:len(template)])
    altcode = code[0:5] + "-" + code[5:8]
    return template_part_one + altcode + template_part_two


