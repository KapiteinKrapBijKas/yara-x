import typing

class Compiler:
    r"""
    Compiles YARA source code producing a set of compiled [`Rules`].
    """
    def new(self, relaxed_re_syntax: bool, error_on_slow_pattern: bool) -> Compiler:
        r"""
        Creates a new [`Compiler`].

        The `relaxed_re_syntax` argument controls whether the compiler should
        adopt a more relaxed syntax check for regular expressions, allowing
        constructs that YARA-X doesn't accept by default.

        YARA-X enforces stricter regular expression syntax compared to YARA.
        For instance, YARA accepts invalid escape sequences and treats them
        as literal characters (e.g., \R is interpreted as a literal 'R'). It
        also allows some special characters to appear unescaped, inferring
        their meaning from the context (e.g., `{` and `}` in `/foo{}bar/` are
        literal, but in `/foo{0,1}bar/` they form the repetition operator
        `{0,1}`).

        The `error_on_slow_pattern` argument tells the compiler to treat slow
        patterns as errors, instead of warnings.
        """
        ...

    def add_source(self, src: str, origin: typing.Optional[str]) -> None:
        r"""
        Adds a YARA source code to be compiled.

        This function may be invoked multiple times to add several sets of YARA
        rules before calling [`Compiler::build`]. If the rules provided in
        `src` contain errors that prevent compilation, the function will raise
        an exception with the first error encountered. Additionally, the
        compiler will store this error, along with any others discovered during
        compilation, which can be accessed using [`Compiler::errors`].

        Even if a previous invocation resulted in a compilation error, you can
        continue calling this function. In such cases, any rules that failed to
        compile will not be included in the final compiled set.

        The optional parameter `origin` allows to specify the origin of the
        source code. This usually receives the path of the file from where the
        code was read, but it can be any arbitrary string that conveys information
        about the source code's origin.
        """
        ...

    def define_global(self, ident: str, value: typing.Any) -> None:
        r"""
        Defines a global variable and sets its initial value.

        Global variables must be defined before calling [`Compiler::add_source`]
        with some YARA rule that uses the variable. The variable will retain its
        initial value when the [`Rules`] are used for scanning data, however
        each scanner can change the variable's value by calling
        [`crate::Scanner::set_global`].

        The type of `value` must be: bool, str, bytes, int or float.

        # Raises

        [TypeError](https://docs.python.org/3/library/exceptions.html#TypeError)
        if the type of `value` is not one of the supported ones.
        """
        ...

    def new_namespace(self, namespace: str) -> None:
        r"""
        Creates a new namespace.

        Further calls to [`Compiler::add_source`] will put the rules under the
        newly created namespace.
        """
        ...

    def ignore_module(self, module: str) -> None:
        r"""
        Tell the compiler that a YARA module is not supported.

        Import statements for unsupported modules will be ignored without
        errors, but a warning will be issued. Any rule that make use of an
        ignored module will be ignored, while the rest of rules that
        don't rely on that module will be correctly compiled.
        """
        ...

    def build(self) -> Rules:
        r"""
        Builds the source code previously added to the compiler.

        This function returns an instance of [`Rules`] containing all the rules
        previously added with [`Compiler::add_source`] and sets the compiler
        to its initial empty state.
        """
        ...

    def errors(self) -> typing.Any:
        r"""
        Retrieves all errors generated by the compiler.

        This method returns every error encountered during the compilation,
        across all invocations of [`Compiler::add_source`].
        """
        ...

    def warnings(self) -> typing.Any:
        r"""
        Retrieves all warnings generated by the compiler.

        This method returns every warning encountered during the compilation,
        across all invocations of [`Compiler::add_source`].
        """
        ...

class Formatter:
    r"""
    Formats YARA rules.
    """
    def new(
        self,
        align_metadata: bool,
        align_patterns: bool,
        indent_section_headers: bool,
        indent_section_contents: bool,
        indent_spaces: int,
        newline_before_curly_brace: bool,
        empty_line_before_section_header: bool,
        empty_line_after_section_header: bool,
    ) -> Formatter:
        r"""
        Creates a new [`Formatter`].

        `align_metadata` allows for aligning the equals signs in metadata definitions.
        `align_patterns` allows for aligning the equals signs in pattern definitions.
        `indent_section_headers` allows for indenting section headers.
        `indent_section_contents` allows for indenting section contents.
        `indent_spaces` is the number of spaces to use for indentation.
        `newline_before_curly_brace` controls whether a newline is inserted before a curly brace.
        `empty_line_before_section_header` controls whether an empty line is inserted before a section header.
        `empty_line_after_section_header` controls whether an empty line is inserted after a section header.
        """
        ...

    def format(self, input: typing.Any, output: typing.Any) -> str:
        r"""
        Format a YARA rule
        """
        ...

class Match:
    r"""
    Represents a match found for a pattern.
    """
    def offset(self) -> int:
        r"""
        Offset where the match occurred.
        """
        ...

    def length(self) -> int:
        r"""
        Length of the match in bytes.
        """
        ...

    def xor_key(self) -> typing.Optional[int]:
        r"""
        XOR key used for decrypting the data if the pattern had the xor
        modifier, or None if otherwise.
        """
        ...

class Pattern:
    r"""
    Represents a pattern in a YARA rule.
    """
    def identifier(self) -> str:
        r"""
        Pattern identifier (e.g: '$a', '$foo').
        """
        ...

    def matches(self) -> tuple:
        r"""
        Matches found for this pattern.
        """
        ...

class Rule:
    r"""
    Represents a rule that matched while scanning some data.
    """
    def identifier(self) -> str:
        r"""
        Returns the rule's name.
        """
        ...

    def namespace(self) -> str:
        r"""
        Returns the rule's namespace.
        """
        ...

    def tags(self) -> tuple:
        r"""
        Returns the rule's tags.
        """
        ...

    def metadata(self) -> tuple:
        r"""
        A tuple of pairs `(identifier, value)` with the metadata associated to
        the rule.
        """
        ...

    def patterns(self) -> tuple:
        r"""
        Patterns defined by the rule.
        """
        ...

class Rules:
    r"""
    A set of YARA rules in compiled form.

    This is the result of [`Compiler::build`].
    """
    def scan(self, data: bytes) -> ScanResults:
        r"""
        Scans in-memory data with these rules.
        """
        ...

    def serialize_into(self, file: typing.Any) -> None:
        r"""
        Serializes the rules into a file-like object.
        """
        ...

    @staticmethod
    def deserialize_from(self, file: typing.Any) -> Rules:
        r"""
        Deserializes rules from a file-like object.
        """
        ...

class ScanResults:
    r"""
    Results produced by a scan operation.
    """
    def matching_rules(self) -> tuple:
        r"""
        Rules that matched during the scan.
        """
        ...

    def module_outputs(self) -> dict:
        r"""
        Rules that matched during the scan.
        """
        ...

def compile(src: str) -> Rules:
    r"""
    Compiles a YARA source code producing a set of compiled [`Rules`].

    This function allows compiling simple rules that don't depend on external
    variables. For more complex use cases you will need to use a [`Compiler`].
    """
    ...
