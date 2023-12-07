YEAR = 2023
DAY = 5
_U = 1
if _U:
    from aoc_lube import fetch, submit
    inp = fetch(YEAR, DAY)
    _U = 0

##### ACTUAL CODE START #####

# The input is in the following format:
#
# seeds: <seed1> <seed2> <...>
#
# seed-to-soil map:
# <dest1> <src1> <rangelen1>
# <dest2> <src2> <rangelen2>
# <...>
#
# soil-to-fertilizer map:
# <...>
#
# <...>
#
# Next is fertilizer-to-water, water-to-light, ...-temperature, ...-humidity,
# then finally humidity-to-location. These maps are stored in the `steps` list.
# Each map is considered a "step", and each set of dest, src, and rangelen is
# appended to the "step" list.

lines = inp.strip().splitlines()
seeds = list(map(int, lines[0].split()[1:]))

# A list of lists of 3-lists (destination, source, length)
steps = []

# Start at line 3; it's the first one in the input with the line format of
#   <dest1> <src1> <rangelen1>
i = 3

while True:
    step = []
    while i < len(lines):
        # The delimiter for parsing a new step is a blank line.
        if line := lines[i]:
            # Split the line to produce 3 separate integer strings
            # that are converted by the `map(int, ...)`.
            step.append(list(map(int, line.split())))
        else:
            # Blank line! Break out.
            break
        i += 1 # Go to the next 3-set in (or the end of) the mapping.
    else:
        break
    steps.append(step)
    i += 2 # From the blank line, skip the header and go straight to the 3-set.

# Getting the minimum value; just assign this to the maximum number-comparable thing.
p1 = float('inf')

for seed in seeds:
    # Process the seed through the steps.
    for step in steps:
        for dest, src, length in step:
            # If the range of the mapping contains the seed...
            #   -----------------------------------
            #  |                seed               |
            # src --------------------------- src + length
            if src <= seed < src + length:
                # Rearranging, the line of code following is:
                #   seed = src + seed-dest
                # Which is basically remapping the seed to `dest` with the same
                # relative position on `src`.
                seed -= src - dest
                # Early break; we already found the range containing the seed.
                break
    # If the resulting location (result of processing seed) is lesser than
    # the current minimum, change it.
    if seed < p1:
        p1 = seed

# `p1` now has the answer to Part 1

# Just a fancy way to pair up every 2 numbers.
I = iter(seeds)
seed_ranges = [*zip(I,I)]

# Stores sliced temporary seed ranges after the processing.
temp_list = []

# While there are still steps (maps) to process the seed ranges...
while steps:
    nxstep, *steps = steps # Basically a .popleft() of some sort;
                           # next step is stored in `nxstep`.
    for start, length in seed_ranges:
        # While we still have some uncovered areas...
        while length:
            for dest, src, maplength in nxstep:
                # Check if any of the ranges overlap with the current seed range.

                # Forward overlap: the seed range starts in the current range.
                #   The seed range may or may not exceed the bounds of the current range.
                #   If it does, adjust `start` and `length` to move to the end of the
                #   current range.
                #
                # (Overlapping figure, bounds exceeding)
                #   -------------------------------
                #  |              ################# |
                # src --------- start ------ src + maplength ---- start + length
                #                 | ###############                   |
                #                  ----------------------------------
                if src <= start < src + maplength:
                    T = min(length, maplength)
                    # Remap to `dest` with relative position on `src`.
                    # Add that area to `temp_list`.
                    temp_list.append([start-src + dest, T])
                    # Skip the whole overlapped area. It's already noted.
                    length -= T
                    start += T
                    break
                # Whole overlap: the seed range contains the current range.
                #
                #    ------------------------------------------------------------
                #   |                                                             |
                #   |    -------------------------------------------------        |
                #   |   | ################################################ |      |
                #   |  src ------------------------------------ src + maplength   |
                #   |                                                             |
                # start -------------------------------------------------- start + length
                elif start < src < src + maplength <= start + length:
                    # Re-process this bit preceding the current range later.
                    seed_ranges.append([start, src - start])
                    # Add the whole destination range to `temp_list`.
                    temp_list.append([dest, maplength])
                    # Skip to the end of the current range.
                    length = start + length - (start := src + maplength)
                    break
                # Backward overlap: the seed range ends in the current range.
                #   Same things as the forward overlap, except the seed range
                #   is now positioned in the back.
                #
                #                       -------------------------------------
                #                      | ###############                      |
                # start ------------- src -------  start + length ------ src + maplength
                #  |                     ############### |
                #   ------------------------------------
                elif start < src < start + length < src + maplength:
                    # Add the part of the destination range corresponding to the
                    # overlap at the start of the current range.
                    temp_list.append([dest, start+length - src])
                    # Re-process the back of the seed range.
                    length = src - start
                    break
            else:
                # The area isn't overlapping anything; keep it as-is.
                temp_list.append([start, length])
                break
    # `temp_list` becomes `seed_ranges` to process for the next step.
    # Clear `temp_list`.
    seed_ranges = temp_list
    temp_list = []

# Finally, the minimum value is obtained as the first value of the
# range that comes first (technically just the start of the range)
# and assigned to `p2`.
p2 = min(start for start, _ in seed_ranges)

###### ACTUAL CODE END ######

submit(YEAR, DAY, 1, lambda: p1)
submit(YEAR, DAY, 2, lambda: p2)
