from aoc_lube import fetch, submit
from functools import cache

YEAR = 2023
DAY = 12

@cache
def count_possibles(springs, contig_dmgs, i=0, j=0):
    """
    Find the possible arrangements matching `contig_dmgs` (with start index `j`)
    in `springs` (with start index `i`). The following algorithm is considered:

    1. Move until a surely/possibly damaged spring (#/?) is found.
    2. Then, start building a "contiguous window".
    3. When the length of the window matches `contig_dmgs[j]` and the following
    character is not a surely damaged spring (#), recurse:
        Start `i` at the position after the following character (`i + 2`).
        Pass an incremented `j` to the recursed function (`j + 1`).
    4. Once the length of the window may exceed `contig_dmgs[j]`, move the
    window forward.
    5. If the window moves forward over a surely damaged spring or reaches the
    end of the row of springs, break.
        The reason why the code needs to break when the window moves over a surely
        damaged string is that skipping over one would mess up the match with
        `contig_dmgs`.
        It's okay skipping over a possibly damaged spring (?) because that can also
        be a working spring (.). This is the reason why step 3 starts at the position
        after the following character IF the following character isn't a surely
        damaged spring.
    The start of the function also checks to see if the `contig_dmgs` structure is
    already matched (by comparing the length of `contig_dmgs` to `j`). If so, and
    the remaining characters in `springs` do not have a surely damaged spring,
    it's considered a possibility.

    Example:

    j = 0
    contig_dmgs:    1, 1, 3
                    ^
    i = 0
    springs:        .???.###
                    ^
    Working spring. Move over it.

    j = 0
    contig_dmgs:    1, 1, 3
                    ^
    i = 1
    springs:        .???.###
                     ^
    Found a possibly damaged spring. Start building a "contiguous window".
    The contiguous window is 1 in length.
    Since the length matches `contig_dmgs[j]` (1 = 1), AND
        .???.###
          ^
    the following character is not a surely damaged spring, recurse;
        
        i + 2 = 1 + 2 = 3
        Start at `i = 3`.
        j + 1 = 0 + 1 = 1
        `j = 1` in the recursion.

    RECURSION 1A

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 3
    springs:        .???.###
                       ^
    Found a possibly damaged spring. Start building a "contiguous window".
    The contiguous window is 1 in length.
    Since the length matches `contig_dmgs[j]` (1 = 1), AND
        .???.###
            ^
    the following character is not a surely damaged spring, recurse;
        
        i + 2 = 3 + 2 = 5
        Start at `i = 5`.
        j + 1 = 1 + 1 = 2
        `j = 2` in the recursion.

    RECURSION 2

    j = 2
    contig_dmgs:    1, 1, 3
                          ^
    i = 5
    springs:        .???.###
                         ^
    Found a surely damaged spring. Start building a "contiguous window".
    The contiguous window is 1 in length.

    j = 2
    contig_dmgs:    1, 1, 3
                          ^
    i = 6
    springs:        .???.###
                         ~^
    The contiguous window is now 2 in length.

    j = 2
    contig_dmgs:    1, 1, 3
                          ^
    i = 7
    springs:        .???.###
                         ~~^
    The contiguous window is now 3 in length.
    Since the length matches `contig_dmgs[j]` (3 = 3), AND
        .???.###
                ^
    the following character is not a surely damaged spring, recurse;
        
        i + 2 = 7 + 2 = 9
        Start at `i = 9`.
        j + 1 = 2 + 1 = 3
        `j = 3` in the recursion.

    RECURSION 3

    j = 3 
    contig_dmgs:    1, 1, 3
    i = 9
    springs:        .???.###

    Oh. It seems like the whole `contig_dmgs` structure was matched already.
    Since `i = 9`, the index exceeds the boundaries of `springs`, therefore
    there are no more surely damaged springs and a possibility was found!

    possibilities returned: 1

    RECURSION 3 END

    Since recursion 2 has reached the end as well, return.

    possibilities returned: 1

    RECURSION 2 END

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 4
    springs:        .???.###
                        ^
    Working spring. Move over.

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 5
    springs:        .???.###
                         ^
    Found a surely damaged spring. Start building a "contiguous window".
    The contiguous window is 1 in length.
    The length matches `contig_dmgs[j]` (1 = 1), BUT
        .???.###
              ^
    the following character is a surely damaged spring.
    That means, no recursion will be done.

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 6
    springs:        .???.###
                         ~^
    Found a surely damaged spring.
    The contiguous window length may exceed `contig_dmgs[j]` (2 > 1), so
    the window has to move forward.
    .???.###
         -^
    However, that means the contiguous window will skip over a surely damaged
    spring, and ruin the match! A break needs to happen, ending recursion 1A.

    possibilities returned: 1

    RECURSION 1A END

    j = 0
    contig_dmgs:    1, 1, 3
                    ^
    i = 2
    springs:        .???.###
                     ~^
    Found a possibly damaged spring.
    The contiguous window length may exceed `contig_dmgs[j]` (2 > 1), so
    the window has to move forward.
    .???.###
     -^
    Since the length matches `contig_dmgs[j]` (1 = 1), AND
        .???.###
           ^
    the following character is not a surely damaged spring, recurse;
        
        i + 2 = 2 + 2 = 4
        Start at `i = 4`.
        j + 1 = 0 + 1 = 1
        `j = 1` in the recursion.

    RECURSION 1B

    Wait... Didn't this happen before?
    It's not in the cache though... Eh, just follow through with it.

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 4
    springs:        .???.###
                        ^
    Working spring. Move over.

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 5
    springs:        .???.###
                         ^
    Found a surely damaged spring. Start building a "contiguous window".
    The contiguous window is 1 in length.
    The length matches `contig_dmgs[j]` (1 = 1), BUT
        .???.###
              ^
    the following character is a surely damaged spring.
    That means, no recursion will be done.

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 6
    springs:        .???.###
                         ~^
    Found a surely damaged spring.
    The contiguous window length may exceed `contig_dmgs[j]` (2 > 1), so
    the window has to move forward.
    .???.###
         -^
    However, that means the contiguous window will skip over a surely damaged
    spring, and ruin the match! A break needs to happen, ending recursion 1B.

    possibilities returned: 0

    RECURSION 1B END

    j = 0
    contig_dmgs:    1, 1, 3
                    ^
    i = 3
    springs:        .???.###
                      ~^
    Found a possibly damaged spring.
    The contiguous window length may exceed `contig_dmgs[j]` (2 > 1), so
    the window has to move forward.
    .???.###
      -^
    Since the length matches `contig_dmgs[j]` (1 = 1), AND
        .???.###
            ^
    the following character is not a surely damaged spring, recurse;
        
        i + 2 = 3 + 2 = 5
        Start at `i = 5`.
        j + 1 = 0 + 1 = 1
        `j = 1` in the recursion.

    RECURSION 1C

    Wait... This happened before as well! Just shorter...
    It's not in the cache too though... Eh, just go.

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 5
    springs:        .???.###
                         ^
    Found a surely damaged spring. Start building a "contiguous window".
    The contiguous window is 1 in length.
    The length matches `contig_dmgs[j]` (1 = 1), BUT
        .???.###
              ^
    the following character is a surely damaged spring.
    That means, no recursion will be done.

    j = 1
    contig_dmgs:    1, 1, 3
                       ^
    i = 6
    springs:        .???.###
                         ~^
    Found a surely damaged spring.
    The contiguous window length may exceed `contig_dmgs[j]` (2 > 1), so
    the window has to move forward.
    .???.###
         -^
    However, that means the contiguous window will skip over a surely damaged
    spring, and ruin the match! A break needs to happen, ending recursion 1C.

    possibilities returned: 0

    RECURSION 1C END

    j = 0
    contig_dmgs:    1, 1, 3
                    ^
    i = 4
    springs:        .???.###
                       ~^
    Found a working spring.
    The contiguous window is broken because a working spring got in the way.
    .???.###
       -^
    Since there aren't any surely damaged springs in the window, we can safely
    discard it and move on.

    Hold on... This is too familiar!

    j = 0
    contig_dmgs:    1, 1, 3
                    ^
    i = 5
    springs:        .???.###
                         ^
    Found a surely damaged spring. Start building a "contiguous window".
    The contiguous window is 1 in length.
    The length matches `contig_dmgs[j]` (1 = 1), BUT
        .???.###
              ^
    the following character is a surely damaged spring.
    That means, no recursion will be done.

    j = 0
    contig_dmgs:    1, 1, 3
                    ^
    i = 6
    springs:        .???.###
                         ~^
    Found a surely damaged spring.
    The contiguous window length may exceed `contig_dmgs[j]` (2 > 1), so
    the window has to move forward.
    .???.###
         -^
    However, that means the contiguous window will skip over a surely damaged
    spring, and ruin the match! A break needs to happen, ending the whole code.

    And we conclude with a total possibility count (from all the recursions) of: 1

    The whole code finally returns a possibility count of 1.
    """
    possibilities = 0

    if j == len(contig_dmgs):
        # Found a match.
        # Check if there is a surely damaged spring among the remaining springs.
        if springs.find('#', i) < 0:
            # `str.find()` returns -1 if the value isn't found
            # in the string (`springs`) with a specified start (`i`).
            # That means, this is a possibility since no more surely damaged
            # springs can be found.
            return 1
        # There's a surely damaged spring. Not a possibility.
        return 0

    contiguous = 0
    sure_dmgs = set() # This keeps track of the indexes with a surely damaged
                      # spring.
    while i < len(springs):
        if springs[i] == '#' or springs[i] == '?':
            if springs[i] == '#':
                sure_dmgs.add(i)

            if contiguous == contig_dmgs[j]:
                # The window length may exceed `contig_dmgs[j]`; move the window forward!
                if i - contiguous in sure_dmgs:
                    # The tail end of the window is a surely damaged spring that
                    # we're moving over. Reasons explained, break out.
                    break
                # Don't change the length after moving forward; it's effectively the same.
            else:
                # Increment the window length.
                contiguous += 1

            # After possibly incrementing the window length, check for a recursion condition.
            if (contiguous == contig_dmgs[j]           # If the window length matches, and either:
                    and (i + 1 >= len(springs)         #     there is no following character
                         or springs[i + 1] != '#')):   #     the following character isn't a surely
                                                       #         damaged spring
                # Recurse!
                possibilities += count_possibles(springs, contig_dmgs, i + 2, j + 1)
        else:
            # Working spring. Breaks contiguity. Discard the window (if there's one).
            if contiguous:
                if {*range(i - contiguous, i)} & sure_dmgs:
                    # If we're skipping over/discarding a window with a surely damaged
                    # spring, reasons already explained, break the loop.
                    break
                # Reset the length (effectively discards the window).
                contiguous = 0
        i += 1

    # We're done. Return the number of possibilities.
    return possibilities

def part_1():
    total = 0
    for springs, contig_dmgs in data:
        total += count_possibles(springs, contig_dmgs)
    return total

def part_2():
    total = 0
    for springs, contig_dmgs in data:
        # Repeat the springs data 5 times, each occurence joined
        # by '?' (possibly damaged spring).
        springs = '?'.join([springs]*5)
        # Also repeat the contiguous damages data 5 times.
        contig_dmgs *= 5
        total += count_possibles(springs, contig_dmgs)
    return total

if __name__ == '__main__':
    inp = fetch(YEAR, DAY)

    data = []
    for line in inp.splitlines():
        springs, contig_dmgs_string = line.split()
        # It *should* be safe to use `eval()` here to make the tuple.
        data.append((springs, eval(contig_dmgs_string)))

    submit(YEAR, DAY, 1, part_1)
    submit(YEAR, DAY, 2, part_2)
