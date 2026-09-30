def feedback(code, guess):
    """
    Calculate exact and partial matches.

    Exact matches are counted first.
    Then partial matches are calculated using only the
    remaining unmatched code and guess symbols.

    Each code position can contribute at most once.
    """

    exact = 0
    remaining_code = []
    remaining_guess = []

    # Step 1: Find exact matches first.
    for code_symbol, guess_symbol in zip(code, guess):
        if code_symbol == guess_symbol:
            exact += 1
        else:
            remaining_code.append(code_symbol)
            remaining_guess.append(guess_symbol)

    # Step 2: Find partial matches among unmatched symbols.
    partial = 0

    for guess_symbol in remaining_guess:
        if guess_symbol in remaining_code:
            partial += 1
            remaining_code.remove(guess_symbol)

    return exact, partial