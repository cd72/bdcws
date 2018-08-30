import os
import re
import logging.config

re_find_headers=re.compile(r'''
    .+                       # Any Character
    \<(strong|b)\>           # <strong>
    Across                   # The word Across
    .*?                      # Optional Characters
    \<\/(strong|b)\>         # </strong>
    .+?                      # Match anything else to the 
    ^                        # start of the next line
''', flags=re.DOTALL | re.VERBOSE | re.MULTILINE)

re_find_footers01=re.compile(r"The Quick Crossword pun.+", flags=re.DOTALL)
re_find_footers02=re.compile(r"Advertisements.+", flags=re.DOTALL)
re_nbsp=re.compile(r"&nbsp;")

re_clue_line=re.compile(r'''
    [y|p|g]\>             # Always starts with <body> or <p> or <strong> tag
    (\d{1,2}[a|d])        # Clue Identifier
    \s*                   # After the clue identifier we can see whitespace
    (.+?)                 # Then the actual clue
    \s*                   # Then more whitespace and an open bracket
    (\([0-9,]+\))         # In brackets we get the word(s) lengths sometimes comma separated
''', re.VERBOSE)


def count_lines(tag, text_block):
    num_lines = len(text_block.splitlines())
    logger.info(f"Number of lines at {tag} is {num_lines}")
    return num_lines

def chop_header(text_block):
    logger.info("chop_header")
    lines_before_chop = count_lines("lines_before_chop", text_block)
    clues_without_headers = re_find_headers.sub('', text_block, 1)
    lines_after_chop = count_lines("lines_after_chop", clues_without_headers)

    assert(lines_after_chop < lines_before_chop)
    assert(lines_before_chop-lines_after_chop > 300)

    return clues_without_headers

def chop_footer(text_block):
    logger.info("chop_footer")
    lines_before_chop = count_lines("lines_before_chop", text_block)
    clues_without_footers = re_find_footers01.sub('', text_block, 1)
    lines_after_chop = count_lines("lines_after_first_chop", clues_without_footers)
    clues_without_footers = re_find_footers02.sub('', clues_without_footers, 1)
    lines_after_chop = count_lines("lines_after_second_chop", clues_without_footers)

    assert(lines_after_chop < lines_before_chop)
    assert(lines_before_chop-lines_after_chop > 300)
    assert(lines_before_chop-lines_after_chop < 1800)
    assert(lines_after_chop < 100)
    return clues_without_footers


def parse_clue(clue_line):
    clue_line = re_nbsp.sub(' ', clue_line)
    logger.info(f"clue line : {clue_line}")
    # Note 28635 has an extra line in the solution

def parse_solution(solution_line):
    solution_line = re_nbsp.sub(' ', solution_line)
    logger.info(f"solution line : {solution_line}")


def get_clues(full_text):
    clue_text = chop_header(full_text)
    clue_text = chop_footer(clue_text)

    clues_processed = 0
    lines = iter(clue_text.splitlines())

    for line in lines:
        logger.debug(f"READING line : {line}")
        m = re_clue_line.search(line)
        if m:

            #clue_number, clue_direction, clue, clue_definition, solution_length = parse_clue(line)
            parse_clue(line)
            #solution, hint = parse_solution(solution_line)


            solution_line = next(lines)
            parse_solution(solution_line)

            clues_processed += 1
        else:
            logger.debug("line does not look like a clue")
        if clues_processed >= 5:
            break

def main():
    logger.info("test message")
    directory_in_str="dts/"
    directory = os.fsencode(directory_in_str)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.endswith(".html"):
            # print(os.path.join(directory, filename))
            logger.info(f"Filename is {filename}")
            with open(os.path.join(directory, file), encoding='utf-8') as fp:
                full_text = fp.read()
                all_clues = get_clues(full_text)
            # break
        else:
            continue
        break


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    main()