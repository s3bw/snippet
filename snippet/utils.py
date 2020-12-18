def ignore_lines(string):
    def _strip(lines):
        for l in lines:
            yield l.strip()

    if result := "\n".join(
        [
            line
            for line in _strip(string.split("\n"))
            if line and not line.startswith("#")
        ]
    ):
        return result
