from typing import Dict, List, Optional, Tuple
import openai


class Prover:
    """An agent that uses an interactive theorem prover to generate proofs."""

    def __init__(
        self,
        goal: str,
        system_prompt_path: str = "prompts/prover.txt",
        model: str = "gpt-3.5-turbo-0613",
    ):
        self._model = model
        self._context: List[Dict[str, str]] = []

        # Load the system prompt from the path
        with open(system_prompt_path, "r") as f:
            system_prompt = f.read()
            self._context.append({"role": "system", "content": system_prompt})
        # Add the goal to the context
        self._context.append({"role": "user", "content": goal})

    def _call_model(self, temperature: float = 0.5) -> str:
        """Call the model with the current context."""
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=self._context,
            temperature=temperature,
        )
        model_output = response["choices"][0]["message"]["content"]
        return model_output

    def step(self, input: Optional[str]) -> Tuple[str, str]:
        if input is not None:
            # Add the user input to the context
            self._context.append({"role": "user", "content": input})

        while True:
            model_output = self._call_model()
            print(f"Raw model output: {model_output}")

            # Add the model output to the context
            self._context.append({"role": "assistant", "content": model_output})

            # Split on code:
            split = model_output.split("```")

            if len(split) == 3:
                break

            # Step again, but remind the model to use the format.
            self._context.append(
                {
                    "role": "user",
                    "content": "Please use the specified format. Do not leave out any of the sections. Do not add any additional output.",
                }
            )

        natural = model_output.split("```")[0]
        coq = model_output.split("```")[1]

        # Strip and leading or trailing whitespace
        coq = coq.strip()
        # Strip any lines containing ```
        coq = "\n".join([line for line in coq.split("\n") if "```" not in line])

        return natural, coq


class Checker:
    """A stateless agent that evaluates the proofs generated by the prover."""

    def __init__(
        self,
        system_prompt_path: str = "prompts/checker.txt",
        model: str = "gpt-3.5-turbo-0613",
    ):
        self._model = model
        with open(system_prompt_path, "r") as f:
            self._system_prompt = f.read()

    def check(self, input: str) -> Tuple[str, bool]:
        """Return feedback on the proof."""
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": input},
            ],
        )
        model_output = response["choices"][0]["message"]["content"]

        # Check if the proof is ACCEPTED
        accepted = "ACCEPTED" in model_output

        return model_output, accepted