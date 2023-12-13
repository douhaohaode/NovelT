import re


def text_process(text ="{暴力枪}累死爷了 不过已经招收了十名中品灵根{一拳}四十个凡品灵根。"):

    matches = re.finditer(r'\{([^}]+)\}', text)

    sounds = []

    for match in matches:
        content = match.group(0)
        start = match.start()
        end = match.end()
        sounds.append((content, start, end))

    # 打印找到的花括号内容和位置
    for content, start, end in sounds:
        print(f"内容: {content}, 位置: ({start}, {end})")

    # 从文本中删除花括号内容
    top = 0
    for content, start, end in sounds:
        text = text[:(start - top)] + text[(end - top):]
        top = end - start

    # 打印删除花括号内容后的文本
    print("删除花括号内容后的文本:", text)

    return (text , sounds)
