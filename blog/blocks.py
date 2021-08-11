from wagtail.core import blocks


CODE_CHOICES = [
    ('python', 'python'),
    ('javascript', 'javascript'),
    ('react', 'react'),
    ('djang', 'django'),
    ('html', 'html'),
    ('css', 'css'),
    ('markup', 'markup'),
    ('arduino', 'arduino'),
    ('matlab', 'matlab'),
    ('c++', 'c++'),
    ('c', 'c'),
    ('sql', 'sql'),
    ('vhdl', 'vhdl'),
    ('verilog', 'verilog'),
]


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=CODE_CHOICES, default="python")
    code = blocks.TextBlock(help_text="Type your code here or copy and paste it from your editor")

    class Meta:
        template = "blocks/code-block.html"
        icon = "openquote"
        label = "Code Block"