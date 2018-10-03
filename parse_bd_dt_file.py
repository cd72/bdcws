import os
import re
import logging.config
import attr

@attr.s(kw_only=True)
class Clue(object):
    puzzle_id = attr.ib()
    clue_id = attr.ib(default=None)
    clue_text = attr.ib(default=None)
    clue_length = attr.ib(default=None)
    hint_text = attr.ib(default=None)
    solution = attr.ib(default=None)

re_find_headers=re.compile(r'''
    .+                       # Any Character
    \<(strong|b|p)\>           # <strong>
    Across\s*                # The word Across
    #.*?                      # Optional Characters
    \<(/strong|/b|/p|br)\>         # </strong>
    .+?                      # Match anything else to the 
    ^                        # start of the next line
''', flags=re.DOTALL | re.VERBOSE | re.MULTILINE)

re_find_footers01=re.compile(r"The Quick Crossword pun.+", flags=re.DOTALL)
re_find_footers02=re.compile(r"Advertisements.+", flags=re.DOTALL)

re_clue_line1=re.compile(r'''
    [y|p|g]\>             # Always starts with <body> or <p> or <strong> tag
    (\d{1,2}[a|d])        # Clue Identifier
    \s*                   # After the clue identifier we can see whitespace
    (.+?)                 # Then the actual clue
    \s*                   # Then more whitespace and an open bracket
    (\([0-9,-]+\))         # In brackets we get the word(s) lengths sometimes comma separated
''', re.VERBOSE)

re_clue_line2=re.compile(r'''
     ^                    # Can start on a new line
    (\d{1,2}[a|d])        # Clue Identifier
    \s*                   # After the clue identifier we can see whitespace
    (.+?)                 # Then the actual clue
    \s*                   # Then more whitespace and an open bracket
    (\([0-9,]+\))         # In brackets we get the word(s) lengths sometimes comma separated
''', re.VERBOSE)

def count_lines(tag, text_block):
    num_lines = len(text_block.splitlines())
    logger.debug(f"Number of lines at {tag} is {num_lines}")
    return num_lines

def chop_header(text_block):
    logger.debug("chop_header")
    lines_before_chop = count_lines("lines_before_chop", text_block)
    clues_without_headers = re_find_headers.sub('', text_block, 1)
    lines_after_chop = count_lines("lines_after_chop", clues_without_headers)

    assert(lines_after_chop < lines_before_chop)
    assert(lines_before_chop-lines_after_chop > 300)
    return clues_without_headers

def chop_footer(text_block):
    logger.debug("chop_footer")
    lines_before_chop = count_lines("lines_before_chop", text_block)
    clues_without_footers = re_find_footers01.sub('', text_block, 1)
    lines_after_chop = count_lines("lines_after_first_chop", clues_without_footers)
    clues_without_footers = re_find_footers02.sub('', clues_without_footers, 1)
    lines_after_chop = count_lines("lines_after_second_chop", clues_without_footers)

    assert(lines_after_chop < lines_before_chop)
    assert(lines_before_chop-lines_after_chop > 300)
    assert(lines_before_chop-lines_after_chop < 1800)
    assert(lines_after_chop < 110)
    return clues_without_footers


def parse_clue(clue_line, crossword_clue):
    logger.debug(f"clue line : {clue_line}")

    # A series of substitutes for cleaning up the data
    clue_line = re.sub(r"&nbsp;", ' ', clue_line)
    clue_line = re.sub(
        r'\<span style="text-decoration: underline;"\>(.+?)\</span\>', "*\g<1>*", clue_line, flags=re.DOTALL)
    clue_line = re.sub(r'<u>(.+?)</u>', "*\g<1>*", clue_line, flags=re.DOTALL)
    clue_line = re.sub(
        r'<span class="mrkUnderS solid"><span class="mrkMoveS">(.+?)</span></span>', "*\g<1>*", clue_line)
    clue_line = re.sub(r'<p>', "", clue_line)
    clue_line = re.sub(r'<br>$', "", clue_line)
    clue_line = re.sub(
        r'<span id="c\d+[a|d]"></span><span id="AcrossClues"></span><strong>(.+)</strong>', "\g<1>", clue_line)
    clue_line = re.sub(r'<span id="c\d+[a|d]"></span><strong>(.+?)</strong>', "\g<1>", clue_line)
    clue_line = re.sub(r'^</strong><strong>\s+</strong>', "", clue_line)
    clue_line = re.sub(r'^<span id="DownClues"></span>', "", clue_line)
    clue_line = re.sub(r'\s+', ' ', clue_line)
    clue_line = re.sub(r'''<strong>(\d{1,2}[a|d])</strong>''', "\g<1>", clue_line)

    logger.info(f"final clue : {clue_line}")

    m = re.match(r'''
        (\d{1,2}[a|d])        # Clue Identifier
        \s*                   # After the clue identifier we can see whitespace
        (.+?)                 # Then the actual clue
        \s*                   # Then more whitespace and an open bracket
        \(([0-9,-]+)\)        # In brackets we get the word(s) lengths sometimes comma separated
        (.*)$                 # Anything else on the rest of the line
    ''', clue_line, re.VERBOSE)
    if m:
        logger.debug(m.groups())
        crossword_clue.clue_id=m.group(1)
        crossword_clue.clue_text=m.group(2)
        crossword_clue.clue_length=m.group(3)
        trailing_text=m.group(4)
    else:
        raise ValueError('The clue finding regex failed..')

    return trailing_text

def parse_solution(solution_line, crossword_clue):
    logger.debug(f"solution line : {solution_line}")
    solution_line = re.sub(r"&nbsp;", ' ', solution_line)
    solution_line = re.sub(r'''<strong>''', '', solution_line)
    solution_line = re.sub(r'''</strong>''', '', solution_line)
    solution_line = re.sub(r'''</p>''', '', solution_line)
    solution_line = re.sub(r'''<br>''', '', solution_line)
    solution_line = re.sub(r'''<em>''', '', solution_line)
    solution_line = re.sub(r'''</em>''', '', solution_line)
    #<span style="color: #008000;">
    solution_line = re.sub(r'''<span style="color: #\d{6};">''', '', solution_line)
    solution_line = re.sub(r'''</span>''', '', solution_line)
    solution_line = re.sub(
        r'''<a\shref="https?://.+?"
        \starget="_blank"
        \sstyle="color:\s*\#......">(.+?)</a>''',
            "\g<1>", solution_line, flags=re.VERBOSE | re.DOTALL)

    solution_line = re.sub(r'''<span class="spoiler" rel="(.+)">Click here!</span>''', "\g<1>:", solution_line)
    solution_line = re.sub(r'''<span class="spoiler" rel="(.+)">Click here!''', "\g<1>:", solution_line)
    solution_line = re.sub(
        r'''<span class="mrkSpoiler" rel="\s.(.+)">Answer:<span class="mrkHintSpacing">''', "\g<1>:", solution_line)
    solution_line = re.sub(r'''<span style="font-size: 12pt;">''', "", solution_line)

    solution_line = re.sub(r'''—''', ':', solution_line)

    #<span class="spoiler" rel="ACIDS">Click here!
    logger.info(f"solution line : {solution_line}")

    m = re.match(r'''
            (.+?)      # Actual Solution
            \s*[:–-]+\s*    # Colon or dash surrounded by optional spaces.  This is a non-default dash
            (.+)       # The hint
        ''', solution_line, re.VERBOSE)
    if m:
        logger.debug(m.groups())
        crossword_clue.hint_text = m.group(2)
        crossword_clue.solution = m.group(1)
    else:
        raise ValueError('The solution finding regex failed')

def process_page(full_text):
    m = re.search(r'''<title>.+(DT\s+\d\d\d\d\d).+</title>''', full_text)
    if m is None:
        logger.info((full_text.splitlines)[2])
        raise ValueError('No title error')
    page_title = m.group(1)
    page_title = re.sub(r'''\s+''', '_',page_title)
    logger.info(page_title)
    assert re.match(r'''DT_\d\d\d\d\d''',page_title)
    crossword_clue = Clue(puzzle_id=page_title, clue_id=None)

    #logger.info(dir(crossword_clue))
    logger.info(crossword_clue)

    clue_text = chop_header(full_text)
    clue_text = chop_footer(clue_text)

    clues_processed = 0
    lines = iter(clue_text.splitlines())

    for line in lines:
        logger.debug(f"READING line : {line}")
        line = re.sub(r'<span style="color: #0000ff;">', "", line)
        line = re.sub(r'<p style="background: #fbfbfb;">', "<p>", line)
        line = re.sub(r'<p style="background: white;">', "<p>", line)
        logger.debug(f"READING mod line : {line}")

        m = re_clue_line1.search(line) or re_clue_line2.search(line)
        if m:

            #clue_number, clue_direction, clue, clue_definition, solution_length = parse_clue(line)
            leftover_text = parse_clue(line, crossword_clue)
            #solution, hint = parse_solution(solution_line)
            logger.debug(f'leftover is {leftover_text}')
            if re.match(r'''<br>''', leftover_text):
                parse_solution(leftover_text, crossword_clue)
            else:
                solution_line = next(lines)
                # TODO 28635 has an extra line in the solution - work out how to deal with this
                parse_solution(solution_line, crossword_clue)

            logger.info(crossword_clue)
            clues_processed += 1

        else:
            logger.debug("line does not look like a clue")
            logger.debug(line)
        if clues_processed >= 5:
            break

    logger.info(f"Processed {clues_processed} clues")
    #assert (clues_processed >= 17)
    #assert (clues_processed <= 35)


def main():
    directory_in_str="dts/"
    directory = os.fsencode(directory_in_str)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.endswith(".html"):
            if filename == 'dt-28743.html':
                continue
            # print(os.path.join(directory, filename))
            #if filename != 'dt-28680.html':
            #    continue
            logger.info(f"Filename is {filename}")
            with open(os.path.join(directory, file), encoding='utf-8') as fp:
                full_text = fp.read()
                all_clues = process_page(full_text)
            # break
        else:
            continue
       # break


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    main()