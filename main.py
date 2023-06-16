from typing import Tuple
from agents import Prover, Checker
from interactive import Coqtop


prover = Prover(
    goal="Prove the commutativity of addition for natural numbers.",
    model="gpt-3.5-turbo",
)
checker = Checker(model="gpt-4-0613")
coqtop = Coqtop()


def check_coq(coq: str) -> Tuple[str, bool]:
    """Check if the coq proof is correct."""
    coqtop.reset()

    output = ""
    success = True
    # Execute the coq script line by line
    for line in coq.split("\n"):
        if line == "":
            continue
        # If the line starts with a coq comment,  skip it
        if line.strip()[:2] == "(*":
            continue

        # Execute the line
        output = coqtop.send(line)
        output = "\n".join(output)

        # Print the result of executing the coq script in yellow
        print("\033[93m" + "> " + line + "\033[0m")
        print("\033[93m" + output + "\033[0m")

        # Check for Error
        if "Error" in output:
            print(">>> FOUND ERROR <<<")
            success = False
            break

    return output, success


feedback = None
accepted = False
while not accepted:
    # Take the first step in the proof
    natural, coq = prover.step(input=feedback)

    # Print the natural language output in blue
    print("\033[94m" + natural + "\033[0m")

    # Print the coq output in red
    print("\033[91m" + coq + "\033[0m")

    coq_output, coq_success = check_coq(coq)

    if not coq_success:
        feedback = f"Coq error: {coq_output}\n Check your proof for corectness, check the Coq code for syntax errors, and try again."
    else:
        # Print the feedback in green
        feedback, accepted = checker.check(natural)
        print("\033[92m" + feedback + "\033[0m")
        if accepted:
            break
